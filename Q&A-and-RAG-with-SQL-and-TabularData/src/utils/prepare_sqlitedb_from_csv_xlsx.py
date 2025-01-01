import os
import pandas as pd
from utils.load_config import LoadConfig
from sqlalchemy import create_engine, inspect
import openai
from langchain_openai import ChatOpenAI





class PrepareSQLFromTabularData:
    """
    A class that prepares a SQL database from CSV or XLSX files within a specified directory.

    This class reads each file, converts the data to a DataFrame, and then
    stores it as a table in a SQLite database, which is specified by the application configuration.
    """
    def __init__(self, directory) -> None:
        """
        Initialize an instance of PrepareSQLFromTabularData.

        Args:
            directory (str): The directory containing the CSV or XLSX files to be converted to SQL tables.
        """
        APPCFG = LoadConfig()
        self.directory = directory
        self.file_dir_list = os.listdir(directory)
        db_path = APPCFG.stored_csv_xlsx_sqldb_directory
        db_path = f"sqlite:///{db_path}"
        self.engine = create_engine(db_path)
        print("Number of csv files:", len(self.file_dir_list))

    def _prepare_db(self):
        """
        Private method to convert CSV/XLSX files from the specified directory into SQL tables.

        Each file's name (excluding the extension) is used as the table name.
        The data is saved into the SQLite database referenced by the engine attribute.
        """
        for file_name in os.listdir(self.directory):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.directory, file_name)
                df = pd.read_csv(file_path)
                df.to_sql(file_name.split('.')[0], self.engine, index=False, if_exists='replace')
        print("==============================")
        print("All csv files are saved into the sql database.")

    def run_pipeline(self):
        """
        Public method to run the data import pipeline, which includes preparing the database
        and validating the created tables. It is the main entry point for converting files
        to SQL tables and confirming their creation.
        """
        self._prepare_db()
