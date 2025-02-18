import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver with webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the target webpage
driver.get("https://www.sastra.edu/about-us/mission-vision.html")  # Change this to your desired webpage

# Create a dictionary to store the extracted data
ui_elements = {
    "static_texts": [],
    "buttons": [],
    "input_fields": [],
    "links": [],
    "dropdowns": [],
    "checkboxes": [],
    "radio_buttons": [],
    "images": []
}

# Extract Static Texts
static_texts = driver.find_elements(By.XPATH, "//p | //span | //div")
for text in static_texts:
    content = text.text.strip()
    if content:
        ui_elements["static_texts"].append(content)

# Extract Buttons
buttons = driver.find_elements(By.XPATH, "//button | //input[@type='submit'] | //input[@type='button']")
for btn in buttons:
    btn_text = btn.text.strip() or btn.get_attribute("value")
    if btn_text:
        ui_elements["buttons"].append(btn_text)

# Extract Input Fields
inputs = driver.find_elements(By.XPATH, "//input[@type='text'] | //input[@type='search'] | //textarea")
for inp in inputs:
    placeholder = inp.get_attribute("placeholder") or "No placeholder"
    ui_elements["input_fields"].append(placeholder)

# Extract Links
links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    href = link.get_attribute("href")
    text = link.text.strip() or "No visible text"
    if href:
        ui_elements["links"].append({"text": text, "href": href})

# Extract Dropdowns
dropdowns = driver.find_elements(By.TAG_NAME, "select")
for dropdown in dropdowns:
    options = dropdown.find_elements(By.TAG_NAME, "option")
    option_texts = [opt.text for opt in options]
    ui_elements["dropdowns"].append(option_texts)

# Extract Checkboxes
checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
for checkbox in checkboxes:
    name = checkbox.get_attribute("name") or "Unnamed Checkbox"
    checked = checkbox.is_selected()
    ui_elements["checkboxes"].append({"name": name, "checked": checked})

# Extract Radio Buttons
radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio']")
for radio in radio_buttons:
    name = radio.get_attribute("name") or "Unnamed Radio Button"
    checked = radio.is_selected()
    ui_elements["radio_buttons"].append({"name": name, "checked": checked})

# Extract Images
images = driver.find_elements(By.TAG_NAME, "img")
for img in images:
    alt_text = img.get_attribute("alt") or "No alt text"
    src = img.get_attribute("src")
    ui_elements["images"].append({"alt": alt_text, "src": src})

# Close WebDriver
driver.quit()

# Save the data to a JSON file
with open("ui_elements.json", "w") as json_file:
    json.dump(ui_elements, json_file, indent=4)

print(" UI elements successfully saved to 'ui_elements.json'!")
