let inputTheme = document.querySelector('input#id_theme')
let selectTheme = document.querySelector('select')


selectTheme.addEventListener('change', updateInputTheme)
document.addEventListener('DOMContentLoaded', getInitialTheme)


function updateInputTheme(event) {
    let themeSelected = this.selectedOptions[0]
    inputTheme.value = themeSelected.innerHTML
}


function getInitialTheme(){
    let selectedOption = document.querySelector('option[selected=""]') 
    if (selectedOption){
        inputTheme.value = selectedOption.innerHTML
    }
}