import React from "react"


// export default function IntroSection() {
//     return (
//         <section>
//             <h1 className="centered">Заголовок для ИНТРЫ</h1>
//             <h3 className="centered" style={{ color: '#666' }}>Начало. тут текст для интры тут текст для интры тут текст для интры тут текст для интры тут текст для интры </h3>
//         </section>
//     )
// }

export default function IntroSection() {
    return ( React.createElement('section', null, 
        [
        React.createElement('h1', { className: 'centered', key: 1 }, "Заголовок для ИНТРЫ"), 
        React.createElement('h3', { className: 'centered', style: { color: '#666' }, key: 2 }, 'Начало. тут текст для интры тут текст для интры тут текст для интры тут текст для интры тут текст для интры'),
        ]
        )
    )
}



