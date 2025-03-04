import { useState, useEffect } from 'react'
import { Link, Outlet, NavLink, useLoaderData } from 'react-router-dom'
import axios from "axios"
import Button from '../Button/Button'
import { API } from "../../apiAxios/apiAxios"
import { updateAccessTokenFromRefreshToken, setAccessToken, getAccessToken } from "../../regusers/AuthService"



function Basket_view() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	// const [goods_in_basket, setGoods_in_basket] = useState([]);
	const {goods_in_basket} = useLoaderData()


	// useEffect(() => {
	// 	fetch('http://127.0.0.1:8000/api/basket/goods/')
	// 		.then(res => res.json())
	// 		.then(data => setGoods_in_basket(data))

	// }, [])

	function Delete_in_basket(good_id) {
		API.get(`api/basket/goods/delete/${good_id}`)
		
		const response = API.get('api/basket/goods/')
		setGoods_in_basket(response.data)
			
		// fetch('http://127.0.0.1:8000/api/basket/goods/')
		// 	.then(res => res.json())
		// 	.then(data => setGoods_in_basket(data))		
	}
	
	//не работает пока....после авторизаци товары не видны


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

		
		<h2><NavLink to="/basket/create/" className={setActive}>Перейти к оформлению заказа</NavLink></h2>


		</>
		)
}



async function getBasket() {
	// const res = await fetch('http://127.0.0.1:8000/api/basket/goods/')
	// const res = API.get("api/basket/goods/")
	// const token = Cookies.get("Authorization");
	// console.log(token);
	// const token = getAccessToken()
	// const res = await axios.get('http://127.0.0.1:8000/api/basket/goods/', {
    //       headers: {
    //         Authorization: token,
    //       },
    //     });
	const res = await API.get('http://127.0.0.1:8000/api/basket/goods/')
	// попробовать просто сделать аксиос запрос


	return res.data
}


const basketLoader = async () => {	
	
	return {goods_in_basket: await getBasket()}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.



export { Basket_view, basketLoader }
