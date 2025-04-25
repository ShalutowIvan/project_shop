import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue } from 'react-router-dom'
import { React, Suspense, useState, useEffect  } from 'react';
import Cookies from "js-cookie";
// import { API } from "../../apiAxios/apiAxios"



function Orders_view() {
	// const {orders} = useLoaderData()

	const [orders, setOrders] = useState([]);

	// if (orders === "error") {
  //   	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
  // 	}

	useEffect(() => {
		fetch(`http://127.0.0.1:9999/api/get_order/`)
			.then(res => res.json())
			.then(data => setOrders(data))

		// fetch(`http://127.0.0.1:9999/api/get_group/`)
        //     .then(res => res.json())
        //     .then(data => setGroups(data));        
	}, [])


	function get_order_completed() {
		fetch(`http://127.0.0.1:9999/api/get_order_completed/`)
			.then(res => res.json())
			.then(data => setOrders(data))
	}

	function get_order_not_completed() {
		fetch(`http://127.0.0.1:9999/api/get_order_not_completed/`)
			.then(res => res.json())
			.then(data => setOrders(data))
	}

	function get_order_all() {
		fetch(`http://127.0.0.1:9999/api/get_order/`)
			.then(res => res.json())
			.then(data => setOrders(data))
	}

	


	return (
		<>
			<h1>Заказы покупателей</h1>
			
			<button onClick={get_order_all}>Все заказы</button>
			&nbsp;&nbsp;&nbsp;
			<button onClick={get_order_completed}>Проведенные заказы</button>
			&nbsp;&nbsp;&nbsp;
			<button onClick={get_order_not_completed}>Не Проведенные заказы</button>
			
					<Suspense fallback={<h2>Loading...</h2>}>
						<Await resolve={orders}>
						{
						(resolvedOrders) => (
							<>
								{
								resolvedOrders?.map(order => (
									<>
									<h3>Номер заказа: {order.order_number}</h3>
									
									<h4>Дата: {order.time_create}</h4>
									
									{order.state_order && <h4>Статус: Проведен</h4>}
									{!order.state_order && <h4>Статус: Не Проведен</h4>}

									<Link key={order.id} to={`/orders/${order.order_number}`}>
										<button>Открыть заказ</button>
									</Link>
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


//лоадер передумал юзать, решил через юзэффект
async function getOrderNumber() {
	const res = await fetch('http://127.0.0.1:9999/api/get_order/')
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


const orderNumberLoader = async () => {	
	// const res = await fetch('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const order_to_json = res.json()
	return {orders: await getOrderNumber()}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Orders_view, orderNumberLoader }
