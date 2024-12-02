let selectedProcessFunction = "Process"
const allProcessFunctions = getAllProcessFunctions();

function getAllProcessFunctions() {
    return fetch('/procfuncs')
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