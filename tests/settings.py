import os
from dotenv import load_dotenv

def read_env_file(f_path = "./test.env"):
    load_dotenv(f_path)
    env_vars = {}

    for k, v in os.environ.items():
        env_vars[k] = v

    return env_vars

settings = read_env_file()