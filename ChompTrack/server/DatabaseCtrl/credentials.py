import os
from dotenv import load_dotenv

load_dotenv()

SQL_CREDENTIALS = {
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASSWORD'),
    'database': os.getenv('SQL_DATABASE'),
    'host': os.getenv('SQL_HOST'),
    'port': int(os.getenv('SQL_PORT', 3306))
}

SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
