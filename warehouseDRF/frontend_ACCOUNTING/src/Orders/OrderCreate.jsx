import Orders_contact_form from './Orders_contact_form'
import { redirect, useNavigation } from 'react-router-dom'
import { API } from "../../apiAxios/apiAxios"

function OrderCreate() {

	const navigation = useNavigation()
	

	return (
		<div>
			<h1>Оформление заказа</h1>

			<Orders_contact_form submitting={navigation.state === 'submitting'} />


		</div>
		)
}



async function createOrderRequest ({fio, phone, delivery_address, pay }) {
	// const res = await fetch('http://127.0.0.1:8000/api/basket/contacts/', {
	// 	method: 'POST',
	// 	headers: { 'Content-Type': 'application/json' },
	// 	body: JSON.stringify({ fio, phone, delivery_address, pay })
	// 	})
	const res = await API.post("/api/basket/contacts/",
				{ fio, phone, delivery_address, pay },
                { withCredentials: true }
                );

	const newOrder = await res.data

	return newOrder
}


async function createOrderAction ({request}) {
	const formData = await request.formData();
	const newOrderObj = {
		fio: formData.get('fio'),
		phone: formData.get('phone'),
		delivery_address: formData.get('delivery_address'),
		pay: formData.get('pay')		
	}
	
		
	const order = await createOrderRequest(newOrderObj)
	
	return redirect('/checkout_list/orders/')
	

}



export { OrderCreate, createOrderAction, createOrderRequest }








