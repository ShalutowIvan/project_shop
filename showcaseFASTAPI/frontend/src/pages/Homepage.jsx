import { Link, Outlet, NavLink, useLoaderData, useLocation } from 'react-router-dom'
// import CustomLink from './CustomLink'
import { useState, useEffect } from 'react'
// import { useAuth } from '../regusers/useAuth'

import Cookies from "js-cookie";
import axios from "axios";


import { getRefreshToken, getAccessToken } from "../regusers/AuthService"
import { jwtDecode } from 'jwt-decode'

import { useAuth } from "../regusers/AuthProvider"

import { API } from "../apiAxios/apiAxios"



export default function Homepage() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
    const [groups, setGroups] = useState([]);
    // const {signout} = useAuth()
    // const [user, setUser] = useState("")
    const { user, logout } = useAuth();
    // const {fio} = useLoaderData()

    // const location = useLocation();
    // const [fullName, setFullName] = useState(location.state?.fullName || '');


    // if (fio) {
    //     setUser(fio.user_name)
    // }

    // async function TestCookie() {
    //     const token = Cookies.get("Authorization")
    //     const verifyAccess = await axios.get(`http://127.0.0.1:8000/api/regusers/auth/verify_access_token/${token}`)
    //     const res = verifyAccess.data
    //     console.log(res);
    //     // console.log(token);
    // }


    // async function TestRout() {
    //     const test = await axios.get("http://127.0.0.1:8000/api/regusers/protected")
    //     console.log(test.data);
    // }



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
    

    
    const removeCookie = () => {
        Cookies.remove("RT");
        Cookies.remove("Authorization");
        logout()
        console.log("All Cookie has been removed!");
    }


        


    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/groups_all/`)
            .then(res => res.json())
            .then(data => setGroups(data));        
        // const token = getAccessToken()
        // if (token) {
        //     const fio = jwtDecode(token)
        //     // console.log(fio.user_name)
        //     setUser(fio.user_name)
        // } 

        // if (!fullName) {
        //     const token = getAccessToken();
        //     if (token){
        //     const decoded = jwtDecode(token);
        //     setFullName(decoded.user_name);}
        // }
        
        
    }, [])

    
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
            

            { !user && 
            <>
            <h3>Не авторизован</h3>
            <h2><NavLink to="/regusers/authorization/" className={setActive}>Войти</NavLink></h2> 
            </>
            }

            { user && 
            <><h1>{user.fullName}</h1>
            <br/>
            <button onClick={removeCookie}>ВЫХОД</button></>
            }
            
            {/*<button onClick={() => signout(() => navigate('/', {replace: true}))}>Выход</button>*/}

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
            
            { !user && <h2>Для заказа товаров нужно зарегистрироваться. Перейдите на вкладку "Войти".</h2> }

            { user && 
            <>
            <h1>Добро пожаловать!</h1>
            <h6>________________________________________</h6>
            </>
            }
            

            <Outlet />
        

      </main>
      
      <footer className="footer">
        <h1>ТУТ ПОДВАЛ</h1>
      	2025 год

      </footer>

      </>
		)


}



// const homeLoader = async () => {     
//     const token = getAccessToken()
//     let token_decode = ""
//     if (token) {
//         token_decode = jwtDecode(token)
//         // token_decode = token_decode.user_name
//         // console.log(fio.user_name)
//         // setUser(token_decode.user_name)
//     } 


//     return { fio: token_decode }
// }




export { Homepage }

