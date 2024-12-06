import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import * as ReactDOMClient from 'react-dom/client'
// import './css/main.css'


createRoot(document.getElementById('root')).render(
  
    <App />
  
)

// const app = ReactDOMClient.createRoot(document.getElementById("app"))

// app.render(<App />)


// <StrictMode>
// </StrictMode>,