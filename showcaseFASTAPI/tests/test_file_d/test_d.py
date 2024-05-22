# from my_test import *
# import pytest




# #параметры просто
# @pytest.mark.parametrize("a, b, res", 
# 	[(10, 2, 5),
# 	(10, 5, 2),
# 	])
# def test_d(a, b, res):
# 	assert dev(a, b) == res


# #тесты на ошибки
# @pytest.mark.parametrize("error, chisl, znam", 
# 	[(ZeroDivisionError, 5, 0),
# 	(TypeError, 5, "2"),
# 	])
# def test_error(error, chisl, znam):
# 	with pytest.raises(error):
# 		dev(chisl, znam)


# @pytest.fixture
# def create_test_data(testdata):	
# 	with open("tests/file.txt", "a") as fo:#тут мы записываем новые данные в файл и сверяем что они записались в него потом
# 		fo.writelines(testdata)


# def test_file():
# 	# with open("tests/file.txt", "w"):#открытие файла на чтение чистит весь файл при открытии, то есть все удаляет
# 	# 	pass	
# 	testdata = ['one\n', 'two\n', 'three\n']
# 	create_test_data(testdata)
# 	assert testdata == read_file("tests/file.txt")



# def test_file2():
# 	# with open("tests/file.txt", "w"):#вынес очистку файла в фикстуру
# 	# 	pass	
# 	testdata = ['one\n', 'two\n', 'three\n', 'four\n']
# 	create_test_data(testdata)
# 	assert testdata == read_file("tests/file.txt")














