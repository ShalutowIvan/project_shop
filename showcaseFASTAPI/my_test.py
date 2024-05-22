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

def dev(a, b):
	return a / b

def read_file(p):
	with open(p, "r") as fo:
		return fo.readlines()