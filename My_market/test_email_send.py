import smtplib
import os
from email.mime.text import MIMEText#это для написания в письме кирилицы

def send_email(message):
	sender = 
	password = 


	serv = 'smtp.gmail.com'
	port = 587
	# server = smtplib.SMTP('сервер', 'порт')#сделали объект сервера
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()#запустили шифрованный обмен по тлс

	try:#логинимся и отправляем сообщения
		server.login(sender, password)
		# server.sendemail('отправитель', 'получатель', f"Subject: тема сообщения\n{message}")#тут будет передваться в письмо только англ текст, message это текст сообщения
		msg = MIMEText(message)
		msg['Subject'] = "Тема сообщения"
		# server.sendemail('отправитель', 'получатель', msg.as_string())#модно указывать sender и тд
		server.sendemail(sender, sender, msg.as_string())
		return 'Письмо успешно отправлено'


	except Exception as _ex:#в случае ошибки будет сообщение выводиться
		return f'ОШИБКА: ==> {_ex}\n Проверьте ваш логин и пароль от почты'


#также разблокировать доступ к почте от ненадежных приложений, иначе не сможем проходить аутентификацию на gmail через питон скрипт
# ссылка для настройки: https://myaccount.google.com/u/0/lesssecureapps



# https://www.youtube.com/watch?v=fn1zQj02qN0&ab_channel=PythonToday
# Анонимная, временная почта на Python для принятия кодов активации | Фриланс на Python

# https://www.youtube.com/watch?v=VniC5LAOYjY&ab_channel=PythonToday
# Практика Python | Как отправить HTML письмо с помощью Python | Email рассылка | Gmail Python





def main():
	message = input('Введите ваше сообшение: ')
	print(send_email(message=message))



if __name__ == "__main__":
	main()