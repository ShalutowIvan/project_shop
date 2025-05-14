import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue } from 'react-router-dom'
import { React, Suspense, useState, useEffect } from 'react';
// import { API } from "../../apiAxios/apiAxios"
import axios from "axios"


// const Receipt = () => {
// 	const receipt = useAsyncValue()

// 	return (
// 		<div>			
			// {receipt?.map( (element) => (
			// 	<>						
			// 		<li>Название товара: {element.product.name_product} || Количество: {element.quantity}</li>						
			// 		<p>___________________________________________________</p>
			// 	</>				
			// 	)
			// )}
// 		</div>
// 		)
// }



//order_state не сработает через состояние надо

function Expense_open() {
	const {expense, expense_number} = useLoaderData()//загрузка данных из лоадера, загружается список товаров в документе и номер документа
	const [state_expense, setState_expense] = useState(null);//состояние для статуса документа
	const [goods_in_expense, setGoods_in_expense] = useState(expense);//состояние с товарами из документа. Изначально берется из лоадера, далее будет меняться при добавлении товара в накладную. В накладной будет форма постоянная для добавления товаров в нее
	// const [goods_in_expense_buffer, setGoods_in_expense_buffer] = useState([])

	const [newGood, setNewGood] = useState("")//состояние для добавления нового товара в накладную. 
	
	const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [repeat_good, setRepeat_good] = useState("")


    // ост тут... сделал получение номера документа в юзэффект....
	// useEffect загружает состояние документа когда документ открываем
	useEffect(() => {
		fetch(`http://127.0.0.1:9999/api/expense_number_open/${expense_number}`)
			.then(res => res.json())
			.then(data => setState_expense(data["state"]))
			.catch((error) => {
        	console.error('Error fetching state receipt:', error);
      			});

        //трай кетч добавить потом?
		// const response = axios.get(`http://127.0.0.1:9999/api/expense_number_open/${expense_number}`);
        // тут что то не так с await... запрос идет в лоадере, в юзэффект он не нужен

         // Добавляем поле customPrice к каждому товару
        // const itemsWithCustomPrice = goods_in_receipt?.map(item => ({
        //     ...item,
        //     customPrice: item.custom_price || null // Используем существующее значение или null
        // }));
                
        // setGoods_in_receipt(itemsWithCustomPrice);


        //загрузка товаров из буфера, актуально после загрузки файла excel с накладной когда новые товары в файле
        // fetch(`http://127.0.0.1:9999/api/receipt_list_open_buffer/${expense_number}/`)
		// 	.then(res => res.json())
		// 	.then(data => setGoods_in_receipt_buffer(data))
		// 	.catch((error) => {
        // 	console.error('Error fetching buffer receipt:', error);
      	// 		});

		
		}, [])
	
	const navigate = useNavigate();

	const goBack = () => {
		return navigate(-1);
	}

	
	// const loadFileReceipt = () => {
	// 	return navigate(`/incoming_documents/load_file/${expense_number}/`);
	// }

	
	//функции для проведения и отмены проведения акта
	function api_expense_list_activate() {
		fetch(`http://127.0.0.1:9999/api/expense_number_open/activate/${expense_number}`)
			.then(res => res.json())
			.then(data => setState_expense(data.state_expense))
	}

	function api_expense_list_deactivate() {
		fetch(`http://127.0.0.1:9999/api/expense_number_open/deactivate/${expense_number}`)
			.then(res => res.json())
			.then(data => setState_expense(data.state_expense))
	}

	//функция для валидации формы
	// const validateForm = () => {
    //     if (!comment) {
    //         setError("Не введен комментарий");
    //         return false;
    //     }
    //     setError('');
    //     return true;
    // }


    //обработчик формы добавления товара
    const addGood_in_expense = async (event) => {
        event.preventDefault();
        // if (!validateForm()) return;
        setLoading(true);
        
        try {            
            const response = await axios.post(
                `http://127.0.0.1:9999/api/expense_goods_add/${expense_number}/`,
                {                 
                newGood,
                },
                    // { withCredentials: true }
                );                        
            setLoading(false);
            if (response.statusText==='OK') {
            	//запись новой позиции в состояние. Добавляется новая позиция в накладную с колвом 1 и названием после записи и ответа от сервера.             	
            	if (response.data["answer"] === "empty") {            		
            		setRepeat_good("Такой товар уже есть в списке")
                	setNewGood("")
                	}
                else {
            	setGoods_in_expense(prevItems => [...prevItems, response.data]);
                console.log("Товар добавлен")
                setNewGood("")//чистим состояние после успешного добавления
                setRepeat_good("")
                }

            } else {
                const errorData = await response.data
                console.log(errorData, 'тут ошибка')                
            }    	

        } catch (error) {
            setLoading(false);
            console.log(error)
            setError('что-то пошло не так');            
        }
    };

    // функиця для изменения состояния количества в накладной, 
    const updateQuantity = (productId, quantity) => {
        setGoods_in_expense(goods_in_expense.map(item => 
            item.product.id === productId 
                ? { ...item, quantity: Math.max(1, quantity) } 
                : item
        ));
    };

    
    //удаление позиции из накладной
    const removeItem = (productId) => {
    	axios.delete(`http://127.0.0.1:9999/api/expense_goods_delete/${productId}/`)//тут просто запрос на удаление по ИД записи в объекте
        setGoods_in_expense(goods_in_expense.filter(item => item.id !== productId));//оставляем те элементы у которых ИД позиции не равен удаляемой
    };

    
    //сохранение накладной. На сервер изменения попадут только после сохранения, до сохранения изменения происходят только в состояниях реакта
    const saveExpense = async () => {
        if (goods_in_expense.length === 0) {
            alert('Добавьте хотя бы один товар в акт');
            return;
        }
        setLoading(true);        
        //отправляю из состояния в реакт ИД объектов позиций и колво в каждой позиции. В джанго при сохранении нужно будет изменить колво, дописать эту логику в джанго осталось. 
        try {
        const expenseData = {
                items: goods_in_expense.map(item => ({
                	id: item.id,
                    // product: item.product.id,
                    quantity: item.quantity,
                    // customPrice: item.customPrice === null ? 0 : item.customPrice
                }))
            };

        const response = await axios.patch('http://127.0.0.1:9999/api/expense_goods_save/', expenseData);
        alert('Акт успешно сохранен!');
        } catch (error) {
            console.error('Ошибка при сохранении акта:', error);
            // alert('Ошибка при сохранении накладной');
        } finally {
            setLoading(false);
        }
    }

        
	return (
		<>

			<h1>Содержание расходного документа</h1>
				<button onClick={goBack}>Назад</button>
				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				{/*<button onClick={loadFileReceipt}>Загрузить файл</button>*/}

					<h2>Номер документа: {expense_number}</h2>	

                    <div className="receipt-editor">
					<table>
                        <thead>
                            <tr>
                                <th>Товар</th>
                                <th>Цена</th>
                                <th>Количество</th>
                                <th>Сумма</th>
                                <th>Действие</th>
                            </tr>
                        </thead>

                        <tbody>
                        {goods_in_expense?.map(item => (
                                <tr key={item.product.id}>
                                    <td>{item.product.name_product}</td>
                                    <td>{item.product.price} руб.</td>
                                    {/*поле колво*/}
                                    {!state_expense && 
                                    <>
                                    <td>
                                        <input
                                            type="number"
                                            min="1"
                                            value={item.quantity}
                                            onChange={(e) => updateQuantity(item.product.id, parseInt(e.target.value))}
                                        />
                                    </td>
                                    </>
                                	}
                                	{state_expense && 
                                	<>
                                	<td>{item.quantity}</td>
                                	</>
                                	}
                                    <td>{item.quantity * item.product.price} руб.</td>                                    
                                    {!state_expense &&                                     
                                    <>
                                    <td>
                                        <button onClick={() => removeItem(item.id)}>
                                            Удалить
                                        </button>
                                    </td>
                                    </>
                                	}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    </div>
                    

                    {!state_expense && 
					<>
					<button onClick={saveExpense}>Сохранить</button>
					&nbsp;&nbsp;
					
					</>
					}

					<br/><br/>


					{/*форма будет тут*/}
					<form onSubmit={addGood_in_expense} style={{ marginBottom: '1rem' }}>                

		                <label htmlFor="id_newGood">Добавление товара: </label>
		                <input 
		                    placeholder="введите название товара"
		                    name="newGood"                    
		                    type="text"
		                    id="id_newGood"
		                    className="control"                        
		                    value={newGood}
		                    onChange={(e) => setNewGood(e.target.value)}   
		                />

		                &nbsp;&nbsp;

		                <button type="submit" disabled={loading}>                    
		                    {loading ? 'Сохраняем...' : 'Добавить'}
		                </button>
		                <br/>

		                {/*если ошибка error отображаем ее в параграфе ниже*/}
		                {error && <p style={{ color: 'red'}}>{error}</p>}
		                
                        {/*обработка ошибки если товар уже есть такой в документе*/}
		                {repeat_good && <p style={{ color: 'red'}}>{repeat_good}</p>}

		            </form>
					

					{state_expense && 
					<>
					<h3>Состояние документа: Проведен</h3>
					<button onClick={api_expense_list_deactivate}>Отменить проведение документа</button>
					</>
					}


					{!state_expense && 
					<>
					<h3>Состояние документа: Не Проведен</h3>
					<button onClick={api_expense_list_activate}>Провести документ</button>
					</>
					}
										
		</>
		)
}



async function getExpenseOpen(number_expense) {	
	const res = await fetch(`http://127.0.0.1:9999/api/expense_list_open/${number_expense}`)//тут берутся все элементы с одним и тем же номером документа

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


const expenseOpenLoader = async ({params}) => {
	
	const expense_number = params.number_exp//после params писать название параметра которое прописали в файле AppRouter.jsx с урлками

	// const receipt_state = params.state_order
	
	return {expense: await getExpenseOpen(expense_number), expense_number}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Expense_open, expenseOpenLoader }
