import Example_method from "./example_method"


const massiv = [{
  title: "Привет мир 1!",
  desc: "Все круто 111",
},
{
  title: "Привет мир 2!",
  desc: "Все круто 222",
},
{
  title: "Привет мир 3!",
  desc: "Все круто 333",
},
{
  title: "Привет мир 4!",
  desc: "Все круто 444",
}
]



export default function MassivSection () {

    return (

<section>
        <h1>React Begin Hello world!</h1>
        <ul>
          <Example_method title="Привет мир!" desc="Все круто" />
          {/* <Example_method title={massiv[0].title} desc={massiv[0].desc} />
          <Example_method {...massiv[1]} />
          <Example_method {...massiv[2]} />
          <Example_method {...massiv[3]} /> */}
          {massiv.map( (el) => {
            return <Example_method key={el.title} {...el} />
            }
            )}

        </ul>
        </section>

    )
}








