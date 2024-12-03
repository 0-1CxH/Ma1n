

function addHoverColorChangeListeners() {
    // Get all buttons with the class "hover-color-change"
    const buttons = document.querySelectorAll('button.hover-color-change');


    // Loop through each button and add a hover listener
    buttons.forEach(button => {

        button.addEventListener('mouseover', () => {
            // Change the color of the button on hover
            button.style.backgroundColor = '#efefef';
        });
        button.addEventListener('mouseout', () => {
            // Revert back to original color when not hovered
            button.style.backgroundColor = 'white';
        });
    });


    const mp_buttons = document.querySelectorAll('button.hover-change-main-process');
    mp_buttons.forEach(
        button => {

            button.addEventListener('mouseover', () => {
                // Change the color of the button on hover
                button.style.backgroundColor = '#efefef';
                button.style.color = 'black';
            });
            button.addEventListener('mouseout', () => {
                // Revert back to original color when not hovered
                button.style.backgroundColor = 'black';
                button.style.color = 'white';
            });
        }
    );

}



function addHoverBorderChangeListeners() {
        // Get all buttons with the class "hover-border-change"
        const buttons = document.querySelectorAll('button.hover-border-change');

        // Loop through each button and add a hover listener
        buttons.forEach(button => {
    
            button.addEventListener('mouseover', () => {
                // Change the color of the button on hover
                button.style.border = '2px dashed black';
            });
            button.addEventListener('mouseout', () => {
                // Revert back to original color when not hovered
                button.style.border = '2px solid grey';
            });
        });

        const mp_buttons = document.querySelectorAll('button.hover-change-main-process');
        mp_buttons.forEach(
            button => {
    
                button.addEventListener('mouseover', () => {
                    button.style.border = '2px dashed black';
                });
                button.addEventListener('mouseout', () => {
                    button.style.border = 'none';
                });
            }
        );
}


addHoverColorChangeListeners();
addHoverBorderChangeListeners();