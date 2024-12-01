const uploadedFiles = []
const fileSizeLimit = 50 * 1024 * 1024

function handleFileUpload(event) {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
      if (files[i].size <= fileSizeLimit) { // Check if file size is <= 100MB
        uploadedFiles.push(files[i]);
        renderMaterialCards();
      } else {
        addNotification(`File "${files[i].name}" (${fileSizeFormatter(files[i].size)}) exceeds the file size limit (${fileSizeFormatter(fileSizeLimit)}) and will not be uploaded.`, 'error');
      }
    }
}

function  fileSizeFormatter(size) {
    let units = 'B';
    let formattedSize = size;
    const sizeLevels = { 'GB': 1024 ** 3, 'MB': 1024 ** 2, 'KB': 1024 };
    
    for (const [unit, limit] of Object.entries(sizeLevels)) {
      if (size >= limit) {
        units = unit;
        formattedSize = size / limit;
        break;
      }
    }
    return formattedSize.toFixed(2) + ' ' + units;
}

function truncateStr(s, maxLength, saveSuffix) {
    const truncatedName = s.length > maxLength ? s.substring(0, maxLength - saveSuffix) + '...' + s.substring(s.length- saveSuffix+1, s.length): s;
    return truncatedName 
}

function fileInfoFormatter(file) {
    const maxLength = 30;
    const truncatedType = file.type.length > maxLength ? file.type.substring(0, maxLength - 3) + '...' : file.type;
    return  truncatedType + ', ' + fileSizeFormatter(file.size);
}

function renderMaterialCards() {

    // 获取 card 容器
    const cardContainer = document.getElementById('material-cards-container');
    if(uploadedFiles.length | enteredLinks.length) {
        cardContainer.style.display = "flex"
    }
    else {
        cardContainer.style.display = "none"
    }
    // 遍历 uploadedFiles 数组并生成卡片 HTML 字符串
    let cardsHtml = '';
    let cardDeckHtml = '';
    //<class="card-title">  <class="card-text">
    // <span class="badge ">[${index + 1}]</span>
    // <span class="badge secondary-badge">[${index + 1}]</span>

    uploadedFiles.forEach((file, index) => {
        cardDeckHtml += `
            <div class="card material-card" style="margin: 2px;">
                <div class="card-body" style="padding: 5px;">
                    <span style="color: black;">${file.name}</span><br>
                    <span style="color: grey; font-size: smaller;"> [${fileSizeFormatter(file.size)}, ${file.type}]</span>
                </div>
            </div>
        `;
    });

    enteredLinks.forEach((link, index) => {
        cardDeckHtml += `
            <div class="card material-card" style="margin: 2px;">
                <div class="card-body" style="padding: 5px;">
                    <span style="color: black;">${link}</span><br>
                    <span style="color: grey; font-size: smaller;">[weblink]</span>
                </div>
            </div>
        `;
    });

    cardsHtml = cardDeckHtml;
    // 将生成的卡片 HTML 字符串插入到 card 容器中
    cardContainer.innerHTML = cardsHtml;
}