import Button from './Button/Button'
import Modal from './Modal/Modal'
import { useState, useRef, useEffect, useCallback } from 'react'
import axios from "axios"
import useInput from "../hooks/useInput"


export default function EffectSection() {
	const input = useInput()

	const [modal, setModal] = useState(false)
	const [loading, setLoading] = useState(false)
	const [users, setUsers] = useState([])

	//вариант с axios. С колбэкеом не работает. Только с обычной функцией
	// const fetchUsers = useCallback(async () => {    
    //     setLoading(true)
    //     await axios.get('https://reqres.in/api/users?page=1').then((res) =>{
    //         setUsers(res.data.data) })
        
    //     setLoading(false)
    
	// }, [])

	//вариант с fetch
	// const fetchUsers = useCallback(async () => {    
    //     setLoading(true)
    //     const response = await fetch('https://jsonplaceholder.typicode.com/users')
    //     const data_users = await response.json()
    //     setUsers(data_users)
    //     setLoading(false)
    
	// }, [])

	//вариант с axios. Только с обычной функцией
	async function fetchUsers() {
		setLoading(true)
		axios.get('https://jsonplaceholder.typicode.com/users').then((res) =>{
			setUsers(res.data) })
		// const response = await fetch('https://jsonplaceholder.typicode.com/users')
		// const data_users = await response.json()
		// setUsers(data_users)
		setLoading(false)
	}

	useEffect(() => {
		fetchUsers()

	}, [fetchUsers])



	function openModal() {
		setModal(true)
	}

	return(
		<section>
			<h3>Effects</h3>


			<Button style={{ marginBottom: '1rem' }} onClick={openModal}>Открыть информацию</Button>

			
			<Modal open={modal}>
				<h3>Hello from modal</h3>
				<p>Lorem ipsum dolor, sit amet consectetur adipisicing, elit. Quasi magni quisquam saepe voluptatibus pariatur nostrum eaque sequi omnis molestias debitis, odio, eligendi sint, aliquam possimus veritatis minus vel repudiandae. Nobis!</p>
				<Button onClick={() => setModal(false)}>Закрыть модалку</Button>
			</Modal>

			{loading && <p>Загрузка</p>}

			{!loading && (
				<>
					<input type="text" className="control" {...input} />
					<h6>{input.value}</h6>
					<ul>
						{users.filter((el) =>
							el.name.toLowerCase().includes(input.value.toLowerCase())
							)
						.map((user) => (
							<li key={user.id}>{user.name}</li>
							))}
					</ul>
				</>
				)}



			{/*<p>{ users.map((user) => (<p key={user.id}>{user.first_name}</p>)) }</p>*/}
		</section>
		)
}