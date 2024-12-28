import classes from "./Button.module.css"

// export default function Button({ children }) {
//     function handleClick() {
//         console.log("раз кнопка нажата ")
//     }

//     const handleMouseEnter = () => {console.log('раз навели мышкой')}
//     return (
//         <button className="button" onClick={handleClick} onMouseEnter={handleMouseEnter}>{children}</button>
//     )
// }



// export default function Button({ children, klicker, isActive}) {
//     // console.log("отобразили кнопку")
//     let classes = 'button'
//     if (isActive) classes += ' active'

//     // return (
//     //     <button className={isActive ? 'button active': 'button'} onClick={klicker} >{children}</button>
//     // )
//     return (
//         <button className={classes} onClick={klicker} >{children}</button>
//     )
// }


// klicker
// onClick={klicker}
// убрал этот параметр и его вызов, и оставил {...props}, и теперь можно передавать любые параметры. Но onClick теперь вызывается как обработчик событий при вызове компонента
export default function Button({ children, ...props}) {
    // console.log("отобразили кнопку")
    // let classes = 'button'
    // if (isActive) classes += ' active'
    // console.log(classes)

    // return (
    //     <button className={classes} onClick={klicker} >{children}</button>
    // )

    return (
        <button 
            {...props}                        
            >
        {children}
        </button>
    )
    

}

// className={isActive ? `${classes.button} ${classes.active}`: classes.button }
// isActive, 