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

function Inventory_open() {
	const {inventory, inventory_number} = useLoaderData()//загрузка данных из лоадера, загружается список товаров в документе и номер документа
	const [state_inventory, setState_inventory] = useState(null);//состояние для статуса документа
	const [goods_in_inventory, setGoods_in_inventory] = useState(inventory);//состояние с товарами из документа. Изначально берется из лоадера, далее будет меняться при добавлении товара в накладную. В накладной будет форма постоянная для добавления товаров в нее
	const [goods_in_inventory_buffer, setGoods_in_inventory_buffer] = useState([])

	
	// добавление группы тут будет через отдельный компонент с формой в select выпадающий список... в товарах такое делал при добавлении товара

	const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [repeat_good, setRepeat_good] = useState("")
    const [view_object, setView_object] = useState(false);//для смены кнопок в jsx
    const [view_change_good, setView_change_good] = useState(false);//для смены кнопок в jsx
    const [good_name, setGood_name] = useState("")//состояние для добавления нового товара в накладную. 

    //поля формы
    const [group, setGroup] = useState("");  

    //для выпадающего списка с группами
    const [groups, setGroups] = useState([]);




	// useEffect загружает состояние документа когда документ открываем
	useEffect(() => {
		fetch(`http://127.0.0.1:9999/api/inventory_number_open/${inventory_number}`)
			.then(res => res.json())
			.then(data => setState_inventory(data["state"]))
			.catch((error) => {
        	console.error('Error fetching state receipt:', error);
      			});

        //загрузка списка групп для выпадающего списка
        fetch(`http://127.0.0.1:9999/api/get_group/`)
                .then(res => res.json())
                .then(data => setGroups(data)); 

        //трай кетч добавить потом?
		// const response = axios.get(`http://127.0.0.1:9999/api/inventory_number_open/${inventory_number}`);
        // тут что то не так с await... запрос идет в лоадере, в юзэффект он не нужен

         // Добавляем поле customPrice к каждому товару
        // const itemsWithCustomPrice = goods_in_inventory?.map(item => ({
        //     ...item,
        //     customPrice: item.custom_price || null // Используем существующее значение или null
        // }));
                
        // setGoods_in_inventory(itemsWithCustomPrice);


        //загрузка товаров из буфера, актуально после загрузки файла excel с накладной когда новые товары в файле
        fetch(`http://127.0.0.1:9999/api/inventory_list_open_buffer/${inventory_number}/`)
			.then(res => res.json())
			.then(data => setGoods_in_inventory_buffer(data))
			.catch((error) => {
        	console.error('Error fetching buffer receipt:', error);
      			});		
		}, [])
	
	const navigate = useNavigate();

	const goBack = () => {
		return navigate(-1);
	}
	
	const loadFileInventory = () => {
		return navigate(`/inventory/load_file/${inventory_number}/`);
	}

	
	//функции для проведения и отмены проведения накладной
	function api_receipt_list_activate() {
		fetch(`http://127.0.0.1:9999/api/inventory_number_open/activate/${inventory_number}`)
			.then(res => res.json())
			.then(data => setState_inventory(data.state_inventory))
	}

	function api_receipt_list_deactivate() {
		fetch(`http://127.0.0.1:9999/api/inventory_number_open/deactivate/${inventory_number}`)
			.then(res => res.json())
			.then(data => setState_inventory(data.state_inventory))
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

    //для отображения поля с добавлением группы
    const make_view_object = () => {
        setView_object(true)
    }

    //обработчик формы добавления группы с товарами
    const addGroup_in_inventory = async (event) => {
        event.preventDefault();
        // if (!validateForm()) return;
        setLoading(true);
        // ссылки в запросах с фронта на бэк должны совпадать полностью до каждого символа сука!!!!!!!!!!!
        try {            
            const response = await axios.post(
                `http://127.0.0.1:9999/api/inventory_add_group/${inventory_number}/`,
                {                 
                name_group: group,
                },
                    // { withCredentials: true }
                );                        
            setLoading(false);
            if (response.statusText==='OK') {
            	//запись новой позиции в состояние. Добавляется новая позиция в накладную с колвом 1 и названием после записи и ответа от сервера.             	
            	if (response.data["answer"] === "empty") {            		
            		setRepeat_good("Товары из группы уже есть в списке")

                	// setNewGood("")
                	}
                else {                        	
                
                setGoods_in_inventory(prevItems => [...prevItems, ...response.data]);//тут идет добавление к массиву объектов в состоянии нового массива из ответа от сервера

                console.log("Товары добавлены")
                setGroup("")//чистим состояние группы после успешного добавления
                setRepeat_good("")
                setError("")
                setView_object(false)
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
        setGoods_in_inventory(goods_in_inventory.map(item => 
            item.product.id === productId 
                ? { ...item, quantity_new: Math.max(0, quantity) } 
                : item
        ));
    };

    //функция для изменения состояния цены товара
    // const updatePrice = (productId, price) => {
    //     setGoods_in_inventory(goods_in_inventory.map(item => 
    //         item.product.id === productId 
    //             ? { ...item, price: Math.max(1, price) } 
    //             : item
    //     ));
    // };

    //проверить передачу цены в БД в джанго
    // const updateCustomPrice = (itemId, newPrice) => {
    //     setGoods_in_inventory(prevItems => 
    //         prevItems.map(item => 
    //             item.id === itemId 
    //                 ? { 
    //                     ...item, 
    //                     customPrice: newPrice === '' ? null : parseFloat(newPrice) 
    //                   } 
    //                 : item
    //         )
    //     );
    // };



    //удаление позиции из инванты
    const removeItem = (productId) => {
    	axios.delete(`http://127.0.0.1:9999/api/inventory_goods_delete/${productId}/`)//тут просто запрос на удаление по ИД записи в объекте
        setGoods_in_inventory(goods_in_inventory.filter(item => item.id !== productId));//оставляем те элементы у которых ИД позиции не равен удаляемой
    };


    const removeItemBuffer = (productId) => {
    	axios.delete(`http://127.0.0.1:9999/api/inventory_goods_buffer_delete/${productId}/`)//тут просто запрос на удаление по ИД записи в объекте
        setGoods_in_inventory_buffer(goods_in_inventory_buffer.filter(item => item.id !== productId));//оставляем те элементы у которых ИД позиции не равен удаляемой
    };


    
    //сохранение накладной. На сервер изменения попадут только после сохранения, до сохранения изменения происходят только в состояниях реакта
    const saveInventory = async () => {
        if (goods_in_inventory.length === 0) {
            alert('Добавьте хотя бы один товар в инвентаризацию');
            return;
        }
        setLoading(true);                
        try {
        const inventoryData = {
                items: goods_in_inventory.map(item => ({
                	id: item.id,
                    // product: item.product.id,
                    quantity_new: item.quantity_new,
                    // customPrice: item.customPrice === null ? 0 : item.customPrice
                }))
            };

        const response = await axios.patch('http://127.0.0.1:9999/api/inventory_goods_save/', inventoryData);
        alert('Инвентаризация успешно сохранена!');
        } catch (error) {
            console.error('Ошибка при сохранении накладной:', error);
            // alert('Ошибка при сохранении накладной');
        } finally {
            setLoading(false);
        }
    }

    //функция для кнопки добавления товара если его нет в БД из буфера
    // ост тут
    const add_if_not_in_base = async (productId) => {

    	setLoading(true);        
    	try {
        	const response = await axios.post(`http://127.0.0.1:9999/api/inventory_list/inventory_add_if_not_in_base/${inventory_number}/`);
    	
    		if (response.statusText==='OK') {
    			//добавили в общий сет
                
            	setGoods_in_inventory(prevItems => [...prevItems, response.data]);

                console.log("Товар добавлен")
                //удалили из сета буфера
                setGoods_in_inventory_buffer(goods_in_inventory_buffer.filter(item => item.id !== productId))
                }
 			else {
                const errorData = await response.data
                console.log(errorData, 'тут ошибка')                
            }

    	} catch (error) {
            console.error('Ошибка при добавлении товаров:', error);            
        } finally {
            setLoading(false);
        }
    }

    //замена товара на другой
    const make_change_good = () => {
        setView_change_good(true)
    }

    const change_if_not_in_base = async (buffer_id, event) => {
        event.preventDefault();
        // if (!validateForm()) return;
        setLoading(true);
        // ссылки в запросах с фронта на бэк должны совпадать полностью до каждого символа сука!!!!!!!!!!!
        try {            
            const response = await axios.post(
                `http://127.0.0.1:9999/api/inventory_goods_change/${buffer_id}/`,
                {                 
                good_name,
                },
                    // { withCredentials: true }
                );                        
            setLoading(false);
            if (response.statusText==='OK') {
                //запись новой позиции в состояние. Добавляется новая позиция в накладную с колвом 1 и названием после записи и ответа от сервера.              
                if (response.data["answer"] === "change") {                  
                    console.log("Товары из группы изменен") 
                    // тут нужно обновить колво в существующем товаре из состояния
                    
                    setGoods_in_inventory(
                        prevGoods => 
                          prevGoods.map(good => 
                            good.id === response.data["good"].id 
                              ? { ...good, ...response.data["good"] }  // Мерджим все изменения
                              : good
                          )
                        )
                    setGoods_in_inventory_buffer(goods_in_inventory_buffer.filter(item => item.id !== buffer_id))
                    }
                else {                          
                
                setGoods_in_inventory(prevItems => [...prevItems, response.data]);

                setGoods_in_inventory_buffer(goods_in_inventory_buffer.filter(item => item.id !== buffer_id))

                console.log("Товар добавлен")
                setGood_name("")
                setRepeat_good("")
                setError("")
                setView_change_good(false)

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


    const total = goods_in_inventory.reduce((sum, item) => sum + (item.quantity * item.price), 0);


	return (
		<>

			<h1>Содержание инвентаризации</h1>
				<button onClick={goBack}>Назад</button>
				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				<button onClick={loadFileInventory}>Загрузить файл</button>

					<h2>Номер инвентаризации: {inventory_number}</h2>	

                    <div className="receipt-editor">
					<table>
                        <thead>
                            <tr>
                                <th>Товар</th>
                                <th>Цена</th>
                                <th>Количество было</th>
                                <th>Количество стало</th>
                                <th>Сумма</th>
                                <th>Действие</th>
                            </tr>
                        </thead>

                        <tbody>
                        {goods_in_inventory?.map(item => (
                                <tr key={item.product.id}>
                                    <td>{item.product.name_product}</td>                                	
                                	<td>{item.product.price} руб.</td>
                                    <td>{item.quantity_old}</td>                                    
                                    
                                    {/*поле колво*/}
                                    {!state_inventory && 
                                    <>
                                    <td>
                                        <input
                                            type="number"
                                            min="0"
                                            value={item.quantity_new}
                                            onChange={(e) => updateQuantity(item.product.id, parseInt(e.target.value))}
                                        />
                                    </td>
                                    </>
                                	}
                                	{state_inventory && 
                                	<>
                                	<td>{item.quantity_new}</td>
                                	</>
                                	}
                                    <td>{item.quantity_new * item.product.price} руб.</td>                                    
                                    {!state_inventory &&                                     
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

                    <h3>Итого: {total} руб.</h3>
                    

                    {/*таблица с товарами из буффера*/}
                    <h2>Этих товаров нет в базе.</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Товар</th>
                                {/*<th>Цена</th>*/}
                                <th>Количество</th>
                                {/*<th>Сумма</th>*/}
                                <th>Действие</th>
                            </tr>
                        </thead>

                        <tbody>
                        {goods_in_inventory_buffer?.map(item => (
                                <tr key={item.id}>
                                    <td>{item.product}</td>
                                    {/*<td>{item.price} руб.</td>*/}
                                    
									<td>{item.quantity_new}</td>
                                    
                                    
                                    {/*<td>{item.quantity * item.product.price} руб.</td>                                    */}
                                    {!state_inventory &&                                     
                                    <>
                                    <td>
                                        <button onClick={() => removeItemBuffer(item.id)}>Удалить</button>
                                        <br/>
                                        <button onClick={() => add_if_not_in_base(item.id)}>Добавить в инвентаризацию</button>
                                        <br/>
                                        
                                        {!view_change_good &&
                                        <button onClick={make_change_good}>Заменить на другой товар</button>
                                        }
                                        {/*ИСПРАВИТЬ ФОРМУ НИЖЕ НА ПОИСК ДЛЯ ИЗМЕНЕНИЕ ТОВАРА, И В ДЖАНГО НАДО УРЛ СДЕЛАТЬ.*/}
                                        {view_change_good &&
                                        
                                        // <form onSubmit={change_if_not_in_base} style={{ marginBottom: '1rem' }}>
                                        <form onSubmit={(event) => change_if_not_in_base(item.id, event) } style={{ marginBottom: '1rem' }}>
                                            <label htmlFor="id_good_name">Поиска товара для замены: </label>
                                            <br/>
                                                <input 
                                                    placeholder="введите название товара"
                                                    name="good_name"                                        
                                                    type="text"
                                                    
                                                    id="id_good_name"
                                                    className="control"                        
                                                    value={good_name}
                                                    onChange={(e) => setGood_name(e.target.value)}   
                                                />                

                                                &nbsp;&nbsp;
                                                <button type="submit" disabled={loading}>                    
                                                    {loading ? 'Сохраняем...' : 'Добавить'}
                                                </button>
                                                <br/>                       
                                                {error && <p style={{ color: 'red'}}>{error}</p>}                       
                                                {repeat_good && <p style={{ color: 'red'}}>{repeat_good}</p>}
                                        </form>
                                        }


                                    </td>
                                    </>
                                	}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    </div>                   

                    {!state_inventory && 
					<>
					<button onClick={saveInventory}>Сохранить</button>
					&nbsp;&nbsp;
					
					</>
					}

					{/*тут будет форма с добавленными товарами в накладной, в ней можно менять колво. Сделать добавление товара и потом в накладной редачить колво и сохранять накладную. Потом если надо проводить*/}

					






					{/*форма добавления группы в инвенту будет тут*/}

                    {!view_object &&
                    <button onClick={make_view_object}>Добавить группу</button>
                    }

					{view_object &&
                    <form onSubmit={addGroup_in_inventory} style={{ marginBottom: '1rem' }}>
                        <label htmlFor="id_group">Группа: </label>                
                            <select
                                name="group"
                                id="id_group"
                                // className="control"                        
                                value={group}
                                onChange={(e) => setGroup(e.target.value)}   
                                // required
                            >
                                <option value="">Выберите группу</option>
                                {groups?.map(group => (
                                    <option key={group.id} value={group.id}>
                                        {group.name_group}
                                    </option>
                                ))}
                            </select>

    		                &nbsp;&nbsp;
    		                <button type="submit" disabled={loading}>                    
    		                    {loading ? 'Сохраняем...' : 'Добавить'}
    		                </button>
    		                <br/>		                
    		                {error && <p style={{ color: 'red'}}>{error}</p>}		                
    		                {repeat_good && <p style={{ color: 'red'}}>{repeat_good}</p>}
		            </form>
					}

					{state_inventory && 
					<>
					<h3>Состояние документа: Проведен</h3>
					<button onClick={api_receipt_list_deactivate}>Отменить проведение документа</button>
					</>
					}


					{!state_inventory && 
					<>
					<h3>Состояние документа: Не Проведен</h3>
					<button onClick={api_receipt_list_activate}>Провести документ</button>
					</>
					}
										
		</>
		)
}



async function getInventoryOpen(number_inventory) {	
	const res = await fetch(`http://127.0.0.1:9999/api/inventory_list_open/${number_inventory}`)//тут берутся все элементы с одним и тем же номером документа

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


const inventoryOpenLoader = async ({params}) => {
	
	const inventory_number = params.number_inv//после params писать название параметра которое прописали в файле AppRouter.jsx с урлками
	
	return {inventory: await getInventoryOpen(inventory_number), inventory_number}
}
//переменная в функции выше в которую присваиваем useLoaderData() должна называться точно также как и переменная, которую возвращаем тут orderNumberLoader, то есть тоже orders, именно так. И дпругих хуках наверно тоже также работает. Иначе не распарсит.






export { Inventory_open, inventoryOpenLoader }
