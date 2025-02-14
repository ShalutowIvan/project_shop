import { Link, Outlet, NavLink } from 'react-router-dom'
// import CustomLink from './CustomLink'
import { useState, useEffect } from 'react'
import { useAuth } from '../regusers/useAuth'
import Cookies from "js-cookie";


export default function Homepage() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
    const [groups, setGroups] = useState([]);
    const {signout} = useAuth()

    function TestCookie() {
        const token = Cookies.get("Authorization");
        console.log(token);
    }


    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/groups_all/`)
            .then(res => res.json())
            .then(data => setGroups(data))

        console.log("TEST!!!!!!!!!!!")

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

        <Outlet />

      </main>
      
      <footer className="footer">
        <h1>ТУТ ПОДВАЛ</h1>
      	2025 год

      </footer>

      </>
		)


}










