from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import *
import os
import urllib.request
import numpy as np

# set up
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(20)
driver.get("https://www.leagueofgraphs.com/summoner/kr/Hide+on+bush")
def closeTab(driver, opened_tabs):
    for i in range(opened_tabs):
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
opened_tabs = 0

# encrypt file names and urls
def encryptChampName(name):
    name = '-'.join(name.split(" "))
    return name

def encryptItemName(name):
    name = '_'.join(name.split(" "))
    return name

# find elements in web
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
see_more = driver.find_element(By.CLASS_NAME, "see_more_button")
see_more.click()
table = driver.find_elements(By.CLASS_NAME, "recentGamesTable")[-1]
kdas = table.find_elements(By.CLASS_NAME, "kda")
status = table.find_elements(By.CLASS_NAME, "victoryDefeatText")

# # get kdas list
kdas_list = []
for kda in kdas:
    kdas_list.append(kda.text)
print(kdas_list)

# # get status list
status_list = []
for stat in status:
    status_list.append(stat.text)
while '' in status_list:
    status_list.remove('')
print(status_list)
        
# # get items list
itemRows = table.find_elements(By.CLASS_NAME, "itemsColumnLight")
rowsOfItems = []
for itemRow in itemRows:
    items = itemRow.find_elements(By.TAG_NAME, 'img')
    rowOfItems = []
    for item in items:
        item_name = encryptItemName(item.get_attribute('alt'))
        rowOfItems.append(item_name)
    rowsOfItems.append(rowOfItems)
print(rowsOfItems)

# # get champs list
champCells = table.find_elements(By.CLASS_NAME, "championCellLight")
champs = []
for cell in champCells:
    cell = cell.find_element(By.TAG_NAME, "img").get_attribute("title").lower()
    champs.append(encryptChampName(cell))
print(champs)

### get data
data = []
if (len(status)==len(kdas) and len(items)==len(champs) and len(status)==len(items)):
    for i in range(len(status)):
        data.append({
            "champion": champs[i],
            "kda": kdas[i],
            "status": status[i],
            "items": items[i]
        })

# download champ's image
def downloadChampImage(driver, name):
    print(f"downloading {name}'s image")
    driver.implicitly_wait(20)
    driver.execute_script('window.open("","_blank");')
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    driver.get(f"https://www.leagueoflegends.com/en-us/champions/{name}/")
    imageSrc = driver.find_element(By.CLASS_NAME, "fyyYJz").find_element(By.TAG_NAME, "img").get_attribute("src")
    file_name = f"images/{name}.png"
    urllib.request.urlretrieve(imageSrc, file_name)

flatten_champs_list = list(dict.fromkeys(champs))

for champ in flatten_champs_list:
    isChampImageExist = os.path.exists(f"C:\\Users\\Administrator\\Documents\\GitHub\\lol-project\\images\\{champ}.png")
    if (not isChampImageExist):
        downloadChampImage(driver, champ)
        opened_tabs += 1
    
driver.switch_to.window(driver.current_window_handle)

# download item's image
def downloadItemImage(driver, item_name):
    driver.implicitly_wait(20)
    driver.execute_script('window.open("","_blank");')
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    driver.get(f"https://leagueoflegends.fandom.com/wiki/{item_name}")
    item_src = driver.find_element(By.TAG_NAME, "section").find_element(By.TAG_NAME, 'img').get_attribute('src')
    file_name = f"items/{item_name}.png"
    urllib.request.urlretrieve(item_src, file_name)

flatten_items_list = [item for sublist in rowsOfItems for item in sublist]
flatten_items_list = list(dict.fromkeys(flatten_items_list))

for item in flatten_items_list:
    isItemImageExist = os.path.exists(f"C:\\Users\\Administrator\\Documents\\GitHub\\lol-project\\items\\{item}.png")
    if not isItemImageExist:
        downloadItemImage(driver, item)
        opened_tabs += 1
    
if opened_tabs > 0:
    closeTab(driver, opened_tabs)
    opened_tabs = 0


















while True:
    pass