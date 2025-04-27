import React from 'react';
import { useParams, Link, useNavigate, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"
// import Button from '../components/Button/Button'
// import { API } from "../apiAxios/apiAxios"
import GroupsAll from "./Groups"



export default function GoodsAll() {
	// console.log(useParams().id);
	// const {slug} = useParams();
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const [goods, setGoods] = useState([]);
	// const [groups, setGroups] = useState([]);
	// const [error, setError] = useState("");


	useEffect(() => {
		fetch(`http://127.0.0.1:9999/api/get_good/`)
			.then(res => res.json())
			.then(data => setGoods(data))

		// fetch(`http://127.0.0.1:9999/api/get_group/`)
        //     .then(res => res.json())
        //     .then(data => setGroups(data));        
	}, [])

	// function Add_in_basket(good_id) {
	// 	API.get(`/api/basket/${good_id}`)			
	// }
	

	return (
		<>			
			{/*группы рисуются сбоку*/}
			<GroupsAll />

			<h1>Список товаров</h1>
			<button><NavLink to="/groups/add/" className={setActive}>Добавить группу</NavLink></button>
			<button><NavLink to="/goods/add/" className={setActive}>Добавить товар</NavLink></button>
			<button><NavLink to="/groups/add/" className={setActive}>Добавить группу</NavLink></button>
			<button><NavLink to="/groups/add/" className={setActive}>Добавить группу</NavLink></button>
			<br/><br/>
			
			
			{goods?.map(good => (
                        <div className="goods" key={good.id}>                        	
                        	<h3>{good.name_product}</h3>
                        	<h4>Цена: {good.price}</h4>
                        	<h4>Остаток: {good.stock}</h4>
                        	{/*<Button onClick={() => Add_in_basket(good.id)}>Добавить в корзину</Button>*/}
                        	{/*<p>{error}</p>*/}
                        </div>
                    ))}

			

		</>
		)

}






