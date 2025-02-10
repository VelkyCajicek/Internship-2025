from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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
    table_button = driver.find_element(By.XPATH, "//input[@type='submit' and @name='list' and @value='Standard/Default Setting']")
    table_index.send_keys(str(index))
    # Slowing the program for safety reasons
    time.sleep(duration)
    table_button.click()
    time.sleep(duration)
    # Main data scraping
    multiplicity = []
    coordinates = []
    coordinate_deviation = ""
    wyckoff_letters = []
    # Since the site has a table hidden at the top it must be done this way
    tables = driver.find_elements(By.CSS_SELECTOR, "tbody")
    # Search the table
    table_rows = tables[1].find_elements(By.CSS_SELECTOR, "tr")
    # Index 1 here since for some reason there is an invisible row
    for i in range(1, len(table_rows)):
        table_cells = table_rows[i].find_elements(By.CSS_SELECTOR, "td")
        # First cell of row
        # Try is there since the shift can appear in the first row
        try:
            multiplicity.append(int(table_cells[0].text))
        except(ValueError):
            coordinate_deviation = table_cells[0].text
            continue
        wyckoff_letters.extend(table_cells[1].text)
        # Final cell of row
        symmetries = table_cells[3].find_elements(By.CSS_SELECTOR, "a")
        coordinates.extend([sequence.text for sequence in symmetries])
    
    # If there is an additional parameter the multiplicity gets larger
    if(coordinate_deviation != ""):
        for i in range(len(multiplicity)):
            multiplicity[i] = int(multiplicity[i] / 2)
    
    time.sleep(duration)
    driver.back()
    time.sleep(duration)
    
    return split_list(coordinates, multiplicity), multiplicity, coordinate_deviation, wyckoff_letters
    
        
if __name__ == "__main__":
    # Create a .txt file for the results
    open('wyckoff_positions_2D_Letters.txt', 'w').close()
    # Determines how much the program is slowed
    duration = 1.5
    final_list = []
    
    driver = webdriver.Edge()
    driver.get("https://www.cryst.ehu.es/plane/get_plane_wp.html")
    driver.implicitly_wait(5)

    for i in range(1, 18):
        final_list, multiplicity, coordinate_deviation, wyckoff_letters = main(i, duration)
        
        with open("wyckoff_positions_2D_Letters.txt", "a") as file:
            file.write(f"# {i} {coordinate_deviation}\n")
            for i in range(len(final_list)):
                if(coordinate_deviation != ""):
                    file.write(f"{wyckoff_letters[i]} : {multiplicity[i] * 2} : {final_list[i]} \n")
                else:
                    file.write(f"{wyckoff_letters[i]} : {multiplicity[i]} : {final_list[i]} \n")
    
    driver.quit()