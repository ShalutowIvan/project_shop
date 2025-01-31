import { useState, useEffect } from 'react'
import { Link, Outlet, NavLink } from 'react-router-dom'
import axios from "axios"
import Button from '../Button/Button'



export default function Basket_view() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const [goods_in_basket, setGoods_in_basket] = useState([]);
	


	useEffect(() => {
		fetch('http://127.0.0.1:8000/api/basket/goods/')
			.then(res => res.json())
			.then(data => setGoods_in_basket(data))

	}, [])

	function Delete_in_basket(good_id) {
		axios.get(`http://127.0.0.1:8000/api/basket/goods/delete/${good_id}`)
		
		fetch('http://127.0.0.1:8000/api/basket/goods/')
			.then(res => res.json())
			.then(data => setGoods_in_basket(data))		
	}
	//удаление работает, но нужно обновлять страницу чтобы увидеть изменения в базе. Если сюда закинуть состояние, то будет постоянный запрос в БД. Что делать пока не знаю. 
	


	return (
		<>
		<h1>Тут будут товары которые есть в корзине</h1>

		{goods_in_basket?.map(good => (
                        <div className="goods" key={good.id}>

                        	<h3>{good.product.name_product}</h3>
                        	<h4>Цена: {good.product.price}</h4>
                        	<h4>Количество: {good.quantity}</h4>
                        	<Button onClick={() => Delete_in_basket(good.id)}>Удалить</Button>
                        </div>
                    ))}



		
		<h2><NavLink to="/basket/contacts/" className={setActive}>Перейти к оформлению заказа</NavLink></h2>


		</>
		)



}




