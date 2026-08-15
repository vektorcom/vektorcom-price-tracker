import os
import sys
from dotenv import load_dotenv

# Initialize and load environment variables
load_dotenv()

# Securely extract settings or gracefully exit if they are missing
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TARGET_STORE_URL = os.getenv("TARGET_STORE_URL")
PRICE_THRESHOLD = float(os.getenv("PRICE_THRESHOLD", 0.0))

if not DISCORD_WEBHOOK_URL:
    print("[CRITICAL ERROR] DISCORD_WEBHOOK_URL is missing from your .env file.")
    sys.exit(1)
