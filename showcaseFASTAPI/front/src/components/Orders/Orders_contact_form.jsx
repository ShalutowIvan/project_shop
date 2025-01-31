import { useState, useRef } from 'react'
import { Link, Outlet, NavLink, Form } from 'react-router-dom'



//форма для оформления заказа
function Orders_contact_form({ submitting }) {
	

	return (
		
           <Form action="/basket/contacts" method='post'>
                <label>
                    ФИО:
                    <input type="text" name="fio" defaultValue="_" />
                </label>
                
                <label>
                    Телефон:
                    <input type="text" name="phone" defaultValue="_" />
                </label>

                <label>
                    Адрес доставки:
                    <input type="text" name="delivery_address" defaultValue="_" />
                </label>

                <label>
                    Способ оплаты:
                    <input type="text" name="pay" defaultValue="1" />
                </label>



                {/*<input type="hidden" name="userId" value="1" />*/}

                <input type="submit" value="Add post" disabled={submitting} />

            </Form> 
	
		)
}

export default Orders_contact_form

