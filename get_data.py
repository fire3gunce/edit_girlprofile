import csv
import sys
import logging
from datetime import date, datetime
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException

from web_startup import WebElement, driver, js_click, LoginInfo
from filepath import logfile
from main import WebSite, get_edit_buttons, get_girl_name


def main(shop_name, site_name):
    LoginInfo(shop_name).login(site_name)
    site = WebSite(shop_name, site_name)
    button_len: int = len(get_edit_buttons(site_name))
    with open('data.csv', 'w') as f:
        writer = csv.writer(f)
        i: int = 0
        while i < button_len:
            # 編集ボタンを押す
            edit_button = get_edit_buttons(site_name)[i]
            driver.execute_script('arguments[0].click();', edit_button)

            # キャスト名を取得する
            girl_name: str = get_girl_name(site_name)
            
            _plan: str = '//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[28]/td/div/input'
            plan: str = driver.find_element(By.XPATH, _plan).get_attribute('value')
            
            writer.writerow
            
            
            
        
    



if __name__ == '__main__':
    this_file: str = sys.argv[0]
    shop_name: str = sys.argv[1]
    site_name: str = sys.argv[2]
    try:
        main(shop_name, site_name)
    except: # 想定外のエラーログを出力。
        error_log: str = f'{logfile()}_{this_file}_{shop_name}.log'
        logging.basicConfig(filename=error_log, filemode='w', encoding='utf-8')
        now: datetime = datetime.now()
        logging.exception(now)
        print(f'想定外のエラー発生。\n"{error_log}"を参照。')
    else:
        print('正常に終了。')
    finally:
        driver.quit()