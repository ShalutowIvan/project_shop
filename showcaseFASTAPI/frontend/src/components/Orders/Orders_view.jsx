import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue } from 'react-router-dom'
import { React, Suspense } from 'react';
import Cookies from "js-cookie";
import { API } from "../../apiAxios/apiAxios"



function Orders_view() {
	const {orders} = useLoaderData()

	if (orders === "error") {
    	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
  	}

	return (
		<>
			<h1>Тут будут мои покупки</h1>

					<Suspense fallback={<h2>Loading...</h2>}>
						<Await resolve={orders}>
						{
						(resolvedOrders) => (
							<>
								{
								resolvedOrders.map(order => (
									<>
									<h3>Номер заказа: {order.id}</h3>
									
									<h4>Дата: {order.time_create}</h4>
									<Link key={order.id} to={`/checkout_list/orders/${order.id}`}>{/*это переход по ссылке Singlepage и он отрисовывает наш id*/}
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



async function getOrderNumber() {
	// const res = await fetch('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const res = await API.get('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const token = Cookies.get("Authorization");
	// console.log(token);

	try {
        // Запрос к защищенному эндпоинту FastAPI        
        const res = await API.get('/api/checkout_list/orders/')
        //если все хорошо возвращаем данные
        return res.data        
      } catch (error) {
      	//если ошибка, то выдаем ошибку
        console.error("Error here: ", error);
        // setError("Failed to fetch user data. Please try again.");
        return "error"
      }

	
}


const orderNumberLoader = async () => {	
	// const res = await fetch('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const order_to_json = res.json()
	return {orders: await getOrderNumber()}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Orders_view, orderNumberLoader }
