import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Fix for ADMIN_IDS to handle missing environment variable
ADMIN_IDS = os.getenv("ADMIN_IDS", "")  # Default to an empty string if not set
if ADMIN_IDS:
    ADMIN_IDS = list(map(int, ADMIN_IDS.split(',')))  # Split by ',' assuming multiple IDs are comma-separated
else:
    ADMIN_IDS = [443809517]  # Default to an empty list if ADMIN_IDS is not set

SPOTIFY_CLIENT_ID = "5941bb8af55d41c5297f616e325"
SPOTIFY_CLIENT_SECRET = "408f04b237aba1b8bfc5da9eff8"
MONGO_URL = os.getenv("MONGO_URL")
COMMAND_PREFIX = ["!", "/"]  # Example of common command prefixes
