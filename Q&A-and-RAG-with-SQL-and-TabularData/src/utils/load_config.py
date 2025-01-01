import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
import shutil
import openai
from langchain_openai import ChatOpenAI
import chromadb
from openai import OpenAI
from openai import Embedding
import openai

print("Environment variables are loaded:", load_dotenv())

class LoadConfig:
    def __init__(self) -> None:
        with open(here("configs/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_directories(app_config=app_config)
        self.load_llm_configs(app_config=app_config)
        self.load_openai_models()
        self.load_chroma_client()
        self.load_rag_config(app_config=app_config)

    def load_directories(self, app_config):
        self.stored_csv_xlsx_directory = str(here(
            app_config["directories"]["stored_csv_xlsx_directory"]))
        self.sqldb_directory = str(here(
            app_config["directories"]["sqldb_directory"]))
        self.uploaded_files_sqldb_directory = str(here(
            app_config["directories"]["uploaded_files_sqldb_directory"]))
        self.stored_csv_xlsx_sqldb_directory = str(here(
            app_config["directories"]["stored_csv_xlsx_sqldb_directory"]))
        self.persist_directory = app_config["directories"]["persist_directory"]

    def load_llm_configs(self, app_config):
        self.model_name = "gpt-3.5-turbo"
        
        self.model_name = app_config["llm_config"]["model_name"]  # Load model name from config

        self.agent_llm_system_role = app_config["llm_config"]["agent_llm_system_role"]

        self.rag_llm_system_role = app_config["llm_config"]["rag_llm_system_role"]
        self.temperature = app_config["llm_config"]["temperature"]  # Load temperature from config
        self.embedding_model_name = os.getenv("embed_deployment_name")
        self.embedding_model_name  = "text-embedding-ada-002"

    def load_openai_models(self):
        openai_api_key = os.environ["OPENAI_API_KEY"]
        openai_api_base = os.environ["OPENAI_API_BASE"]

        # Set the OpenAI API key and base URL
        # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=openai_api_base)'
        # openai.api_base = openai_api_base

        # This will be used for the GPT and embedding models
        self.openai_embedding_client = openai
        
            # Initialize the OpenAI client with the API key and base URL
        self.openai_client = openai.OpenAI(
            api_key=openai_api_key , 
            base_url=openai_api_base
        )
        
        self.openai_client = openai

        # Initialize the ChatOpenAI model
        self.langchain_llm = ChatOpenAI(
            api_key=openai_api_key,
            model_name=self.model_name,
            temperature=self.temperature)

    def load_chroma_client(self):
        self.chroma_client = chromadb.PersistentClient(
            path=str(here(self.persist_directory)))

    def load_rag_config(self, app_config):
        self.collection_name = app_config["rag_config"]["collection_name"]
        self.top_k = app_config["rag_config"]["top_k"]

    def remove_directory(self, directory_path: str):
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(
                    f"The directory '{directory_path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory_path}' does not exist.")