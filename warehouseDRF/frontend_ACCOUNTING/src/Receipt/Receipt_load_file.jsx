import { useParams, Link, useNavigate, useLoaderData, Await, useAsyncValue, NavLink } from 'react-router-dom'
import { React, Suspense, useState, useEffect } from 'react';
import Cookies from "js-cookie";
// import { API } from "../../apiAxios/apiAxios"
import axios from "axios"


function Receipt_load_file() {
    //поля формы    
    const [load_file, setLoad_file] = useState(null);   
    const {number_doc} = useParams();
    
    //тут состояния ошибки и загрузки
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [responseData, setResponseData] = useState(null);
    
    // const { login } = useAuth();

    const validateForm = () => {
        if (!load_file) {
            setError("Есть пустые поля, заполните, пожалуйста!");
            return false;
        }
        setError('');
        return true;
    }

    const navigate = useNavigate();

    const goBack = () => {
        return navigate(-1);
    }
   
	

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);
        const formData = new FormData();
        formData.append('load_file', load_file);

        try {            
            const response = await axios.post(
                `http://127.0.0.1:9999/api/receipt_goods/load_file/${number_doc}/`,
                formData,
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
                navigate(`/incoming_documents/${number_doc}`);

            } else {
                const errorData = await response.data
                console.log(errorData, 'тут ошибка')
                // setError(errorData.detail || 'аутентификация не прошла');
            }        

        } catch (error) {
            setLoading(false);
            console.log(error)
            setError('что-то пошло не так');            
        }    
    };

    const load_template = async () => {
        setLoading(true);

        try {
            const response = await axios.get(
                'http://127.0.0.1:9999/api/receipt_goods/url_from_load_template_receipt/', 
                {
                    responseType: 'blob', // важно для скачивания файлов
                }
            );
            
            // Создаем URL для blob
            const url = window.URL.createObjectURL(new Blob([response.data]));
            
            // Создаем ссылку и эмулируем клик
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'receipt_template.xlsx');
            document.body.appendChild(link);
            link.click();
            
            // Убираем ссылку после скачивания
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);
            
        } catch (err) {
            setError('Ошибка при скачивании файла');
            console.error('Download error:', err);
        } finally {
            setLoading(false);
        }
    };
    
	return (
		<>
        
		<h1>Загрузка файла накладной</h1>
        <button onClick={goBack}>Назад</button>
        <p>______________________________________</p>
        <p>Шаблон для загрузки файла с накладной.</p>
        <button onClick={load_template} disabled={loading}>Скачать шаблон</button>
        <p>______________________________________</p>

        <h3>Загрузка файла накладной</h3>
		<form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>                

                <label htmlFor="id_load_file">Выберите файл накладной: </label>
                <input 
                    placeholder="загрузите файл накладной"
                    // name="load_file"
                    type="file"
                    id="id_load_file"
                    className="control"                        
                    // value={photo}
                    accept=".xlsx,.xls"
                    onChange={(e) => setLoad_file(e.target.files[0])}   
                />

                <br/><br/>

                <button type="submit" disabled={loading}>                    
                    {loading ? 'Сохраняем...' : 'Загрузить'}
                </button>
                <br/>

                {/*если ошибка error отображаем ее в параграфе ниже*/}
                {error && <p style={{ color: 'red'}}>{error}</p>}

            </form>

        </>
		)
}


export { Receipt_load_file }
