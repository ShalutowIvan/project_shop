import Button from "./Button/Button"
import { useState, useRef } from 'react'


//тут для каждого значения отдельное состояние!!!!!!!!!!!!!
// export default function FeedbackSection() {
//     const [name, setName] = useState('')
//     const [reason, setReason] = useState('help')
//     const [hasError, setHasError] = useState(false)

//     function handleNameChange(event) {
//         // console.log(event.target.value)
//         setName(event.target.value)
//         setHasError(event.target.value.trim().length === 0)
//     }

//     function changeReason(event) {
//         setReason(event.target.value)
//     }

//     function toggleError() {
//         // setHasError(!hasError)
//         // setHasError(!hasError)
//         setHasError((param) => !param)
//         setHasError((param) => !param)
//     }

//     return (
//         <section>
//             <h3>Обратная связь</h3>

//             <Button onClick={toggleError}>Какой-то Error</Button>

//             <form>
//                 <label htmlFor="name">Ваше имя</label>
//                 <input 
//                     type="text"
//                     id="name"
//                     className="control"
//                     value={name}
//                     style={{
//                         border: hasError ? '2px solid red' : null,
//                     }}
//                     onChange={ handleNameChange } 

//                 />

//                 <label htmlFor="reason">Причина обращения</label>
//                 <select id="reason" className="control" value={ reason } onChange={ changeReason }>
//                     <option value="error">Ошибка</option>
//                     <option value="help">Нужна помощь</option>
//                     <option value="suggest">Предложение</option>
//                 </select>

//                 <pre>
//                     Name: {name}
//                     <br/>
//                     Reason: {reason}
//                 </pre>

//                 <Button disabled={hasError} isActive={!hasError}>Отправить</Button>
//             </form>
//         </section>
//     )
// }


function StateVsRef() {
    const inp = useRef()
    const [show, setShow] = useState(false)

    // function changeVal(event) {
    //     setVal(event.target.value)
    // } // сделал через стрелочную функцию. Но можно и так через обычную функцию. 
    function handleKeyDown(event) {
        if (event.key === 'Enter') {
            setShow(true)
        }
    }

    console.log(inp)

    return (
        <>
            <h1>{inp.current?.value}</h1>
            <h3>Input value: { show && inp.current.value }</h3>
            <input
            ref={inp}
            type="text"
            className='control'            
            onKeyDown={handleKeyDown}
            
            />

        </>
        )
}

//тут для нескольких значений одно состояние


export default function FeedbackSection() {
    const [form, setForm] = useState({
        name: "",
        hasError: false, 
        reason: 'help'
    })
    // const [name, setName] = useState('')
    // const [reason, setReason] = useState('help')
    // const [hasError, setHasError] = useState(false)

    function handleNameChange(event) {
        // console.log(event.target.value)
        // setName(event.target.value)
        // setHasError(event.target.value.trim().length === 0)
        // setForm({
        //     name: event.target.value,
        //     hasError: event.target.value.trim().length === 0,
        //     reason: form.reason
        // })
        setForm((prev) => ({
            ...prev,
            name: event.target.value,
            hasError: event.target.value.trim().length === 0,
        })

            )
    }


    // function changeReason(event) {
    //     // setReason(event.target.value)
    // } // вместо этой функции напишем стрелочную со спред параметром там где select c Причина обращения в обработчике onChange

    // function toggleError() {
    //     // setHasError(!hasError)
    //     // setHasError(!hasError)
    //     // setHasError((param) => !param)
    //     // setHasError((param) => !param)
    // }

    return (
        <section>
            <h3>Обратная связь</h3>

            {/*<Button onClick={toggleError}>Какой-то Error</Button>*/}

            <form style={{ marginBottom: '1rem' }}>
                <label htmlFor="name">Ваше имя</label>
                <input 
                    type="text"
                    id="name"
                    className="control"
                    value={form.name}
                    style={{
                        border: form.hasError ? '2px solid red' : null,
                    }}
                    onChange={ handleNameChange } 

                />

                <label htmlFor="reason">Причина обращения</label>
                <select 
                    id="reason"
                    className="control"
                    value={ form.reason }
                    onChange={(event) =>
                    setForm((prev) => ({ ...prev, reason: event.target.value }))
                    }>
                    <option value="error">Ошибка</option>
                    <option value="help">Нужна помощь</option>
                    <option value="suggest">Предложение</option>
                </select>

                <pre>
                    Name: {form.name}
                    <br/>
                    Reason: {form.reason}
                    <br/>
                    {/*{JSON.stringify(form, null, 2)}*/}
                </pre>

                <Button disabled={form.hasError} isActive={!form.hasError}>
                    Отправить
                </Button>

            </form>


            <hr />
            <StateVsRef />


        </section>
    )
}


