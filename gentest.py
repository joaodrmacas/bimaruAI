from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_driver_binary = "C:/Users/Massas/OneDrive/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

# Create a new instance of the web driver

# Open the website
driver.get("https://lukerissacher.com/battleships")

# Find and click the "10x10" button
ten_by_ten_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "Btn10"))
)
ten_by_ten_button.click()

# Find and click the "Settings" button
settings_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "BtnSettings"))
)
settings_button.click()

# Find and click the "Hard Mode" checkbox
hard_mode_checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "ChkHardMode"))
)
hard_mode_checkbox.click()

close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "popup-close"))
)
close_button.click()



#Ler Tabuleiro

for test in range(100):

    page_source = driver.page_source

    # Use Beautiful Soup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the table with class 'puzzle width-10'
    table = soup.find('table', class_='puzzle width-10')

    # Find the first row in the table
    table = table.find_all('tr')
    first_row = table[0]

    # Find all the cells (td) in the first row
    cells = first_row.find_all('th')
    col_values = [int(cell.get_text()) for cell in cells[1:]]
    row_values=[]

    hints = []

    for i in range(1,11):
        row_values.append(int(table[i].find('th').get_text()))
        row = table[i].find_all('td')
        for j in range(len(row)):
            i_element = row[j].find('i')
            
            if i_element is not None and 'blank' not in i_element.get('class', []):
                classes = i_element.get('class',[])
                if classes[0]=='revealed':
                    typed = classes[1]
                    if typed == 'sub':
                        typed = 'C'
                    if typed == 'cap-bottom':
                        typed = 'B'
                    if typed == 'middle':
                        typed = 'M'
                    if typed == 'cap-right':
                        typed = 'R'
                    if typed == 'cap-left':
                        typed = 'L'
                    if typed == 'cap-top':
                        typed = 'T'
                else:
                    typed = 'W'
                hints.append((i-1,j,typed))


    # Copy the values of each cell into an array

    fname = f'tests/test{test}.txt'
    with open(fname, 'w+') as file:
        # Write the column values
        file.write('ROW\t' + '\t'.join(str(value) for value in row_values) + '\n')
        
        # Write the row values
        file.write('COLUMN\t' + '\t'.join(str(value) for value in col_values) + '\n')
        
        # Write the length of hints array
        file.write(str(len(hints)) + '\n')
        
        # Write the hints
        for hint in hints:
            file.write('HINT\t' + '\t'.join(str(value) for value in hint) + '\n')
    
    new = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "BtnNew"))
    )
    new.click()

    # Print the array of cell values
    # Close the browser
driver.quit()