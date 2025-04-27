import { useState, useRef, useEffect } from 'react'
import { Link, Outlet, NavLink, useNavigate, redirect } from 'react-router-dom'
import axios from "axios";
import Cookies from "js-cookie";
// import { API } from "../apiAxios/apiAxios"
// import { setAccessToken, setRefreshToken } from "./AuthService"
import { jwtDecode } from 'jwt-decode'
import GroupsAll from "./Groups"
// import { useAuth } from './AuthProvider'



export default function GoodsAdd() {
    //поля формы
    const [name_product, setName_product] = useState("_");
    const [vendor_code, setVendor_code] = useState("_");
    const [price, setPrice] = useState(0.0);
    const [stock, setStock] = useState(0);
    const [photo, setPhoto] = useState(null);
    const [group, setGroup] = useState("");

    const [groupss, setGroupss] = useState([]);

    


    //тут состояния ошибки и загрузки
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    
    
    // const { login } = useAuth();

    useEffect(() => {
            fetch(`http://127.0.0.1:9999/api/get_group/`)
                .then(res => res.json())
                .then(data => setGroupss(data));        
        }, [])


    const validateForm = () => {
        if (!name_product || !vendor_code || !price || !stock) {
            setError("Есть пустые поля, заполните, пожалуйста!");
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
                "http://127.0.0.1:9999/api/тут исправить на верную ссылку/",
                {                 
                    name_product,
                    vendor_code,
                    price,
                    stock,
                    photo,
                    group,
                },
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',  // важно для загрузки файлов
                    },
                }
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
    
    };

    
	return (
		<>

        <GroupsAll />
        
		<h1>Создание товара</h1>

		<form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
                

                <label htmlFor="id_name_product">Название товара: </label>
                <input 
                    placeholder="введите название товара"
                    name="name_product"                    
                    type="text"
                    id="id_name_product"
                    className="control"                        
                    value={name_product}
                    onChange={(e) => setName_product(e.target.value)}   
                />

                <br/><br/>

                <label htmlFor="id_vendor_code">Артикул: </label>
                <input 
                    placeholder="введите артикул"
                    name="vendor_code"                    
                    type="text"
                    id="id_vendor_code"
                    className="control"                        
                    value={vendor_code}
                    onChange={(e) => setVendor_code(e.target.value)}   
                />

                <br/><br/>

                <label htmlFor="id_price">Цена: </label>
                <input 
                    placeholder="введите цену"
                    name="price"                                        
                    type="number"
                    
                    id="id_price"
                    className="control"                        
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}   
                />

                <br/><br/>

                <label htmlFor="id_stock">Остаток: </label>
                <input 
                    placeholder="введите остаток"
                    name="stock"
                    type="number"
                    id="id_stock"
                    className="control"                        
                    value={stock}
                    onChange={(e) => setStock(e.target.value)}   
                />

                <br/><br/>

                <label htmlFor="id_photo">Фото: </label>
                <input 
                    placeholder="загрузите фото товара"
                    name="photo"
                    type="file"
                    id="id_photo"
                    className="control"                        
                    // value={photo}
                    accept="image/*"
                    onChange={(e) => setPhoto(e.target.files[0])}   
                />

                <br/><br/>

                <label htmlFor="id_group">Группа: </label>                
                <select
                    name="group"
                    id="id_group"
                    // className="control"                        
                    value={group}
                    onChange={(e) => setGroup(e.target.value)}   
                    // required
                >
                    <option value="">Выберите группу</option>
                    {groupss?.map(group => (
                        <option key={group.id} value={group.id}>
                            {group.name_group}
                        </option>
                    ))}
                </select>

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