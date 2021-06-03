from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

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
    print( f"Интернет отключится через {date_compare} дня(ней). Сумма на счету {sum_count}" if date_compare >= 0 else "Интернет уже отключен. Пополните ваш счет" )
except TimeoutException:
    print("Не смог зайти в личный кабинет.")
