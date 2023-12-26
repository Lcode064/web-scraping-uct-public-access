from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Get the directory of the file containing student numbers
scr_dir = os.path.dirname(__file__)
rel_path = 'stdnum.txt'
abs_path = os.path.join(scr_dir, rel_path)

with open(abs_path, 'r') as std_num:
    students = std_num.read()

# Get the path for the txt file to write achievements to
scr = os.path.dirname(__file__)
path1 = 'achiv.txt'
fil = os.path.join(scr,path1)

std_list = students.split("\n")


# Initialize the WebDriver
driver = webdriver.Chrome()
url = 'https://publicaccess.uct.ac.za/psp/public/EMPLOYEE/SA/c/UCT_PUBLIC_MENU.UCT_SS_ADV_PUBLIC.GBL?'
driver.get(url)

# Find the achievements of each student

with open(fil, 'w') as writ:
    for std in std_list:
        # Switch to the iframe by its name or ID
        driver.switch_to.frame('ptifrmtgtframe')

        # Find elements within the iframe
        input_field = driver.find_element(By.ID, 'UCT_DERIVED_PUB_CAMPUS_ID')
        submit_button = driver.find_element(By.ID, 'UCT_DERIVED_PUB_SS_DERIVED_LINK')


        # Input a value into the field
        input_value = std
        input_field.send_keys(input_value)

        # Click the submit button
        submit_button.click()

        # Allow time for the next page to load
        time.sleep(10)  # Adjust this time according to the page load speed

        # Assuming elements are within a table, find the table first
        table = driver.find_element(By.ID, 'win0divPSPAGECONTAINER')  # Replace 'win0divPSPAGECONTAINER' with the correct table ID

        # Find all rows in the table
        rows = table.find_elements(By.XPATH, '//tr[contains(@id, "trHONORS$0_row")]')

        # Loop through all rows
        writ.write(std + ":\n")
        writ.write("-----------------------\n")
        for row in rows:
            # Get the text or attributes from elements within the row
            year = row.find_element(By.CSS_SELECTOR, 'span[id^="UCT_PUB_AWD_VW_ACAD_YEAR"]').text
            career = row.find_element(By.CSS_SELECTOR, 'span[id^="UCT_PUB_AWD_VW_ACAD_CAREER"]').text
            degree = row.find_element(By.CSS_SELECTOR, 'span[id^="UCT_PUB_AWD_VW_DESCR2"]').text
            description = row.find_element(By.CSS_SELECTOR, 'span[id^="UCT_PUB_AWD_VW_DESCRFORMAL"]').text
            date_received = row.find_element(By.CSS_SELECTOR, 'span[id^="UCT_PUB_AWD_VW_DT_RECVD"]').text
            
            # Print the extracted values
            writ.write("Year: " + year + "\n")
            writ.write("Career: " +career+"\n")
            writ.write("Degree: "+ degree+"\n")
            writ.write("Description: "+ description+"\n")
            writ.write("Date Received: "+ date_received+"\n")
            writ.write("---------------------\n")
        writ.write("\n******************************************************************\n")
        driver.get(url)

# Close the browser when done
driver.quit()
