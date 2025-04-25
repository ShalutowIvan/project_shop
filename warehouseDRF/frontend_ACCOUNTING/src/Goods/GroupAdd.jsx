import { useState, useRef } from 'react'
import { Link, Outlet, NavLink, useNavigate, redirect } from 'react-router-dom'
import axios from "axios";
import Cookies from "js-cookie";
// import { API } from "../apiAxios/apiAxios"
// import { setAccessToken, setRefreshToken } from "./AuthService"
import { jwtDecode } from 'jwt-decode'
import GroupsAll from "./Groups"
// import { useAuth } from './AuthProvider'



export default function GroupAdd() {
    //поля формы
    const [name_group, setName_group] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    
    
    // const { login } = useAuth();


    const validateForm = () => {
        if (!name_group) {
            setError("Не введено название группы");
            return false;
        }
        setError('');
        return true;
    }

    const navigate = useNavigate();

    // const goHome = () => navigate("/");
	

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);

        try {            
            const response = await axios.post(
                "http://127.0.0.1:9999/api/add_group/",
                {                 
                name_group,                
                },
                    // { withCredentials: true }
                );
            setLoading(false);
            
            if (response.statusText==='OK') {            
                
                //если все ок, то переходим в список товаров                
                navigate("/goods_all/");

            } else {
                const errorData = await response.data
                console.log(errorData, 'тут ошибка после ввода кредов')
                // setError(errorData.detail || 'аутентификация не прошла');
            }
    
        

        } catch (error) {
            setLoading(false);
            console.log(error)
            setError('что-то пошло не так');            
        }

    
    // return redirect('/')

    };

    

	return (
		<>

        <GroupsAll />
        
		<h1>Создание группы</h1>

		<form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
                

                <label htmlFor="id_name_group">Название группы: </label>
                <input 
                    placeholder="введите название группы"
                    name="name_group"                    
                    type="text"
                    id="id_name_group"
                    className="control"                        
                    value={name_group}
                    onChange={(e) => setName_group(e.target.value)}   
                />

                <br/><br/>                

                <button type="submit" disabled={loading}>                    
                    {loading ? 'Сохраняем...' : 'Добавить'}
                </button>
                <br/>

                {/*если ошибка error отображаем ее в параграфе ниже*/}
                {error && <p style={{ color: 'red'}}>{error}</p>}

            </form>

        </>
		)



}



// axios запрос возвращает объект