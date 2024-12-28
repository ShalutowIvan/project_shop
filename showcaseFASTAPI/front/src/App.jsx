import './index.css'
import { useState, useEffect } from 'react'
import axios from "axios"
import Aside from './components/Aside/Aside'
import Header from './components/Header/Header'
// import GoodsView from './components/GoodsView'
import Button from './components/Button/Button'


// import { BrowserRouter } from 'react-router-dom'




function App() { 
  const [gr, setGr] = useState("0")//это отфильтрованная группа
  // const [loading, setLoading] = useState(false)
  const [groups, setGroups] = useState([])

  const [goods, setGoods] = useState([])


  async function loadGroup() {
    // setLoading(true)
    axios.get('http://127.0.0.1:8000/api/groups_all/').then((res) => {
      setGroups(res.data) })
    // const response = await fetch('https://jsonplaceholder.typicode.com/users')
    // const data_users = await response.json()
    // setUsers(data_users)
    // setLoading(false)
  }


  async function filterGoods(slug) {
    // setLoading(true)
    setGr(slug) 
    await axios.get(`http://127.0.0.1:8000/api/goods_in_group/${ slug }`).then((res) =>{
      setGoods(res.data) })    
  }

  
  useEffect(() => {    
    loadGroup()      
    filterGoods(gr)//это срабатывает только 1 раз
  }, [])

 

  return (
    <>
      
      <Header />
      
      <h3>Все группы</h3>
      
      {/*<Aside groups={ groups }></Aside> */}
      <aside>
         
          <ul>
          { groups.map( (el) => {
            return (<Button key={ el.id } onClick={ () => {
              filterGoods(el.slug)              
            } }>{el.name_group}</Button>)
            }
            ) }
          </ul>       

        
      </aside>
      
      <main>
        

        {/*<h1>{gr}</h1> */}
        {/*<GoodsView className="goods" slug={ gr }></GoodsView>*/}
        
        {/*тут вывод товаров*/}
        <ul>
        { goods?.map( (el) => {
          return (<li key={el.id}>{el.name_product}</li>)
        }
          ) }
        
        </ul>
      

      </main> 

    </>
  )
}

export default App


// filter_good(filter=el.name_group)
