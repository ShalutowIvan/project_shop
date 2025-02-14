import { useState } from 'react'
import Button from './Button/button'


const json_example = {
    bla: "бла бла бла бла бла бла бла бла бла бла бла бла ",
    tra: "тра та та та тра та та та тра та та та тра та та та ",
    python: "print(Hello World) print(Hello World) print(Hello World) ",
  }


export default function Json_example_section () {
    const [contentType, setContentType] = useState(null)

    function handleClick(type) {
        // console.log("кликнули на кнопку", type)
        // param = type
        setContentType(type)
        console.log(contentType)
      }
     

    return (
        
        <section>
          <h3>Заголовок № 2</h3>
          <Button isActive={contentType==="bla"} onClick={() => handleClick("bla")}>Кнопарь №1</Button>
          <Button isActive={contentType==="tra"} onClick={() => handleClick("tra")}>Кнопарь №2</Button>
          <Button isActive={contentType==="python"} onClick={() => handleClick("python")}>Кнопарь №3</Button>
          
        {/* { contentType ? 
        ( <p>{json_example[contentType]}</p> ) :
        ( <p>Нажми на кнопку</p> )
        } */}
        {/* {tabContent} */} 

        {!contentType && <p>Нажми на кнопку</p> }
        { contentType && <p>{json_example[contentType]}</p>}

        </section>

        
    )
}











