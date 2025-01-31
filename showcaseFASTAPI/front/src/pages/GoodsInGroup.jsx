import React from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"

import Button from '../components/Button/Button'


export default function GoodsInGroup() {
	// console.log(useParams().id);
	const {slug} = useParams();
	const [goods, setGoods] = useState([]);
	// const navigate = useNavigate();


	useEffect(() => {
		fetch(`http://127.0.0.1:8000/api/goods_in_group/${slug}`)
			.then(res => res.json())
			.then(data => setGoods(data))

	}, [slug])
	
	const url_basket_add = "http://127.0.0.1:8000/api/basket/"

	function Add_in_basket(good_id) {
		axios.get(`http://127.0.0.1:8000/api/basket/${good_id}`)		
	}


	return (
		<>

			{/*{goods && (
				<>
					<h3>{post.title}</h3>
					<p>{post.body}</p>
					<Link to={`/posts/${id}/edit`}>Редактировать</Link>
				</>
				)}*/}
			{
                goods?.map(good => (
                        <div className="goods" key={good.id}>
                        	
                        	<h3>{good.name_product}</h3>
                        	<h4>Цена: {good.price}</h4>
                        	<h4>Остаток: {good.stock}</h4>
                        	<Button onClick={() => Add_in_basket(good.id)}>Добавить в корзину</Button>
                        </div>
                    ))
            }


            	




		</>
		)

}






