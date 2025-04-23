// Nav-bar Scripts
const body = document.querySelector("body");
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.toggle');
const searchBtn = body.querySelector('.search-box');
const modeSwitch = body.querySelector('.toggle-switch');
const modeText = body.querySelector('.mode-text');

toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close');
});

const sidebarMobile = body.querySelector('.sidebar-mobile');
const largura = window.innerWidth;
sidebarMobile.addEventListener('click', () => {
    sidebar.classList.remove('close');
    sidebar.classList.toggle('active-menu-mobile');

    if (window.innerWidth <= 900) {
        // Remove event listeners duplicados e adiciona apenas uma vez
        toggle.onclick = () => {
            sidebar.classList.toggle('active-menu-mobile');
        };
    }
});


// 