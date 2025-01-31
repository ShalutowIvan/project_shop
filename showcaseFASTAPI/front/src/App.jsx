// import './index.css'
// import { useState, useEffect } from 'react'
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


function App() { 
  // const [gr, setGr] = useState("0")//это отфильтрованная группа
  // const [loading, setLoading] = useState(false)
  // const [groups, setGroups] = useState([])

  // const [goods, setGoods] = useState([])


  // async function loadGroup() {
  //   // setLoading(true)
  //   axios.get('http://127.0.0.1:8000/api/groups_all/').then((res) => {
  //     setGroups(res.data) })
  //   // const response = await fetch('https://jsonplaceholder.typicode.com/users')
  //   // const data_users = await response.json()
  //   // setUsers(data_users)
  //   // setLoading(false)
  // }


  // async function filterGoods(slug) {
  //   // setLoading(true)
  //   setGr(slug) 
  //   await axios.get(`http://127.0.0.1:8000/api/goods_in_group/${ slug }`).then((res) =>{
  //     setGoods(res.data) })    
  // }

  
  // useEffect(() => {    
  //   loadGroup()      
  //   filterGoods(gr)//это срабатывает только 1 раз
  // }, [])

 

  return (


    <RouterProvider router={AppRouter} />


    
  )
}

export default App


// filter_good(filter=el.name_group)
