from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django.forms import model_to_dict

# class TestApi(generics.ListAPIView):
# 	queryset = Goods.objects.all()#делаем просто запрос таблицы
# 	serializer_class = GoodsSerializer#это класс сериализатор. Его нужно импортировать из файла serializers.py. В нем будут все сериализаторы. Перейдем в этот файл и сделаем этот класс
# 	#пропишем также текущее представление в urls.py в файле проекта. Текущий класс просто возвращает json для, чтобы потом какое-то другое приложение его обработало

# class GoodsAPIView(APIView):
# 	def get(self, request):#request - содержит все параметры входящего get запроса
# 		# lst = Goods.objects.all().values()
# 		lst = Goods.objects.all()
# 		# return Response({'goods': list(lst)})#теперь по ссылке будет возвращаиться просто json ответ. Пока возвращается просто строка без использования сериализатора
# 		return Response({'goods': GoodsSerializer(lst, many=True).data})#передали сюда сериализатор, чтобы он конвертировал значения, и обращаемся к коллекции data чтобы вернулся словарь данных. 
# 		#получается так, сначала формируется список из объектов класса Goods и записывается в переменную lst, затем весь список объектов передается на сериализатор GoodsSerializer и устанавливаем параметр many=True. Сериализатор преобразует список объектов в список из словарей и он записывается в переменную с названием data. Далее класс Response преобразует весь список словарей в байтовую JSON строку по аналогии с методом encode, также применяя метод JSONRenderer. Сделаем тоже самое для пост запроса. Допишем туда сериализатор

	
# 	def post(self, request):
# 		serializer = GoodsSerializer(data=request.data)#передаем данные из запроса в сериализатор
# 		serializer.is_valid(raise_exception=True)#генерируем исключение в случае если проверка не проходит, оказыватся можно так его передавать в качестве параметра. Исключение будет в виде подсказок, а не просто текст ошибки. ЛУчше его прописывать, так клиенту понятнее что от него хотят
# 		serializer.save()#этот метод вызывает метод create из serializer и добавляется новая запись. В постмане все работает как раньше

# 		# post_new = Goods.objects.create(
# 		# 	name_product = request.data['name_product'],
# 		# 	slug = request.data['slug'],
# 		# 	price = request.data['price'],
# 		# 	photo = request.data['photo'],
# 		# 	stock = request.data['stock'],
# 		# 	group_id = request.data['group_id']
# 		# )#так как в сериализаторе прописали метод create, то теперь в методе пост он не нужен. Но тут нужно прописать вызов метода save()

# 		# return Response({'post': model_to_dict(post_new)})
# 		# return Response({'post': GoodsSerializer(post_new).data})#тут вернется json строка, словарь data преобразован классом Response в json строку, и эту строку видит клиент и в постмане мы ее тоже видит как будто мы клиент в постмане. Если указать не выерные данные в словаре в постмане то есть в пост запросе, то будет ошибка, сериализатор ее вернет. Чтобы не было ошибки можно сделать проверку перед созданием объекта в базе. 
# 		return Response({'post': serializer.data})#новый объект с данными теперь не создаем, и используем тот объект, который сделали ранее. 


# 	def put(self, request, *args, **kwargs):
# 		#сначала определим идентификатор записи которую мы будем менять - pk
# 		pk = kwargs.get("pk", None)#берем из kwargs ключ pk, если его нет то None будет
# 		if not pk:#если ключа pk нет
# 			return Response({"error": "Method PUT not allowed"})#возвращается ошибка, то метод put не определен. То есть ключ pk не указать, то мы не знаем какой объект менять. 

# 		try:
# 			instance = Goods.objects.get(pk=pk)#присвоили в instance запись по ключу pk
# 		except:
# 			return Response({"error": "Objects does not exists"})

# 		serializer = GoodsSerializer(data=request.data, instance=instance)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()#save вызывает метод update сериализаторе. 
# 		return Response({"post": serializer.data})
# 		#получается так, если указать в объекте GoodsSerializer только data, то будет метод create, а если указать еще и instance, то это будет метод update. Так как в update нужно указать параметр в запросе, то нужно прописать еще одну урл с параметром в urls.py. Срабатывает это все автоматом как в фастапи. И в постмане для изменения теперь нужно выбирать put запрос, а не пост
# 		#передал запрос с параметром, все отработало как надо. Также в джанго получается можно несколько урл добавлять и с параметром и без.


# 	def delete(self, request, *args, **kwargs):
# 		pk = kwargs.get("pk", None)
# 		if not pk:
# 			return Response({"error": "Method DELETE not allowed"})

# 		#тут код для удаления найденного объекта из бд

# 		return Response({"post": "delete good" + str(pk)})#примерно так выглядит метод для удаления. Можно потом самому доделать, тут вроде не сложно. можно юзать стандартные функции орм джанго. Также в постмане нужно выбирать вид запроса DELETE


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


# class GoodsAPIList(generics.ListCreateAPIView):
# 	queryset = Goods.objects.all()#ссылается на список записей возвращаемх клиенту
# 	serializer_class = GoodsSerializer#второй атрибут ссылается на класс сериализатор который применяется к queryset
# 	#теперь этот класс будет возвращать записи по гет запросу и добавлять записи по пост запросу. Поменял такжде класс в urls.py.
# 	#теперь в браузере при гет запросе все будет также отображаться. И внизу будет форма для добавления записей. Форма рабочая. НА странице возвратится сам json который будет декодирован. Через постман также можно отправлять запросы. Класс ListCreateAPIView наследует 2 миксина для работы с моделями и GenericAPIView для классов представлений. Также есть 2 метода гет и поста, для пост и гет запросов. Внутри эти миксины и дженерик делает примерно то же самое что и мы делали с функциями encode и decode. То есть база есть хорошая. Можно ее брать за основу. 


# class GoodsAPIUpdate(generics.UpdateAPIView):
# 	queryset = Goods.objects.all()#тут те же самые параметры указываем. Это ленивый запрос. И при изменении будет изменена только одна запись в момент когда мы изменим и возвратим. Скорее всего потом будем фильтровать по параметру в урл
# 	serializer_class = GoodsSerializer


# class GoodsAPIDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Goods.objects.all()
# 	serializer_class = GoodsSerializer

# class GoodsViewSet(viewsets.ModelViewSet):#внутри те же самые параметры. Перейдем теперь в urls.py, там теперь в урл можно писать еще и параметры с видами запросов и названиями методов для их обработки, все это прописывается в виде словарей, ключ это название запроса, значение это название метода. Прочитать про название методов для запросов можно в док-ции. 
# 	queryset = Goods.objects.all()
# 	serializer_class = GoodsSerializer


# class GoodsViewSet(viewsets.ReadOnlyModelViewSet):#внутри те же самые параметры. Перейдем теперь в urls.py, там теперь в урл можно писать еще и параметры с видами запросов и названиями методов для их обработки, все это прописывается в виде словарей, ключ это название запроса, значение это название метода. Прочитать про название методов для запросов можно в док-ции. 
# 	queryset = Goods.objects.all()
# 	serializer_class = GoodsSerializer

# class GoodsViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    viewsets.GenericViewSet):#можно и вот вручную наследовать все классы. Эти же миксины наследуются в классе ModelViewSet, и мы можем убирать не нужный нам миксин, тогда например не будет возможности удалять позицию по сылке роутера. 
# 	# queryset = Goods.objects.all()
# 	serializer_class = GoodsSerializer

# 	#импорт из from rest_framework.decorators import action. Пропишем метод для вывода групп. Странно, почему нельзя сделать другой вью сет для групп, но посмотрим
# 	# @action(methods=['get'], detail=False)#это декоратор для того чтобы можно было прописать свой маршрут, помимо тех что формируются автоматом. 
# 	# def group(self, request):
# 	# 	gr = Group.objects.all()
# 	# 	return Response({'groups': [g.name_group for g in gr]})#возвращаем json со списоком групп
# 	#теперь появится новый маршрут после good будет дописано автоматом group: http://127.0.0.1:8000/api/v1/good/group/
# 	#имя маршрута будет такое: goods-group, дописывается название функции с декоратором action
# 	# Но если в нашем случае если прописать еще параметр цифру для фильтрации после good и потом еще слово group, то будет ошибка, что такого маршрута нет. Чтобы ошибки не было нужно прописать detail=True и в параметрах функции указать параметр pk=None. Тогда можно будет переходить по этой ссылке с параметром. Ссылка такая получается http://127.0.0.1:8000/api/v1/good/1/group/
# 	@action(methods=['get'], detail=True)
# 	def group(self, request, pk=None):
# 		# gr = Group.objects.all()
# 		gr = Group.objects.get(pk=pk)#можно еще прописать так, и тогда тот параметр цифра будет влиять на фильтрацию групп, и если теперь перейти по ссылке http://127.0.0.1:8000/api/v1/good/1/group/, то вывдетеся первая группа с pk=1. Получается как бы параметр функции не в конце урл. Получается можно делать нестандартные маршруты в классах вьюсет (viewsets). То есть тут вьюшка как бы для товаров, но другие модели тоже можно выводить с текущим роутером. И декоратор action как бы добавляет новую функцию к текущему роутеру, но с другими действиями. 		
# 		return Response({'groups': [g.name_group for g in gr]})#возвращаем json со списоком групп


# 	def get_queryset(self):
# 		pk = self.kwargs.get("pk")#получили параметр pk. 
# 		if not pk:#если нет такой записи то возвращаются все записи по нужному нам списку
# 			return Goods.objects.all()[:3]
		

# 		return Goods.objects.filter(pk=pk)#иначе если есть параметр pk в таблице, то его выводим. Причем тут фильтр ищет не из первых 3-х значений. 

		#теперь будут только первые 3 выводиться. Теперь можно убрать атрибут queryset, но надо не забыть прописать basename в роутере. Но теперь если указать параметр в ссылке, то будет ошибка. Нужно получать этот параметр в функции get_queryset. 


#сделаем 3 представления для создания, обновления и удаления
class GoodsAPIList(generics.ListCreateAPIView):
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, )

    		
class GoodsAPIUpdate(generics.RetrieveUpdateAPIView):
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer
	permission_classes = (IsOwnerOrReadOnly, )


class GoodsAPIDestroy(generics.RetrieveDestroyAPIView):
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer
	permission_classes = (IsAdminOrReadOnly, )#прописали свой пермиссионс, теперь удалять может только админ, а другие могут только смотреть. 

#пропишем маршруты для текущих вьюшек. И теперь любой пользак может что-либо делать с данными с нашего сайта. Это означает что безопасности нет вообще. 
# Сделаем так чтобы можно было добавлять записи только если авторизован пользак. Можно воспользоваться классом IsAuthenticatedOrReadOnly. Его нужно прописать в атрибуте permission_classes в виде кортежа. Теперь без авторизации нельзя добавлять статьи
#это чтобы поле с пользаком скрывалось при добавлении через форму в урлке от джанго, которое мы делаем через форму вьюшки GoodsAPIList. Мы тут создаем скрытое поле, и там по умолчанию прописываем текущего пользака. 

#далее преположим что удалять может только админ. Сделаем такое разрешение. Пропишем permission_classes = (IsAdminUser, ) в классе GoodsAPIDestroy
#если так прописать то удалять сможет только админ. Но просматривать может тоже только админ. Такого класса в джанго нет, чтобы нельзя было удалять, но можно было просматривать. Но его можно создать самому. 
# Есть класс BasePermission, в нем есть 2 метода:
# def has_permission(self, request, view):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         return True

# def has_object_permission(self, request, view, obj):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         return True
# Первый метод has_permission позволяет настраивать права доступа на уровне всего запроса (от клиента), а второй метод has_object_permission – права доступа на уровне отдельного объекта (данных, записи БД).
#Сделаем свой класс назовем его IsAdminOrReadOnly, чтобы просматривать записи мог каждый, а удалять только админ. Сделаем отдельный файл permissions.py, в нем будут наши собственные permissions

# Сделаем так, чтобы изменять записи мог только автор. А просматиривать могут также все пользаки. 
#Сделал класс IsOwnerOrReadOnly и записал его в виде кортежа во вьшке GoodsAPIUpdate. Теперь все работает как нам надо. Если есть авторизация, то можно просмотреть и редачить записи, а если нет авторизации, то только смотреть. 








