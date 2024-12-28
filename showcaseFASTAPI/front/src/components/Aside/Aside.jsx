import { useState, useRef, useEffect, useCallback } from 'react'
import axios from "axios"


export default function Aside({ groups, filter_good }) {
	
	
	//когда пишу зависимость то есть функцию loadGroup в квадратных скобках запросы идут на сервер постоянно. Если не писать зависимость, то запросы постоянно не идут. хз почему





	return (
		<aside>
			
				<>
					<ul>
						
						
						<button>{ groups }</button>
						
						
					</ul>

				</>
				
		


		</aside>

		)


}


