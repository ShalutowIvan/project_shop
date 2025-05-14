import { useState, useRef } from 'react'
import { Link, Outlet, NavLink, useNavigate, redirect } from 'react-router-dom'
import axios from "axios";
import Cookies from "js-cookie";
// import { API } from "../apiAxios/apiAxios"
// import { setAccessToken, setRefreshToken } from "./AuthService"
import { jwtDecode } from 'jwt-decode'

// import { useAuth } from './AuthProvider'



function Inventory_create() {    
    //поля формы
    const [comment, setComment] = useState("");
    //состояния ошибки и загрузки
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    
    // const { login } = useAuth();

    const validateForm = () => {
        if (!comment) {
            setError("Не введен комментарий");
            return false;
        }
        setError('');
        return true;
    }

    const navigate = useNavigate();
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);

        try {            
            const response = await axios.post(
                "http://127.0.0.1:9999/api/inventory_list_create/",
                {                 
                comment,                
                },
                    // { withCredentials: true }
                );
            setLoading(false);
            
            if (response.statusText==='OK') {
                //если все ок, то переходим в список доков
                navigate("/inventory/");
            } else {
                const errorData = await response.data
                console.log(errorData, 'тут ошибка при создании')
                // setError(errorData.detail || 'аутентификация не прошла');
            }
        } catch (error) {
            setLoading(false);
            console.log(error)
            setError('что-то пошло не так');            
        }    
    };   

	return (
		<>        
		<h1>Создание документа инвентаризации</h1>

		<form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>                

                <label htmlFor="id_comment">Комментарий: </label>
                <input 
                    placeholder="введите комментарий"
                    name="comment"                    
                    type="text"
                    id="id_comment"
                    className="control"                        
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}   
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


export {Inventory_create}