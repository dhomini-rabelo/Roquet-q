let textInputs = document.querySelectorAll('input[type="text"]')
let passwordInputs = document.querySelectorAll('input[type="password"]')


textInputs.forEach((input) => {
    input.addEventListener('blur', strip)
})

passwordInputs.forEach((input) => {
    input.addEventListener('blur', strip)
})

function strip(event) {
    event.currentTarget.value = event.currentTarget.value.trim()
}