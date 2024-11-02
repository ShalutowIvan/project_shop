# from src.db_t import Base, engine, DATABASE_URL, Session
# from src.showcase.models_t import *
# from src.regusers.models_t import *



# try:
#     Base.metadata.create_all(bind=engine)
#     # Base.metadata.drop_all(engine)
# except Exception as ex:
#     print("ОШИБКА ТУТ !!!!!!!!!!!")
#     print(ex)
# from datetime import datetime
# dt = datetime.now()
# # datetime.strptime(str(datetime.now()), '%Y-%m-%d')
# print("!!!!!!!!!!!!!!!!!!!!!!!!!", type(dt))
# print(dt)

# def dev(a, b):
# 	return a / b

# def read_file(p):
# 	with open(p, "r") as fo:
# 		return fo.readlines()


# def func(a, z):
# 	for i in range(a, z):
# 		yield i


# gen = func(1, 10)

# for i in gen:
# 	print(i)

# a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
# b = set(a)
# print(b)

# import time
 
# # начальное время
# start_time = time.time()
 
# # код, время выполнения которого нужно измерить
# a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
# b = set(a)
# res = len(a) - len(b)
 
# # конечное время
# end_time = time.time()
 
# # разница между конечным и начальным временем
# elapsed_time = end_time - start_time
# print('Elapsed time: ', elapsed_time)




from pydantic import BaseModel

class Number(BaseModel):
	id: int

a = Number(id=1)
a.id = "asd"
print(a.id)






