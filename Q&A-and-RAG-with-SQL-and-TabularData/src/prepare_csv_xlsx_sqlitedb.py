import os
from dotenv import load_dotenv
from utils.prepare_sqlitedb_from_csv_xlsx import PrepareSQLFromTabularData
from utils.load_config import LoadConfig

# Load environment variables
load_dotenv()

# Ensure required environment variables are set
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY environment variable is not set"
assert os.getenv("OPENAI_API_BASE"), "OPENAI_API_BASE environment variable is not set"

# Initialize configuration
APPCFG = LoadConfig()

if __name__ == "__main__":
    prep_sql_instance = PrepareSQLFromTabularData(APPCFG.stored_csv_xlsx_directory)
    prep_sql_instance.run_pipeline()
