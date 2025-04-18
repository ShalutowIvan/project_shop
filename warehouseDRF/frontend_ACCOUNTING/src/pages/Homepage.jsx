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
    const [groups, setGroups] = useState([]);
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

            <p>Заказ товаров ></p>
            <h2><NavLink to="/checkout_list/orders/" className={setActive}>Мои покупки</NavLink></h2>
            <h2><NavLink to="/basket/goods/" className={setActive}>Корзина</NavLink></h2>
            


            <p>Информация о пользователе ></p>
            

        </header>

      <aside>
          
          <h3><NavLink to="/groups_all/" className={setActive}>Все группы</NavLink></h3>

            {
                groups?.map(group => (
                        <NavLink key={group.id} to={`/groups/${group.slug}`} className={setActive}>
                            <li>{group.name_group}</li>
                        </NavLink>
                    ))
            }
      </aside>

      <main>
            
            
            

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

