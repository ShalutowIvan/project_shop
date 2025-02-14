import { useAuth } from './useAuth'








export default function Logout() {
	const {signout} = useAuth()

	return (
		<>
		<h1>Кнопка выйти переехала в Homepage</h1>
		<button onClick={() => signout(() => navigate('/', {replace: true}))} >Выход</button>
		</>
		)



}




