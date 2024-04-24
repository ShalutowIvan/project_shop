# from learn_pytest import division


# def division(a, b):
# 	return a / b


# def test_division_good():
# 	assert division(10, 2) == 5#assert проверяет является ли выражение значением тру


# def test_division_not_good():
# 	assert division(10, 2) == 2


# def test_main():
# 	assert 1 == 1



# def test_main2():
# 	assert 2 == 2

from src.file import A#pytest не увидит такой импорт, так как он не видит где находится наш код в файлах проекта. поэтому нужен конфигурационный файл для pytest

def test_a():
	assert A.x == 1
