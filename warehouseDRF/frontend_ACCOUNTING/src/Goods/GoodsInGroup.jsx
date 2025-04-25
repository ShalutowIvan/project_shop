import React from 'react';
import { useParams, Link, useNavigate, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"
import GroupsAll from "./Groups"

// import Button from '../components/Button/Button'
// import { API } from "../apiAxios/apiAxios"

export default function GoodsInGroup() {
	// console.log(useParams().id);
	const {slug} = useParams();
	const [goods, setGoods] = useState([]);
	// const navigate = useNavigate();	
	
	useEffect(() => {		
		fetch(`http://127.0.0.1:9999/api/get_good_in_group/${slug}`)
			.then(res => res.json())
			.then(data => setGoods(data))

	}, [slug])
	
	// function Add_in_basket(good_id) {
	// 	API.get(`http://127.0.0.1:8000/api/basket/${good_id}`)
	// 	//не знаю как уведомить пользака об ошибке при добавлении товара без авторизации. У меня просто ничего не происходит на странице	
	// }


	return (
		<>

			<GroupsAll />
			
			{
                	goods?.map(good => (
                        <div className="goods" key={good.id}>
                        	
                        	<h3>{good.name_product}</h3>
                        	<h4>Цена: {good.price}</h4>
                        	<h4>Остаток: {good.stock}</h4>
                        	{/*<Button onClick={() => Add_in_basket(good.id)}>Добавить в корзину</Button>*/}
                        </div>
                    	))
            		}

		</>
		)
}






