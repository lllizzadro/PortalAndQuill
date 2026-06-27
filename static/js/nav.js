const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector("nav");

toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen);
});

const emailBtn = document.querySelector("#email-btn");
if (emailBtn) {
    emailBtn.addEventListener("click", () => {
        const message = document.querySelector("#message").value;
        const subject = encodeURIComponent("Message from the Portal & Quill website");
        const body = encodeURIComponent(message);
        window.location.href = `mailto:info@portalandquill.com?subject=${subject}&body=${body}`;
    });
}