import { useState, useRef } from 'react'
import { Link, Outlet, NavLink } from 'react-router-dom'



//форма для оформления заказа
export default function Orders_contact_form() {
	const [form, setForm] = useState({        
        fio: "",
        phone: "",        
        delivery_address: "",
        pay: "",
    })



	return (
		<>
		<h1>Оформление заказа</h1>

		<form style={{ marginBottom: '1rem' }}>
                

                <label htmlFor="id_fio">ФИО: </label>
                <input 
                	placeholder="ФИО"
                	name="fio"                	
                    type="text"
                    id="id_fio"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}         
                                
                />

                <br/><br/>

                <label htmlFor="id_phone">Телефон: </label>
                <input 
                	placeholder="Введите номер телефона"
                	name="phone"
                    type="text"
                    id="id_phone"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}       
                                  
                />                

                <br/><br/>

                <label htmlFor="id_delivery_address">Адрес доставки: </label>
                <input 
                    placeholder="Адрес доставки"
                    name="delivery_address"
                    type="text"
                    id="id_delivery_address"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}                                  
                />

                <br/><br/>

                <label htmlFor="id_pay">Способ оплаты: </label>
                <input 
                    placeholder="1 если нал, 2 если безнал"
                    name="pay"
                    type="text"
                    id="id_pay"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}       
                                  
                />

                 <br/><br/>



                <button type="submit" disabled={form.hasError} isActive={!form.hasError}>
                    Оформить
                </button>

            </form>

            

		</>
		)

}