import { useState, useRef } from 'react'








export default function Registration() {
	const [form, setForm] = useState({
        name: "",
        email: "",
        password1: "",
        password2: "",
        hasError: false,
    })


	function handleNameChange(event) {
        
        setForm((prev) => ({
            ...prev,
            name: event.target.value,
            hasError: event.target.value.trim().length === 0,
        })

            )
    }


	return (
		<>
		<h1>Регистрация</h1>

		<form style={{ marginBottom: '1rem' }}>
                <label htmlFor="id_name">Ваше имя: </label>
                <input 
                	placeholder="введите ФИО"
                	name="name"
                    type="text"
                    id="id_name"
                    className="control"
                    value={form.name}
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}   
                    onChange={ handleNameChange }                  
                />

                <br/>

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

                <br/>

                <label htmlFor="id_password1">Пароль: </label>
                <input 
                	placeholder="Придумайте пароль"
                	name="password1"
                    type="password"
                    id="id_password1"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}       
                                  
                />

                <br/>

                <label htmlFor="id_password2">Повторите пароль: </label>
                <input 
                	placeholder="Повторите пароль"
                	name="password2"
                    type="password"
                    id="id_password2"
                    className="control"
                    
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}            
                            
                />

                <br/><br/>

                <button type="submit" disabled={form.hasError} isActive={!form.hasError}>
                    Зарегистрироваться
                </button>

            </form>

		</>
		)

}

// у меня пока что проверка на пустое поле работает только на поле имени name остальные поля не валидируются. Пока так оставил.


