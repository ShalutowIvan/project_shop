from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from rest_framework import generics, viewsets, mixins
from .models import *
from .serializers_goods import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Subquery, OuterRef

from django.forms import model_to_dict

from .forms import *
from django.core.exceptions import ObjectDoesNotExist

import random
import string
import os
import requests
import pandas as pd
from transliterate import translit
from .utils import handle_uploaded_file
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage




#для получения списка товаров
class Get_good(APIView):

	def get(self, request):
		good = Goods.objects.all()

		return Response(GoodsSerializer(instance=good, many=True).data)


# для получения списка групп в витрине для апи
# @login_required
class Get_group(APIView):

	def get(self, request):
		group = Group.objects.all()

		return Response(GroupSerializer(instance=group, many=True).data)
		# groups = Group.objects.all()
        # serializer = GroupSerializer(groups, many=True)
        # return Response(serializer.data)
		

class Get_good_in_group(APIView):

	def get(self, request, group_slug):
		# group = Goods.objects.filter(state_order=group_slug)
		goods_in_group = Goods.objects.filter(group__slug=group_slug)

		return Response(GoodsSerializer(instance=goods_in_group, many=True).data)


class Group_add_api(APIView):
    def post(self, request):
        serializer = Group_add_Serializer(data=request.data)
        if serializer.is_valid():
            name_group = serializer.validated_data['name_group']
            slug = translit(name_group, language_code='ru', reversed=True)
            new_group = Group(name_group=name_group, slug=slug)
            new_group.save()
            
            return Response({"success": True, "data": serializer.validated_data})
        else:
            return Response({"error": serializer.errors}, status=400)



    
# from rest_framework import viewsets
# class Goods_add_api(viewsets.ModelViewSet):
class Goods_add_api(APIView):

	# def get(self, request):
	# 	good = Goods.objects.all()

	# 	return Response(GoodsSerializer(instance=good, many=True).data)


	def post(self, request, *args, **kwargs):
		# print(request.data["name_product"])
		serializer = Goods_add_Serializer(data=request.data)

		if serializer.is_valid():
			# print(serializer.validated_data)
			slug = translit(serializer.validated_data["name_product"], language_code='ru', reversed=True)
			serializer.validated_data["slug"] = slug
			# serializer.validated_data["user"] = self.request.user# юзера потом тянуть из токена, когда запилю авторизацию. 


			serializer.save()
            
			return Response({"success": True, })
		else:

			return Response({"error": serializer.errors}, status=400)


# ост в джанго тут. нужно сделать роутер для DRF в urls.py или что-то подобное... разобраться, посмотреть видео selfedu чтобы память освежить. 

#загрузка файла с товарами
class Goods_load_file_api(APIView):

	def post(self, request, *args, **kwargs):

		
		# p = request.POST
		# f = request.FILES#тут мультивалуедикт
		# file = request.FILES['load_file']#тут имя файла
		# context = {"goods_in_file": db_goods}#тут объект <class 'pandas.core.frame.DataFrame'>
		fake_user = User.objects.get(id=1)

		groups_query = list(Group.objects.all())#можно пополнять этот лист при создании группы
		groups = [i.name_group.lower() for i in groups_query]
		goods_query = Goods.objects.all()
		goods_in_base = { i.name_product: i.vendor_code for i in goods_query }		
		goods = []
		new_groups = []



		try:
			file = request.FILES['load_file']#тут имя файла
			db_goods = pd.read_excel(file)
			db_goods.fillna(0, inplace=True)#эта строка заполняет пустые ячейки нулями 0.0
			no_group = Group.objects.get(slug="no_group")
			
			letters = string.ascii_lowercase
			print("!!!!!!!!!!!!!!!!!!!!!!")		
			print(db_goods)


			for i in db_goods.values:			
				if goods_in_base.get(i[0]) != None or i[1] in goods_in_base.values():#если есть в базе товар с артикулом или названием, то не добавляем
					continue

				if i[4] == 0.0:#если группа не заполнена, то кидаем товар в "без группы"
					goods.append(Goods(
					name_product=i[0], 
					slug=translit(i[0], language_code='ru', reversed=True), 
					vendor_code=''.join(random.choice(letters) for i in range(15)), 
					price=i[2],
					stock=i[3],
					group=no_group,
					photo=str(i[5]),
					user=fake_user
					) )
				elif i[4].lower() in groups:#если группа есть
					gr = groups_query[groups.index(i[4].lower())]
					goods.append(Goods(
					name_product=i[0], 
					slug=translit(i[0], language_code='ru', reversed=True), 
					vendor_code=i[1],#тут если не в файле его нет, то проставится 0. Пока так оставил
					price=i[2],
					stock=i[3],
					group=gr,
					photo=str(i[5]),
					user=fake_user
					) )				
				elif i[4].lower() not in groups:#если группа заполнена, но ее нет в базе
					group_obj = Group(name_group=i[4].title(), slug=translit(i[4], language_code='ru', reversed=True))				
					groups_query.append(group_obj)#то для обновления текущего списка объектов групп, чтобы в нем были новые группы. Это нужно в случае если появится новая группа и в нее товар грузим, выше в предыдущем условии пригождается
					groups.append(group_obj.name_group.lower())#список названий групп пополняем, для дальнейших проверок
					new_groups.append(group_obj)#список новых объектов групп, их потом в БД закинем после цикла					
					goods.append(Goods(
					name_product=i[0], 
					slug=translit(i[0], language_code='ru', reversed=True), 
					vendor_code=i[1], 
					price=i[2],
					stock=i[3],
					group=group_obj,
					photo=str(i[5]),
					user=fake_user
					) )

				
				# else:#ост тут. Можно группу нулем заполнить и добавить без группы, но могут быть нюансы... подумать
							
			if new_groups != []:
				groups_create = Group.objects.bulk_create(new_groups)

			if goods != []:
				goods_create = Goods.objects.bulk_create(goods)

			return Response({
                'message': 'File processed successfully',
                # 'data': data,
                # 'rows_count': len(data)
            }, status=status.HTTP_200_OK)

		except Exception as ex:
			print(ex)
			return Response(
                {'error': str(ex)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


#скачивание шаблона для загрузки файла
@api_view(['GET'])
def url_from_load_template_api(request):	
	path = os.path.abspath(r"shop\static\shop\xls\template.xlsx")
	response = FileResponse(open(path, 'rb'))
	
	return response
	



# это обработчик формы для загрузки нескольких файлов
class BulkImageUploadView(APIView):
    parser_classes = [MultiPartParser]  # Для обработки multipart/form-data
    
    def post(self, request, format=None):
        if not request.FILES:
            return Response(
                {"error": "No files provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        saved_files = []
        errors = []
        
        # Обрабатываем все файлы из запроса
        for file_key in request.FILES:
            uploaded_file = request.FILES[file_key]
            
            try:
                # Сохраняем файл в папку 'uploads/' (автоматически создаётся)
                file_path = default_storage.save(
                    os.path.join('', uploaded_file.name),
                    uploaded_file
                )
                saved_files.append({
                    'name': uploaded_file.name,
                    'url': default_storage.url(file_path),
                    'size': uploaded_file.size
                })
            except Exception as e:
                errors.append({
                    'name': uploaded_file.name,
                    'error': str(e)
                })
        
        response_data = {
            'saved_files': saved_files,
            'errors': errors,
            'total_uploaded': len(saved_files)
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


#для проверки расширений при загрузке файлов фото
# ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
# if not uploaded_file.name.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
#     # Вернуть ошибку

#роут для удаления лишних загруженных файлов с сервера. 
class CleanUnusedFilesView(APIView):
    def get(self, request, format=None):
        # Получаем все используемые файлы из БД
        used_files = set()
        for product in Goods.objects.all():
            if product.photo:
                used_files.add(product.photo.name)
        
        # Сканируем медиа-папку
        media_root = settings.MEDIA_ROOT
        deleted_files = []
        errors = []
        
        for root, _, files in os.walk(media_root):
            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, media_root)
                
                # Проверяем, используется ли файл в БД
                if relative_path not in used_files:
                    try:
                        os.remove(file_path)
                        deleted_files.append(relative_path)
                    except Exception as e:
                        errors.append({
                            'file': relative_path,
                            'error': str(e)
                        })
        
        return Response({
            'deleted_files': deleted_files,
            'errors': errors,
            'total_deleted': len(deleted_files)
        }, status=status.HTTP_200_OK)



class Group_delete_api(APIView):
	def post(self, request):
		# good = Goods.objects.get(id=good_id)
		# groups = Group.objects.all()
		
		
		try:
			#ищем группу			
			group = Group.objects.get(id=int(request.data["group"]))
			
			#ищем товары с этой группой
			goods_in_group = list(Goods.objects.filter(group__slug=group.slug))						
			if goods_in_group != []:
				#если группа не пустая, то нужен рендер на другую форму с выбором группы куда переносить товары. Закинем туда также контекст с группой которую удаляем и с списком объектов с товарами				
				return Response({"success": True, "answer": group.id})
				
			elif goods_in_group == []:
				#если группа пустая то удаляем группу, для метки передаем текст delete, его нужно будет проверять в ответе в data. Если ответ сервера в data равен delete, то удаляем группу и делаем редирект на список товаров в реакт.
				group.delete()
				
				return Response({"success": True, "answer": "delete"})

		
		except Exception as ex:

			return Response({"error": ex}, status=400)
		
		# из формы получаем группу ИД и далее нужно првоерить что группа пустая или нет, если не пустая, то выбрать группу куда перенести товар, если пустая просто удалить...



#урл для переноса товаров в новую группу
class Select_group_to_transfer_api(APIView):
	def post(self, request, group_id):
		try:
			group_delete = Group.objects.get(id=group_id)#нашел объект группы		

			group_new = Group.objects.get(id=int(request.data["group"]))#берем из формы новую группу, в нее переносим товары
			
			#тут логика переноса всех товаров из удаляемой группы в новую группу, потом удаляемую группу нужно удалить...
			goods_in_group = list(Goods.objects.filter(group__id=group_id))#товары из удаляемой группы
			for i in goods_in_group:#меняем группу у всех товаров
				i.group = group_new

			gd = Goods.objects.bulk_update(objs=goods_in_group, fields=["group",])#коммит в БД с изменениями группы

			group_delete.delete()#удаление старой группы
			#после того как убрали товары, не удаляется так как есть связь с таблицей инвенты.... Если инвенту по группе делали, то нельзя удалить так как есть связь. Как убрать связь не знаю. За счет связи удобно работает форма добавления группы. 
			# чекбокс это boolfield
			return Response({"success": True}, status=status.HTTP_200_OK)
		except Exception as ex:

			return Response({"error": ex}, status=400)



@api_view(['GET'])
def group_without_delete(request, group_id):
	groups = list(Group.objects.all())
	group_delete = Group.objects.get(id=group_id)
	groups.remove(group_delete)
	return Response(GroupSerializer(instance=groups, many=True).data)


# далее поиск товара, изменение товара, удаление товара. 3 кнопки еще в товарах. Ост редакт товара
class Goods_modify_api(APIView):
	
	def post(self, request, good_id):
		good = Goods.objects.get(id=good_id)
		# group = Group.objects.all()
		serializer = Goods_add_Serializer(data=request.data)
	
		if serializer.is_valid():
			# file_photo = request.FILES['photo']#FILES это словарь с ключами из имен полей с файлами
			# # print("!!!!!!!!!!!!!!!!!!!!!")#пустое поле с фото не грузится
			# # print(file_photo)

			# image = Image.open(file_photo)
			# image.verify()

			path = os.path.abspath("media/" + str(good.photo))#полный абсолютный путь к файлу из БД		
			if os.path.exists(path):#если файл есть там, то удаляем, если нет, то не удаляем
				f = str(good.photo)#берем путь к файлу из базы
				new_file = f[:f.rfind('/') + 1] + serializer.validated_data["photo"].name#заменяем в пути к файлу имя файла, это потом в БД пойдет
				os.remove(path)#удаляем сам файл на сервере
				handle_uploaded_file(file_name=file_photo, path="media/" + f[:f.rfind('/') + 1])#загружаем новый файл в ту же самую папку
			else:
				new_file = file_photo.name
				handle_uploaded_file(file_name=file_photo, path="media/")

			good.name_product = serializer.validated_data["name_product"]
			good.vendor_code = serializer.validated_data["vendor_code"]
			good.price = float(serializer.validated_data["price"].replace(",", "."))
			good.photo = new_file
			good.group = Group.objects.get(id=int(serializer.validated_data["group"]))
			good.save()			
	
			return Response({"success": True, })
		else:	

			return Response({"error": serializer.errors}, status=400)


# def post(self, request, *args, **kwargs):
# 		# print(request.data["name_product"])
# 		serializer = Goods_add_Serializer(data=request.data)

# 		if serializer.is_valid():
# 			# print(serializer.validated_data)
# 			slug = translit(serializer.validated_data["name_product"], language_code='ru', reversed=True)
# 			serializer.validated_data["slug"] = slug
# 			# serializer.validated_data["user"] = self.request.user# юзера потом тянуть из токена, когда запилю авторизацию. 


# 			serializer.save()
            
# 			return Response({"success": True, })
# 		else:

# 			return Response({"error": serializer.errors}, status=400)




	
#удаление товара
def goods_delete(request, good_id):

	good = Goods.objects.get(id=good_id)
	path = os.path.abspath("media/" + str(good.photo))
	if os.path.isfile(path):
		os.remove(path)#удаляем сам файл на сервере
	
	good.delete()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


		


