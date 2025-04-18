import { useState, useEffect } from 'react'
import { Link, Outlet, NavLink, useLoaderData } from 'react-router-dom'
import axios from "axios"
import Button from '../Button/Button'
import { API } from "../../apiAxios/apiAxios"
import { updateAccessTokenFromRefreshToken, setAccessToken, getAccessToken } from "../../regusers/AuthService"





function Basket_view() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';	
	// const [error, setError] = useState("");
	const {goods} = useLoaderData()//по идеее тут запрос идет, но если в трай его закинуть, то его не видно вне трай кетч
	
	const [goods_in_basket, setGoods_in_basket] = useState(goods);
	


	// useEffect(() => {
	// 	fetch('http://127.0.0.1:8000/api/basket/goods/')
	// 		.then(res => res.json())
	// 		.then(data => setGoods_in_basket(data))

	// }, [])

	async function Delete_in_basket(good_id) {
				
		try {
        	await API.get(`/api/basket/goods/delete/${good_id}`)
		
			const response = await API.get('/api/basket/goods/')
			setGoods_in_basket(response.data)
      	} catch (error) {
      		//если ошибка, то выдаем ошибку. Ошибка тут не выдается, но и не удаляет позицию из корзины без авторизации
        	console.error("Error here: ", error);        	
        	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
      	}			
	}	

	if (goods === "error") {
    	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
  	}


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
	
	
	// const res = await API.get('/api/basket/goods/')
	try {
        // Запрос к защищенному эндпоинту FastAPI        
        const res = await API.get('/api/basket/goods/')
        //если все хорошо возвращаем данные
        return res.data        
      } catch (error) {
      	//если ошибка, то выдаем ошибку
        console.error("Error hear: ", error);
        // setError("Failed to fetch user data. Please try again.");
        return "error"
      }


	
}


const basketLoader = async () => {

	// try{
		
	// 	goods = await getBasket()

	// }
	// catch (error) {
    //     console.error("Error HEAR:", error);
    //     goods = "Error"
    // }
	
    return {goods: await getBasket()}	

}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.



export { Basket_view, basketLoader }
