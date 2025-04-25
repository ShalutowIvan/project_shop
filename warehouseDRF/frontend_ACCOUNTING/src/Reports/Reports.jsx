import { Link, Outlet, NavLink, useLoaderData, useLocation } from 'react-router-dom'
// import CustomLink from './CustomLink'
import { useState, useEffect } from 'react'
// import { useAuth } from '../regusers/useAuth'

import Cookies from "js-cookie";
import axios from "axios";


// import { getRefreshToken, getAccessToken } from "../regusers/AuthService"
import { jwtDecode } from 'jwt-decode'

// import { useAuth } from "../regusers/AuthProvider"

// import { API } from "../apiAxios/apiAxios"



export default function Reports() {
	const setActive = ({isActive}) => isActive ? 'active-link' : '';
    
      
	return (
		<>
		        <h1>Отчеты</h1>
            
            <h2><NavLink to="/reports/income_report/" className={setActive}>Отчеты по приходу</NavLink></h2>
            <h2><NavLink to="/reports/expense_report/" className={setActive}>Отчет по расходу</NavLink></h2>
            <h2><NavLink to="/reports/sales_report/" className={setActive}>Отчет по проданным товарам по дате</NavLink></h2>
            <h2><NavLink to="/reports/sales_report_summary/" className={setActive}>Отчет по количеству продаж за период</NavLink></h2>
            
      </>
		)


}



export { Reports }

