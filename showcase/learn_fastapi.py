# uvicron это как бы переводчик между питоном и nginx
#клиент отправляет запрос (или через сайт, мобильное приложение, постман, терминал и тд) на наш сервер
# через hhtps или http на 80 или 443 порт
#далее выступает reverse proxy сервер, чаще всего это nginx. Далее nginx передает запрос на ASGI, и ASGI передает это в наше приложение на fastapi написанное на питоне
#само приложение не умеет интегрироваться напрямую в сеть инета и ему нужны посредники, которые будут например защищать от ддос атак например, для этого нужен nginx. Но nginx не умеет работать с питоновскими приложениями. Для этого нужен uvicorn, он для взаимодействия в питоновским приложением. uvicorn асинхронный , если примерно то он переводит с питоновкого на язык nginx
#то есть прилетает запрос в nginx, он отправляет это в uvicorn, далее отправляется в наше приложение и обрабатывается какая-то логика приложения. Далее обратно по той же цепочке, fastapi--uvicorn--nginx--клиент
#fastapi основан на Starlette и Pydentic
# Starlette - ответчает за веб
# Pydentic - отвечает за сериализацию и валидацию. 
# проект у препода: платформа для обучения для студентов
#для юзеров лучше юзать uuid вместо id.
#инфа про докер есть в первом видео ост 15 мин:
# https://www.youtube.com/watch?v=UkwpJyvf8CA&list=PLlKID9PnOE5jiWTTsshCXdz5qvg8JWezX&ab_channel=luchanos
#он делает постгерс в докер файле. ВЕРНУТЬСЯ К ДОКЕРУ ПОЗЖЕ.
#немного поправил движок алхимии
#логика в добавлении пользователя:!!!!!!!!!!!!!!!!!!!!!
# он там сделал класс, это на 27 мин. В котором будет добавляться пользователь в сессию. Выглядит странно, но вроде норм. 

#также сделал базовый класс для схем pydentic и в нем прописал класс Config в котором прописал:
# orm_mode = True
#это чтобы Pydentic переводил все данные в Json, то есть в словари. Потом можно наследовать всех схемы на основе этого класса, а не BaseModel. 
# юзера валидировал как uuid.UUID в модели Pydentic, странно
#сделал еще валидаторы ФИО, чтобы должны быть только буквы в ФИО. Кажется верное решение. У меня просто name, типа логин. Мне наверно пока не надо.
#далее он валидирует роутер юзера схемой Pydentic которую он сделал для юзера
#в алембик можно писать не асинхронный psycopg2
#в постмане можно писать ссылки и тип запроса, там возвращается ответ от сервера. По сути похоже на доку фаст апи swagger. 


#архитектура авторизации!!!!!!!!!!!!!!!!!!!!!!!!
#клиент делает запрос к серверу и передает туда логин и пароль. Сервер отдает клиенту refresh токен через  HTTP_ONLY COOKIE, он должен получен только через http, и не может быть получен с помощью JS и не может быть иным способом изменен с помощью JS. Срок жизни рефреш токена долгий, зависит от масштаба проекта. Обычно этот токен содержит цифровой отпечаток, он содержит инфу о клиенте который сделал запрос. То есть инфа о браузере, заголовки в запросе и тд. Эту инфу нужно проверять каждый раз когда будем работать с рефреш токеном. Обновляет рефреш токен либо сам пользователь, либо сервер. Лучше если будет обновлять рефреш токен сам пользователь, введя свои логин и пароль. 
#есть правило, 1 рефреш токен может обмениваться на 1 рефреш токен.
#Сервер содержит базу данных, которая содержит инфу о состоянии всех рефреш токенов. То есть сервер знает что происходит с каждым рефреш токеном. То есть мы можем фиксировать что какой-то токен ранее уже менялся без аутентификации - к примеру. И если пользователь захочет получить новый тот же самый рефреш токен, то он не сможет это сделать. В случае если злоумышленник получил рефреш токен и пытается его обновить, то он также не сможет это сделать. И это будет дубль и тогда и новый и старый токены попадают в блек лист (черный список). Также в черный список попадают все токены, которые не прошли отпечаток пальца (отпечаток пользователя). И тогда система будет заставлять повторно пройти ауетентификацию. Хранится рефреш токен только на сервере, все что касается рефреш токена - это взаимодействие с сервером авторизации. Нигде более он не должен отображаться, только на сервере. Он нужен для определения кем пользователь является. 
#Также есть access токены. Их можно получить только имея действующий рефреш токен. 
#сначала мы проходим авторизацию, на сервере создается рефреш токен, либо проверяется инфа, что это мы через рефреш токен - сверяется отпечаток и тд, и если все верно, то сервер выдает пользователю токен доступа - access token. Токен доступа нельзя отозвать, даже если он скомпрометирован, то есть украден. Время действия ecces token (JWT) маленькое. Инфа в JWT токене должна быть максимально короткая, достаточная для того, чтобы наше приложение могло определить что это нужный нам пользователь. Пользак передает JWT и сервер приложение наше возвращает нужные данные. Хранится JWT в памяти клиента, то есть или куки или ОЗУ. Если он закроет вкладку или браузер, ему заново надо получить access token. Для разных сервисов может использоваться разные токены, 
ост 16 мин











