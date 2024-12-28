import { useState, useRef, useEffect, useCallback } from 'react'
import axios from "axios"
import '../index.css'



// export default function GoodsView({ slug }) {
// 	// const [loading, setLoading] = useState(false)
// 	// const [goods, setGoods] = useState([])


// 	// async function loadGoods() {
// 	// 	// setLoading(true)
// 	// 	axios.get(`http://127.0.0.1:8000/api/goods_in_group/${ slug }`).then((res) =>{
// 	// 		setGoods(res.data) })
// 	// 	// const response = await fetch('https://jsonplaceholder.typicode.com/users')
// 	// 	// const data_users = await response.json()
// 	// 	// setUsers(data_users)
// 	// 	// setLoading(false)
// 	// }

// 	// useEffect(() => {
// 	// 	loadGoods()

// 	// }, [])
// 	//когда пишу зависимость то есть функцию loadGroup в квадратных скобках запросы идут на сервер постоянно. Если не писать зависимость, то запросы постоянно не идут. хз почему





// 	return (


// 					<>
// 						{goods.map((el) => (
// 						<li key={el.id}>
// 						{el.name_product}
// 						</li>
// 						))}
// 					</>
		

// 		)
// }











