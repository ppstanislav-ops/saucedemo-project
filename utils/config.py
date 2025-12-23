import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://www.saucedemo.com/"  # Без пробелов в конце
    DEFAULT_TIMEOUT = 10000 

    # Пользователи
    STANDARD_USER = {
        "username": "standard_user",
        "password": "secret_sauce"
    }

    LOCKED_OUT_USER = {
        "username": "locked_out_user",
        "password": "secret_sauce"
    }

    PERFORMANCE_GLITCH_USER = {
        "username": "performance_glitch_user",
        "password": "secret_sauce"
    }

    PROBLEM_USER = {
        "username": "problem_user",
        "password": "secret_sauce"
    }