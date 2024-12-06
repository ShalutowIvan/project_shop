// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
import React, { useState, useEffect } from "react"
import axios from "axios"




const baseUrl = 'http://127.0.0.1:8000/checkout_list/orders/all/'

// axios.get(baseUrl).then((res) =>{
//       // console.log(res.data.data)//взяли пользаков из api, теперь выведем их на экран. Теперь нужно поменять название ключей, так как в апи другие названия ключей идут, и не совпадают с нашими
//       this.setState({ users: res.data.data })
//     })

function App() {
  

  return (
    <div>
      const synchro = () => {
        axios.get('http://127.0.0.1:8000/checkout_list/orders/all/').then((resp) => {
          console.log(resp.data)
        })
      }
      

    </div>
  )
}

// проблема с cors в проекте fastapi.....
// кажется vite не нужен

export default App
