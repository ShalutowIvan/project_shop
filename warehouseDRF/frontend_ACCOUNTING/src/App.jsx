// import { useState } from 'react'
import AppRouter from "./AppRouter"
// import { AuthProvider } from "./regusers/AuthProvider";
import { BrowserRouter, HashRouter, RouterProvider } from 'react-router-dom'
// import './index.css'



function App() {
  

  return (
    <>
      <RouterProvider router={AppRouter} />
    </>
  )
}

export default App
