import React from 'react';
import { useParams, Link, useNavigate, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"
import GroupsAll from "./Groups"
import usePersistedState from './filterGoods/usePersistedState';
import SearchBox from './filterGoods/SearchBox';


export default function GoodsInGroup() {
	
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const {slug} = useParams();

	const [goods, setGoods] = useState([]);
	const [error, setError] = useState(null);
	const [loading, setLoading] = useState(true);
	const [isSearchPerformed, setIsSearchPerformed] = useState(false);
	const [searchTerm, setSearchTerm] = usePersistedState('productSearch', '');


	// const navigate = useNavigate();	

	const fetchProducts = async (searchQuery = '') => {
    setLoading(true);
    try {
      const url = searchQuery 
        ? `http://127.0.0.1:9999/api/products/search/${slug}?Q=${encodeURIComponent(searchQuery)}`
        : `http://127.0.0.1:9999/api/products/search/${slug}`;
      
      const response = await axios.get(url);
      setGoods(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      setError(err.message);
      setGoods([]);
    } finally {
      setLoading(false);
    }
  };
	
	useEffect(() => {		
		// fetch(`http://127.0.0.1:9999/api/get_good_in_group/${slug}`)
		// 	.then(res => res.json())
		// 	.then(data => setGoods(data))

		fetchProducts()
	}, [slug])
	
	const navigate = useNavigate();

	const modifyGood = (good_id) => {
		return navigate(`/goods/modify/${good_id}/`);
	}

	function deleteGood(good_id) {
		axios.get(`http://127.0.0.1:9999/api/goods_delete/${good_id}`)		
		setGoods(currentState => currentState.filter(item => item.id !== good_id));
	}


	if (loading) return <div className="loading">Загрузка товаров...</div>;
	if (error) return <div className="error">Ошибка: {error}</div>;

	const handleSearch = (e) => {
    	e.preventDefault();
    	if (searchTerm.trim()) {
      		fetchProducts(searchTerm);
      		setIsSearchPerformed(true);
    		}
  		};

  // Обработчик сброса
  	const handleResetSearch = () => {
    	setSearchTerm('');
    	setIsSearchPerformed(false);
    	fetchProducts(); // Загружаем все товары сразу
  		};


	return (
		<>

			<GroupsAll />

			<SearchBox
		        searchTerm={searchTerm}
		        onSearchChange={setSearchTerm}
		        onSearchSubmit={handleSearch}
		      	/>


		    {isSearchPerformed && (
        	<div>          		          	
          	<button onClick={handleResetSearch}>Сбросить поиск</button>        	
        	</div>
      		)}
      
      		<p>Количество товаров: {goods.length}</p>


			
			   		{goods?.map(good => (
                        <div className="goods" key={good.id}>
                        	<img 
                            src={good.photo} 
                            alt={good.name_product} 
                            className="product-image"
                        	/>
                        	<h4>{good.name_product}</h4>
                        	<h4>Цена: {good.price}</h4>
                        	<h4>Остаток: {good.stock}</h4>
                        	<button onClick={() => modifyGood(good.id)}>Редактировать</button>
                        	&nbsp;&nbsp;
                        	<button onClick={() => deleteGood(good.id)}>Удалить</button>                        	
                        </div>
                    ))}		

		</>
		)
}






