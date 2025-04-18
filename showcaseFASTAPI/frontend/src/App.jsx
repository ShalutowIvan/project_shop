// import './index.css'
import { useState, useEffect } from 'react'
// import axios from "axios"
// import Aside from './components/Aside/Aside'
// import Header from './components/Header/Header'
// import GoodsView from './components/GoodsView'
// import Button from './components/Button/Button'

import { BrowserRouter, HashRouter, RouterProvider } from 'react-router-dom'
// import { Routes, Route, Link, Navigate } from 'react-router-dom'

// import Homepage from './pages/Homepage';
// import GoodsInGroup from './pages/GoodsInGroup';
// import GoodsAll from './pages/GoodsAll';


// import Authorization from './regusers/Authorization';
// import Registration from './regusers/Registration';
// import Logout from './regusers/Logout';
// import Forgot_password from './regusers/Forgot_password';
// import Registration_verify from './regusers/Registration_verify';


// import Basket_view from './components/Basket/Basket_view';
// import Orders_view from './components/Orders/Orders_view';
// import Orders_contact from './components/Orders/Orders_contact'


import AppRouter from "./AppRouter"
import { AuthProvider } from "./regusers/AuthProvider";




import axios from "axios";
import Cookies from "js-cookie";

import { setAccessToken, setRefreshToken, getAccessToken, getRefreshToken } from "./regusers/AuthService"

//функция для обновления аксес токена
// const updateAccessTokenFromRefreshToken = async () => {
//   const refreshToken = Cookies.get("RT");
//   if (!refreshToken) {
//     throw new Error("No refresh token found");
//   }

//   // const response = await axios.post(`/api/regusers/auth/update_access_token/${refreshToken}`, {
//   //   refresh_token: refreshToken,
//   // });
//   const response = await axios.get(`/api/regusers/auth/update_access_token/${refreshToken}`);

//   // if (response.data.access_token) {
//   //   localStorage.setItem("access_token", response.data.access_token);
//   // }
//   console.log(response.data)
//   // return response.data;
// };




function App() { 
  

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
        
  //       const accessToken = Cookies.get("Authorization");
        
  //       if (!accessToken) {
  //         // Если access токена нет, пробуем обновить его с помощью refresh токена
  //         await updateAccessTokenFromRefreshToken();
  //       }
  //       // Здесь можно сделать запрос к защищенному эндпоинту
  //     } catch (error) {
  //       console.error("Error:", error);
  //     }
  //   };

  //   fetchData();
  // }, []);


  // это обновление токена с useEffect происходит только при обновлении страницы.
  // useEffect(() => {
  //       const fetchData = async () => {
  //           try {
  //               const refreshToken = getRefreshToken();
  //               const testAccessToken = getAccessToken();

  //               if (!testAccessToken) {
  //               // Если access токена нет, пробуем обновить его с помощью refresh токена
  //                   if (refreshToken){
  //                   const responseUpdate = await axios.get(`http://127.0.0.1:8000/api/regusers/auth/update_access_token/${refreshToken}`)

  //                   // Cookies.set("Authorization", responseUpdate.data["Authorization"], {
  //                   // expires: 0.0005, // Кука истечет через 30 дней, тут указывается колво дней
  //                   // path: "/", // Кука будет доступна на всех страницах        
  //                   // sameSite: "lax", // Защита от CSRF-атак
  //                   // });
  //                   setAccessToken(responseUpdate.data["Authorization"])
  //                   console.log("аксес токен истек, и обновлен")
  //                   }
  //                   else {
  //                     console.log("Залогиньтесь повторно, рефреш истек")
  //                   }
                    
  //               }
  //               else {
  //                 console.log("Аксес токен не истек")
  //               }
  //           // Здесь можно сделать запрос к защищенному эндпоинту
  //           } catch (error) {
  //           console.error("Error:", error);
  //           }
  //           };

  //       fetchData();
  //   }, [])




  return (

    // <AuthProvider>

        <RouterProvider router={AppRouter} />

    // </AuthProvider>
    
  )
}

export default App


// filter_good(filter=el.name_group)
