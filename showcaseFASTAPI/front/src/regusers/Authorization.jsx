import { useState, useRef } from 'react'
import { Link, Outlet, NavLink } from 'react-router-dom'




export default function Authorization() {
	const [form, setForm] = useState({        
        email: "",
        password: "",        
        hasError: false,
    })


	function handleNameChange(event) {
        
        setForm((prev) => ({
            ...prev,
            email: event.target.value,
            hasError: event.target.value.trim().length === 0,
        })

            )
    }




	return (
		<>
		<h1>Вход</h1>

		<form style={{ marginBottom: '1rem' }}>
                

                <label htmlFor="id_email">Электронная почта: </label>
                <input 
                	placeholder="e-mail"
                	name="email"                	
                    type="email"
                    id="id_email"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}         
                                
                />

                <br/><br/>

                <label htmlFor="id_password">Пароль: </label>
                <input 
                	placeholder="Введите пароль"
                	name="password"
                    type="password"
                    id="id_password"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}       
                                  
                />

                

                <br/><br/>

                <button type="submit" disabled={form.hasError} isActive={!form.hasError}>
                    Войти
                </button>

            </form>

            <h2><NavLink to="/regusers/registration/">Регистрация</NavLink></h2>

            <h2><NavLink to="/regusers/forgot_password/">Забыли пароль</NavLink></h2>




		</>
		)



}




