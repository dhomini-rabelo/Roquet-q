let form = document.querySelector('form')

form.addEventListener('submit', showError)

function showError(event) {
    let inputsText = document.querySelectorAll('input[type="text"]')
    let inputsPassword = document.querySelectorAll('input[type="password"]')
    inputsText.forEach((input) => {
        if (input.value.trim() === ''){
            event.preventDefault()
            input.style.border = '2px solid red'
        }
    })
    inputsPassword.forEach((input) => {
        if (input.value.trim() === ''){
            event.preventDefault()
            input.style.border = '2px solid red'
        }
    })
}