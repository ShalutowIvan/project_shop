import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue } from 'react-router-dom'
import { React, Suspense, useState, useEffect } from 'react';
// import { API } from "../../apiAxios/apiAxios"


// ост тут....

const Order = () => {
	const order = useAsyncValue()

	return (
		<div>			
			{order?.map( (element) => (
				<>						
					<li>Название товара: {element.product_id.name_product}</li>
					<li>Количество: {element.quantity}</li>									
					<li>Адрес доставки: {element.delivery_address}</li>
					<li>Телефон: {element.phone}</li>					
					{/*{element.state_order && <h3>Состояние заказа: Проведен</h3>}
					{!element.state_order && <h3>Состояние заказа: Не Проведен</h3>}*/}	
					<p>____________________________________________</p>
				</>
				
				)
			)}
		</div>
		)
}



//order_state не сработает через состояние надо

function OrderOpen() {
	// const {order, order_number, order_state} = useLoaderData()
	//как я понял order подставляется в компонент Order который прописали выше
	//<Await resolve={order}> тут происходит перебор элементов как в map. Только для каждого элемента еще применяется функция компонента Order
	const {order_number} = useParams();
	const [goods, setGoods] = useState([]);
	const [state_order, setState_order] = useState(null);



	useEffect(() => {
		fetch(`http://127.0.0.1:9999/api/get_order/${order_number}`)
			.then(res => res.json())
			.then(data => setGoods(data))
			.catch((error) => {
        	console.error('Error fetching orders:', error);        	
      			});		
		}, [])
	
	useEffect(() => {
    	if (goods.length > 0) {  // Проверяем, что массив не пустой
      	const firstElement = goods[0];  // Берём первый заказ
      	setState_order(firstElement.state_order);  // Сохраняем его состояние
    			}
  		}, [goods]);  // Зависимость от `goods` — эффект выполнится при изменении списка



	const navigate = useNavigate();

	const goBack = () => {
		return navigate(-1);
	}

	// if (order === "error") {
  //   	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
  // 	}


	function api_order_list_activate() {
		fetch(`http://127.0.0.1:9999/api/order_list/open/activate/${order_number}`)
			.then(res => res.json())
			.then(data => setState_order(data.state_order))
	}

	function api_order_list_deactivate() {
		fetch(`http://127.0.0.1:9999/api/order_list/open/deactivate/${order_number}`)
			.then(res => res.json())
			.then(data => setState_order(data.state_order))
	}

	return (
		<>

			<h1>Содержание заказа</h1>
				<button onClick={goBack}>Назад</button>

					<Suspense fallback={<h2>Orders is Loading...</h2>}>
						<Await resolve={goods}>
							<h2>Номер заказа: {order_number}</h2>							
							
							<Order />							
						</Await>
					</Suspense>								


					{state_order && 
					<>
					<h3>Состояние заказа: Проведен</h3>
					<button onClick={api_order_list_deactivate}>Отменить проведение заказа</button>
					</>
					}


					{!state_order && 
					<>
					<h3>Состояние заказа: Не Проведен</h3>
					<button onClick={api_order_list_activate}>Провести заказ</button>
					</>
					}
										
		</>
		)
}



async function getOrderOpen(order_number) {	
	const res = await fetch(`http://127.0.0.1:9999/api/get_order/${order_number}`)//тут берутся все элементы с одним и тем же номером заказа

	// try {
  //       const res = await API.get(`/api/checkout_list/orders/${id}`)			
	// 	return res.data
  //     } catch (error) {
  //     	//если ошибка, то выдаем ошибку
  //       console.error("Error here: ", error);
  //       // setError("Failed to fetch user data. Please try again.");
  //       return "error"
  //     }


  return res.json()
}


const orderOpenLoader = async ({params}) => {
	const order_number = params.id
	const order_state = params.state_order
	
	
	return {order: await getOrderOpen(order_number), order_number, order_state}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { OrderOpen, orderOpenLoader }
