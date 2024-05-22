# import requests
# import json
# import datetime



# class SomeResourceClient:
# 	def __init__(self, url):
# 		self.url = url


# 	def __user_get_status(self, user_id):
# 		# resp = requests.get("https://www.avito.ru/web/user/get-status/177068588")
# 		resp = requests.get(f"{self.url}/web/user/get-status/{user_id}")
# 		json_data = json.loads(resp.text)#загружаем json формат из запроса
# 		c = 1
# 		return json_data


# 	def get_user_lastaction(self, user_id):
# 		json_data = self.__user_get_status(user_id)
# 		last_action = json_data['lastActionTime']
# 		time_diff = json_data["timeDiff"]
# 		return datetime.fromtimestamp(last_action - time_diff)



# some_client = SomeResourceClient("https://www.avito.ru")

# # print(some_client.user_get_status(177068588))
# print(some_client.get_user_lastaction(177068588))#у меня тут ограничение по ip и у меня тут нет словаря и пишет ошибку keyerror

		


