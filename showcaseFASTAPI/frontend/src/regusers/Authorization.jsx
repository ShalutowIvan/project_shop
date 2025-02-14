import { useState, useRef } from 'react'
import { Link, Outlet, NavLink, useNavigate } from 'react-router-dom'
import axios from "axios";
import Cookies from "js-cookie";


export default function Authorization() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const validateForm = () => {
        if (!email || !password) {
            setError("не введены логин или пароль");
            return false;
        }
        setError('');
        return true;
    }


	// const [form, setForm] = useState({        
    //     email: "",
    //     password: "",        
    //     hasError: false,
    // })
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);

        try {            
            const response = await axios.post(
                "http://127.0.0.1:8000/api/regusers/auth",
                {                 
                email, 
                password,
                },
                { withCredentials: true }
                );
            setLoading(false);
        

        //это выводится
        // console.log("access: ", response.data["Authorization"]);
        // console.log("refresh: ", response.data["RT"]);

        // const cookies = response.headers["set-cookie"]; это не существует
            

            
            if (response.statusText==='OK') {
                // const data = await response.json()
                Cookies.set("Authorization", response.data["Authorization"], {
                expires: 0.1, // Кука истечет через 30 дней, тут указывается колво дней
                path: "/", // Кука будет доступна на всех страницах        
                sameSite: "lax", // Защита от CSRF-атак
                });
                Cookies.set("RT", response.data["RT"], {
                expires: 30, // Кука истечет через 30 дней, тут указывается колво дней
                path: "/", // Кука будет доступна на всех страницах        
                sameSite: "lax", // Защита от CSRF-атак
                });

            } else {
                const errorData = await response.data
                console.log(errorData, 'тут ошибка после ввода кредов')
                // setError(errorData.detail || 'аутентификация не прошла');
            }


        
        // const token = Cookies.get("theme");
        // console.log(document.cookie)

        // const cookies2 = response.headers;
        // console.log(token);
        // if (response.status === 200) {
        // console.log("Login successful!");
        // navigate("/profile"); // Перенаправление на страницу профиля
        // }

        } catch (error) {
            setLoading(false);
            setError('аутентификация не прошла, попробуйте еще раз');            
        }
    };

    // function TestCookie() {
    //     const token = Cookies.get("Authorization");
    //     console.log(token);
    // }

	return (
		<>
		<h1>Вход</h1>

		<form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
                

                <label htmlFor="id_email">Электронная почта: </label>
                <input 
                    placeholder="e-mail"
                    name="email"                    
                    type="email"
                    id="id_email"
                    className="control"                        
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}   
                />

                <br/><br/>

                <label htmlFor="id_password">Пароль: </label>
                <input 
                    placeholder="Введите пароль"
                    name="password"
                    type="password"
                    id="id_password"
                    className="control"                     
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}      
                />

                

                <br/><br/>

                <button type="submit" disabled={loading}>                    
                    {loading ? 'Входим в...' : 'Вход'}
                </button>
                <br/>

                {/*если ошибка error отображаем ее в параграфе ниже*/}
                {error && <p style={{ color: 'red'}}>{error}</p>}

            </form>

            <h2><NavLink to="/regusers/registration/">Регистрация</NavLink></h2>

            <h2><NavLink to="/regusers/forgot_password/">Забыли пароль</NavLink></h2>


            <h1>{email}</h1>
            <h1>{password}</h1>

            {/*<button onClick={TestCookie}>Тест куки</button>*/}

		</>
		)



}



// axios запрос возвращает объект