import classes from "./Button.module.css"



export default function Button({ children, ...props}) {
    

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