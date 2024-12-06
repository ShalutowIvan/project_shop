import React from "react"


//создали класс, и унаследовали его от React.Component
// class Users extends React.Component {
//   //сделаем список пользователей, как бы имитация объектов, каждый пользак это словарь, как бы json формат. То есть как будто мы их взяли из базы
//   users = [
//     {
//       id: 1,
//       firstname: 'Bob',
//       lastname: 'Marley',
//       biograph: 'bla bla bla',
//       age: 40,
//       isHappy: false
//     },
//     {
//       id: 2,
//       firstname: 'Bred',
//       lastname: 'Pitt',
//       biograph: 'крутой актер',
//       age: 44,
//       isHappy: true
//     }
//   ]
  
//   // users = []

//   render() {
//     if (this.users.length > 0){
//     return (
//       <div>
//       {this.users.map((el) => (<div className="user" key={el.id}>
//         <h3>{el.firstname} {el.lastname}</h3>
//         <p>{el.biograph}</p>
//         <b>{el.isHappy === true ? 'Счастлив :)' : 'Грустно :('}</b>
//         </div>))}
//     </div>
//           )  
//                               }
//     else{
//       return (<div className="user">
//         <h3>Пользователей нет</h3>
//         </div>)
//     }


//     }
// }

//css класс добавили во внутренний div, чтобы стиль применился к внутреннему элементу по отдельности

//также нужно добавлять ключ во внутренний div, у нас это id, то есть уникальный идентификатор. Это нужно для корректной работы метода map
// key={el.id}
// без ключа выводится ошибка скопировал ее ниже:

// Users.js:29 Warning: Each child in a list should have a unique "key" prop.
// Check the render method of `Users`. See https://reactjs.org/link/warning-keys for more information.
//     at div
//     at Users (http://localhost:3000/static/js/bundle.js:261:5)
//     at main
//     at div
//     at App (http://localhost:3000/static/js/bundle.js:98:1)

// добавим еще условие вне html кода. Если массив пустой, то напишем об этом. Если не пустой, то выведем
//также можно добавлять условие и в самом html коде в виде тернарного оператора

//для вывода списка используем метод map
// <div>
//       {this.users.map((el) => (<div>
//         <h3>{el.firstname} {el.lastname}</h3>
//         <p>{el.biograph}</p>
//         </div>))}
// </div>
//тут мы обратились в нашему списку, и перебрали ему с помощью функции map, эта функция перебирает список и используем к нему фунцию, в нашем случае стрелочную, которая берет каждый элемент и распарсивает его в html структуру, которую мы прописали

// export default Users
//по умолчанию экспортируем компонент Users


// тут ниже продвинутая инфа с 8 урока по формам!!!!!!!!!!!!!!!!!
// сделаем конструктор для состояний. То есть теперь массив users, который ранее юзали, стал состоянием. И он у нас будет меняться


// import User_view from "./User_view"


// class Users extends React.Component { 
//   constructor(props) {
//     super(props)
//     this.state = {
//       users: [
//     {
//       id: 1,
//       firstname: 'Bob',
//       lastname: 'Marley',
//       biograph: 'bla bla bla',
//       age: 40,
//       isHappy: false
//     },
//     {
//       id: 2,
//       firstname: 'Brad',
//       lastname: 'Pitt',
//       biograph: 'Крутой Актер из бойцовского клуба',
//       age: 44,
//       isHappy: true
//     }
//   ]
//     }
//   }
  

//   render() {
//     if (this.state.users.length > 0){
//     return (<div>
//       {this.state.users.map((el) =>( 
//         <User_view key={el.id} user={el} />

//         ))}
//     </div>)  
//                               }
//     else{
//       return (<div className="user">
//         <h3>Пользователей нет</h3>
//         </div>)
//     }


//     }
// }
// //в условиях теперь мы просто обращаемся через состояния
// //лучше создать отдельный компонент, который будет выводить каждого пользака на экран
// // лучше все разбивать, на компоненты, чтобы все было понятно, такая логика фреймворка
// // параметр называется user, ему передали значения, в него передали объект
// // то есть меняющиеся параметры нужно делать через компонент функцию, и в нее передавать параметр, а параметр должен быть состоянием. Если состояние изменится, то все динамически будет меняться. 

// export default Users




import User_view from "./User_view"


class Users extends React.Component { 
  
  render() {
    if (this.props.users.length > 0){
    return (<div>
      {this.props.users.map((el) =>( 
        <User_view onEdit={this.props.onEdit} onDelete={this.props.onDelete} key={el.id} user={el} />

        ))}
    </div>)  
                              }
    else{
      return (<div className="user">
        <h3>Пользователей нет</h3>
        </div>)
    }


    }
}

// теперь вместо состояния мы берем параметр, и вместо state пишем props это означает параметр функции. И теперь оно через состояние выводится на экран. То есть перебирается и выводится. Пока только список перенесли в основной файл. Теперь нужно сделать добавление пользака в список который записан в состояние
// добавим при вызове компоненты User_view свойства onDelete={this.props.onDelete}
// далее перейдем в User_view, и пропишем там обработчик событий и наверно параметр
// добавили еще одно свойство onEdit={this.props.onEdit}
// далее идем в User_view
// там мы переиспользуем компонент для добавления пользака, но только мы не добавлять будем а редактировать. Но логика пока просто вывод в консоль. 


export default Users



