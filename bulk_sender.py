#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import time
import random
import os
import urllib.request
from typing import List, Dict
from string import Template

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from rich.console import Console
from rich.progress import track
import winsound
from urllib.parse import quote


# ======================
# Configuration Constants
# ======================

CSV_FILE = "contacts.csv"
RETRY_LIMIT = 2
MIN_DELAY_SEC = 3
MAX_DELAY_SEC = 5
SESSION_DIR = os.path.join(os.getcwd(), "whatsapp_session")

REPLY_KEYWORDS = {"help", "support", "urgent", "problem"}
AUTO_REPLY_MESSAGE = "We'll contact you shortly! Our team is reviewing your request."
MONITOR_INTERVAL_SEC = 30

# Rich console setup
console = Console()


# ======================
# Utility Functions
# ======================

def log(message: str, style: str = "white") -> None:
    """Log timestamped message with Rich styling."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[{style}][{timestamp}] {message}[/]")


def beep_success() -> None:
    winsound.Beep(1000, 200)


def beep_fail() -> None:
    winsound.Beep(400, 400)


# ======================
# Selenium Setup & Helpers
# ======================

def configure_chrome_options() -> Options:
    """Configure Chrome options for WhatsApp Web automation — silent & clean."""
    chrome_options = Options()
    
    # Session persistence
    chrome_options.add_argument(f"--user-data-dir={SESSION_DIR}")
    chrome_options.add_argument("--profile-directory=Default")
    
    # Anti-bot evasion
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Stability/performance
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 🔇 SUPPRESS ALL BROWSER LOGS (critical for clean output)
    chrome_options.add_argument("--log-level=3")                      # FATAL only
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-component-update")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-service-autorun")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    return chrome_options


def check_internet_connection() -> bool:
    """Verify internet connectivity to WhatsApp Web."""
    try:
        urllib.request.urlopen("https://web.whatsapp.com", timeout=10)
        return True
    except Exception as e:
        log(f"❌ Network error: Cannot access WhatsApp Web — {e}", "red")
        return False


def initialize_driver() -> webdriver.Chrome:
    """Initialize and return a configured Chrome WebDriver — silent DevTools."""
    chrome_options = configure_chrome_options()
    
    # 🔇 Suppress "DevTools listening on..." message
    service = Service()
    service.log_path = os.devnull  # Discard ChromeDriver logs
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def wait_for_whatsapp_login(driver: webdriver.Chrome, timeout: int = 30) -> bool:
    """Wait until WhatsApp Web is logged in (chat list appears)."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Chat list"]'))
        )
        return True
    except TimeoutException:
        return False


def prompt_qr_scan(driver: webdriver.Chrome) -> None:
    """Prompt user to scan QR and validate login."""
    log("📱 Scan QR code in WhatsApp and press Enter when done...", "cyan")
    input()
    if not wait_for_whatsapp_login(driver):
        log("❌ Login failed after QR scan. Exiting.", "red")
        driver.quit()
        exit(1)


# ======================
# Message & Template Handling
# ======================

def render_message_template(template_str: str, name: str, phone: str) -> str:
    """Safely substitute placeholders in message template."""
    return Template(template_str).safe_substitute(
        name=name,
        phone=phone,
        date=time.strftime('%Y-%m-%d'),
        time=time.strftime('%H:%M')
    )


# ======================
# WhatsApp Interaction
# ======================

def send_whatsapp_message(
    driver: webdriver.Chrome,
    name: str,
    phone: str,
    raw_message: str,
    retry_limit: int = RETRY_LIMIT,
    is_reply: bool = False,
) -> bool:
    """
    Send a WhatsApp message to a phone number.
    Returns True if successful, False otherwise.
    """
    if not is_reply:
        message = render_message_template(raw_message, name, phone)
    else:
        message = raw_message

    encoded_message = quote(message)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
    main_window = driver.current_window_handle

    for attempt in range(1, retry_limit + 1):
        try:
            # Open new tab
            driver.execute_script(f"window.open('{url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])

            # Wait for input box
            wait = WebDriverWait(driver, 30)
            input_box = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                )
            )
            time.sleep(random.uniform(1, 3))

            # Send via ENTER or button fallback
            try:
                input_box.send_keys(Keys.ENTER)
            except Exception:
                send_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
                )
                send_button.click()

            log(f"✅ Sent to {name} ({phone})", "green")
            beep_success()

            # Cleanup tab
            time.sleep(2)
            driver.close()
            driver.switch_to.window(main_window)

            # Delay *only* for non-reply messages
            if not is_reply:
                delay = random.uniform(MIN_DELAY_SEC, MAX_DELAY_SEC)
                time.sleep(delay)

            return True

        except Exception as e:
            log(f"⚠ Attempt {attempt} failed for {phone}: {e}", "yellow")
            # Ensure we return to main window on failure
            try:
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(main_window)
            except Exception:
                pass
            time.sleep(5)

    log(f"❌ Failed to send to {phone}", "red")
    beep_fail()
    return False


# ======================
# Contact Processing
# ======================

def load_contacts_from_csv(csv_path: str) -> List[Dict[str, str]]:
    """Parse and validate contacts from CSV. Returns list of valid contacts."""
    contacts = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_phone = row.get("Phone", "").strip()
                name = row.get("Name", "").strip()
                message = row.get("Message", "").strip()

                # Clean phone: remove + and spaces
                phone = raw_phone.replace("+", "").replace(" ", "")
                if phone.isdigit() and len(phone) >= 10:
                    contacts.append({"name": name, "phone": phone, "message": message})
                else:
                    log(f"⚠ Invalid phone number skipped: '{raw_phone}'", "yellow")
    except Exception as e:
        log(f"❌ Error reading CSV '{csv_path}': {e}", "red")
        raise

    if not contacts:
        log("❌ No valid contacts found in CSV.", "red")
    return contacts


# ======================
# Main Workflow
# ======================

def main_bulk_send() -> None:
    """Main entry point: Load contacts and send messages."""
    if not check_internet_connection():
        exit(1)

    driver = initialize_driver()
    try:
        driver.get("https://web.whatsapp.com")

        if not wait_for_whatsapp_login(driver):
            prompt_qr_scan(driver)

        contacts = load_contacts_from_csv(CSV_FILE)
        if not contacts:
            return

        log(f"🚀 Starting bulk send for {len(contacts)} contacts...", "magenta")

        success_count = 0
        for contact in track(contacts, description="Sending messages…"):
            if send_whatsapp_message(
                driver, contact["name"], contact["phone"], contact["message"]
            ):
                success_count += 1

        log(
            f"🎉 Sent {success_count}/{len(contacts)} messages.",
            "bold green" if success_count == len(contacts) else "bold yellow"
        )

    except KeyboardInterrupt:
        log("\n👋 Bulk send interrupted by user.", "yellow")
    except Exception as e:
        log(f"💥 Unexpected error: {e}", "red")
        raise
    finally:
        log("CloseOperation: Quitting WebDriver...", "blue")
        driver.quit()


# ======================
# Entry Point
# ======================

if __name__ == "__main__":
    main_bulk_send()