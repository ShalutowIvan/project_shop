from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


#Модель для товаров. База наполняться и изменяться будет через API
class Goods(models.Model):
	name_product = models.CharField(max_length=255, default='_', verbose_name="Название товара")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
	price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена")
	photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
	stock = models.FloatField(verbose_name="Остаток")
	availability = models.BooleanField(default=True, verbose_name="Доступность")
	group = models.ForeignKey('Group', on_delete=models.PROTECT, verbose_name="Группа товара", null=True)#миграцию пока не делал с null

	def __str__(self):
		return self.name_product

	# def get_absolute_url(self):
	# 	return reverse('post', kwargs={'post_slug': self.slug})

	class Meta:#прописали внутренний мета класс для указания названия приложения в админке
		verbose_name = "Товар"
		verbose_name_plural = "Товары"#это для множественного числа, чтобы буква s не дописывалась автоматом
		ordering = ['stock', 'name_product']
		index_together = (('id', 'slug'),)


#модель групп. База наполняться и изменяться будет через API
class Group(models.Model):
	name_group = models.CharField(max_length=255, default='_', db_index=True, verbose_name="Название группы")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

	def __str__(self):
		return self.name_group


	def get_absolute_url(self):
		return reverse('group', kwargs={'group_slug': self.slug})

	class Meta:
		verbose_name = "Группа"
		verbose_name_plural = "Группы"
		ordering = ['name_group']


#модель инфы об организации. База наполняться и изменяться будет через API
class Organization(models.Model):
	name_org = models.CharField(max_length=255, default='_', verbose_name="Название организации")	
	inn_kpp = models.CharField(max_length=255, default='0', verbose_name="ИНН-КПП")	
	ogrn = models.IntegerField(default=0, verbose_name="ОГРН")
	working_mode = models.CharField(max_length=255, default='_', verbose_name="Режим работы")
	about = models.TextField(blank=True, verbose_name="О компании")
	adres = models.CharField(max_length=255, default='_', verbose_name="Адрес организации")	
	phone = models.IntegerField(default=0, verbose_name="Телефон")
	email_name = models.CharField(max_length=255, default='_', verbose_name="Электронная почта")
	telegram = models.CharField(max_length=255, default='_', verbose_name="Контакты в Telegram")
	whatsApp = models.CharField(max_length=255, default='_', verbose_name="Контакты в WhatsApp")


	def __str__(self):
		return self.name_org


	# def get_absolute_url(self):
	# 	return reverse('post', kwargs={'post_slug': self.slug})

	class Meta:
		verbose_name = "Организация"
		verbose_name_plural = "Организация"
		


#список заказов хочу купить
class Order_list_want_by(models.Model):
	name_product = models.CharField(max_length=255, default='_', verbose_name="Название товара")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
	price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена")
	quantity = models.FloatField(verbose_name="Количество")
	availability = models.BooleanField(default=True, verbose_name="Доступность")
	group = models.ForeignKey('Group', on_delete=models.PROTECT, verbose_name="Группа товара")
	time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
	time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")



	def __str__(self):
		return self.name_product


	class Meta:
		verbose_name = "Товары, которые хочу купить"
		verbose_name_plural = "Товары, которые хочу купить"
		ordering = ['time_create', 'name_product']



# #список заказов купили раньше - история покупок
class Order_list_bought(models.Model):
	name_product = models.CharField(max_length=255, default='_', verbose_name="Название товара")
	# slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
	price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена")
	quantity = models.FloatField(verbose_name="Количество")
	# availability = models.BooleanField(default=True, verbose_name="Доступность")
	group = models.ForeignKey('Group', on_delete=models.PROTECT, verbose_name="Группа товара")
	time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

	def __str__(self):
		return self.name_product


	class Meta:
		verbose_name = "История покупок"
		verbose_name_plural = "История покупок"
		ordering = ['time_create', 'name_product']


# товары в корзине
class Baskets(models.Model):
	user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
	product = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name="Товар")
	quantity = models.FloatField(default=0, verbose_name="Количество")
	created_timestamp = models.DateTimeField(auto_now_add=True)
	availability = models.BooleanField(default=True, verbose_name="Доступность")
	price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена")

	
	def __str__(self):
		return f'Корзина для {self.user.username} | Продукт: {self.product.name_product}'

	class Meta:
		verbose_name = "Товары в корзине"
		verbose_name_plural = "Товары в корзине"
		ordering = ['-price', 'product']

	# def sum(self):
	# 	return self.product.price * self.quantity
# миграции не срабатывают. что то не так с таблицей юзер он не импортировался. 
# Сама миграция не срабатывает

# class Users(models.Model):
