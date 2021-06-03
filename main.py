import ctypes, os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# класс констант для окна сообщений функции ShowMessage
class _Const(object):
    ICON_EXLAIM = 0x30  # желтый треугольник
    ICON_INFO = 0x40    # синий восклицательный знак
    ICON_STOP = 0x10    # красный крестик
    MB_OK = 0

CONST = _Const()

def ShowMessage(title, text, btn_icon):
    # if system is Windows
    if os.name == 'nt':
        return ctypes.windll.user32.MessageBoxW(0, text, title, btn_icon)
    else:
        print(text)


options = Options()
options.add_argument("--headless")
# if chromedriver not found - load it
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# load page of SITV provider
driver.get('https://stat.sitv.com.ua')

login = driver.find_element_by_name("login")
pwd = driver.find_element_by_name("password")
btn = driver.find_element_by_name("commit")
# insert login for your cabinet
login.send_keys("")
# insert password for your cabinet
pwd.send_keys("")
btn.click()

delay = 20 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[5]/div/table/tbody/tr[2]/td[2]/p')))
    sum_count = driver.find_element_by_xpath("/html/body/div[3]/div[5]/div/table/tbody/tr[1]/td[2]/p").text
    date_exired = datetime.strptime(driver.find_element_by_xpath("/html/body/div[3]/div[5]/div/table/tbody/tr[2]/td[2]/p").text, "%d/%m/%Y")
    date_now = datetime.now()
    date_compare = (date_exired - date_now).days
    ShowMessage('Завершение работы', f"Интернет отключится через {date_compare} дня(ней).\nСумма на счету {sum_count}" if date_compare >= 0 else "Интернет уже отключен. Пополните ваш счет", CONST.MB_OK | CONST.ICON_INFO)
except TimeoutException:
    ShowMessage('Произошла ошибка', "Не смог зайти в личный кабинет.")

driver.quit()
