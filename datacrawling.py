from dis import show_code
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import *
import os
import urllib.request
from format.template import getHTMLfile
import pandas as pd
import pathlib

class Bot():
    def __init__(self,player="Hide on bush",show_web=False):
    # set up
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.opened_tabs = 0
        self.PATH = "file://" + str(pathlib.Path(__file__).parent.resolve())
        self.show_web = show_web
        self.player = player
        
    def __closeTab(self,driver, opened_tabs):
        for i in range(opened_tabs):
            driver.switch_to.window(driver.window_handles[1])
            driver.close()

    # encrypt file names and urls
    def __encryptChampName(self,name):
        name = '-'.join(name.split(" "))
        return name

    def __encryptItemName(self,name):
        name = '_'.join(name.split(" "))
        return name
    
    def __encryptPlayerName(self, name):
        while " " in name:
            name = name.replace(" ", "+")
        return name

    # download champ's image
    def __downloadChampImage(self,driver, name):
        print(f"downloading {name}'s image")
        driver.implicitly_wait(20)
        driver.execute_script('window.open("","_blank");')
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        driver.get(f"https://www.leagueoflegends.com/en-us/champions/{name}/")
        imageSrc = driver.find_element(By.CLASS_NAME, "fyyYJz").find_element(By.TAG_NAME, "img").get_attribute("src")
        file_name = f"images/{name}.png"
        urllib.request.urlretrieve(imageSrc, file_name)
        
    # download item's image
    def __downloadItemImage(self,driver, item_name):
        print(f"downloading item: {item_name}")
        driver.implicitly_wait(20)
        driver.execute_script('window.open("","_blank");')
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        try:
            driver.get(f"https://leagueoflegends.fandom.com/wiki/{item_name}")
            item_src = driver.find_element(By.TAG_NAME, "section").find_element(By.TAG_NAME, 'img').get_attribute('src')
            file_name = f"items/{item_name}.png"
            urllib.request.urlretrieve(item_src, file_name)
        except:
            driver.close()
            driver.execute_script('window.open("","_blank");')
            driver.get(f"https://leagueoflegends.fandom.com/wiki/%27{item_name}%27")
            item_src = driver.find_element(By.TAG_NAME, "section").find_element(By.TAG_NAME, 'img').get_attribute('src')
            file_name = f"items/{item_name}.png"
            urllib.request.urlretrieve(item_src, file_name)
        
    # download html screenshot
    def __downloadHTMLfile(self, driver,path, idx):
        driver.implicitly_wait(20)
        driver.execute_script('window.open("","_blank");')
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        driver.get(path)
        driver.save_screenshot(f"screenshots/screenshot{idx}.png")
        
    # find elements in web
    def fetchData(self):
        self.driver.implicitly_wait(20)
        self.driver.get("https://www.leagueofgraphs.com/summoner/kr/"+self.__encryptPlayerName(self.player))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        see_more = self.driver.find_element(By.CLASS_NAME, "see_more_button")
        see_more2 = self.driver.find_element(By.CLASS_NAME, "see_more_ajax_button")
        try:
            see_more.click()
        except:
            see_more2.click()
        table = self.driver.find_elements(By.CLASS_NAME, "recentGamesTable")[-1]
        kdas = table.find_elements(By.CLASS_NAME, "kda")
        status = table.find_elements(By.CLASS_NAME, "victoryDefeatText")

        # # get kdas list
        kdas_list = []
        for kda in kdas:
            kdas_list.append(kda.text)
        print("kda length: ", len(kdas_list))
        
        # # get status list
        status_list = []
        for stat in status:
            status_list.append(stat.text)
        while '' in status_list:
            status_list.remove('')
        print("status length: ", len(status_list))
                
        # # get items list
        itemRows = table.find_elements(By.CLASS_NAME, "itemsColumnLight")
        rowsOfItems = []
        for itemRow in itemRows:
            items = itemRow.find_elements(By.TAG_NAME, 'img')
            rowOfItems = []
            for item in items:
                item_alt = item.get_attribute('alt')
                item_name = self.__encryptItemName(item_alt)
                rowOfItems.append(item_name)
            rowsOfItems.append(rowOfItems)

        # # get champs list
        champCells = table.find_elements(By.CLASS_NAME, "championCellLight")
        champs = []
        for cell in champCells:
            cell = cell.find_element(By.TAG_NAME, "img").get_attribute("title").lower()
            champs.append(self.__encryptChampName(cell))
        print("Champs length: ", len(champs))

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
        print('data length: ', len(data))
        df = pd.DataFrame(data)
        df.to_csv('data.csv', sep=',', encoding='utf-8')
        
        flatten_champs_list = list(dict.fromkeys(champs))

        # download champ image
        for champ in flatten_champs_list:
            isChampImageExist = os.path.exists(f"images/{champ}.png")
            if (not isChampImageExist):
                self.__downloadChampImage(self.driver, champ)
                self.opened_tabs += 1
            
        self.driver.switch_to.window(self.driver.current_window_handle)


        flatten_items_list = [item for sublist in rowsOfItems for item in sublist]
        flatten_items_list = list(dict.fromkeys(flatten_items_list))

        # download item image
        for item in flatten_items_list:
            isItemImageExist = os.path.exists(f"items/{item}.png")
            if not isItemImageExist:
                self.__downloadItemImage(self.driver, item)
                self.opened_tabs += 1
        
        # screenshot html 
        for idx, match in enumerate(data):
            isFileExist = os.path.exists(f"matchtemplates/template{idx}.html")
            isScreenShotExist = os.path.exists(f"screenshots/screenshot{idx}.png")
            path = f"{self.PATH}/matchtemplates/template{idx}.html"
            if not isScreenShotExist:
                self.__downloadHTMLfile(self.driver, path, idx)
                self.opened_tabs += 1
            if not isFileExist:
                with open(f'matchtemplates/template{idx}.html', 'w') as file:
                    html = getHTMLfile(match)
                    file.write(html)
                    file.close()
            
        # close tabs
        if self.opened_tabs > 0:
            self.__closeTab(self.driver, self.opened_tabs)
            self.opened_tabs = 0

        # finish fetching
        print("\nDone fetching data")
        while self.show_web:
            pass
        # return dataFrame
        df = pd.read_csv('data.csv', index_col=0)
        return df
        