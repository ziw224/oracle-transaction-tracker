import asyncio, oracledb, traceback, uvicorn, os
from contextlib import asynccontextmanager
from configure import setup_logging, read_key, unzip_instant_client, unzip_wallet, username, password, wallet_pw, logger
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List

# Global variables
pool = None
LOGS_DIR = "logs"

# Llifespan event handler to initialize and close the database connection pool
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the DB pool
    await create_db_pool()
    yield
    # Close the DB pool
    await close_db_pool()

# app = FastAPI()
app = FastAPI(lifespan=lifespan)
# html templating
templates = Jinja2Templates(directory="templates")

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

async def create_db_pool():
    global pool
    try:
        pool = oracledb.create_pool(
            user=username,
            password=password,
            dsn="cbdcauto_low",
            min=2,
            max=10,
            increment=1,
            encoding="UTF-8",
            config_dir="./wallet",
            wallet_location="./wallet",  # You can also specify the TNS_ADMIN environment variable instead
            wallet_password=wallet_pw
        )
        logger.info("Database connection pool created successfully.")
    except oracledb.DatabaseError as e:
        error, = e.args
        logger.error(f"Error connecting to the database: {error.message}")
        raise

async def close_db_pool():
    global pool
    if pool:
        pool.close()
        logger.info("Database connection pool closed.")

@app.get("/test/hello")
async def hello():
    global pool
    try:
        # Use asyncio.wait_for to set a timeout for acquiring a connection
        logger.info("Attempting to acquire a connection from the pool.")
        async with asyncio.wait_for(pool.acquire(), timeout=5) as conn:
            logger.info("Got a connection from the pool.")
            # You would typically perform some database operations here.
            # For example: `await conn.execute(...)`
            # For now, we'll just return a success message.
            message = "Hello World with a database connection!"
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
            print(e)
            logger.error("Database connection issue." + e)
            raise HTTPException(status_code=500, detail="Database connection issue.")
    finally:
        # Release the connection back to the pool if acquired
        if 'conn' in locals():
            pool.release(conn)
    return {"message": message}

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
    print("Starting up...")
    setup_logging()
    logger.info("Starting up...")
    read_key()
    unzip_instant_client()
    unzip_wallet()
    print("Setup complete. Starting server...")
    logger.info("////////// SETUP COMPLETE - SERVER STARTING //////////")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()