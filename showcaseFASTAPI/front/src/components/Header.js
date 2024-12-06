import React from "react"


//создали класс, и унаследовали его от React.Component
class Header extends React.Component {
  render() {
    return (
      <header className="header">
          {this.props.nazvanie}          
      </header>
      )  
    }
}


export default Header
//по умолчанию экспортируем компонент Header









