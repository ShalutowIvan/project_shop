import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue, NavLink } from 'react-router-dom'
import { React, Suspense, useState } from 'react';
import Cookies from "js-cookie";
// import { API } from "../../apiAxios/apiAxios"
import axios from "axios"


function Expense_view() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
	const {expenses} = useLoaderData()
	const [list_expenses, setList_expenses] = useState(expenses)
	

	function deleteDocu(expense_number) {		
		axios.get(`http://127.0.0.1:9999/api/expense_delete/${expense_number}/`)		
		setList_expenses(currentState => currentState.filter(item => item.id !== expense_number));		
		
	}

	return (
		<>
			<h1>Расходные документы</h1>

			<h2><NavLink to="/expense_documents/create/">Создать документ</NavLink></h2>

					<Suspense fallback={<h2>Loading...</h2>}>
						<Await resolve={list_expenses}>
						{
						(resolvedExpenses) => (
							<>
								{
								resolvedExpenses?.map(expense => (
									<>
									<h3>Номер документа: {expense.id}</h3>
									
									<h4>Дата: {expense.time_create}</h4>
									{expense.state && <h3>Состояние документа: Проведен</h3>}
									{!expense.state && <h3>Состояние документа: Не Проведен</h3>}
									<Link key={expense.id} to={`/expense_documents/${expense.id}`}>
										<button>Открыть документ</button>
									</Link>	
									&nbsp;&nbsp;&nbsp;																		
									{!expense.state &&
									<button onClick={() => deleteDocu(expense.id)}>Удалить документ</button>		
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



async function getExpenseNumber() {
	const res = await fetch('http://127.0.0.1:9999/api/expense_list_view/')
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


const expenseNumberLoader = async () => {	
	// const res = await fetch('http://127.0.0.1:8000/api/checkout_list/orders/')
	// const order_to_json = res.json()
	return {expenses: await getExpenseNumber()}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Expense_view, expenseNumberLoader }
