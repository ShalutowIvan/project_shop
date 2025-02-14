import { useState, useRef } from 'react'
import { Link, Outlet, NavLink, Form } from 'react-router-dom'



//форма для оформления заказа
function Orders_contact_form({ submitting }) {
	

	return (
		
           <Form action="/basket/create" method='post'>
                <label>
                    ФИО:
                    <input type="text" name="fio" defaultValue="_" />
                </label>
                
                <br/>

                <label>
                    Телефон:
                    <input type="text" name="phone" defaultValue="_" />
                </label>

                <br/>

                <label>
                    Адрес доставки:
                    <input type="text" name="delivery_address" defaultValue="_" />
                </label>

                <br/>

                <label>
                    Способ оплаты:
                    <input type="text" name="pay" defaultValue="1" />
                </label>

                <br/><br/>

                {/*<input type="hidden" name="userId" value="1" />*/}

                <input type="submit" value="Оформить заказ" disabled={submitting} />

            </Form> 
	
		)
}

export default Orders_contact_form

