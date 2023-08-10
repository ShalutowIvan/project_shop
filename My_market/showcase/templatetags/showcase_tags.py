from django import template
from showcase.models import *

register = template.Library()

#сделали функцию как простой тег, чтобы можно было избежать дублирование запроса всех групп в функциях views файла. Файл с тегами можно подключить в шаблонах html прописав {% load showcase_tags %}. Чтобы подключить тег в html нужно еще написать {% getgr as gr %}. Это нужно в случае если мы нескольких функциях делаем один и тот запрос. Теперь если юзать тег, то этот запрос из функций представлений можно удалить. 
@register.simple_tag(name='getgr')
def get_group():
	return Group.objects.all()


#еще можно делать тег который возвращает кусок html страницы
@register.inclusion_tag('showcase/list_group.html')
def show_gr():
	groups = Group.objects.all()
	return {"groups": groups}
#это вместо цикла который группы перебирает. Его теперь можно убрать из стартого шаблон html и написать туда просто тег show_gr по названию функции. В тегах еще можно делать фильтры или сортировки, их нужно прописать в параметрах самой функции тега. 

