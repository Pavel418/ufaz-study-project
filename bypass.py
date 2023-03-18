import time
import bs4

driver = uc.Chrome() 
driver.get('https://bina.az/items/2000000')
time.sleep(5)

# Get the HTML source of the page using the driver
html = driver.page_source
# Print the HTML source
print( html)

# Close the driver
driver.quit()