import React from "react"
import { IoCloseCircleSharp, IoHammerSharp } from 'react-icons/io5'
import AddUser from "./AddUser"//это форма для добавления пользака. Не стали делать новую

class User_view extends React.Component { 
  constructor(props) {
    super(props)
    this.state = {
      editForm: false
    }
  }
  //сделали конструктор для формы. При нажатии на молоток будет значение либо тру либо фолз




  user = this.props.user//то есть мы тут прописали параметр компонента, который будем указывать при вызове. А ниже уже будет работать с этой переменной с условиями. Название параметра мы тут указали, он называется user. В другой функции по нему также нужно будет обращаться, и в него передавать значения. Далее идем в IoHammerSharp. Там при клике будет менять состояние на противоположное значение. То есть при нажатии на кнопку молотка форму можно открывать и закрывать. Далее пропишем логику, в которой будет видно, что форма будет выводиться когда editForm будет тру
  // чтобы прописать условие без тернарного оператора, а просто условие типа "если" "то", то можно прописать булевое значение затем знак &&. 
  // то есть булевое значение если тру то выполняется код дальше

  render() {
    
    return (
      <div className="user">
        <IoCloseCircleSharp onClick={() => this.props.onDelete(this.user.id)} className="delete-icon" />
        <IoHammerSharp onClick={() => {
          this.setState({
              editForm: !this.state.editForm
            })
        }} className="edit-icon" />
        <h3>{this.user.first_name} {this.user.last_name}</h3>
        <p>{this.user.biograph}</p>
        <p>{this.user.email}</p>
        <img src={this.user.avatar} />
        <b>{this.user.isHappy === true ? 'Счастлив :)' : 'Грустно :('}</b>
        
        {this.state.editForm && <AddUser user={this.user} onAdd={this.props.onEdit} />}
      </div>
      )

    }
}

// пропишем здесь свойство onClick={() => this.props.onDelete(this.user.id)}
// оно означает что при клике будет срабатывать функция, которая передается в параметр компонента onDelete, то есть параметр компонента это функция, и в нее передается параметр функции this.user.id, и user также передается как параметр в компоненте
//теперь идет в App.js. Там добавим метод editUser
//в консоль не выводится уникальный идентификатор. Нужно это исправить. Мы передаем все поля кроме id. Нужно прописать, что в случае передачи метода для редактирования, то нужно еще писать id. Перейдем в AddUser.js


export default User_view


//стили для формы в aside
// aside form input:not([type="checkbox"]),
// aside form textarea, 
// aside form button {
//   width: 80%;
//   padding: 15px 5%;
//   font-family: 'Montserrat', sans-serif;
//   font-weight: 300;
//   margin-bottom: 10px;
//   border: 0;
//   background: #222;
//   color: #fff;
//   outline: none;
//   font-size: 15px;

// }
// /*стили применяются к списку элементов*/

// aside form input[type="checkbox"]{
//   margin: 10px;
// }

// aside form button {
//   width: 300px;
//   cursor: pointer;
//   transition: transform 500ms ease;
// }

// aside form button:hover {
//   transform: scale(1.1);

// }


