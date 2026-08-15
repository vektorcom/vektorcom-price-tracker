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
            
            title = page.locator("h1.product-title").inner_text(timeout=5000).strip()
            price_text = page.locator(".current-price").inner_text(timeout=5000).strip()
            cleaned_price = float(price_text.replace("$", "").replace(",", "").strip())
            
            return {"title": title, "price": cleaned_price, "success": True}
            
        except Exception as e:
            logging.error(f"Automated scraping run blocked: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            browser.close()

def send_chat_notification(message: str):
    """Routes alerts outwards using the secure environment webhook token."""
    payload = {"content": message}
    try:
        response = requests.post(config.DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 204:
            logging.info("Vektorcom notification successfully routed to Discord.")
    except Exception as e:
        logging.error(f"Network routing failure to webhook: {str(e)}")

def main():
    logging.info("Initiating scheduled Vektorcom operational routine...")
    init_database()
    
    data = scrape_product_data()
    if not data["success"]:
        return
        
    current_price = data["price"]
    product_title = data["title"]
    
    # Store history and evaluate logic rules using config thresholds
    log_price_to_db(product_title, current_price)
    
    if current_price < config.PRICE_THRESHOLD:
        alert_msg = (
            f"🚨 **Vektorcom Price Drop Notification** 🚨\n"
            f"**Product:** {product_title}\n"
            f"**Current Price:** ${current_price} (Below threshold of ${config.PRICE_THRESHOLD}!)\n"
            f"**Link:** {config.TARGET_STORE_URL}"
        )
        send_chat_notification(alert_msg)
    else:
        logging.info("Price remains stable. Monitoring loop resting.")

if __name__ == "__main__":
    main()
