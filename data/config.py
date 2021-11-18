from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Taking the value of the string type
ADMINS = env.list("ADMINS")  # Here we will have a list of admins
IP = env.str("ip")  # Also str, but for the IP address of the host

DB_USER = env.str('DB_USER') # DB User-Owner Name
DB_PASS = env.str('DB_PASS') # DB Yser-Owner Password
DB_HOST = env.str('DB_HOST') # DB IP ( local host usually)
DB_NAME = env.str('DB_NAME') # DB DATABASE self name

I18N_DOMAIN = "testbot" # Name of localisation domain (A translation file template will be created with this domain and will be used by the system to connect the translations themselves in the future.)
BASE_DIR = Path(__file__).parent # directory of the entire bot
LOCALES_DIR = BASE_DIR / "locales"  # translations are stored here

# Variables for UCassa ( DEVELOPMENT )
# UTOKEN = env.str("yootoken")

# New variables for the Qiwi Api Library
QIWI_TOKEN = env.str("qiwi")
WALLET_QIWI = env.str("wallet")  # phone number
QIWI_PUBKEY = env.str("qiwi_p_pub")  # Public key for generating a payment link

