function setFileName() {
    var selectedFile = document.getElementById("file").files.item(0).name;
    var fileName = document.getElementById("name");
    fileName.value = selectedFile;
}