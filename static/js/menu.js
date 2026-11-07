document.documentElement.classList.add('menu-js');

const menuToggle = document.querySelector('.menu-toggle');
const mainMenu = document.querySelector('#menu-principal');
const dropdown = document.querySelector('.site-header .dropdown');
const dropdownToggle = dropdown?.querySelector('.dropdown-btn');

if (menuToggle && mainMenu) {
    const setMenuOpen = (isOpen) => {
        mainMenu.classList.toggle('is-open', isOpen);
        menuToggle.setAttribute('aria-expanded', String(isOpen));
        menuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
    };

    menuToggle.addEventListener('click', () => {
        const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
        setMenuOpen(!isOpen);
    });

    const setDropdownOpen = (isOpen) => {
        if (!dropdown || !dropdownToggle) {
            return;
        }

        dropdown.classList.toggle('is-open', isOpen);
        dropdownToggle.setAttribute('aria-expanded', String(isOpen));
    };

    if (dropdown && dropdownToggle) {
        dropdownToggle.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                const isOpen = dropdownToggle.getAttribute('aria-expanded') === 'true';
                setDropdownOpen(!isOpen);
            }
        });
    }

    mainMenu.addEventListener('click', (event) => {
        if (event.target.closest('a')) {
            setMenuOpen(false);
            setDropdownOpen(false);
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            if (dropdownToggle?.getAttribute('aria-expanded') === 'true') {
                setDropdownOpen(false);
                dropdownToggle.focus();
            } else if (menuToggle.getAttribute('aria-expanded') === 'true') {
                setMenuOpen(false);
                menuToggle.focus();
            }
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            setMenuOpen(false);
            setDropdownOpen(false);
        }
    });
}
