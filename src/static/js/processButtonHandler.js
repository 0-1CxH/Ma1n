const allProcessFunctions = getAllProcessFunctions();
let selectedProcessFunction = "Process"

function getAllProcessFunctions() {
    return fetch(get_proc_funcs_url)
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('Error fetching process functions:', error);
            return [];
        });
}

function getSelectedProcessFunction() {
    return selectedProcessFunction;
}

function mainSubmit() {
    const formData = new FormData();
    formData.append('userInput', getEditorUserInputValue());
    // Assuming uploadedFiles and enteredLinks are accessible and are arrays
    // console.log(uploadedFiles)
    uploadedFiles.forEach(file => {
        formData.append('uploadedFiles', file);
    });
    const joinedLinks = enteredLinks.join('\n');
    formData.append('enteredLinks', joinedLinks);
    // enteredLinks.forEach(link => {
    //     formData.append('enteredLinks', link + '\n');
    // });
    formData.append('selectedProcessFunction', getSelectedProcessFunction());

    // debug
    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }

    fetch(submit_session_url, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            console.log('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        addNotification('Session submitted successfully! Session ID: ' + data.sessionId, 'success');
        console.log('Form submission success:', data);
        let sessionId = data.sessionId;
        window.location.href = `${fetch_session_url}?id=${sessionId}`;
    })
    .catch(error => {
        addNotification('Error submitting form: ' + error.message, 'error');
    });

    
}


document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById('main-process-dropdown-button');
    const dropdownMenu = document.getElementById('main-process-dropdown-menu');

    dropdownButton.addEventListener('click', () => {
        if (dropdownMenu.style.display === 'block') {
            dropdownMenu.style.display = 'none';
        } else {
            dropdownMenu.style.display = 'block';
        }
    });

    allProcessFunctions.then(data => {
        let menuHTML = '';
        data.data.forEach(functionName => {
            menuHTML += `<button class="dropdown-item process-dropdown-menu-item primary-font">${functionName}</button>`;
        });
        dropdownMenu.innerHTML = menuHTML;
    });

    dropdownMenu.addEventListener('click', (event) => {
        if (event.target.classList.contains('process-dropdown-menu-item')) {
            selectedProcessFunction = event.target.textContent;
            dropdownMenu.style.display = 'none';
            document.getElementById('main-process-button').textContent = getSelectedProcessFunction();
        }
    });


});
// 