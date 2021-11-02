let copyCodeButton = document.querySelector('.copy')

copyCodeButton.addEventListener('click', copyCode)

function copyCode() {
    console.log('oi')
    let code = document.querySelector('#the_code')
    code.focus()
    code.select()
    document.execCommand('copy')
}