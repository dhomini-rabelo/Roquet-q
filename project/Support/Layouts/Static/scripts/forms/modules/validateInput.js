function createError(input, message){
    let idInput = input.getAttribute('id');
    let error = document.createElement('p');
    error.innerHTML =  `<p id="error_1_${idInput}" class="invalid-feedback"><strong>${message}</strong></p>`
    input.appendChild(error);
}


export function inputValidator(input) {
    let state = input.getAttribute('required');
    if (state === undefined && input.value==''){
        createError(input, 'Este campo é obrigatório');
    }
}