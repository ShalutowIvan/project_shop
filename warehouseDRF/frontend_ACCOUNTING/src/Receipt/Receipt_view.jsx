import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue, NavLink } from 'react-router-dom'
import { React, Suspense } from 'react';
import Cookies from "js-cookie";
// import { API } from "../../apiAxios/apiAxios"



function Receipt_view() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const {receipts} = useLoaderData()

	// if (orders === "error") {
  //   	return <><h1>{"Вам нужно залогиниться!"}</h1></>;
  // 	}


	function receipt_create() {


	}


	return (
		<>
			<h1>Приходные документы</h1>

			<h2><NavLink to="/incoming_documents/create/">Создать документ</NavLink></h2>

					<Suspense fallback={<h2>Loading...</h2>}>
						<Await resolve={receipts}>
						{
						(resolvedReceipts) => (
							<>
								{
								resolvedReceipts?.map(receipt => (
									<>
									<h3>Номер документа: {receipt.id}</h3>
									
									<h4>Дата: {receipt.time_create}</h4>
									<Link key={receipt.id} to={`/incoming_documents/${receipt.id}`}>
										<button>Открыть документ</button>
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



async function getReceiptNumber() {
	const res = await fetch('http://127.0.0.1:9999/api/receipt_list_view/')
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


const receiptNumberLoader = async () => {	
	// const res = await fetch('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const order_to_json = res.json()
	return {receipts: await getReceiptNumber()}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Receipt_view, receiptNumberLoader }
