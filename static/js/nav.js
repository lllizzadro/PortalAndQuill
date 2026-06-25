const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector("nav");

toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen);
});