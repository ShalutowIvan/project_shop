import { Route, Navigate, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
// import Aside from './components/Aside/Aside'
// import Header from './components/Header/Header'
import { Homepage } from './pages/Homepage';
// import GoodsInGroup from './pages/GoodsInGroup';
import GoodsAll from './pages/GoodsAll';

// import Authorization from './regusers/Authorization';
// import Registration from './regusers/Registration';
// import Registration_verify from './regusers/Registration_verify';

// import Forgot_password from './regusers/Forgot_password';
// import Forgot_password_verify from './regusers/Forgot_password_verify';
// import Logout from './regusers/Logout';


// import { Basket_view, basketLoader } from './components/Basket/Basket_view';
// import { Orders_view, orderNumberLoader } from './components/Orders/Orders_view';
// import { OrderOpen, orderOpenLoader } from './components/Orders/OrderOpen';

// import { OrderCreate, createOrderAction} from './components/Orders/OrderCreate'

//авторизация
// import { Loginpage } from "./regusers/Loginpage";
// import { RequireAuth } from "./regusers/RequireAuth";
// import { Profile } from "./regusers/Profile";

// import { AuthProvider } from "./regusers/AuthProvider"
// import { Private } from "./regusers/Private";
// import { AuthProvider } from "./regusers/AuthProvider";



{/*<AuthProvider>*/}


const AppRouter = createBrowserRouter(createRoutesFromElements(
       
	<Route path="/" element={
        
              <Homepage /> 
        
         } >

          <Route path="groups_all/" element={
              // <Private>
                     <GoodsAll />
              // </Private>
              }              
               />
          
          {/*<Route path="groups/:slug" element={<GoodsInGroup />} />*/}

          
          {/*<Route path="basket/goods/" element={
            
                <Basket_view />
            
            } loader={basketLoader} />*/}
          
          {/*<Route path="basket/create/" element={<OrderCreate />} action={createOrderAction} />*/}
          
          {/*<Route path="checkout_list/orders/" element={<Orders_view />} loader={orderNumberLoader} />
          <Route path="checkout_list/orders/:id" element={<OrderOpen />} loader={orderOpenLoader} />*/}

          {/*<Route path="profile" element={<Profile />} />*/}
        

        </Route>

        


	))



export default AppRouter    
     
        
