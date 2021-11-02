var notPermissionTypes = {
    'file': 0,
    'submit': 0,
    'hidden': 0
}


export function setRequiredInputs(optionals){
    let weInputs = document.querySelectorAll('input');

    weInputs.forEach((input) => {
        let type = input.getAttribute('type');
        let idInput = input.getAttribute('id');
        
        if ((!(type in notPermissionTypes))&&(!(idInput in optionals))){
            input.setAttribute('required', '');
        }

    });
}

export function setValueForInput(idInput, value){
    let input = document.querySelector(`input#${idInput}`);

    let type = input.getAttribute('type');
    
    if ((!(type in notPermissionTypes))&&(!(idInput))){
        input.setAttribute('value', value);
    }
}


export function changeTypeInput(idInput, newType) {
    let input = document.querySelector(`input#${idInput}`);

    input.setAttribute('type', newType);
}


export function addError(idInput, errorMessage) {
    let input = document.querySelector(`input#${idInput}`);
    let currentClass = input.getAttribute('class');
    input.setAttribute('class', `${currentClass} is-invalid`);
    let weError = `<p id="error_1_${idInput}" class="invalid-feedback"><strong>${errorMessage}</strong></p></strong></p> </div>`
    input.appendChild(weError);
}
