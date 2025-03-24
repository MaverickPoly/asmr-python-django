// Create poll
document.getElementById("add-question").addEventListener("click", () => {
    let container = document.getElementById("questions-container");
    let input = document.createElement('input');
    input.type = "text";
    input.name = "questions";
    input.placeholder = "Enter a question";
    container.appendChild(input);
});

