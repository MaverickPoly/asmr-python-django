document.getElementById("total_questions").addEventListener("change", onQuestionsChange)


// When we change the total_questions input field
function onQuestionsChange() {
    let numQuestions = parseInt(this.value);
    let container = document.getElementById("questions-container");
    container.innerHTML = "";

    for (let i = 1; i <= numQuestions; i++) {
        let fieldset = document.createElement("fieldset");
        fieldset.className = "border border-gray-300 p-4 rounded-lg bg-gray-50 shadow-sm mb-4";

        fieldset.innerHTML = `
                <legend class="text-xl font-semibold text-gray-700">Question ${i}</legend>

                <div class="flex flex-col">
                    <label class="text-lg font-medium text-gray-600">Question:</label>
                    <input 
                        type="text" name="question_${i}" required
                        class="p-2 border rounded-lg focus:ring focus:ring-green-500"
                    >
                </div>

                <div class="grid grid-cols-2 gap-4 mt-2">
                    <div class="flex flex-col">
                        <label class="font-medium text-gray-600">Answer 1:</label>
                        <input 
                            type="text" name="answer_1_${i}" required
                            class="p-2 border rounded-lg focus:ring focus:ring-green-500"
                        >
                    </div>
                    
                    <div class="flex flex-col">
                        <label class="font-medium text-gray-600">Answer 2:</label>
                        <input 
                            type="text" name="answer_2_${i}" required
                            class="p-2 border rounded-lg focus:ring focus:ring-green-500"
                        >
                    </div>

                    <div class="flex flex-col">
                        <label class="font-medium text-gray-600">Answer 3:</label>
                        <input 
                            type="text" name="answer_3_${i}" required
                            class="p-2 border rounded-lg focus:ring focus:ring-green-500"
                        >
                    </div>

                    <div class="flex flex-col">
                        <label class="font-medium text-gray-600">Answer 4:</label>
                        <input 
                            type="text" name="answer_4_${i}" required
                            class="p-2 border rounded-lg focus:ring focus:ring-green-500"
                        >
                    </div>
                </div>

                <div class="mt-4">
                    <label class="text-lg font-medium text-gray-600">Correct Answer (1-4):</label>
                    <input 
                        type="number" name="correct_answer_${i}" min="1" max="4" required
                        class="p-2 border rounded-lg focus:ring focus:ring-green-500 w-24"
                    >
                </div>
            `;

        container.appendChild(fieldset);
    }
}
