import { Link, Outlet, NavLink, useLoaderData, useLocation } from 'react-router-dom'
// import CustomLink from './CustomLink'
import { useState, useEffect } from 'react'
// import { useAuth } from '../regusers/useAuth'

import Cookies from "js-cookie";
import axios from "axios";


// import { getRefreshToken, getAccessToken } from "../regusers/AuthService"
import { jwtDecode } from 'jwt-decode'

// import { useAuth } from "../regusers/AuthProvider"

// import { API } from "../apiAxios/apiAxios"



export default function Homepage() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
    
    // const {signout} = useAuth()
    // const [user, setUser] = useState("")
    // const { user, logout } = useAuth();
    // const {fio} = useLoaderData()

    // const location = useLocation();
    // const [fullName, setFullName] = useState(location.state?.fullName || '');


    
    // useEffect(() => {
    //     fetch(`http://127.0.0.1:8000/api/groups_all/`)
    //         .then(res => res.json())
    //         .then(data => setGroups(data));        
                
    // }, [])

    
    // else {

    // }

    // с useEffect срабатывает смена кнопок, но только при обновлении страницы, автоматом не срабатывает. Через лоадер пока не работает у меня. Как сделать лучше хз

	return (
		<>
		<header>
            <h2><NavLink to="/" className={setActive}>Home</NavLink></h2>

            <p>Разделы ></p>
            <h2><NavLink to="/orders/" className={setActive}>Заказы</NavLink></h2>
            <h2><NavLink to="/goods_all/" className={setActive}>Товары</NavLink></h2>
            <h2><NavLink to="/incoming_documents/" className={setActive}>Приходные документы</NavLink></h2>
            <h2><NavLink to="/expense_documents/" className={setActive}>Расходные документы</NavLink></h2>
            <h2><NavLink to="/inventory/" className={setActive}>Инвентаризация</NavLink></h2>
            <h2><NavLink to="/reports/" className={setActive}>Отчеты</NavLink></h2>
            


            <p>Информация о пользователе ></p>

            

        </header>

      <aside>
          
        <p>Что то тут будет</p>

          
      </aside>

      <main>
            
            <h1>Добро пожаловать!</h1>
            <h6>________________________________________</h6>
            

            <Outlet />
        

      </main>
      
      <footer className="footer">
        <h1>ТУТ ПОДВАЛ</h1>
      	2025 год

      </footer>

      </>
		)


}



export { Homepage }

