const addTagButton = document.getElementById("add-tag");
const tagsContainer = document.getElementById("tags-container");

addTagButton.addEventListener("click", () => {
    const newTagInput = document.createElement("input");
    newTagInput.type = "text";
    newTagInput.name = "tags";
    newTagInput.placeholder = "Tag...";
    newTagInput.required = true;
    newTagInput.className = "bg-white p-2 rounded-lg w-full outline-none border border-neutral-300 focus:border-emerald-600";

    tagsContainer.appendChild(newTagInput);
})