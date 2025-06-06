import { Route, Navigate, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
// import Aside from './components/Aside/Aside'
// import Header from './components/Header/Header'
import { Homepage } from './Start/Homepage';
import GoodsInGroup from './Goods/GoodsInGroup';
import GoodsAll from './Goods/GoodsAll';
import GroupAdd from './Goods/GroupAdd';
import GoodsAdd from './Goods/GoodsAdd';
import GoodsLoadFile from './Goods/GoodsLoadFile';
import ImageUploader from './Goods/ImageUploader';
import FileCleaner from './Goods/FileCleaner';
import GroupDelete from './Goods/GroupDelete';
import SelectGroupAfterDelete from './Goods/SelectGroupAfterDelete';
import GoodsModify from './Goods/GoodsModify';



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
import { Receipt_create } from './Receipt/Receipt_create';
import { Receipt_open, receiptOpenLoader } from './Receipt/Receipt_open';
import { Receipt_load_file } from './Receipt/Receipt_load_file';

//расходные документы
import { Expense_view, expenseNumberLoader } from './Expense/Expense_view';
import { Expense_create } from './Expense/Expense_create';
import { Expense_open, expenseOpenLoader } from './Expense/Expense_open';

//инвентаризация
import { Inventory_view, inventoryNumberLoader } from './Inventory/Inventory_view';
import { Inventory_create } from './Inventory/Inventory_create';
import { Inventory_open, inventoryOpenLoader } from './Inventory/Inventory_open';
import { Inventory_load_file } from './Inventory/Inventory_load_file';



//отчеты
import { Reports } from './Reports/Reports';








const AppRouter = createBrowserRouter(createRoutesFromElements(
       
	<Route path="/" element={        
              <Homepage />         
         }>


          {/*заказы*/}
          <Route path="orders/" element={<Orders_view />}  />          
          <Route path="orders/:order_number" element={<OrderOpen />}  />

          {/*товары*/}
          <Route path="goods_all/" element={<GoodsAll />} />          
          <Route path="groups/:slug" element={<GoodsInGroup />} />
          <Route path="groups/add/" element={<GroupAdd />} />
          <Route path="goods/add/" element={<GoodsAdd />} />
          <Route path="goods/load_file/" element={<GoodsLoadFile />} />
          <Route path="goods/load_images/" element={<ImageUploader />} />
          <Route path="goods/clean_images/" element={<FileCleaner />} />
          <Route path="groups/delete/" element={<GroupDelete />} />
          <Route path="groups/selectgroupafterdelete/:id" element={<SelectGroupAfterDelete />} />
          <Route path="goods/modify/:id" element={<GoodsModify />} />
          
          {/*<Route path="basket/goods/" element={
            
                <Basket_view />
            
            } loader={basketLoader} />*/}
          
          {/*<Route path="basket/create/" element={<OrderCreate />} action={createOrderAction} />*/}
                

          {/*<Route path="profile" element={<Profile />} />*/}
          {/*приходные документы*/}
          <Route path="incoming_documents/" element={<Receipt_view />} loader={receiptNumberLoader} />
          <Route path="incoming_documents/create/" element={<Receipt_create />} />
          <Route path="incoming_documents/:number_doc" element={<Receipt_open />} loader={receiptOpenLoader} />
          <Route path="incoming_documents/load_file/:number_doc" element={<Receipt_load_file />} />


          {/*расходные документы*/}
          <Route path="expense_documents/" element={<Expense_view />} loader={expenseNumberLoader} />
          <Route path="expense_documents/create/" element={<Expense_create />} />
          <Route path="expense_documents/:number_exp" element={<Expense_open />} loader={expenseOpenLoader} />

          {/*инвентаризация*/}
          <Route path="inventory/" element={<Inventory_view />} loader={inventoryNumberLoader} />
          <Route path="inventory/create/" element={<Inventory_create />} />
          <Route path="inventory/:number_inv" element={<Inventory_open />} loader={inventoryOpenLoader} />
          <Route path="inventory/load_file/:number_inv" element={<Inventory_load_file />} />




          {/*отчеты*/}
          <Route path="reports/" element={<Reports />} />


        </Route>

        


	))



export default AppRouter    
     
        
