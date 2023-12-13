import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=options)
driver.implicitly_wait(1)
driver.set_window_size('1000', '1000')


class LoginInfo:
    def __init__(self, shop: str, site: str) -> None:
        config = configparser.ConfigParser()
        if shop == 'hanpa':
            config_path = '../../profile/profileH.ini'
        elif shop == 'gingin':
            config_path = '../../profile/profileG.ini'
        config.read(config_path, encoding='utf-8')

        self.user_id = config.get(site, 'id')
        self.user_pw = config.get(site, 'pw')
        self.site = site

        match self.site:
            case 'official':
                self.url = 'https://shop.f-webmas.com/login'
            case 'heaven':
                self.url = 'https://newmanager.cityheaven.net/'
            case 'bananavi':
                self.url = 'https://kanri.bananavi.jp/shizuoka/shopadmin/pc/'
            case 'delija':
                self.url = 'https://deli-fuzoku.jp/entry/'
            case 'fuuja':
                self.url = 'https://fuzoku.jp/entry/'
            case 'delitown':
                self.url = 'https://admin.dto.jp/a/auth/input'
            case 'ekichika':
                self.url = 'https://ranking-deli.jp/admin/login'
            case 'kuchikomi':
                self.url = 'https://fujoho.jp/index.php?p=login&from=logout'
            case 'purelovers':
                self.url = 'https://www.purelovers.com/shop/login/index/'
            case 'nukinavi':
                self.url = 'https://www.nukinavi-toukai.com/manager_new/login.aspx'

    def login(self) -> None:
        driver.get(self.url)

        match self.site:
            case 'official':
                input_id = driver.find_element(By.NAME, 'data[Owner][mail_address]')
                input_pw = driver.find_element(By.NAME, 'data[Owner][password]')
                login_btn = driver.find_element(By.CSS_SELECTOR, '.btn.btn-large')
            case 'heaven':
                input_id = driver.find_elements(By.ID, 'id')[1]
                input_pw = driver.find_elements(By.ID, 'pass')[1]
                login_btn = driver.find_elements(By.NAME, 'login')[1]
            case 'bananavi':
                input_id = driver.find_element(By.NAME, 'username')
                input_pw = driver.find_element(By.NAME, 'password')
                login_btn = driver.find_element(By.NAME, 'btn_login')
            case 'delija' | 'fuuja':
                input_id = driver.find_element(By.ID, 'form_username')
                input_pw = driver.find_element(By.ID, 'form_password')
                login_btn = driver.find_element(By.ID, 'button')
            case 'delitown':
                input_id = driver.find_element(By.NAME, 'login_id')
                input_pw = driver.find_element(By.NAME, 'password')
                login_btn = driver.find_element(By.ID ,'login_button')
            case 'ekichika':
                input_id = driver.find_element(By.ID, 'form_email')
                input_pw = driver.find_element(By.ID, 'form_password')
                login_btn = driver.find_element(By.ID, 'form_submit')
            case 'kuchikomi':
                input_id = driver.find_element(By.NAME, 'email')
                input_pw = driver.find_element(By.NAME, 'password')
                login_btn = driver.find_element(By.NAME, 'login')
            case 'purelovers':
                input_id = driver.find_element(By.NAME, 'id')
                input_pw = driver.find_element(By.NAME, 'password')
                login_btn = driver.find_elements(By.NAME, 'submit_button')[1]
            case 'nukinavi':
                input_id = driver.find_element(By.NAME, 'TxtId')
                input_pw = driver.find_element(By.NAME, 'TxtPass')
                login_btn = driver.find_element(By.NAME, 'Submit1')

        input_id.send_keys(self.user_id)
        input_pw.send_keys(self.user_pw)
        driver.execute_script('arguments[0].click();', login_btn)