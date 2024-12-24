from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
from collections import Counter
import tkinter.filedialog as fd
import tkinter.messagebox as mbx
import time
import pyfiglet
import os

display_text = big_text = pyfiglet.figlet_format("KENO !", font="slant")
print(display_text)

input("Press enter [Entrée] to select the path to Chrome Webdriver >>> ")
try:
    of = fd.askopenfile(
        title="Chrome WebDriver",
        filetypes=(("Executable file", "*.exe"),)
    )

    service_path = of.name
    url = "https://tvbetframe29.com/?lng=FR&token=5a7db4ce-09f2-45c4-8a05-00d370655f26&clientId=5753&tagId=10&singleGame=9#/game/9/"

    print("Preparing webdriver options and services...")
    service = Service(service_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    print("Initializing webdriver...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_position(-10000, 0)

    try:
        print("Connecting to 1xbet servers...")
        driver.get(url)
        print("Visiting webpage, this may take a few seconds...")
        wait = WebDriverWait(driver, 20)
        print("Fetching necessary data...")

        try:
            print("Selecting 'Aleatoire' button to click it, class=btn-game-variation__text...")
            div_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-game-variation__text')))
            results_array = []

            print("All things are ready ! Fetching 50 selected arrays...")
            for i in range(50):
                try:
                    div_element.click()
                except ElementClickInterceptedException:
                    print("Element not clickable yet. Retrying...")
                    mbx.showerror("ERROR", "Element not clickable yet. Retrying...")
                    continue

                time.sleep(2)

                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                div_elements = soup.find_all('div', class_='game-cell--has-selected')

                if not div_elements:
                    print("No elements found with the specified class. Retrying...")
                    mbx.showerror("ERROR","No elements found with the specified class. Retrying...")
                    continue

                mycutearray = [element.get_text() for element in div_elements]
                results_array.append(mycutearray)
                print(f"Selected array [{i+1}]: ", str(mycutearray).strip("''[]"))

            all_numbers = [num for array in results_array for num in array]
            count = Counter(all_numbers)
            most_common_number, count_of_most_common = count.most_common(1)[0]
            print(f"{most_common_number} (repeated {count_of_most_common} times)")
            mbx.showinfo("INFO", f"Most common number: {most_common_number} (repeated {count_of_most_common} times)")

        except TimeoutException as toe:
            print("Element not found within the given time frame. Check if the class name is correct or if the element is present on the page.")
            mbx.showerror("ERROR", f"Element not found within the given time frame. Check if the class name is correct or if the element is present on the page.\n{str(toe)}")

    except Exception as e:
        print(f"An error occurred: {e}")
        mbx.showerror("ERROR", f"An error occurred: {e}")
except Exception:
    mbx.showwarning("WARNING", "Select the Chrome WebDriver to continue !")
    quit()