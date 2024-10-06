from dataclasses import dataclass
from typing import Literal, TypeAlias, Optional, TypeVar

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





import os

a = "C:/Users/shalutov/Desktop/python/INTERNET_MARKET/DRF_ACCOUNTING/ACCOUNTING/media/photos/2024/10/05/1640757399_2-sobakovod-club-p-sobaki-sobachya-budka-2.jpg"


if os.path.exists(a):
	print("YES")


