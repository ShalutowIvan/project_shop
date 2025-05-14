import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue, NavLink } from 'react-router-dom'
import { React, Suspense, useState } from 'react';
import Cookies from "js-cookie";
// import { API } from "../../apiAxios/apiAxios"
import axios from "axios"


function Inventory_view() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const {inventorys} = useLoaderData()
	const [list_inventorys, setList_inventorys] = useState(inventorys)
	

	function deleteDoc(inventory_number) {		
		axios.get(`http://127.0.0.1:9999/api/inventory_delete/${inventory_number}/`)		
		setList_inventorys(currentState => currentState.filter(item => item.id !== inventory_number));
	}

	return (
		<>
			<h1>Список инвентаризаций</h1>

			<h2><NavLink to="/inventory/create/">Создать документ</NavLink></h2>

					<Suspense fallback={<h2>Loading...</h2>}>
						<Await resolve={list_inventorys}>
						{
						(resolvedInventorys) => (
							<>
								{
								resolvedInventorys?.map(inventory => (
									<>
									<h3>Номер документа: {inventory.id}</h3>									
									<h4>Дата: {inventory.time_create}</h4>

									{inventory.state && <h3>Состояние документа: Проведен</h3>}
									{!inventory.state && <h3>Состояние документа: Не Проведен</h3>}

									<Link key={inventory.id} to={`/inventory/${inventory.id}`}>
										<button>Открыть документ</button>
									</Link>
									&nbsp;&nbsp;&nbsp;																		
									{!inventory.state &&
									<button onClick={() => deleteDoc(inventory.id)}>Удалить документ</button>		
									}		
									<p>__________________________________________________________</p>
									</>
								))
								}
							</>)
					}
				</Await>
			</Suspense>
								
		</>
		)
}



async function getInventoryNumber() {
	const res = await fetch('http://127.0.0.1:9999/api/inventory_list_view/')
	// const res = await API.get('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const token = Cookies.get("Authorization");
	// console.log(token);

	// try {
  //       // Запрос к защищенному эндпоинту FastAPI        
  //       const res = await API.get('/api/checkout_list/orders/')
  //       //если все хорошо возвращаем данные
  //       return res.data        
  //     } catch (error) {
  //     	//если ошибка, то выдаем ошибку
  //       console.error("Error here: ", error);
  //       // setError("Failed to fetch user data. Please try again.");
  //       return "error"
  //     }

	return res.json()
}


const inventoryNumberLoader = async () => {	
	// const res = await fetch('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const order_to_json = res.json()
	return {inventorys: await getInventoryNumber()}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Inventory_view, inventoryNumberLoader }
