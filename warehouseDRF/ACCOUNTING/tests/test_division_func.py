# from learn_pytest import division


def division(a, b):
	return a / b


def test_division_good():
	assert division(10, 2) == 5#assert проверяет является ли выражение значением тру


def test_division_not_good():
	assert division(10, 2) == 2


