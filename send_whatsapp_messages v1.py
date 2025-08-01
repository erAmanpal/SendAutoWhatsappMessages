import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from urllib.parse import quote

# Configure Edge options to avoid detection
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')

# Define the path to your EdgeDriver
service = Service(executable_path="C:\\Users\\amanp\\OneDrive\\Desktop\\My data\\2526 1\\msedgedriver.exe")

# Load the CSV with required headers: Name, Phone, Message
try:
    #contacts_df = pd.read_csv("contacts.csv")
    contacts_df = pd.read_csv('contacts.csv', dtype={'Phone': str})
except Exception as e:
    print(f"❌ Failed to read contacts.csv: {e}")
    exit()

# Ensure required columns exist
required_cols = {"Name", "Phone", "Message"}
if not required_cols.issubset(contacts_df.columns):
    print(f"❌ CSV file must contain the columns: {required_cols}")
    exit()

# Start Edge browser with WhatsApp Web
driver = webdriver.Edge(service=service, options=options)
driver.get("https://web.whatsapp.com")
print("📷 Please scan the QR code if not logged in.")
input("✅ Press Enter after WhatsApp Web has loaded...")

# Loop through contacts and send messages
for index, row in contacts_df.iterrows():
    name = str(row['Name']).strip()
    phone = str(row['Phone']).strip()
    message = str(row['Message']).strip()

    # Skip invalid numbers (must start with +)
    if not phone.startswith('+'):
        print(f"⚠️ Skipping invalid number (must start with '+'): {phone}")
        continue

    # Encode message for URL
    encoded_message = quote(message)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"

    driver.get(url)
    time.sleep(10)  # Wait for chat to load (adjust if needed)

    try:
        # Click the send button
        send_button = driver.find_element(By.XPATH, "//button[@aria-label='Send']")
        send_button.click()
        print(f"✅ Message sent to {phone} ({name})")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Failed to send message to {phone} ({name}): {e}")
        continue

print("🎉 All messages processed.")
driver.quit()
