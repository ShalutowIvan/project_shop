import './Modal.css'
import { createPortal } from 'react-dom'
import { useEffect, useRef } from 'react'

// export default function Modal({ children, open }) {
// 	return(
// 		<dialog open={open}>
// 			{children}
// 		</dialog>
// 		)
// }


// export default function Modal({ children, ...props }) {
// 	return(
// 		<dialog {...props}>
// 			{children}
// 		</dialog>
// 		)
// }

//теперь после импорта портала вместо jsx 
export default function Modal({ children, open }) {
	const dialog = useRef()

	useEffect(() => {
		if (open) {
		dialog.current.showModal()
		} else {
		dialog.current.close()
		}
	}, [open])

	

	return createPortal(
		<dialog ref={dialog}>{children}</dialog>,
		document.getElementById('modal')
		)
}


 // open={open}
