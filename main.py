from datetime import datetime
from bs4 import BeautifulSoup
import mechanize

url = 'https://stat.sitv.com.ua/personal_log_in'
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Mozilla/5.0')]
br.open(url, timeout=10.0)

try:
    form = br.forms()[1]
    # put your username here
    form['login'] = ''
    # put your pasword here
    form['password'] = ''
    html = br.open( form.click(name='commit'), timeout=10.0 ).get_data()
    br.close()
    bs = BeautifulSoup(html, 'lxml')
    info_container = bs.findAll('div', {'class': 'info_container'})[1].findAll('p')
    sum_count, date_expired = (info.text for info in info_container[1::2])
    date_compare = (datetime.strptime(date_expired, "%d/%m/%Y") - datetime.now()).days
    if date_compare == 0:
        print( 'Быстрее пополняй счет.\nИнтернет сегодня отключится!' )
    elif date_compare < 0:
        print( "Интернет уже отключен. Пополните ваш счет!" )
    elif 0 < date_compare <= 2:
        print( f"Интернет отключится через {date_compare} дня(ей). Сумма на счету {sum_count}" )
except:
    br.close()
    print( 'Не смог зайти в кабинет пользователя.\nПроверьте логин и пароль.' )
    
