import './index.css'
import { useState, useEffect } from 'react'
import axios from "axios"
import Aside from './components/Aside/Aside'
import Header from './components/Header/Header'
// import GoodsView from './components/GoodsView'
import Button from './components/Button/Button'

import { BrowserRouter, HashRouter } from 'react-router-dom'
import { Routes, Route, Link, Navigate } from 'react-router-dom'

import Homepage from './pages/Homepage';
import GoodsInGroup from './pages/GoodsInGroup';
import GoodsAll from './pages/GoodsAll';


import Authorization from './regusers/Authorization';
import Registration from './regusers/Registration';
import Logout from './regusers/Logout';
import Forgot_password from './regusers/Forgot_password';
import Registration_verify from './regusers/Registration_verify';


import Basket_view from './components/Basket/Basket_view';
import Orders_view from './components/Orders/Orders_view';






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
    <BrowserRouter>
      
      {/*<Header />*/}
      
      <Routes>
        <Route path="/" element={<Homepage />}>

          <Route path="regusers/authorization/" element={<Authorization />} />
          <Route path="regusers/registration/" element={<Registration />} />
          <Route path="regusers/logout/" element={<Logout />} />
          <Route path="regusers/forgot_password/" element={<Forgot_password />} />
          <Route path="regusers/registration_verify/" element={<Registration_verify />} />

          <Route path="groups_all/" element={<GoodsAll />} />
          <Route path="groups/:slug" element={<GoodsInGroup />} />

          
          <Route path="basket/goods/" element={<Basket_view />} />

          <Route path="checkout_list/orders/" element={<Orders_view />} />

        

        </Route>


      </Routes>

      
      {/*<Aside groups={ groups }></Aside>*/}
      
      {/*<aside>
          <h3>Все группы</h3>
          <ul>
          { groups.map( (el) => {
            return (<Button key={ el.id } onClick={ () => {
              filterGoods(el.slug)              
            } }>{el.name_group}</Button>)
            }
            ) }
          </ul>    
      </aside>*/}
      
        

        {/*<h1>{gr}</h1> */}
        {/*<GoodsView className="goods" slug={ gr }></GoodsView>*/}
        
        {/*тут вывод товаров*/}
        {/*<ul>
        { goods?.map( (el) => {
          return (<li key={el.id}>{el.name_product}</li>)
        }
          ) }
        
        </ul>*/}
      

    </BrowserRouter>
  )
}

export default App


// filter_good(filter=el.name_group)
