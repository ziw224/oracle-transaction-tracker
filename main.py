import docker, oracledb, traceback, uvicorn, os
from contextlib import asynccontextmanager
from configure import setup_logging, read_key, unzip_instant_client, unzip_wallet, logger
from fastapi import FastAPI, HTTPException, Request, Response, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path as PathLib
from docker.errors import NotFound

# Global variables
connection, container = None, None
LOGS_DIR = "logs"
app = FastAPI()
docker_client = docker.from_env()
templates = Jinja2Templates(directory="templates")  # html templating

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    global connection, container

    # Startup
    setup_logging()
    logger.info("Starting up...")
    credentials = read_key()
    username = credentials['username']
    password = credentials['password']
    wallet_pw = credentials['wallet_pw']
    unzip_instant_client()
    unzip_wallet()
    logger.info("////////// SETUP COMLETE //////////")
    logger.info("Attemping to connect to the database.")
    try:
        logger.info("Autonomous Database Username: " + username)
        connection = oracledb.connect(
            user=username,
            password=password,
            # dsn="cbdcauto_low",
            dsn="lw41k4xzf2od0kvy_low",
            config_dir="./wallet",
            wallet_location="./wallet",
            wallet_password=wallet_pw
        )
        logger.info("Database connection established.")
        logger.info("Autonomous Database Version: " + connection.version)

        # Run the container
        container = docker_client.containers.run(
            "opencbdc-tx-twophase",
            network="2pc-network",
            command="/bin/bash",
            stdin_open=True,
            tty=True,
            detach=True
        )
        logger.info(f"Connected to wallet docker container {container.short_id}.") 
    except oracledb.DatabaseError as e:
        error, = e.args
        logger.error(f"Error connecting to the database: {error.message}")
    except NotFound as e:
        # Handle the NotFound error
        print(f"Error: {e.explanation}")
        raise HTTPException(status_code=404, detail="Docker network not found.")
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))

    yield  # separates the startup and shutdown logic

    # Shutdown
    if connection:
        connection.close()
        logger.info("Database connection closed.")
    # closing container
    if container:
        container.stop()
        logger.info("Disconnected to wallet docker container stopped.")

app = FastAPI(lifespan=app_lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    # Log the stack trace
    traceback_str = "".join(traceback.format_tb(exc.__traceback__))
    print(f"Exception caught: {exc}\nStack trace:\n{traceback_str}")
    logger.error(f"Exception caught: {exc}\nStack trace:\n{traceback_str}")
    return templates.TemplateResponse("error.html", {
        "request": request,
        "message": "Internal Server Error. Check the logs endpoint for more details."
    }, status_code=500)

@app.get("/admin")
async def admin():
    return FileResponse('build/index.html')

@app.get("/test/hello")
async def hello():
    global connection
    cursor = None
    try:
        logger.info("Getting database connection for /test/hello endpoint.")
        cursor = connection.cursor()
        # cursor.execute("SELECT * FROM admin.test_shard")
        # for row in cursor:
        #     logger.info(row[0])
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            # ORA-01017: invalid username/password; logon denied
            logger.error("Database credentials are invalid.")
            raise HTTPException(status_code=400, detail="Database credentials are invalid.")
        else:
            # Generic error handler for database issues
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        if cursor:      # release cursor
            logger.info("Releasing cursor on /test/hello endpoint.")
            cursor.close()
    return {"message": "Hello World"}

@app.get("/cbdc-wallets")
async def get_wallets():
    cbdc_wallet_file = "cbdc_wallets.txt"
    wallets = []
    try:
        if os.path.exists(cbdc_wallet_file):
            with open(cbdc_wallet_file, "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    wallet_number = parts[0]
                    wallet_address = parts[1] if len(parts) > 1 else None
                    wallets.append({"wallet_number": wallet_number, "wallet_address": wallet_address})
        return {"wallets": wallets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

############
# COMMANDS #
############  
@app.get("/command/mint-tokens/{userid}/{num_utxos}/{value_per_utxo}")
async def mint_tokens(userid: int, num_utxos: int, value_per_utxo: int):
    """
    Mint new coins to a specific user's wallet: a specified number of UTXOs each with a given value.
    """
    mempool_filename = f"mempool{userid}.dat"
    wallet_filename = f"wallet{userid}.dat"
    try:
        command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg {mempool_filename} {wallet_filename} mint {num_utxos} {value_per_utxo}"
        exec_id = docker_client.api.exec_create(container.id, f"/bin/bash -c '{command}'")
        exec_output = docker_client.api.exec_start(exec_id)
        output_lines = exec_output.decode('utf-8').strip().split("\n")  # Split the output by new lines (\n)
        output_dict = {f"line_{index}": line for index, line in enumerate(output_lines, start=1)}
        return {"output": output_dict}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/command/inspect-wallet/{userid}")
async def inspect_wallet(userid: int):
    """
    Return wallet and mempool information for the specified user.
    """
    mempool_filename = f"mempool{userid}.dat"
    wallet_filename = f"wallet{userid}.dat"
    try:
        command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg {mempool_filename} {wallet_filename} info"
        exec_id = docker_client.api.exec_create(container.id, f"/bin/bash -c '{command}'")
        exec_output = docker_client.api.exec_start(exec_id)
        return {"output": exec_output.decode('utf-8').strip().split("\n")}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/command/new-wallet")
async def new_wallet():
    """
    Create a new wallet with a unique number.
    """
    cbdc_wallet_file = "cbdc_wallets.txt"
    # Read the latest wallet number and increment it
    if not os.path.exists(cbdc_wallet_file):
        latest_number = 0
    else:
        with open(cbdc_wallet_file, "r") as file:
            latest_number = int(file.read().strip().split(',')[0])  # Split by comma and take the first element
    new_number = latest_number + 1
    mempool_filename = f"mempool{new_number}.dat"
    wallet_filename = f"wallet{new_number}.dat"
    try:
        command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg {mempool_filename} {wallet_filename} newaddress"
        exec_id = docker_client.api.exec_create(container.id, f"/bin/bash -c '{command}'")
        exec_output = docker_client.api.exec_start(exec_id)
        output_lines = exec_output.decode('utf-8').strip().split("\n")
        output_dict = {f"line_{index}": line for index, line in enumerate(output_lines, start=1)}
        wallet_address = output_dict.get("line_3", None)  # Check if line_3 exists and get the wallet address
        wallet_info_to_write = f"{new_number},{wallet_address}" if wallet_address else str(new_number)
        with open(cbdc_wallet_file, "a") as file:
            file.write(f"{wallet_info_to_write}\n")
        return {"output": output_dict, "wallet_number": new_number, "wallet_address": wallet_address}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/command/send-tokens/{wallet_number}/{amount}/{address}")
async def send_tokens(wallet_number: int, amount: int, address: str = Path(..., title="The address to send tokens to")):
    """
    Send tokens from a specified wallet to another wallet (amount is total value, not utxos).
    """
    mempool_filename = f"mempool{wallet_number}.dat"
    wallet_filename = f"wallet{wallet_number}.dat"
    try:
        command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg {mempool_filename} {wallet_filename} send {amount} {address}"
        exec_id = docker_client.api.exec_create(container.id, ["/bin/bash", "-c", command])
        exec_output = docker_client.api.exec_start(exec_id)
        output_lines = exec_output.decode('utf-8', 'replace').strip().split("\n")  # Using 'replace' to handle undecodable bytes
        output_dict = {f"line_{index}": line for index, line in enumerate(output_lines, start=1)}
        return {"output": output_dict}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except UnicodeDecodeError as e:
        logger.error(f"Unicode decoding error: {e}")

@app.get("/command/import-tokens/{userid}/{importinput}")
async def import_tokens(userid: int, importinput: str):
    """
    Import tokens to a user's wallet using importinput data, and then sync the wallet.
    """
    mempool_filename = f"mempool{userid}.dat"
    wallet_filename = f"wallet{userid}.dat"
    try:
        import_command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg {mempool_filename} {wallet_filename} importinput {importinput}"
        exec_id_import = docker_client.api.exec_create(container.id, f"/bin/bash -c '{import_command}'")
        import_output = docker_client.api.exec_start(exec_id_import)
        sync_command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg {mempool_filename} {wallet_filename} sync"
        exec_id_sync = docker_client.api.exec_create(container.id, f"/bin/bash -c '{sync_command}'")
        sync_output = docker_client.api.exec_start(exec_id_sync)

        import_output_lines = import_output.decode('utf-8').strip().split("\n")
        sync_output_lines = sync_output.decode('utf-8').strip().split("\n")
        output_dict = {
            "import_output": {f"line_{index}": line for index, line in enumerate(import_output_lines, start=1)},
            "sync_output": {f"line_{index}": line for index, line in enumerate(sync_output_lines, start=1)}
        }
        return {"output": output_dict}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))

#############
# ENDPOINTS #
#############
@app.get("/table/input")
async def get_input(request: Request):
    """
    Return the contents of the test_shard table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/input endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.input")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            formatted_row = []
            for item in row:
                if isinstance(item, bytes):                                 # Check if the item is binary
                    formatted_row.append(item.hex())                        # Convert binary to hex
                else:
                    formatted_row.append(item)                              # otherwise keep as is
            rows.append(formatted_row)
        if "application/json" in request.headers.get("accept", ""):         # Check the 'Accept' header in the request
            return {"columns": columns, "rows": rows}                       # Respond with JSON if 'application/json' is specified in the 'Accept' header
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "Input Table"
        })
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            # ORA-01017: invalid username/password; logon denied
            logger.error("Database credentials are invalid.")
            raise HTTPException(status_code=400, detail="Database credentials are invalid.")
        else:
            # Generic error handler for database issues
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        if cursor:      # release cursor
            logger.info("Releasing cursor on /table/input endpoint.")
            cursor.close()

@app.get("/table/output")
async def get_output(request: Request):
    """
    Return the contents of the output table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/output endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.output")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            formatted_row = []
            for item in row:
                if isinstance(item, bytes):
                    formatted_row.append(item.hex())
                else:
                    formatted_row.append(item)
            rows.append(formatted_row)
        if "application/json" in request.headers.get("accept", ""):         # Check the 'Accept' header in the request
            return {"columns": columns, "rows": rows}                       # Respond with JSON if 'application/json' is specified in the 'Accept' header
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "Output Table"
        })
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            # ORA-01017: invalid username/password; logon denied
            logger.error("Database credentials are invalid.")
            raise HTTPException(status_code=400, detail="Database credentials are invalid.")
        else:
            # Generic error handler for database issues
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        if cursor:      # release cursor
            logger.info("Releasing cursor on /table/output endpoint.")
            cursor.close()

@app.get("/table/transaction")
async def get_transaction(request: Request):
    """
    Return the contents of the transaction table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/transaction endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.transaction")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            formatted_row = []
            for item in row:
                if isinstance(item, bytes):
                    formatted_row.append(item.hex())
                else:
                    formatted_row.append(item)
            rows.append(formatted_row)
        if "application/json" in request.headers.get("accept", ""):         # Check the 'Accept' header in the request
            return {"columns": columns, "rows": rows}                       # Respond with JSON if 'application/json' is specified in the 'Accept' header
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "Transaction Table"
        })
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            # ORA-01017: invalid username/password; logon denied
            logger.error("Database credentials are invalid.")
            raise HTTPException(status_code=400, detail="Database credentials are invalid.")
        else:
            # Generic error handler for database issues
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        if cursor:      # release cursor
            logger.info("Releasing cursor on /table/transaction endpoint.")
            cursor.close()

@app.get("/table/uhs")
async def get_transaction(request: Request):
    """
    Return the contents of the uhs table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/uhs endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.uhs")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            formatted_row = []
            for item in row:
                if isinstance(item, bytes):
                    formatted_row.append(item.hex())
                else:
                    formatted_row.append(item)
            rows.append(formatted_row)
        if "application/json" in request.headers.get("accept", ""):         # Check the 'Accept' header in the request
            return {"columns": columns, "rows": rows}                       # Respond with JSON if 'application/json' is specified in the 'Accept' header
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "UHS Table"
        })
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            # ORA-01017: invalid username/password; logon denied
            logger.error("Database credentials are invalid.")
            raise HTTPException(status_code=400, detail="Database credentials are invalid.")
        else:
            # Generic error handler for database issues
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        if cursor:      # release cursor
            logger.info("Releasing cursor on /table/uhs endpoint.")
            cursor.close()

@app.get("/table/test")
async def get_test_table(request: Request):
    """
    Return the contents of the test_table table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/test endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.test_table")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            rows.append((row[0], row[1], row[2]))
        if "application/json" in request.headers.get("accept", ""):         # Check the 'Accept' header in the request
            return {"columns": columns, "rows": rows}                       # Respond with JSON if 'application/json' is specified in the 'Accept' header
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "Test Table"
        })
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            # ORA-01017: invalid username/password; logon denied
            logger.error("Database credentials are invalid.")
            raise HTTPException(status_code=400, detail="Database credentials are invalid.")
        else:
            # Generic error handler for database issues
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        if cursor:      # release cursor
            logger.info("Releasing cursor on /table/test endpoint.")
            cursor.close()

@app.get("/logs", response_class=HTMLResponse)
async def get_logs(request: Request):
    """
    Return an HTML list of log filenames in the logs directory or the content of the log file if there is only one.
    """
    try:
        logs = os.listdir(LOGS_DIR)
        logs = [log for log in logs if os.path.isfile(os.path.join(LOGS_DIR, log))]
        if len(logs) == 1:
            filepath = os.path.join(LOGS_DIR, logs[0])
            with open(filepath, "r") as file:
                content = file.read()
            return Response(content=content, media_type="text/plain")
        else:
            return templates.TemplateResponse("log_list.html", {"request": request, "log_files": logs})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/{filename}", name="read_log")
async def read_log(request: Request, filename: str):
    """
    Return the content of the specified log file.
    """
    filepath = os.path.join(LOGS_DIR, filename)
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r") as file:
                content = file.read()
            return Response(content=content, media_type="text/plain")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error reading file.")
    else:
        raise HTTPException(status_code=404, detail="File not found.")

# mount build directory
app.mount("/", StaticFiles(directory="build", html=True), name="static")

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()