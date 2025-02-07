import { Route, Navigate, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
import Aside from './components/Aside/Aside'
import Header from './components/Header/Header'
import Homepage from './pages/Homepage';
import GoodsInGroup from './pages/GoodsInGroup';
import GoodsAll from './pages/GoodsAll';

import Authorization from './regusers/Authorization';
import Registration from './regusers/Registration';
import Logout from './regusers/Logout';
import Forgot_password from './regusers/Forgot_password';
import Registration_verify from './regusers/Registration_verify';

import Basket_view from './components/Basket/Basket_view';
import { Orders_view, orderNumberLoader } from './components/Orders/Orders_view';
import { OrderOpen, orderOpenLoader } from './components/Orders/OrderOpen';

import { OrderCreate, createOrderAction} from './components/Orders/OrderCreate'

//авторизация
import { Loginpage } from "./regusers/Loginpage";
import { RequireAuth } from "./regusers/RequireAuth";



const AppRouter = createBrowserRouter(createRoutesFromElements(

	<Route path="/" element={<Homepage />}>

          <Route path="regusers/authorization/" element={<Authorization />} />
          <Route path="regusers/registration/" element={<Registration />} />
          <Route path="regusers/logout/" element={<Logout />} />
          <Route path="regusers/forgot_password/" element={<Forgot_password />} />
          <Route path="regusers/registration_verify/:token"
                 element={<Registration_verify />}
                 
           />

          <Route path="login" element={<Loginpage />} />


          <Route path="groups_all/" element={<GoodsAll />} />
          <Route path="groups/:slug" element={<GoodsInGroup />} />

          
          <Route path="basket/goods/" element={
            <RequireAuth>
                <Basket_view />
            </RequireAuth>
            } />
          
          <Route path="basket/create/" element={
            <RequireAuth>
                <OrderCreate />
            </RequireAuth>
            } 
          action={createOrderAction} />
          
          <Route path="checkout_list/orders/" element={<Orders_view />} loader={orderNumberLoader} />
          <Route path="checkout_list/orders/:id" element={<OrderOpen />} loader={orderOpenLoader} />


        

        </Route>




	))



export default AppRouter    
     
        



// {/*<Aside groups={ groups }></Aside>*/}
      
//       {/*<aside>
//           <h3>Все группы</h3>
//           <ul>
//           { groups.map( (el) => {
//             return (<Button key={ el.id } onClick={ () => {
//               filterGoods(el.slug)              
//             } }>{el.name_group}</Button>)
//             }
//             ) }
//           </ul>    
//       </aside>*/}
      
        

//         {/*<h1>{gr}</h1> */}
//         {/*<GoodsView className="goods" slug={ gr }></GoodsView>*/}
        
//         {/*тут вывод товаров*/}
//         {/*<ul>
//         { goods?.map( (el) => {
//           return (<li key={el.id}>{el.name_product}</li>)
//         }
//           ) }
        
//         </ul>*/}