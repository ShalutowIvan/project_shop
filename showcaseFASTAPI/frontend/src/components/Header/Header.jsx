import { useState, useEffect } from 'react'
// import eagle from '../../img/eagle.jpg'
import './Header.css'
// import { styled } from 'styled-components'


// const Header_style = styled.header`
//   height: 150px;
//   display: flex;
//   padding: 0 2rem;
//   justify-content: space-between;
//   align-items: center;
//   border-bottom: 1px solid #ccc;
// `



export default function Header() {
  
  const [time_now, setTime_now] = useState(new Date())  
  // const time_now = new Date()
  // console.log("Привет")

  // useEffect(() => {
  //   const interval = setInterval(() => setTime_now(new Date(), 1000))
  //   return () => {
  //     clearInterval()
  //     console.log('чистка интервала сработала')
  //   }    
  // }, [])

  // setInterval(() => setTime_now(new Date(), 1000))
  


    return(
      <header>
        <h1>ТУТ ХЕДЕР</h1>
        {/*<img src={eagle} alt={"eagle"} />*/}
        
        
        <span>Время сейчас { time_now.toLocaleTimeString() }</span>
      </header>
    )
}






