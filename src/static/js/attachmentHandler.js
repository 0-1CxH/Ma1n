const uploadedFiles = []
const fileSizeLimit = 50 * 1024 * 1024

function handleFileUpload(event) {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
      if (files[i].size <= fileSizeLimit) { // Check if file size is <= 100MB
        uploadedFiles.push(files[i]);
      } else {
        addNotification(`File "${files[i].name}" (${fileSizeFormatter(files[i].size)}) exceeds the file size limit (${fileSizeFormatter(fileSizeLimit)}) and will not be uploaded.`, 'error');
      }
    }
}

function  fileSizeFormatter(size) {
    let units = 'B';
    let formattedSize = size;
    console.log(size)
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

function fileInfoFormatter(file) {
    return 'File: ' + file.name + '\nType: ' + file.type + '\nSize: ' + fileSizeFormatter(file.size);
}