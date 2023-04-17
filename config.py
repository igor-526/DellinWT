import os
import dotenv

dotenv.load_dotenv()

host = str(os.getenv("HOST"))
database = str(os.getenv("DB"))
user = str(os.getenv("USER"))
password = str(os.getenv("PASSWORD"))
port = str(os.getenv("PORT"))

resetdb = int(os.getenv("R_DB"))
upd_auto = int(os.getenv("U_AUTO"))
upd_cont = int(os.getenv("U_CONTACTS"))
upd_city = 1
upd_base = 1

token = str(os.getenv("TOKEN"))

POSTGRES_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
