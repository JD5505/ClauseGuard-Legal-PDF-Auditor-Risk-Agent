from dotenv import load_dotenv
load_dotenv()

import os
db_url = os.getenv("DB_CONN")
api_key = os.getenv("GROQ_API_KEY")