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
            "ghcr.io/mit-dci/opencbdc-tx-twophase",
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

############
# COMMANDS #
############
@app.get("/command/mint-tokens")
async def mint_tokens():
    """
    Mint tokens.
    """
    try:
        exec_id = docker_client.api.exec_create(container.id, "/bin/bash -c './build/src/uhs/client/client-cli 2pc-compose.cfg mempool0.dat wallet0.dat mint 10 5'")
        exec_output = docker_client.api.exec_start(exec_id)
        output_lines = exec_output.decode('utf-8').strip().split("\n")  # Split the output by new lines (\n)
        output_dict = {f"line_{index}": line for index, line in enumerate(output_lines, start=1)}
        return {"output": output_dict}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/command/inspect-wallet")
async def inspect_wallet():
    """
    Return wallet information.
    """
    try:
        exec_id = docker_client.api.exec_create(container.id, "/bin/bash -c './build/src/uhs/client/client-cli 2pc-compose.cfg mempool0.dat wallet0.dat info'")
        exec_output = docker_client.api.exec_start(exec_id)
        return {"output": exec_output.decode('utf-8').strip().split("\n")}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/command/new-wallet")
async def new_wallet():
    """
    Return new wallet information.
    """
    try:
        exec_id = docker_client.api.exec_create(container.id, "/bin/bash -c './build/src/uhs/client/client-cli 2pc-compose.cfg mempool1.dat wallet1.dat newaddress'")
        exec_output = docker_client.api.exec_start(exec_id)
        output_lines = exec_output.decode('utf-8').strip().split("\n")  # Split the output by new lines (\n)
        output_dict = {f"line_{index}": line for index, line in enumerate(output_lines, start=1)}
        return {"output": output_dict}
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/command/send-tokens/{address}")
async def send_tokens(address: str = Path(..., title="The address to send tokens to")):
    """
    Send tokens to another wallet.
    """
    try:
        command = f"./build/src/uhs/client/client-cli 2pc-compose.cfg mempool0.dat wallet0.dat send 30 {address}"
        exec_id = docker_client.api.exec_create(container.id, ["/bin/bash", "-c", command])
        exec_output = docker_client.api.exec_start(exec_id)
        output_lines = exec_output.decode('utf-8').strip().split("\n")
        output_dict = {f"line_{index}": line for index, line in enumerate(output_lines, start=1)}
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
            # row_str = ', '.join(map(str, row))
            # logger.info(row_str)
            rows.append(row)
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
            # Convert the bytestring to hexadecimal representation
            hex_data = row[0].hex().upper() if row[0] else None
            # Append the converted hex_data and the timestamp_col to the rows list
            rows.append((hex_data, row[1]))
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
            # Convert the bytestring to hexadecimal representation
            hex_data = row[0].hex().upper() if row[0] else None
            rows.append((hex_data, row[1], row[2]))
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
            # Convert the bytestring to hexadecimal representation
            hex_data = row[0].hex().upper() if row[0] else None
            rows.append((hex_data, row[1], row[2]))
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
            # Convert the bytestring to hexadecimal representation
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

@app.get("/api/logs", response_class=HTMLResponse)
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

@app.get("/api/logs/{filename}", name="read_log")
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

@app.get("/{full_path:path}", include_in_schema=False)
async def catch_all(full_path: str):
    logger.info(f"Requested path: {full_path}")
    build_path = PathLib(__file__).parent / "build" / "index.html"
    if not build_path.is_file():
        return HTMLResponse("Build directory not found.", status_code=404)
    return FileResponse(str(build_path))

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()