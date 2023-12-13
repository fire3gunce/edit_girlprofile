import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from lib import start_up
from time import sleep


class WebSite:
    def __init__(self, shop_name: str , site_name: str) -> None:
        if shop_name == 'hanpa':
            self.target_op: str = 'ブルマ'
            self.exclusion_op: str = '拘束'
            self.target_comment: str = '特進料金'
            self.add_comment: str = '\n【延長料金30分12,000円頂く女の子になります。】'
            match site_name:
                case 'heaven':
                    self.girls_url: str\
                        = 'https://newmanager.cityheaven.net/C2GirlNonPublishList.php?shopdir=so_hanpajyanai_n'
                case 'delitown':
                    self.girls_url: str\
                        = 'https://admin.dto.jp/shop-admin/12014/gal/list'
                case 'kuchikomi':
                    self.girls_url: str\
                        = 'https://fujoho.jp/index.php?sh=17380&p=shp_girl_list'
        elif shop_name == 'gingin':
            self.target_comment: str = 'プレミアムクラス'
            self.add_comment: str = '\n【延長料金30分10,000円頂く女の子になります。】'
            match site_name:
                case 'heaven':
                    self.girls_url: str\
                        = 'https://newmanager.cityheaven.net/C2GirlNonPublishList.php?shopdir=so_waka-gin'
                case 'delitown':
                    self.girls_url: str\
                        = 'https://admin.dto.jp/shop-admin/17482/gal/list'
                case 'kuchikomi':
                    self.girls_url: str\
                        = 'https://fujoho.jp/index.php?sh=25965&p=shp_girl_list'

        match site_name:
            case 'bananavi':
                self.girls_url: str\
                    = 'https://kanri.bananavi.jp/shizuoka/shopadmin/pc/girl.php'
            case 'ekichika':
                self.girls_url: str\
                    = 'https://ranking-deli.jp/admin/girls/'
            case 'purelovers':
                self.girls_url: str\
                    = 'https://shop-admin.purelovers.com/shop/new-edit-girl/'
            case 'nukinavi':
                self.girls_url: str\
                    = 'https://www.nukinavi-toukai.com/manager_new/gals/'

        self.site_name: str = site_name

    def transition_to_girls(self) -> None:
        if self.site_name == 'delija' or self.site_name == 'fuuja':
            girls_page = driver.find_element(By.LINK_TEXT, '在籍嬢一覧')
            driver.execute_script('arguments[0].click();', girls_page)
        else:
            driver.get(self.girls_url)


def get_edit_buttons(site_name: str) -> list:
    match site_name:
        case 'heaven':
            sleep(1)
            edit_buttons: list = driver.find_elements(By.XPATH, '//input[@value="修正"]')
        case 'bananavi':
            edit_buttons: list = driver.find_elements(By.CLASS_NAME, 'girlname_name')
        case 'delija' | 'fuuja':
            sleep(1)
            edit_buttons: list = driver.find_elements(
                By.XPATH, '//input[@type="button" and @value="編集"]')
        case 'delitown':
            edit_buttons: list = driver.find_elements(By.XPATH, '//a[text()="編集"]')
        case 'ekichika':
            edit_buttons: list = driver.find_elements(By.XPATH, '//img[@alt="編集"]')
        case 'kuchikomi':
            i: int = 1
            edit_buttons: list = []
            while True:
                try:
                    button = driver.find_element(
                        By.XPATH,
                        f'//*[@id="page-content-wrapper"]/div[6]/div[2]/div[{i}]/ul/li[10]/a')
                    edit_buttons.append(button)
                    i += 1
                except NoSuchElementException:
                    break
        case 'purelovers':
            edit_buttons:list = driver.find_elements(By.XPATH, '//button[contains(text(),"	編集")]')
        case 'nukinavi':
            edit_buttons:list = driver.find_elements(By.CSS_SELECTOR, '.btn.bottom')
    return edit_buttons


def get_girl_name(site_name: str) -> str:
    match site_name:
        case 'heaven':
            girl_name: str = driver.find_element(By.NAME, 'girls_name').get_attribute('value')
        case 'bananavi':
            girl_name: str = driver.find_element(By.NAME, 'fudol_name').get_attribute('value')
        case 'delija' | 'fuuja':
            girl_name: str = driver.find_element(By.ID, 'form_girl_name').get_attribute('value')
        case 'delitown':
            girl_name: str = driver.find_element(By.ID, 'name').get_attribute('value')
        case 'ekichika':
            girl_name: str = driver.find_element(By.ID, 'form_name').get_attribute('value')
        case 'kuchikomi':
            girl_name: str = driver.find_elements(By.CLASS_NAME, 'input-block')[0].text
        case 'purelovers':
            girl_name: str = driver.find_element(By.NAME, 'name').get_attribute('value')
        case 'nukinavi':
            girl_name: str = driver.find_element(By.ID, 'txtName').get_attribute('value')
    return girl_name


def edit_comment(girl_name: str) -> None:
    try:
        comment_area = driver.find_element(
            By.XPATH, f"//textarea[contains(text(),'{site.target_comment}')]")
    except NoSuchElementException:
        pass
    else:
        comment_area.send_keys(Keys.CONTROL + Keys.END)
        comment_area.send_keys(site.add_comment)
        print(f"{girl_name}: 特進の延長料金追加")


def edit_options(site_name: str) -> None:
    match site_name:
        case 'heaven' | 'delija' | 'fuuja' | 'delitown' | 'ekichika':
            try:
                op_area = driver.find_element(
                    By.XPATH,
                    f"//input[not(contains(@value,'{site.exclusion_op}')) \
                    and contains(@value,'{site.target_op}')]")
            except NoSuchElementException:
                pass
            else:
                op_value: str = op_area.get_attribute('value')
                new_op_value: str = op_value.replace(site.target_op, '')
                op_area.send_keys(Keys.CONTROL, 'a')
                op_area.send_keys(Keys.DELETE)
                op_area.send_keys(new_op_value)
        case 'bananavi' | 'kuchikomi' | 'nukinavi':
            try:
                op_area = driver.find_element(
                    By.XPATH,
                    f"//textarea[not(contains(text(),'{site.exclusion_op}')) \
                    and contains(text(),'{site.target_op}')]")
            except NoSuchElementException:
                pass
            else:
                op_value: str = op_area.text
                new_op_value: str = op_value.replace(site.target_op, '')
                op_area.send_keys(Keys.CONTROL, 'a')
                op_area.send_keys(Keys.DELETE)
                op_area.send_keys(new_op_value)


def do_post(site_name: str) -> None:
    def return_to_girls():
        WebSite(shop_name, site_name).transition_to_girls()

    match site_name:
        case 'heaven':
            submit = driver.find_element(By.XPATH, '//input[@value="更新する"]')
            driver.execute_script('arguments[0].click();', submit)
            Alert(driver).accept()
            return_to_girls()
        case 'bananavi':
            submit = driver.find_element(By.XPATH, '//input[@value="確認画面へ"]')
            driver.execute_script('arguments[0].click();', submit)
            done = driver.find_element(By.NAME, 'send')
            driver.execute_script('arguments[0].click();', done)
            Alert(driver).accept()
        case 'delija':
            submit = driver.find_element(By.XPATH, '//label[text()="登録する"]')
            driver.execute_script('arguments[0].click();', submit)
        case 'fuuja':
            submit = driver.find_element(By.NAME, 'entry-submit')
            driver.execute_script('arguments[0].click();', submit)
        case 'delitown':
            submit = driver.find_element(By.XPATH, '//input[@value="確認画面へ進む"]')
            driver.execute_script('arguments[0].click();', submit)
            done = driver.find_element(By.XPATH, '//input[@value="変更する"]')
            driver.execute_script('arguments[0].click();', done)
            sleep(1)
        case 'ekichika':
            submit = driver.find_element(By.ID, 'form_update-btn')
            driver.execute_script('arguments[0].click();', submit)
            return_to_girls()
        case 'kuchikomi':
            submit = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn_submit')
            driver.execute_script('arguments[0].click();', submit)
            done = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn_submit')
            driver.execute_script('arguments[0].click();', done)
        case 'purelovers':
            submit = driver.find_element(By.NAME, 'submit_button')
            driver.execute_script('arguments[0].click();', submit)
            done = driver.find_element(
                By.XPATH, '//input[@name="submit_button" and @value="更新"]')
            driver.execute_script('arguments[0].click();', done)
            return_to_girls()
        case 'nukinavi':
            submit = driver.find_element(By.NAME, 'ctl00$c_body$ctl11')
            driver.execute_script('arguments[0].click();', submit)
            done = driver.find_element(By.NAME, 'ctl00$c_body$ctl20')
            driver.execute_script('arguments[0].click();', done)
            return_to_girls()


def main() -> None:
    button_len: int = len(get_edit_buttons(site_name))
    i: int = 0
    while i < button_len:
        # 編集ボタンを押す
        edit_button = get_edit_buttons(site_name)[i]
        driver.execute_script('arguments[0].click();', edit_button)

        # キャスト名を取得する
        girl_name: str = get_girl_name(site_name)

        # 店長コメント編集
        edit_comment(girl_name)

        # OP編集
        if shop_name == 'hanpa':
            edit_options(site_name)

        # 変更した内容で更新する
        do_post(site_name)

        i += 1
        print(f"{girl_name}: 完了({i}/{button_len})")


shop_name: str = sys.argv[1]
site_name: str = sys.argv[2]
driver = start_up.driver

site = WebSite(shop_name, site_name)
login = start_up.LoginInfo(shop_name, site_name)
login.login()
site.transition_to_girls()
main()

if site_name == 'bananavi':
    i: int = 2
    while True:
        try:
            next_button = driver.find_element(By.XPATH, '//a[@title="next page"]')
        except NoSuchElementException:
            break
        else:
            driver.execute_script('arguments[0].click();', next_button)
            print(f'\n-------{i}ページ目-------')
            main()
            i += 1
elif site_name == 'nukinavi':
    i: int = 2
    while True:
        next_button = driver.find_element(By.XPATH, '//a[text()="≫"]')
        if next_button.get_attribute('href') != 'javascript:void(0)':
            driver.execute_script('arguments[0].click();', next_button)
            print(f'\n-------{i}ページ目-------')
            main()
            i += 1
        else:
            break

driver.quit()