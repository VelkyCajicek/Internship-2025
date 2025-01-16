from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

def check_string(input_text):
    if(len(input_text) != 0):
        if(input_text[0] == "(" and input_text[-1] == ")"):
            return True
    return False

def split_list(input_list, lengths):
    sublists = []
    start = 0
    for length in lengths:
        sublists.append(input_list[start:start + length])
        start += length
    return sublists

def main(index):
    # Get name of group
    title = driver.find_element(By.CSS_SELECTOR, "h2").text
    # Input box
    table_index = driver.find_element(By.XPATH, "//input[@type='text' and @name='gnum' and @size='3']")
    table_index.clear()
    # Choose button
    table_button = driver.find_element(By.XPATH, "//input[@type='submit' and @name='standard' and @value='Standard/Default Setting']")
    table_index.send_keys(str(index))

    time.sleep(3)
    table_button.click()
    time.sleep(3)

    # Gets a text links
    symmetry_list = []
    symmetries_elements = driver.find_elements(By.CSS_SELECTOR, "a")
    for i in range(len(symmetries_elements)):
        if(check_string(symmetries_elements[i].text)):
            symmetry_list.append(symmetries_elements[i].text)

    # Multiplicities
    table_multiplicities = []
    table_multiplicities_raw = driver.find_elements(By.CSS_SELECTOR, "td")
    for i in range(len(table_multiplicities_raw)):
        if(bool(re.match(r"[0-9]+$", table_multiplicities_raw[i].text)) and table_multiplicities_raw[i].text != "1"):
            table_multiplicities.append(int(table_multiplicities_raw[i].text))

    time.sleep(3)
    driver.back()
    time.sleep(3)

    print(title)

    return split_list(symmetry_list, table_multiplicities), table_multiplicities

if __name__ == "__main__":
    # Might be temporary (clears .txt file)
    open('wyckoff_positions.txt', 'w').close()
    
    driver = webdriver.Edge()
    driver.get("https://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-wp-list")
    driver.implicitly_wait(5)
    
    for i in range(1,5):
        final_list, table_multiplicities = main(i)

        with open("wyckoff_positions.txt", "a") as file:
            file.write(f"# {i}\n")
            for i in range(len(final_list)):
                    file.write(f"{table_multiplicities[i]} : {final_list[i]} \n")
    
    driver.quit()