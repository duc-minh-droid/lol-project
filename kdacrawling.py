from fileinput import close
from tkinter import E
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import *
import os
import urllib.request

# set up
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(20)
driver.get("https://www.leagueofgraphs.com/summoner/kr/Hide+on+bush")
def closeTab(driver, opened_tabs):
    for i in range(opened_tabs):
        driver.switch_to.window(driver.window_handles[1])
        driver.close()

# find elements in web
table = driver.find_elements(By.CLASS_NAME, "recentGamesTable")[-1]
kdas = table.find_elements(By.CLASS_NAME, "kda")
status = table.find_elements(By.CLASS_NAME, "victoryDefeatText")

# download champ's image
# champCells = table.find_elements(By.CLASS_NAME, "championCellLight")
# champs = []
opened_tabs = 0
        
# def downloadChampImage(driver, name):
#     driver.implicitly_wait(20)
#     driver.execute_script('window.open("","_blank");')
#     driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
#     driver.get(f"https://www.leagueoflegends.com/en-us/champions/{name}/")
#     imageSrc = driver.find_element(By.CLASS_NAME, "fyyYJz").find_element(By.TAG_NAME, "img").get_attribute("src")
#     file_name = f"images/{name}.png"
#     urllib.request.urlretrieve(imageSrc, file_name)
    
# for cell in champCells:
#     cell = cell.find_element(By.TAG_NAME, "img").get_attribute("title").lower()
#     champs.append(cell)
# for champ in champs:
#     downloadChampImage(driver, champ)
#     opened_tabs += 1
    
# closeTab(driver, opened_tabs)
# opened_tabs = 0
    
# # get kdas list
# kdas_list = []
# for kda in kdas:
#     kdas_list.append(kda.text)

# # get status list
# status_list = []
# for stat in status:
#     status_list.append(stat.text)
# for stat in status_list:
#     if stat == '':
#         status_list.remove(stat)

# get item
def encryptItemName(name):
    name = '_'.join(name.split(" "))
    return name

def downloadItemImage(driver, item_name):
    driver.implicitly_wait(20)
    driver.execute_script('window.open("","_blank");')
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    driver.get(f"https://leagueoflegends.fandom.com/wiki/{item_name}")
    # item_src = driver.find_element(By.TAG_NAME, "body")
    print(driver.title)

itemRows = table.find_elements(By.CLASS_NAME, "itemsColumnLight")
rowsOfItems = []
for itemRow in itemRows:
    items = itemRow.find_elements(By.TAG_NAME, 'img')
    rowOfItems = []
    for item in items:
        item_name = encryptItemName(item.get_attribute('alt'))
        # downloadItemImage(driver, item_name)
        opened_tabs += 1
        rowOfItems.append(item_name)
    rowsOfItems.append(rowOfItems)

# closeTab(driver, opened_tabs)
# opened_tabs = 0
for i in range(3):
    downloadItemImage(driver, 'Void_Staff')

while True:
    pass