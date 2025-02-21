import { Link, Outlet, NavLink } from 'react-router-dom'
// import CustomLink from './CustomLink'
import { useState, useEffect } from 'react'
import { useAuth } from '../regusers/useAuth'

import Cookies from "js-cookie";


import axios from "axios";




//функция для обновления аксес токена
// const updateAccessTokenFromRefreshToken = async () => {
//   const refreshToken = Cookies.get("RT");
//   if (!refreshToken) {
//     throw new Error("No refresh token found");
//   }
  
//   const response = await fetch(`/api/regusers/auth/update_access_token/${refreshToken}`);

//   return response.json()
// };






export default function Homepage() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
    const [groups, setGroups] = useState([]);
    const {signout} = useAuth()

    async function TestCookie() {
        const token = localStorage.getItem("Authorization"); 
        const verifyAccess = await axios.get(`http://127.0.0.1:8000/api/regusers/auth/verify_access_token/${token}`)
        const res = verifyAccess.data
        console.log(res);
        // console.log(token);
    }

    // const updateAccessTokenFromRefreshToken = async () => {
    //   const refreshToken = Cookies.get("RT");
    // if (!refreshToken) {
    //     throw new Error("No refresh token found");
    // }
  
    // // const response = fetch(`http://127.0.0.1:8000/api/regusers/auth/update_access_token/${refreshToken}`);

    // const response = await axios.post(`http://127.0.0.1:8000/api/regusers/auth/update_access_token/${refreshToken}`)

    // // const res = response.json()
    // console.log(response.data.Authorization)
    // // return response.json()
    // };




    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/groups_all/`)
            .then(res => res.json())
            .then(data => setGroups(data));


                    

    }, [])




	return (
		<>
		<header>
            <h2><NavLink to="/" className={setActive}>Home</NavLink></h2>

            <p>Ссылки реги ></p>
            <h2><NavLink to="/regusers/authorization/" className={setActive}>Войти</NavLink></h2>
            <h2><NavLink to="/regusers/registration/" className={setActive}>Регистрация</NavLink></h2>
            {/*<h2><NavLink to="/regusers/logout/" className={setActive}>Выйти</NavLink></h2>*/}
            
            <h2><NavLink to="/regusers/registration_verify/" className={setActive}>Завершение регистрации</NavLink></h2>

            <p>Заказ товаров ></p>
            <h2><NavLink to="/checkout_list/orders/" className={setActive}>Мои покупки</NavLink></h2>
            <h2><NavLink to="/basket/goods/" className={setActive}>Корзина</NavLink></h2>
            
            <button onClick={() => signout(() => navigate('/', {replace: true}))}>Выход</button>

        </header>

      <aside>
          
          <h3><NavLink to="/groups_all/" className={setActive}>Все группы</NavLink></h3>

            {
                groups.map(group => (
                        <NavLink key={group.id} to={`/groups/${group.slug}`} className={setActive}>
                            <li>{group.name_group}</li>
                        </NavLink>
                    ))
            }
      </aside>

      <main>

            <button onClick={TestCookie}>Тест куки</button>
            <br/>
            {/*<button onClick={updateAccessTokenFromRefreshToken}>Тест обновления куки</button>*/}

        <Outlet />

      </main>
      
      <footer className="footer">
        <h1>ТУТ ПОДВАЛ</h1>
      	2025 год

      </footer>

      </>
		)


}










