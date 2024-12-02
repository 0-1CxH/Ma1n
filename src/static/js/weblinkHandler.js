const enteredLinks = []
let showLinkEntryModal = false


function handleLinkInput() {
    showLinkEntryModal = !showLinkEntryModal; // Show modal
    console.log(showLinkEntryModal)
    toggleLinkInputModal();
}

function extractUrls(text) {
    const urlPattern = /\b((https?|ftp|smtp|telnet):\/\/)?([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})+)(:[0-9]{1,5})?(\/[^\s:"]*)?\b/g;
    let matches = text.match(urlPattern);
    return matches || [];
}

function toggleLinkInputModal() {
    const linkInputModal = document.getElementById('link-input-modal');
    if (showLinkEntryModal) {
        linkInputModal.style.display = 'block'; // Show modal
        linkInputModal.style.border = "2px dashed black"
        linkInputModal.style.backgroundColor = "#efefef";
        Array.from(linkInputModal.children).forEach(child => {
            child.style.display = 'block'; // Show sub-elements
        });     
    } else {
        linkInputModal.style.display = 'none'; // Hide modal
        linkInputModal.style.border = "none"
        linkInputModal.style.backgroundColor = "white";
        Array.from(linkInputModal.children).forEach(child => {
            child.style.display = 'none'; // Show sub-elements
        });     
    }
}


function linkModalAdaptiveHeight() {
    const linkInputTextbox = document.getElementById('link-input-modal-textbox');
    linkInputTextbox.addEventListener('change', adjustTextboxSize);
    linkInputTextbox.addEventListener('input', adjustTextboxSize);

    function adjustTextboxSize() {
        const proxHeight = Math.ceil(linkInputTextbox.value.length / 20); 
        const extraEmPerLine = linkInputTextbox.value.split('\n').length; // each new line needs 1em
        linkInputTextbox.style.height = `calc(${proxHeight}vh + ${extraEmPerLine}em)`;
        linkInputTextbox.style.width = `calc(${proxHeight * 15}vw)`;
    }
}


function clearLinkInputModalTextBox() {
    const linkInputTextBox = document.getElementById('link-input-modal-textbox');
    linkInputTextBox.value = '';
    linkInputTextBox.style.height = '1em';
    linkInputTextBox.style.width = '1em';
}

function handleConfirmLink() {
    const weblinkInput = document.getElementById('link-input-modal-textbox').value;
    const lines = weblinkInput.split('\n');
    lines.forEach(line => {
        const urls = extractUrls(line);
        if (urls.length === 0) {
            if (line.trim() !== '') {
                addNotification(`No URL found in the provided line: "${line}".`, 'error');
            }
        }
        enteredLinks.push(...urls);
        renderMaterialCards();
    });
    clearLinkInputModalTextBox();
}

toggleLinkInputModal();
linkModalAdaptiveHeight();