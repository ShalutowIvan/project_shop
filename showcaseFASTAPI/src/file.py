from typing import Union

class A:
	x = 1


class Calculator:
	def divide(self, x: Union[int, float], y: Union[int, float]) -> int | float:
		if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
			raise TypeError("аргумент должен быть числом")
		if y == 0:
			raise ZeroDivisionError("Делитель не может быть 0")
		return x / y


	def add(self, x: Union[int, float], y: Union[int, float]) -> int | float:
		if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):#выводим ошибку если аргумент не число. хотя строки тоже могут складываться. но наш тест выдаст ошибку, так как мы сделали проверку на типы
			raise TypeError("аргумент должен быть числом")
		return x + y




if __name__ == "__main__":
	calculator = Calculator()