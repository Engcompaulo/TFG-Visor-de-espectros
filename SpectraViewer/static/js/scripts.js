function setFileName() {
    var fileName = document.getElementById("name");
    if (fileName.value == null || fileName.value === "") {
        var selectedFile = document.getElementById("file").files.item(0).name;
        var extensionIndex = selectedFile.lastIndexOf(".");
        fileName.value = selectedFile.substring(0, extensionIndex);
    }
}

function confirmDeletion() {
    return confirm("¿Estás seguro de que quieres eliminar ese elemento?");
}

function getModelParameters() {
    var selected = document.getElementById("select-model").selectedIndex;
    var model = document.getElementById("select-model").options[selected].value;
    var url = "/model-parameters/" + model;
    $("#parameters-form").load(url);
}