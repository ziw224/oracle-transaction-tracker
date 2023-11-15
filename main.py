import asyncio, oracledb, traceback, uvicorn, os
from contextlib import asynccontextmanager
from configure import setup_logging, read_key, unzip_instant_client, unzip_wallet, logger
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# from typing import List

# Global variables
connection = None
LOGS_DIR = "logs"
app = FastAPI()
templates = Jinja2Templates(directory="templates")  # html templating

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    global connection

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
            dsn="cbdcauto_low",
            config_dir="./wallet",
            wallet_location="./wallet",
            wallet_password=wallet_pw
        )
        logger.info("Database connection established.")
        logger.info("Autonomous Database Version: " + connection.version)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        logger.error(f"Error connecting to the database: {error.message}")

    yield  # separates the startup and shutdown logic

    # Shutdown
    if connection:
        connection.close()
        logger.info("Database connection closed.")

app = FastAPI(lifespan=app_lifespan)

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
    except asyncio.TimeoutError:
        # Handle the timeout case
        logger.info("Database connection acquisition timed out after 5 seconds.")
        raise HTTPException(status_code=500, detail="Database connection acquisition timed out.")
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

@app.get("/table/test_shard", response_class=HTMLResponse)
async def get_test_shard(request: Request):
    """
    Return the contents of the test_shard table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/test_shard endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.test_shard")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            # row_str = ', '.join(map(str, row))
            # logger.info(row_str)
            rows.append(row)
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "test_shard Table"
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
            logger.info("Releasing cursor on /table/test_shard endpoint.")
            cursor.close()

@app.get("/table/shard_data", response_class=HTMLResponse)
async def get_shard_data(request: Request):
    """
    Return the contents of the test_shard table.
    """
    cursor = None
    try:
        logger.info("Getting database connection for /table/shard_data endpoint.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.shard_data")
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor:
            # Convert the bytestring to hexadecimal representation
            hex_data = row[0].hex().upper() if row[0] else None
            # Append the converted hex_data and the timestamp_col to the rows list
            rows.append((hex_data, row[1]))
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "rows": rows,
            "columns": columns,
            "table_title": "shard_data Table"
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
            logger.info("Releasing cursor on /table/test_shard endpoint.")
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
    uvicorn.run(app, host="0.0.0.0", port=8000)