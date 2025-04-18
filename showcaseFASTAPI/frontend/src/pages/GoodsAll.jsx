import React from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"
import Button from '../components/Button/Button'
import { API } from "../apiAxios/apiAxios"




export default function GoodsAll() {
	// console.log(useParams().id);
	// const {slug} = useParams();
	const [goods, setGoods] = useState([]);
	const [error, setError] = useState("");


	useEffect(() => {
		fetch(`http://127.0.0.1:8000/api/goods_all/`)
			.then(res => res.json())
			.then(data => setGoods(data))
	}, [])

	function Add_in_basket(good_id) {
		// try {
		// 	res = API.get(`http://127.0.0.1:8000/api/basket/${good_id}`)
		// }
		// catch (error) {
		// 	setError("error");
		// }

		API.get(`/api/basket/${good_id}`)
		// console.log(res)
		//не знаю как уведомить пользака об ошибке при добавлении товара без авторизации. У меня просто ничего не происходит на странице. Трай кетч не работает и состояние не меняется


		
	}
	

	return (
		<div>

			{/*{goods && (
				<>
					<h3>{post.title}</h3>
					<p>{post.body}</p>
					<Link to={`/posts/${id}/edit`}>Редактировать</Link>
				</>
				)}*/}
			
			{goods?.map(good => (
                        <div className="goods" key={good.id}>                        	
                        	<h3>{good.name_product}</h3>
                        	<h4>Цена: {good.price}</h4>
                        	<h4>Остаток: {good.stock}</h4>
                        	<Button onClick={() => Add_in_basket(good.id)}>Добавить в корзину</Button>
                        	<p>{error}</p>
                        </div>
                    ))}


		</div>
		)

}






