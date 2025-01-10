import { useState, useRef } from 'react'









export default function Forgot_password() {
	const [form, setForm] = useState({        
        email: "",        
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
		<h1>Введите почту для восстановления пароля</h1>

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
                

                <button type="submit" disabled={form.hasError} isActive={!form.hasError}>
                    Восстановить пароль
                </button>

            </form>






		</>
		)



}




