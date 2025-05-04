import React from 'react';
import { useParams, Link, useNavigate, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"
// import Button from '../components/Button/Button'
// import { API } from "../apiAxios/apiAxios"
import GroupsAll from "./Groups"
import usePersistedState from './hooks/usePersistedState';
import SearchBar from './filterGoods/SearchBar';

import { filterProducts } from './filterGoods/filterProducts';
// import ProductList from './filterGoods/ProductList';




export default function GoodsAll() {
	// console.log(useParams().id);
	// const {slug} = useParams();
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const [goods, setGoods] = useState([]);
	// const [groups, setGroups] = useState([]);
	// const [error, setError] = useState("");
	
	//состояние для поиска товара
	// const [fgoods, setFgoods] = useState("");
	const [searchTerm, setSearchTerm] = usePersistedState('productSearch', '');

	useEffect(() => {
		fetch(`http://127.0.0.1:9999/api/get_good/`)
			.then(res => res.json())
			.then(data => setGoods(data))

		// fetch(`http://127.0.0.1:9999/api/get_group/`)
        //     .then(res => res.json())
        //     .then(data => setGroups(data));        
	}, [])
	

	const filteredProducts = filterProducts(goods, searchTerm);

	const navigate = useNavigate();
	
	const modifyGood = (good_id) => {
		return navigate(`/goods/modify/${good_id}/`);
	}

	function deleteGood(good_id) {
		axios.get(`http://127.0.0.1:9999/api/goods_delete/${good_id}`)
		
		// fetch(`http://127.0.0.1:9999/api/get_good/`)
		// 	.then(res => res.json())
		// 	.then(data => setGoods(data))
		setGoods(currentState => currentState.filter(item => item.id !== good_id));
	}

	const findGoods = () => {
		setGoods(currentState => currentState.filter(item => item.name_product === fgoods));
	}

	

	return (
		<>			
			{/*группы рисуются сбоку*/}
			<GroupsAll />

			<h1>Список товаров</h1>
			<button><NavLink to="/groups/add/" className={setActive}>Добавить группу</NavLink></button>
			&nbsp;&nbsp;&nbsp;
			<button><NavLink to="/goods/add/" className={setActive}>Добавить товар</NavLink></button>
			&nbsp;&nbsp;&nbsp;
			<button><NavLink to="/goods/load_file/" className={setActive}>Загрузить файл</NavLink></button>
			&nbsp;&nbsp;&nbsp;
			<button><NavLink to="/goods/load_images/" className={setActive}>Загрузить фото товаров</NavLink></button>
			&nbsp;&nbsp;&nbsp;
			<button><NavLink to="/goods/clean_images/" className={setActive}>Очистка неиспользуемых фото</NavLink></button>
			&nbsp;&nbsp;&nbsp;
			<button><NavLink to="/groups/delete/" className={setActive}>Выбрать группу для удаления</NavLink></button>
			<br/><br/>

			<h1>Каталог товаров</h1>
      			<SearchBar 
        		searchTerm={searchTerm}
        		onSearchChange={setSearchTerm}
      			/>

			{/* <form onSubmit={findGoods} style={{ marginBottom: '1rem' }}>                
                <label htmlFor="id_name_group">Поиск товара: </label>
                <input 
                    placeholder="введите название товара"
                    name="name_product"                    
                    type="text"
                    id="id_name_product"
                    className="control"                        
                    value={fgoods}
                    onChange={(e) => setFgoods(e.target.value)}   
                />
                &nbsp;&nbsp;
                <button type="submit">                    
                    Найти
                </button>                
				
               
            </form> */}


			<div className="search-info">
        	{searchTerm && (
          		<p>Результаты поиска по запросу: "{searchTerm}"</p>
        		)}
        		<p>Найдено товаров: {filteredProducts.length}</p>
      		</div>

			
			{goods?.map(good => (
                        <div className="goods" key={good.id}>                        	
                        	<h3>{good.name_product}</h3>
                        	<h4>Цена: {good.price}</h4>
                        	<h4>Остаток: {good.stock}</h4>
                        	<button onClick={() => modifyGood(good.id)}>Редактировать</button>
                        	&nbsp;&nbsp;
                        	<button onClick={() => deleteGood(good.id)}>Удалить</button>
                        	{/*<Button onClick={() => Add_in_basket(good.id)}>Добавить в корзину</Button>*/}
                        	{/*<p>{error}</p>*/}
                        </div>
                    ))}

			

		</>
		)

}






