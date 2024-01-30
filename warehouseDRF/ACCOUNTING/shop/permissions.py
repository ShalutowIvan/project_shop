from rest_framework import permissions

#разрешение на уровне запроса
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:#SAFE_METHODS - это методы GET HEAD OPTIONS, то есть это кортеж из этих методов. Эти запросы для чтения данных
            return True#возвращаем тру, это означает что права доступа предоставлены, фолз будет значить не предоставлены. В других методах DRF также переопреден метод has_permission
        #иначе возвращаем проверку пользака на права админа. Проверяем есть ли права админа. 
        return bool(request.user and request.user.is_staff)
        #теперь применим его в нашей вьюшке. 

#Класс permissions для разрешения доступа к объектам на редактирование. Читать можно всем, но редачить только юзеру который его создал. 
#разрешение для конкретного объекта БД
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """ 
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
 
        # Write permissions are only allowed to the owner of the snippet.
        #разрешение на редактирование есть только у пользака - создателя владельца объекта, если они равны, то будет тру возвращено. Сравнение идет из свойства user объекта и юзеров из запроса
        return obj.user == request.user

#Применим этот класс во вьшке GoodsAPIUpdate

