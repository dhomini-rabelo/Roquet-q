let form = document.querySelector('form')

form.addEventListener('submit', showError)

function showError(event) {
    let input = document.querySelector('input')
    if (input.value.trim() === ''){
        event.preventDefault()
        input.style.border = '2px solid red'
    }
}