const editorModes = ["plain", "markdown"]
let currentEditorModeIndex = 0
let currentEditorMode = "plain"

function changeEditorMode() {
    currentEditorModeIndex = (currentEditorModeIndex + 1) % editorModes.length;
    setEditorMode(editorModes[currentEditorModeIndex]);
}

function setEditorMode(mode) {
    currentEditorMode = mode
    renderEditor()
}

function renderEditor() {
    const mainInputEditor = document.getElementById("main-input-editor");
    const editorPlaceHolder = `Text in your instructions` + 
    `, and upload files or enter web links if you need. ` + 
    `Current editor mode: ${currentEditorMode}, click the button to switch.`
    if (currentEditorMode === "plain") {
        mainInputEditor.innerHTML = `
            <textarea class="base-editor full-width-text-editor" placeholder="${editorPlaceHolder}"></textarea>
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
            <textarea class="base-editor half-width-text-input-left" placeholder="${editorPlaceHolder}"></textarea>
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

function getEditorUserInputValue() {
    const mainInputEditor = document.getElementById("main-input-editor");
    if (currentEditorMode === "plain") {
        return mainInputEditor.querySelector(".full-width-text-editor").value;
    } else if (currentEditorMode === "markdown") {
        return mainInputEditor.querySelector(".half-width-text-input-left").value;
    }
    return ""; // Default return if no matching mode
}



renderEditor();