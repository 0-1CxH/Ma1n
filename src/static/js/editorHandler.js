const currentEditorMode = "markdown"

function setEditorMode(mode) {
    currentEditorMode = mode
    renderEditor()
}

function renderEditor() {
    const mainInputEditor = document.getElementById("main-input-editor");
    if (currentEditorMode === "plain") {
        mainInputEditor.innerHTML = `
            <textarea class="base-editor full-width-text-editor""></textarea>
        `;
        // adaptive height
        const inputDiv = mainInputEditor.querySelector(".full-width-text-editor");
        inputDiv.addEventListener("input", () => {
            const proxHeight = Math.ceil(inputDiv.value.length / 50); // 50 characters per line approximation
            const extraEmPerLine = inputDiv.value.split('\n').length; // each new line needs 1em
            inputDiv.style.height = `calc(${proxHeight}vh + ${extraEmPerLine}em)`;
        });
    } else if (currentEditorMode === "markdown") {
        mainInputEditor.innerHTML = `
        <div class="d-flex">
            <textarea class="base-editor half-width-text-input-left"></textarea>
            <div class="base-editor half-width-text-output-right""></div>
        </div>
        `;
        const inputDiv = mainInputEditor.querySelector(".half-width-text-input-left");
        const outputDiv = mainInputEditor.querySelector(".half-width-text-output-right");
        // adaptive height and real time render 
        inputDiv.addEventListener(
            "input", () => {
                const markdownText = inputDiv.value;
                outputDiv.innerHTML = marked(markdownText);


                const proxHeight = Math.ceil(inputDiv.value.length / 50); // 50 characters per line approximation
                const extraEmPerLine = inputDiv.value.split('\n').length; // each new line needs 1em
                inputDiv.style.height = `calc(${proxHeight}vh + ${extraEmPerLine}em)`;
                outputDiv.style.height = inputDiv.style.height
            }
        );

    } 
}



renderEditor();