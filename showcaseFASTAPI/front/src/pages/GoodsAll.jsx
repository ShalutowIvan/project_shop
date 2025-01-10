import React from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"

export default function GoodsAll() {
	// console.log(useParams().id);
	// const {slug} = useParams();
	const [goods, setGoods] = useState([]);
	// const navigate = useNavigate();


	useEffect(() => {
		fetch(`http://127.0.0.1:8000/api/goods_all/`)
			.then(res => res.json())
			.then(data => setGoods(data))

	}, [])
	

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
                        <h3 className="goods">{good.name_product}</h3>
                    ))}


		</div>
		)

}






