# import time

# # webdriver это и есть набор команд для управления браузером
# from selenium import webdriver

# # импортируем класс By, который позволяет выбрать способ поиска элемента
# from selenium.webdriver.common.by import By

# # инициализируем драйвер браузера. После этой команды вы должны увидеть новое открытое окно браузера
# driver = webdriver.Chrome()

# # команда time.sleep устанавливает паузу в 5 секунд, чтобы мы успели увидеть, что происходит в браузере
# time.sleep(5)

# # Метод get сообщает браузеру, что нужно открыть сайт по указанной ссылке
# driver.get("https://stepik.org/lesson/25969/step/12")
# time.sleep(5)

# # Метод find_element позволяет найти нужный элемент на сайте, указав путь к нему. Способы поиска элементов мы обсудим позже
# # Метод принимает в качестве аргументов способ поиска и значение, по которому мы будем искать
# # Ищем поле для ввода текста
# textarea = driver.find_element(By.CSS_SELECTOR, ".textarea")

# # Напишем текст ответа в найденное поле
# textarea.send_keys("get()")
# time.sleep(5)

# # Найдем кнопку, которая отправляет введенное решение
# submit_button = driver.find_element(By.CSS_SELECTOR, ".submit-submission")

# # Скажем драйверу, что нужно нажать на кнопку. После этой команды мы должны увидеть сообщение о правильном ответе
# submit_button.click()
# time.sleep(5)

# # После выполнения всех действий мы должны не забыть закрыть окно браузера
# driver.quit()



# курс python today по selenium!!!!!!!!!!!!!!!!!!

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# import time
# from fake_useragent import UserAgent


# url = "http://127.0.0.1:8000/"
# # service = Service(executable_path='C:\\Users\\shalutov\\Desktop\\python\\INTERNET_MARKET\\FAST_API\\chromedriver\\chromedriver.exe')
# useragent = UserAgent()

# options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={useragent.opera}")#юзер агент для браузера ие


# service = Service(executable_path=r'C:\Users\shalutov\Desktop\python\INTERNET_MARKET\FAST_API\chromedriver\chromedriver.exe')


# driver = webdriver.Chrome(service=service, options=options)
#сюда передаем абсолютный путь к драйверу хрома. По инфе из стековерфлоу, нужно так прописывать путь. Также обяз нужен актуальный хромдрайвер в папке.

# try:
# 	# driver.get(url=url)#открываем нашу урл
# 	#и делаем паузу	
# 	# time.sleep(5)

# 	# driver.get(url="https://rp5.ru/")
# 	# time.sleep(5)
# 	# driver.save_screenshot("2.png")
# 	# time.sleep(2)
# 	#в драйвере еще много разных функций, для примера выше сделал скрин страницы
# 	driver.get(url="https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
# 	time.sleep(10)

# except Exception as ex:
# 	print(ex)

# finally:
# 	driver.close()
# 	driver.quit()


# Python Selenium #2 Как изменить User-Agent Chrome, Firefox
#User-Agent это инфа о пользаке который посетил сайт. Можно так понимать кто зашел на сайт
# или можно скрыть того кто посетил сайт
# у хрома есть много опций. Сейчас будем юзать опцию user-agent
#опция перезаписывает дефолтный юзерагент, меняя на кастомный. ЗАчем его менять не понятно. 
# юзер агент это как бы инфа о пользаке который заходит на сайт о системе и тд
# юзерагент можно записывать в объект options
#также можно запускать браузер под другим IP адресом через прокси, то есть прокси это перенаправление маршрута поиска сайта, то есть запрос идет сначала на сервер прокси, потом от прокси на нужный нам ресурс, потом обратно



################################################################################################
#курс селениум алексей коледачкин!!!!!!!!!!!!!!!!!!!!!!!!!
#можно еще установить webdriver-manager
#он нужен для установки драйвера для браузера, чтобы ставить вручную вебдрайвер. 

# # инициализация драйвера
# from selenium import webdriver#импорт веьдрайвера для запуска браузера

# #драйвер для хрома
# from webdriver_manager.chrome import ChromeDriverManager#импортировали хромдрайвер

# from selenium.webdriver.chrome.service import Service#он появился в селениум4. Этот клас отвечает за установку драйвера, за его открытие и закрытие.

# #для firefox
# # from webdriver_manager.firefox import GeckoDriverManager
# # from selenium.webdriver.firefox.service import Service

# #для хрома
# #создаем объект service и в него установить драйвер
# service = Service(executable_path=ChromeDriverManager().install())#executable_path - это путь к драйверу браузера. В нашем случае это класс ChromeDriverManager, и у него мы вызываем метод install(). Получается автоматом ставится драйвер и не надо его в гугле качать вручную. 
# driver = webdriver.Chrome(service=service)#указываем service то есть даем в параметр объект которым будет управляться хром. 
# #раньше когда не было класса service нужно было руками писать открытие и закрытие. Сейчас все автоматом работает.


# # # для firefox
# # service = Service(executable_path=GeckoDriverManager().install())#класс Service от хрома работает и firefox почему-то, но криво, браузер не закрывается автоматом. 
# # driver = webdriver.Firefox(service=service)


# УПРАВЛЕНИЕ НАВИГАЦИЕЙ БРАУЗЕРА # Урок 3 - SELENIUM (Полный курс)

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://yandex.ru"
driver.get(url)#просто открыли ссылку
#добавим слип, чтобы браузер сразу не закрывался
time.sleep(10)#скрипт удет спать 5 сек и браузер не закроется пока не пройдет 5 сек. То есть клас Service так работает, что он не закрывает браузер пока скрипт не завершится весь. В дальнейшем будет спец методы для слипов и тд. 

driver.back()#возвращает браузер назад, как кнопка назад в браузере

time.sleep(5)

driver.forward()

time.sleep(5)

driver.refresh()

time.sleep(5)


# ПОЛУЧЕНИЕ ДАННЫХ И ИХ ВАЛИДАЦИЯ # Урок 4 - SELENIUM (Полный курс)



