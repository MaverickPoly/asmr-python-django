const header = document.querySelector("header");
const menuBtn = document.querySelector("#menu-btn");

menuBtn.addEventListener("click", () => {
    header.classList.toggle("active");
    menuBtn.children[0].classList.toggle("fa-times");
});

window.addEventListener("scroll", () => {
    header.classList.remove("active");
    menuBtn.children[0].classList.remove("fa-times");
})
