from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

def check_string(input_text):
    if(len(input_text) != 0):
        if(input_text[0] == "(" and input_text[-1] == ")"):
            return True
    return False

def split_list(input_list, lengths):
    sub_lists = []
    start = 0
    for length in lengths:
        sub_lists.append(input_list[start:start + length])
        start += length
    return sub_lists

def main(index, duration):
    # Input box
    table_index = driver.find_element(By.XPATH, "//input[@type='text' and @name='gnum' and @size='3']")
    table_index.clear()
    # Choose button
    table_button = driver.find_element(By.XPATH, "//input[@type='submit' and @name='standard' and @value='Standard/Default Setting']")
    table_index.send_keys(str(index))
    # Slowing the program for safety reasons
    time.sleep(duration)
    table_button.click()
    time.sleep(duration)
    # Main data scraping
    multiplicity = []
    coordinates = []
    coordinate_deviation = ""
    # Since the site has a table hidden at the top it must be done this way
    tables = driver.find_elements(By.CSS_SELECTOR, "tbody")
    # Search the table
    table_rows = tables[1].find_elements(By.CSS_SELECTOR, "tr")
    for i in range(1, len(table_rows)):
        table_cells = table_rows[i].find_elements(By.CSS_SELECTOR, "td")
        try:
            multiplicity.append(int(table_cells[0].text))
        except(ValueError):
            continue
        # Final cell of row
        symmetries = table_cells[3].find_elements(By.CSS_SELECTOR, "a")
        coordinates.extend([sequence.text for sequence in symmetries])
    
    # If there is an additional parameter the multiplicity gets larger
    
    moved_coordinates = tables[1].find_elements(By.CSS_SELECTOR, "td")
    for i in range(len(moved_coordinates)):
        if(bool(re.match(r"\(.*\)\s\+\s\(.*\)", moved_coordinates[i].text))):
            coordinate_deviation = moved_coordinates[i].text
            
    divider = 1
    if(coordinate_deviation != ""):
        match(coordinate_deviation.count("(")):
            case 2: divider = 2
            case 3: divider = 3
            case 4: divider = 4
        
        for i in range(len(multiplicity)):
            multiplicity[i] = int(multiplicity[i] / divider)
    
    time.sleep(duration)
    driver.back()
    time.sleep(duration)
    
    return split_list(coordinates, multiplicity), multiplicity, coordinate_deviation, divider

if __name__ == "__main__":
    # Wait time
    duration = 1.5
    # Might be temporary (clears .txt file)
    open('wyckoff_positions_3D.txt', 'w').close()
    
    driver = webdriver.Edge()
    driver.get("https://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-wp-list")
    driver.implicitly_wait(5)
    
    for i in range(1,231):
        final_list, table_multiplicities, coordinate_deviation, divider = main(i, duration)

        with open("wyckoff_positions_3D.txt", "a") as file:
            file.write(f"# {i} {coordinate_deviation}\n")
            for i in range(len(final_list)):
                    if(coordinate_deviation != ""):
                        file.write(f"{table_multiplicities[i] * divider} : {final_list[i]} \n")
                    else:
                        file.write(f"{table_multiplicities[i]} : {final_list[i]} \n")
    
    driver.quit()