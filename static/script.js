let nav = {'Главная': "/index", 'Новости': "/news", 'О компании': "/about", 'Магазин': "/shop", 'Контакты': "/contacts"};

function Nav(nav){
    let {navigation: n} = props; // n - короткое название (alias)переменной navigation; перезаписали название переменной
    return(
        <nav>
            <ul>
                {Object.keys(n).map(elem => {
                    return (
                        <li key={elem}>
                            <a href={props.navigation[elem]}>{elem}</a>
                        </li>
                    )
                })}
            </ul>
        </nav>
    )
}