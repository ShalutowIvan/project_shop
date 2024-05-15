import pytest
from src.showcase.schemas import *
from src.db_t.database import Session as session
# from contextlib import nullcontext as does_not_raise#nullcontext означет что нет ошибки исключения с контекстом

# class TestCalculator:
# 	@pytest.mark.parametrize(
# 	"x, y, res, expectation",
# 	[(1, 2, 0.5, does_not_raise()),
# 	(5, -1, -5, does_not_raise()),
# 	(5, "1", -5, pytest.raises(TypeError)),
# 	(5, 0, -5, pytest.raises(ZeroDivisionError))]
# 	)
# 	def test_divide(self, x, y, res, expectation):#4-ый параметр нужно указывать в кортежах с параметрами
# 		with expectation:#теперь мы прописали тесты и указали где будет ошибка, а где нет. И должно все отловиться. Это как бы мы ожидаем что программа так отработает, и она так и отработает. 
# 			assert Calculator().divide(x, y) == res


# 	@pytest.mark.parametrize(
# 	"x, y, res, expectation",
# 	[(1, 2, 3, does_not_raise()),
# 	(5, -1, 4, does_not_raise()),
# 	(5, "-1", 4, pytest.raises(TypeError))]
# 	)
# 	def test_add(self, x, y, res, expectation):
# 		with expectation:#4-ый параметр нужно указывать в кортежах с параметрами. тут мы ожидали ошибку с типами в третьем тесте, так и было, и pytest ошибок не выдал
# 			assert Calculator().add(x, y) == res




@pytest.fixture
def goods():
    goods = [
        Goods(name_product="Хлеб", vendor_code="qwe-123", stock=10, price=30, slug="hleb", photo="tut", availability=True, group=1),
        Goods(name_product="Масло", vendor_code="asd-123", stock=11, price=150, slug="maslo", photo="tut2", availability=True, group=1),
        Goods(name_product="Молоко", vendor_code="zxc-123", stock=12, price=55, slug="milk", photo="tut3", availability=True, group=1),
    ]
    return goods



# @pytest.mark.usefixtures("empty_goods")
class TestGoods:

	# def test_count_goods(self, goods):
    #     for i in goods:
    #         CandiesService.add(candy)#тут должен быть класс товаров

    #     assert CandiesService.count() == 3


    def test_list_candies(self, goods):
        # for i in goods:
        #     Goods.add(i)
        session.add_all(goods)

        session.commit()

        # all_candies = CandiesService.list()
        # for added_candy in all_candies:
        #     assert added_candy in candies
