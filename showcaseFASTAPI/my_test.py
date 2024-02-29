# import time
# # from numba import njit

# # начальное время
# start_time = time.time()
 
# # код, время выполнения которого нужно измерить
# # @njit
# def test():
#     for i in range(0, 1000000):
#         pass

# test()
# # конечное время
# end_time = time.time()
 
# # разница между конечным и начальным временем
# elapsed_time = end_time - start_time
# print('Elapsed time: ', elapsed_time)



import requests

rq = requests.get("http://127.0.0.1:9999/api/get_good/")
res = rq.json()
print("!!!!!!!!!!!!!!!!!!!!!!!!")
print(res)


