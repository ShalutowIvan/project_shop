# from dataclasses import dataclass
# from typing import Literal, TypeAlias, Optional, TypeVar

# #TypeAlias - это для указания нескольких классов с конструкторами, типа или один конструктор или другой может быть выбран при создании объекта

# @dataclass
# class NonEmptyResponse:	
# 	data: str
# 	empty: Literal[False] = False
# 	#тут типа конструктор не пустого объекта

# @dataclass
# class EmptyResponse:	
# 	data: Literal[""] = ""
# 	empty: Literal[True] = True
# 	#тут пустой объект и данные не должно давать указывать 


# # a = Response(data="I have data")
# Response: TypeAlias = EmptyResponse or NonEmptyResponse
# a = EmptyResponse(data="qwe")
# # b = Response(data="asd")
# print(a.data)

# # создается с данными, но не должно

# #можно указывать значения которые будут в объекте

# @dataclass
# class Number:
# 	num: int


# a = Number(num="asd")


# print(a.num)

# N = TypeVar('N', int)

# @dataclass
# class Number(N):
# 	n: N

# S = TypeVar('S', str)
# # S = TypeVar('S', bound=str)

# # def func[S: str](x: S) -> S:
# # 	return x

# def func[S: str](x: S) -> S:
#     """Печатает x с заглавной буквы и возвращает x."""
#     print(x.capitalize())
#     return x

# a = func(x="asd")
# print(a)

# from transliterate import translit
# ru_text = "Вася"
# text = translit(ru_text, language_code='ru', reversed=True)
# print(text)
# import os
# path = os.path.abspath("xls/inventory.xlsx")#выводится путь к файлу питона
#
# # print(os.path.isfile(path))
# print(path)

# arr1 = ['p', 'y', 't', 'h', 'o', 'n', ' ', '3', '.', '0', '0']
# res = list(filter(lambda a: a=="0", arr1))
# print(res)

# class Python:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b


# obj = Python(1, 2)
# print(obj.__dict__)


#так можно тоже грузить в xls
# fn = "xls/error.xlsx"
# wb = load_workbook(fn)
#
# wb.save(fn)
# wb.close()



# Мила решила отпраздновать свой день рождения в кругу N
#  друзей. Она хочет заказать роллы для всех, поэтому нашла большой сет из T
#  роллов. Про i
# -го друга она знает, что чтобы насытиться, он должен съесть не менее ai
#  роллов, и что максимальное количество роллов, которое он может съесть, равно bi
# .

# Мила попросила вас посчитать, хватит ли T
#  роллов, чтобы все наелись и при этом не осталось лишних роллов.

# Входные данные
# В первой строке даны целые числа N
#  и T
#  (1≤N≤105;0≤T≤1014)
# .

# Во второй и третьей строках даны N
#  целых чисел ai
#  и N
#  целых чисел bi
#  соответственно (0≤ai≤bi≤109)
# .

# Выходные данные
# Выведите 'YES', если выбранный сет роллов подходит, или 'NO', если не подходит.

# Система оценки
# В этой задаче одна группа тестов стоимостью 10 баллов.

# Пример
# Входные данныеСкопировать
# 4 8
# 1 2 1 2
# 4 5 3 6
# Выходные данныеСкопировать
# YES

# N, T = map(int, input().split())
# a = list(map(int, input().split()[:N]))
# b = list(map(int, input().split()[:N]))
# print(a)
# print(b)
# while True:
# 	a = list(map(int, input().split()))
# 	if len(a) == N:
# 		break

# while True:
# 	b = list(map(int, input().split()))
# 	if len(b) == N:
# 		break


# N, T = (4, 8)
# # N, T = (4, 15)
# a = [1, 2, 1, 2]
# b = [4, 5, 3, 6]#18 макс, а попробуем 17 скушать

# for i in a:#все съели минимум
# 	T -= i

# if T < 0:
# 	print('NO')
# elif T == 0:
# 	print('YES')
# elif T != 0:
# 	for i in range(len(a)):
# 		if T == 0:			
# 			break
# 		for j in range(b[i] - a[i]):
# 			T -= 1#кормим каждого участника по одному ролу и проверяем остался ли остаток
# 			if T == 0:
# 				print('YES')				
# 				break
# if T != 0:
# 	print('NO')
# так 4 теста проходят


# чтобы все наелись и при этом не осталось лишних роллов.







