const selectedNodes = []

function toggleNodeSelection(nodeId) {
    const nodeElement = document.getElementById(`node-item-card-${nodeId}`);
    const nodeIndex = selectedNodes.indexOf(nodeId);

    if (nodeIndex === -1) {
      // Add nodeId to selectedNodes
      selectedNodes.push(nodeId);
      // Change border to indicate selection
      nodeElement.style.border = '2px dashed black';
    } else {
      // Remove nodeId from selectedNodes
      selectedNodes.splice(nodeIndex, 1);
      // Revert border to original style
      nodeElement.style.border = '1px dashed grey';
    }
  }

function toggleNodeSelectionForLevel(level) {
    const nodesAtLevel = document.querySelectorAll(`#node-cards-row-container-level-${level} .node-item-card, #node-cards-row-container-level-${level} .node-item-card-full-width`);
    let changedCount = 0;
    nodesAtLevel.forEach(nodeElement => {
        const nodeId = nodeElement.id.replace('node-item-card-', '');
        const nodeIndex = selectedNodes.indexOf(nodeId);

        if (nodeIndex === -1) {
            // Add nodeId to selectedNodes
            selectedNodes.push(nodeId);
            // Change border to indicate selection
            nodeElement.style.border = '2px dashed black';

            changedCount += 1;
        };

    });
            
    if (changedCount == 0) {
        nodesAtLevel.forEach(nodeElement => {
            const nodeId = nodeElement.id.replace('node-item-card-', '');
            const nodeIndex = selectedNodes.indexOf(nodeId);
    
            if (nodeIndex === -1) {
            } else {
                // Remove nodeId from selectedNodes
                selectedNodes.splice(nodeIndex, 1);
                // Revert border to original style
                nodeElement.style.border = '1px dashed grey';
            }
    
        });
            
    }
}

function hideProgressBar() {
    const convSubmitProgressContainer = document.getElementById('conv-submit-progress-container');
    convSubmitProgressContainer.style.height = "0";
    convSubmitProgressContainer.style.marginTop = "0";
    convSubmitProgressContainer.style.marginButtom = "0";
}

function showInputBox() {
    const mainInputEditor = document.getElementById("main-input-editor");
    mainInputEditor.innerHTML = `
        <div class="d-flex align-items-center justify-content-center">

            <textarea class="buttom-editor full-width-text-editor" 
                id="buttom-editor" placeholder="You can select/unselect node(s) by clicking each node card, or all nodes in a row by clicking the row blank. "
                onkeydown="if (event.shiftKey && event.key === 'Enter') { 
                    event.preventDefault(); 
                    const inputValue = document.getElementById('buttom-editor').value;
                    if ( inputValue != null) {
                        if (inputValue.trim() != '') {
                            stepSubmit(true, false);
                            return
                        }
                    }
                    addNotification('Need non-empty instructions, not submitting.', 'error')
                }"></textarea>
            <button class="btn bigger-round-button" 
                onclick="
                const inputValue = document.getElementById('buttom-editor').value;
                    if ( inputValue != null) {
                        if (inputValue.trim() != '') {
                            stepSubmit(true, false);
                            return
                        }
                    }
                    addNotification('Need non-empty instructions, not submitting.', 'error');
                "
                onmouseover="this.style.backgroundColor='#efefef'; this.style.border='2px dashed black';" 
                onmouseout="this.style.backgroundColor='white'; this.style.border='2px solid grey';">
                <img src="/static/images/up.png" alt="TakeStep" width="20px" height="20px">
            </button>

        </div>
    `;
    const allRowsContainer = document.getElementById('all-rows-container');
    allRowsContainer.style.maxHeight = "75vh";
    allRowsContainer.style.height = "auto";
   


}

function hideInputBox() {
    const mainInputEditor = document.getElementById("main-input-editor");
    mainInputEditor.innerHTML = ``;
    const allRowsContainer = document.getElementById('all-rows-container');
    allRowsContainer.style.maxHeight = "85vh";
    allRowsContainer.style.height = "auto";
    const convSubmitProgressContainer = document.getElementById('conv-submit-progress-container');
    convSubmitProgressContainer.style.height = "16px";
    convSubmitProgressContainer.style.marginTop = "2vh";
    convSubmitProgressContainer.style.marginButtom = "2vh";
}

function stepSubmit(triggered_by_button, triggered_by_reset) {

    const formData = new FormData();
    formData.append('sessionId', currentSessionId)
    if (triggered_by_button) {
        const userInput = document.getElementById('buttom-editor').value;
        formData.append('userInput', userInput);
        formData.append('selectedNodes', selectedNodes.join(";"))
    }
    if (triggered_by_reset) {
        formData.append('resetNode', triggered_by_reset)
    }
    
    console.log(formData)

    hideInputBox();

    fetch(take_step_url, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            addNotification(`Session deletion has encoutered error, status code=${response.status}: ${response.statusText}`, 'error')
        }
        else{
            return response.json();
        } 
    })
    .then(data => {
        if(data.code == 0) {
            window.location.href = fetch_session_url + '?id=' + currentSessionId + '&step=0';
        }
        else {
            addNotification(data.reason, "error")
        }
    })
    .catch(error => {
        addNotification('Error submitting form: ' + error.message, 'error');
    });



    
}
