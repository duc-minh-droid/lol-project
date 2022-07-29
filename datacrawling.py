from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import *
import os
import urllib.request
from format.template import getHTMLfile

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

# # get status list
status_list = []
for stat in status:
    status_list.append(stat.text)
while '' in status_list:
    status_list.remove('')
        
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

# # get champs list
champCells = table.find_elements(By.CLASS_NAME, "championCellLight")
champs = []
for cell in champCells:
    cell = cell.find_element(By.TAG_NAME, "img").get_attribute("title").lower()
    champs.append(encryptChampName(cell))

### get data
data = []
isEqualSize = len(status_list)==len(kdas_list) and len(rowsOfItems)==len(champs) and len(status_list)==len(rowsOfItems)
if isEqualSize:
    for i in range(len(kdas_list)):
        data.append({
            "champion": champs[i],
            "kda": kdas_list[i],
            "status": status_list[i],
            "items": rowsOfItems[i]
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
    isChampImageExist = os.path.exists(f"images/{champ}.png")
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
    isItemImageExist = os.path.exists(f"items/{item}.png")
    if not isItemImageExist:
        downloadItemImage(driver, item)
        opened_tabs += 1
    
# download html screenshot
def downloadHTMLfile(driver,path, idx):
    driver.implicitly_wait(20)
    driver.execute_script('window.open("","_blank");')
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    driver.get(path)
    driver.save_screenshot(f"screenshots/screenshot{idx}.png")
    
for idx, match in enumerate(data):
    isFileExist = os.path.exists(f"matchtemplates/template{idx}.html")
    isScreenShotExist = os.path.exists(f"screenshots/screenshot{idx}.png")
    path = f"file:///Users/ducminh/Desktop/private-code/lol-project/matchtemplates/template{idx}.html"
    if not isFileExist:
        with open(f'matchtemplates/template{idx}.html', 'w') as file:
            html = getHTMLfile(match)
            file.write(html)
            file.close()
    if not isScreenShotExist:
        downloadHTMLfile(driver, path, idx)
        opened_tabs += 1
    
    
# close tabs
if opened_tabs > 0:
    closeTab(driver, opened_tabs)
    opened_tabs = 0


















while True:
    pass