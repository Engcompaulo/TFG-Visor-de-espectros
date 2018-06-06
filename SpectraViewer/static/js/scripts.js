function setFileName() {
    var fileName = document.getElementById("name");
    if (fileName.value == null || fileName.value === "") {
        var selectedFile = document.getElementById("file").files.item(0).name;
        var extensionIndex = selectedFile.lastIndexOf(".");
        fileName.value = selectedFile.substring(0, extensionIndex);
    }
}