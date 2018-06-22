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

function enableSubmit() {
    document.getElementById("submit").disabled = false;
}

function getModelParameters() {
    var model = document.getElementById("select-model").value;
    var url = "/model-parameters/" + model;
    enableSubmit();
    $("#parameters-form").load(url);
}