import asyncio, oracledb, traceback, uvicorn, os
from contextlib import asynccontextmanager
from configure import setup_logging, read_key, unzip_instant_client, unzip_wallet, username, password, wallet_pw, logger
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List

# Global variables
connection = None
LOGS_DIR = "logs"

# Lifespan event handler to initialize and close the database connection pool
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Initialize the DB pool
#     await create_db_connection()
#     yield
#     # Close the DB pool
#     await close_db_connection()

app = FastAPI()
# app = FastAPI(lifespan=lifespan)
# html templating
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    global connection

    # Startup logic
    setup_logging()
    logger.info("Starting up...")
    read_key()
    unzip_instant_client()
    unzip_wallet()
    
    try:
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn="cbdcauto_low",
            config_dir="./wallet",
            wallet_location="./wallet",
            wallet_password=wallet_pw
        )
        logger.info("Database connection established.")
        print(connection.ping())
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
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

async def create_db_connection():
    global connection
    try:
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn="cbdcauto_low",
            config_dir="./wallet",
            wallet_location="./wallet",
            wallet_password=wallet_pw
        )
        logger.info(connection.ping())
        logger.info("Autonomous Database Version:", connection.version)
        logger.info("Database connection pool created successfully.")
    except oracledb.DatabaseError as e:
        error, = e.args
        logger.error(f"Error connecting to the database: {error.message}")
        raise

async def close_db_connection():
    global connection
    if connection:
        connection.close()
        logger.info("Database connection closed.")

@app.get("/test/hello")
async def hello():
    global connection
    try:
        # Use asyncio.wait_for to set a timeout for acquiring a connection
        logger.info("Attempting to acquire a connection from the pool.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.test_blockchain")
        for row in cursor:
            print(row[0], row[1])
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
            # print(e)
            logger.error("Database connection issue." + str(e))
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        # Release the connection back to the pool if acquired
        if cursor:
            logger.info("Releasing cursor.")
            cursor.close()
        if connection:
            logger.info("Releasing connection.")
            connection.close()
    return {"message": "Hello World"}

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
    # print("Starting up...")
    # setup_logging()
    # logger.info("Starting up...")
    # read_key()
    # unzip_instant_client()
    # unzip_wallet()
    # print("Setup complete. Starting server...")
    logger.info("////////// SETUP COMPLETE - SERVER STARTING //////////")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()