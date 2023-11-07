import os, zipfile, logging, shutil
from datetime import datetime

username, password, wallet_pw = "", "", ""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a custom logger
def setup_logging():
    '''
    Setup the logging configuration.
    '''
    global logger
    logs_dir = "logs"
    if not os.path.exists(logs_dir):        # Create logs directory if it doesn't exist
        os.makedirs(logs_dir)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")        # Generate a timestamped filename for the log file
    filename = f"{logs_dir}/log-{timestamp}.txt"
    f_handler = logging.FileHandler(filename)       # file handler
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('[%(asctime)s] - (%(levelname)s) - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    f_handler.setFormatter(f_format)            # formatter
    logger.addHandler(f_handler)

# read file for passcodes and username
def read_key():
    '''
    Read the key file for the username, password, and wallet password.
    '''
    global username, password, wallet_pw
    logger.info("////////// KEY FILE //////////")
    with open('key.txt', 'r') as f:
        for line in f:
            if line.startswith('username'):
                username = line.split('=')[1].strip()
                logger.info("Username read from key file")
            if line.startswith('password'):
                password = line.split('=')[1].strip()
                logger.info("Password read from key file")
            if line.startswith('wallet_password'):
                wallet_pw = line.split('=')[1].strip()
                logger.info("Wallet password read from key file")
    if username == "" or password == "" or wallet_pw == "":
        logger.error("Username, password or wallet password is empty")
        print("Username, password or wallet password is empty. Exiting...")
        exit(1)

# unzip instant client zip files
def unzip_instant_client():
    '''
    Unzip the instant client zip files to the current directory.
    '''
    logger.info("////////// INSTANT CLIENT //////////")
    instantclient_zip_dir = './instantclient_zip'  # Directory where zip files are located
    base_dir = '.'
    # Check if the 'network' and 'sdk' folders exist in the 'instantclient' directory
    instantclient_dir = os.path.join(base_dir, 'instantclient')
    if os.path.exists(instantclient_dir):
        contents = os.listdir(instantclient_dir)
        if 'network' in contents and 'sdk' in contents:
            logger.info("Both 'network' and 'sdk' directories exist in 'instantclient'. No need to unzip.")
            return
    # Unzip files from instantclient_zip to the current directory (base_dir)
    for item in os.listdir(instantclient_zip_dir):
        if item.endswith('.zip'):
            file_path = os.path.join(instantclient_zip_dir, item)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    logger.info(f"Unzipping {item} into {base_dir} ...")
                    zip_ref.extractall(base_dir)
                    logger.info(f"Unzipped {item} successfully.")
            except zipfile.BadZipFile:
                logger.error(f"The file {item} is not a zip file or it is corrupted.")
                print(f"The file {item} is not a zip file or it is corrupted. Exiting...")
            except PermissionError:
                logger.error(f"The process lacks the necessary permissions to extract {item}.")
                print(f"The process lacks the necessary permissions to extract {item}. Exiting...")
            except Exception as e:
                logger.error(f"An error occurred while unzipping {item}: {e}")
                print(f"An error occurred while unzipping {item}: {e}. Exiting...")
    # Rename the unzipped directories by removing the version number
    for item in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, item)) and item.startswith('instantclient_') and item != 'instantclient_zip':
            # If there's already a directory named 'instantclient', remove it
            if os.path.exists(instantclient_dir):
                shutil.rmtree(instantclient_dir)
            os.rename(os.path.join(base_dir, item), instantclient_dir)
            logger.info(f"Renamed {item} to 'instantclient'.")

# unzip wallet zip files
def unzip_wallet():
    '''
    Unzip the wallet zip files to the wallet directory.
    '''
    logger.info("////////// WALLET //////////")
    wallet_zip_dir = './wallet_zip'
    wallet_dir = './wallet'  # Directory where the wallet files should be extracted
    if not os.path.exists(wallet_dir):          # Create wallet directory if it doesn't exist
        os.makedirs(wallet_dir)
        logger.info(f"Created directory {wallet_dir}.")
    for item in os.listdir(wallet_zip_dir):     # Unzip files from wallet_zip to the wallet directory
        if item.endswith('.zip'):
            file_path = os.path.join(wallet_zip_dir, item)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:        # Extract the zip file
                    logger.info(f"Unzipping {item} into {wallet_dir}...")
                    zip_ref.extractall(wallet_dir)
                    logger.info(f"Unzipped {item} successfully.")
            except zipfile.BadZipFile:      # If the file is not a zip file or it is corrupted
                logger.error(f"The file {item} is not a zip file or it is corrupted.")
                print(f"The file {item} is not a zip file or it is corrupted. Exiting...")
            except PermissionError:         # If the process lacks the necessary permissions to extract the file
                logger.error(f"The process lacks the necessary permissions to extract {item}.")
                print(f"The process lacks the necessary permissions to extract {item}. Exiting...")
            except Exception as e:          # If an error occurs while unzipping the file
                logger.error(f"An error occurred while unzipping {item}: {e}")
                print(f"An error occurred while unzipping {item}: {e}. Exiting...")
    rewrite_sqlnet_ora()    # Rewrite sqlnet.ora file

# rewrite sqlnet.ora file
def rewrite_sqlnet_ora():
    '''
    Rewrite the sqlnet.ora file to point to the wallet directory.    
    '''
    sqlnet_ora_path = './wallet/sqlnet.ora'
    if not os.path.exists(sqlnet_ora_path):             # If the file doesn't exist
        logger.error(f"File {sqlnet_ora_path} does not exist.")
        print(f"File {sqlnet_ora_path} does not exist. Exiting...")
        return
    with open(sqlnet_ora_path, 'w') as f:
        f.write("WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY=\"./wallet\")))\n")
        f.write("SSL_SERVER_DN_MATCH=yes\n")
    logger.info(f"Rewrote {sqlnet_ora_path} successfully.")
