import React from 'react';
import { useParams, Link, useNavigate, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from "axios"
// import Button from '../components/Button/Button'
// import { API } from "../apiAxios/apiAxios"
import GroupsAll from "./Groups"
import usePersistedState from './filterGoods/usePersistedState';
import SearchBox from './filterGoods/SearchBox';

// import { filterProducts } from './filterGoods/filterProducts';
// import ProductList from './filterGoods/ProductList';




export default function GoodsAll() {
	// console.log(useParams().id);
	// const {slug} = useParams();
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const [goods, setGoods] = useState([]);
	
	//состояние для поиска товара
	// const [fgoods, setFgoods] = useState("");
	const [searchTerm, setSearchTerm] = usePersistedState('productSearch', '');
  	const [loading, setLoading] = useState(true);
  	const [error, setError] = useState(null);  	
  	const [isSearchPerformed, setIsSearchPerformed] = useState(false);


  	// Функция загрузки товаров
  	const fetchProducts = async (searchQuery = '') => {
    setLoading(true);
    try {
      const url = searchQuery 
        ? `http://127.0.0.1:9999/api/products/search/?Q=${encodeURIComponent(searchQuery)}`
        : 'http://127.0.0.1:9999/api/products/search/';
      
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
		// fetch(`http://127.0.0.1:9999/api/get_good/`)
		// 	.then(res => res.json())
		// 	.then(data => setGoods(data))

	// 	const fetchProducts = async () => {
    //   try {
    //     const response = await axios.get('http://127.0.0.1:9999/api/get_good/');
    //     setGoods(response.data);
    //     setLoading(false);
    //   } catch (err) {
    //     setError(err.message);
    //     setLoading(false);
    //   }
    // };

    // fetchProducts();
		fetchProducts()
	}, [])
	

	const navigate = useNavigate();
	
	const modifyGood = (good_id) => {
		return navigate(`/goods/modify/${good_id}/`);
	}

	function deleteGood(good_id) {
		axios.get(`http://127.0.0.1:9999/api/goods_delete/${good_id}`)		
		setGoods(currentState => currentState.filter(item => item.id !== good_id));
	}

	
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



  	if (loading) return <div className="loading">Загрузка товаров...</div>;
	if (error) return <div className="error">Ошибка: {error}</div>;

	

	return (
		<>			
			{/*группы рисуются сбоку*/}
			<GroupsAll />

			<h1>Каталог товаров</h1>
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

			
      		{/*тут беда со стилями для фото и товаров!!!!!!!!!!!!*/}
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






