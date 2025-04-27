import { Route, Navigate, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
// import Aside from './components/Aside/Aside'
// import Header from './components/Header/Header'
import { Homepage } from './Start/Homepage';
import GoodsInGroup from './Goods/GoodsInGroup';
import GoodsAll from './Goods/GoodsAll';
import GroupAdd from './Goods/GroupAdd';
import GoodsAdd from './Goods/GoodsAdd';


// import Authorization from './regusers/Authorization';
// import Registration from './regusers/Registration';
// import Registration_verify from './regusers/Registration_verify';

// import Forgot_password from './regusers/Forgot_password';
// import Forgot_password_verify from './regusers/Forgot_password_verify';
// import Logout from './regusers/Logout';


// import { Basket_view, basketLoader } from './components/Basket/Basket_view';
import { Orders_view, orderNumberLoader } from './Orders/Orders_view';
import { OrderOpen, orderOpenLoader } from './Orders/OrderOpen';

// import { OrderCreate, createOrderAction} from './components/Orders/OrderCreate'

//авторизация
// import { Loginpage } from "./regusers/Loginpage";
// import { RequireAuth } from "./regusers/RequireAuth";
// import { Profile } from "./regusers/Profile";

// import { AuthProvider } from "./regusers/AuthProvider"
// import { Private } from "./regusers/Private";
// import { AuthProvider } from "./regusers/AuthProvider";
//приходные документы
import { Receipt_view, receiptNumberLoader } from './Receipt/Receipt_view';
//расходные документы
import { Expense_view, expenseNumberLoader } from './Expense/Expense_view';
//инвентаризация
import { Inventory_view, inventoryNumberLoader } from './Inventory/Inventory_view';
//отчеты
import { Reports } from './Reports/Reports';








const AppRouter = createBrowserRouter(createRoutesFromElements(
       
	<Route path="/" element={
        
              <Homepage /> 
        
         } >


          {/*заказы*/}
          {/*loader={orderNumberLoader}*/}
          <Route path="orders/" element={<Orders_view />}  />
          {/*loader={orderOpenLoader}*/}
          <Route path="orders/:order_number" element={<OrderOpen />}  />




          {/*товары*/}
          <Route path="goods_all/" element={
              // <Private>
                     <GoodsAll />
              // </Private>
              }              
               />
          
          <Route path="groups/:slug" element={<GoodsInGroup />} />

          <Route path="groups/add/" element={<GroupAdd />} />

          <Route path="goods/add/" element={<GoodsAdd />} />



          
          {/*<Route path="basket/goods/" element={
            
                <Basket_view />
            
            } loader={basketLoader} />*/}
          
          {/*<Route path="basket/create/" element={<OrderCreate />} action={createOrderAction} />*/}
                

          {/*<Route path="profile" element={<Profile />} />*/}
          {/*приходные документы*/}
          <Route path="incoming_documents/" element={<Receipt_view />} loader={receiptNumberLoader} />
          {/*расходные документы*/}
          <Route path="expense_documents/" element={<Expense_view />} loader={expenseNumberLoader} />
          {/*инвентаризация*/}
          <Route path="inventory/" element={<Inventory_view />} loader={inventoryNumberLoader} />
          {/*отчеты*/}
          <Route path="reports/" element={<Reports />} />


        </Route>

        


	))



export default AppRouter    
     
        
