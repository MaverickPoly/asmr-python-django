// ====== Register | Edit Profile - Pages Functionality

const linkAddBtn = document.getElementById("social_link_add");
const linksContainer = document.getElementById("links_container");
const socialLinkNumber = 1;

linkAddBtn.addEventListener("click", () => {
    const newLinkInput = document.createElement("input");
    newLinkInput.type = "url";
    newLinkInput.placeholder = "New social link..."
    newLinkInput.name = `social_links`
    newLinkInput.required = true;
    newLinkInput.className = "rounded-md border border-neutral-300 focus:border-neutral-500 mb-5 p-2 outline-none text-sm bg-white flex-1 mr-2"

    linksContainer.appendChild(newLinkInput);
    socialLinkNumber++;
})


// Skills
const skillAddBtn = document.getElementById("skill_add");
const skillsContainer = document.getElementById("skills_container");
const skillNumber = 1

skillAddBtn.addEventListener("click", () => {
    const newSkillInput = document.createElement("input");
    newSkillInput.type = "text";
    newSkillInput.placeholder = "Enter new skill..."
    newSkillInput.name = `skill_${skillNumber}`
    newSkillInput.required = true;
    newSkillInput.className = "rounded-md border border-neutral-300 focus:border-neutral-500 mb-5 p-2 outline-none text-sm bg-white flex-1 mr-2"

    skillsContainer.appendChild(newSkillInput);
    skillNumber++;
})



const typeSelect = document.getElementById("account_type");

const skillsField = document.getElementById("skills_field")
const organizationField = document.getElementById("organization_field")

typeSelect.addEventListener("change", () => {
    const selectedType = typeSelect.value;
    if (selectedType === "employer") {
        organizationField.classList.add("flex");
        organizationField.classList.remove("hidden");
        skillsField.classList.remove("flex");
        skillsField.classList.add("hidden");
    } else {
        skillsField.classList.add("flex");
        skillsField.classList.remove("hidden");
        organizationField.classList.remove("flex");
        organizationField.classList.add("hidden");
    }
})

