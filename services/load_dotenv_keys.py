from dotenv import load_dotenv
import os
from typing import Tuple

def load_dotenv_keys() -> Tuple[str,str]:

    load_dotenv()

    flask_secret_key = os.getenv('FLASK_SECRET_KEY')
    huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')

    if not flask_secret_key or not huggingface_api_key:
        raise RuntimeError("Error: Variáveis de ambiente em falta")

    return flask_secret_key, huggingface_api_key
