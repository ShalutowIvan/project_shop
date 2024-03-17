from django.db import models
from django.contrib.auth.models import User

class Goods(models.Model):
	name_product = models.CharField(max_length=255, default='_', verbose_name="Название товара")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
	vendor_code = models.CharField(max_length=255, default='_', verbose_name="Артикул")
	price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Цена")
	photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
	stock = models.FloatField(verbose_name="Остаток")
	availability = models.BooleanField(default=True, verbose_name="Доступность")
	group = models.ForeignKey('Group', on_delete=models.PROTECT, verbose_name="Группа товара", null=True)#миграцию пока не делал с null
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",)# сделал поле юзера, чтобы было видно кто товар создал. Будет конечно 1 пользак, но лучше все же слелать ограничение. 

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



class Order_list_bought(models.Model):
	fio = models.CharField(max_length=255, default='_', verbose_name="Покупатель")
	phone = models.CharField(max_length=255, default='_', verbose_name="Телефон")	
	product_id = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name="Товар")#тут указать только код товара то есть ИД и ИД должен совпадать в витрине и в учетной системе, так как это связанное поле тип int. Если что можно и название потом прокинуть, но пока не надо
	quantity = models.FloatField(default=0, verbose_name="Количество")	
	order_number = models.IntegerField(verbose_name="Номер заказа")
	time_create = models.DateTimeField(verbose_name="Время создания")#время создания заказа покупателем
	delivery_address = models.CharField(max_length=255, default='_', verbose_name="Адрес организации")


	def __str__(self):
		return f"Товар: {self.product_id}, Количество: {self.quantity}"


	class Meta:
		verbose_name = "Список заказов"
		verbose_name_plural = "Списки заказов"
		ordering = ['time_create', 'product_id']


class Receipt_number(models.Model):
	comment = models.CharField(max_length=255, default='_', verbose_name="Комментарий")
	time_create = models.DateTimeField(auto_now_add=True)
	state = models.BooleanField(default=False, verbose_name="состояние")	

#тут по идее связь 1 ко многим, в одной накладной много товаров, то есть много товаров с одинаковым номером накладной. Либо наоборот, думать надо
#кажется 1 ко многим не очень
#для удаления будет отдельная урл. и там отдельный запрос. 

	def __str__(self):
		return f"Номер= {self.pk} Дата= {self.time_create} Комментарий= {self.comment}"


	class Meta:
		verbose_name = "Номер накладной"
		verbose_name_plural = "Номера накладных"
		ordering = ['time_create']




class Receipt_list(models.Model):
	product = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name="Товар")
	number_receipt = models.IntegerField(default=0, verbose_name="Номер накладной")#этот номер берется из id таблицы Receipt_number
	quantity = models.FloatField(default=0, verbose_name="Количество")	
	user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")	

	def __str__(self):
		return f"Товар: {self.product}, Количество: {self.quantity}"


	class Meta:
		verbose_name = "Список приходных документов"
		verbose_name_plural = "Списки приходных документов"
		ordering = ['product']







