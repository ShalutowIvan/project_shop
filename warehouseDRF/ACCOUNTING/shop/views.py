from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict

# class TestApi(generics.ListAPIView):
# 	queryset = Goods.objects.all()#делаем просто запрос таблицы
# 	serializer_class = GoodsSerializer#это класс сериализатор. Его нужно импортировать из файла serializers.py. В нем будут все сериализаторы. Перейдем в этот файл и сделаем этот класс
# 	#пропишем также текущее представление в urls.py в файле проекта. Текущий класс просто возвращает json для, чтобы потом какое-то другое приложение его обработало

class GoodsAPIView(APIView):
	def get(self, request):#request - содержит все параметры входящего get запроса
		# lst = Goods.objects.all().values()
		lst = Goods.objects.all()
		# return Response({'goods': list(lst)})#теперь по ссылке будет возвращаиться просто json ответ. Пока возвращается просто строка без использования сериализатора
		return Response({'goods': GoodsSerializer(lst, many=True).data})#передали сюда сериализатор, чтобы он конвертировал значения, и обращаемся к коллекции data чтобы вернулся словарь данных. 
		#получается так, сначала формируется список из объектов класса Goods и записывается в переменную lst, затем весь список объектов передается на сериализатор GoodsSerializer и устанавливаем параметр many=True. Сериализатор преобразует список объектов в список из словарей и он записывается в переменную с названием data. Далее класс Response преобразует весь список словарей в байтовую JSON строку по аналогии с методом encode, также применяя метод JSONRenderer. Сделаем тоже самое для пост запроса. Допишем туда сериализатор

	
	def post(self, request):
		serializer = GoodsSerializer(data=request.data)#передаем данные из запроса в сериализатор
		serializer.is_valid(raise_exception=True)#генерируем исключение в случае если проверка не проходит, оказыватся можно так его передавать в качестве параметра. Исключение будет в виде подсказок, а не просто текст ошибки. ЛУчше его прописывать, так клиенту понятнее что от него хотят
		serializer.save()#этот метод вызывает метод create из serializer и добавляется новая запись. В постмане все работает как раньше

		# post_new = Goods.objects.create(
		# 	name_product = request.data['name_product'],
		# 	slug = request.data['slug'],
		# 	price = request.data['price'],
		# 	photo = request.data['photo'],
		# 	stock = request.data['stock'],
		# 	group_id = request.data['group_id']
		# )#так как в сериализаторе прописали метод create, то теперь в методе пост он не нужен. Но тут нужно прописать вызов метода save()

		# return Response({'post': model_to_dict(post_new)})
		# return Response({'post': GoodsSerializer(post_new).data})#тут вернется json строка, словарь data преобразован классом Response в json строку, и эту строку видит клиент и в постмане мы ее тоже видит как будто мы клиент в постмане. Если указать не выерные данные в словаре в постмане то есть в пост запросе, то будет ошибка, сериализатор ее вернет. Чтобы не было ошибки можно сделать проверку перед созданием объекта в базе. 
		return Response({'post': serializer.data})#новый объект с данными теперь не создаем, и используем тот объект, который сделали ранее. 


	def put(self, request, *args, **kwargs):
		#сначала определим идентификатор записи которую мы будем менять - pk
		pk = kwargs.get("pk", None)#берем из kwargs ключ pk, если его нет то None будет
		if not pk:#если ключа pk нет
			return Response({"error": "Method PUT not allowed"})#возвращается ошибка, то метод put не определен. То есть ключ pk не указать, то мы не знаем какой объект менять. 

		try:
			instance = Goods.objects.get(pk=pk)#присвоили в instance запись по ключу pk
		except:
			return Response({"error": "Objects does not exists"})

		serializer = GoodsSerializer(data=request.data, instance=instance)
		serializer.is_valid(raise_exception=True)
		serializer.save()#save вызывает метод update сериализаторе. 
		return Response({"post": serializer.data})
		#получается так, если указать в объекте GoodsSerializer только data, то будет метод create, а если указать еще и instance, то это будет метод update. Так как в update нужно указать параметр в запросе, то нужно прописать еще одну урл с параметром в urls.py. Срабатывает это все автоматом как в фастапи. И в постмане для изменения теперь нужно выбирать put запрос, а не пост
		#передал запрос с параметром, все отработало как надо. Также в джанго получается можно несколько урл добавлять и с параметром и без.


	def delete(self, request, *args, **kwargs):
		pk = kwargs.get("pk", None)
		if not pk:
			return Response({"error": "Method DELETE not allowed"})

		#тут код для удаления найденного объекта из бд

		return Response({"post": "delete good" + str(pk)})#примерно так выглядит метод для удаления. Можно потом самому доделать, тут вроде не сложно. можно юзать стандартные функции орм джанго. Также в постмане нужно выбирать вид запроса DELETE


#теперь мы принимаем данные, проверяем что они валидны, потом записываем их, потом возвращаем в функции как результат

# model_to_dict - это стандартная функция из обычного джанго для преобразования модели джанго класса Goods в словарь

#также в сериализаторе можно указать параметр read_only=True, тогда при пост запросе его можно будет не указывать и не будет исключения, так как будет использоваться для чтения в гет запросе. 

#так примерно выглядит исключение:
# {
#     "name_product": [
#         "Обязательное поле."
#     ],
#     "slug": [
#         "Обязательное поле."
#     ],
#     "vendor_code": [
#         "Обязательное поле."
#     ]
# }

#словарь для пост запроса.   	
# {   
#     "name_product": "Какой-то товар2",
#     "slug": "tovar2",
# 	  "vendor_code": "_",
#     "price": 777,
#     "photo": "photos/2024/01/28/47470.970.jpg",
#     "stock": 666,
#     "group_id": 3 
# }	


class GoodsAPIList(generics.ListCreateAPIView):
	queryset = Goods.objects.all()#ссылается на список записей возвращаемх клиенту
	serializer_class = GoodsSerializer#второй атрибут ссылается на класс сериализатор который применяется к queryset
	#теперь этот класс будет возвращать записи по гет запросу и добавлять записи по пост запросу. Поменял такжде класс в urls.py.
	#теперь в браузере при гет запросе все будет также отображаться. И внизу будет форма для добавления записей. Форма рабочая. НА странице возвратится сам json который будет декодирован. Через постман также можно отправлять запросы. Класс ListCreateAPIView наследует 2 миксина для работы с моделями и GenericAPIView для классов представлений. Также есть 2 метода гет и поста, для пост и гет запросов. Внутри эти миксины и дженерик делает примерно то же самое что и мы делали с функциями encode и decode. То есть база есть хорошая. Можно ее брать за основу. 






