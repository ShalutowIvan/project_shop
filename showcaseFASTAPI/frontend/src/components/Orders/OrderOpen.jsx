import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue } from 'react-router-dom'
import { React, Suspense } from 'react';
import { API } from "../../apiAxios/apiAxios"




const Order = () => {
	const order = useAsyncValue()

	return (
		<div>			
			{order?.map( (element) => (
				<>						
					<li>Адрес доставки: {element.delivery_address}</li>
					<li>Телефон: {element.phone}</li>
					<li>Название товара: {element.product.name_product}</li>
					<li>Количество: {element.quantity}</li>					
					<li>Состояние заказа: {element.state_order}</li>					
					<p>____________________________________________</p>
				</>
				
				)
			)}
		</div>
		)
}




function OrderOpen() {
	const {order, id} = useLoaderData()

	const navigate = useNavigate();

	const goBack = () => navigate(-1);

	if (order === "error") {
    	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
  	}

	return (
		<>

			<h1>Содержание заказа</h1>
				<button onClick={goBack}>Назад</button>

					<Suspense fallback={<h2>Orders is Loading...</h2>}>
						<Await resolve={order}>
							<h2>Номер заказа: {id}</h2>
							<Order />							
						</Await>
					</Suspense>								

		</>
		)
}



async function getOrderOpen(id) {	

	try {
        const res = await API.get(`/api/checkout_list/orders/${id}`)			
		return res.data
      } catch (error) {
      	//если ошибка, то выдаем ошибку
        console.error("Error here: ", error);
        // setError("Failed to fetch user data. Please try again.");
        return "error"
      }
}


const orderOpenLoader = async ({params}) => {
	const id = params.id
	
	
	return {order: await getOrderOpen(id), id}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { OrderOpen, orderOpenLoader }
