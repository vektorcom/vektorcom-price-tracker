# ======================================================================
# VEKTORCOM™ - PRODUCTION AUTOMATION ENGINE (MODULAR VERSION)
# ======================================================================

import logging
import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

# Import custom workspace configurations cleanly from config.py
import config

# Configure automated error logs inside the dedicated /logs directory
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/tracker.log"),
        logging.StreamHandler()
    ]
)

def init_database():
    """Ensures local SQLite tracking tables exist inside the /data directory."""
    conn = sqlite3.connect("data/tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            product_title TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

def log_price_to_db(title: str, price: float):
    """Commits a historic snapshot run directly to local tracking records."""
    conn = sqlite3.connect("data/tracker.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO price_history (timestamp, product_title, price) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, price)
    )
    conn.commit()
    conn.close()

def scrape_product_data() -> dict:
    """Uses Playwright browser layers to parse data via secured variables."""
    logging.info(f"Vektorcom Engine launching browser for: {config.TARGET_STORE_URL}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Vektorcom Automation Agent v1.0")
        page = context.new_page()
        
        try:
            # Target URL loaded directly from your config module configuration
            page.goto(config.TARGET_STORE_URL, timeout=30000)
