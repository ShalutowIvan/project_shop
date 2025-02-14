import Button from "./Button/button"

export default function TabsSection({ active, izmenenie }) {
    return (
        <section style={{ marginBottom: '1rem' }}>
            <Button isActive={active === 'main'} onClick={() => izmenenie('main')}>Главная</Button>
            <Button isActive={active === 'feedback'} onClick={() => izmenenie('feedback') }>Обратная связь</Button>
            <Button isActive={active === 'effect'} onClick={() => izmenenie('effect') }>Эффект</Button>
        </section>

    )

}