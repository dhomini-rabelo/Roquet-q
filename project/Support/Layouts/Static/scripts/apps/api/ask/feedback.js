export function showMessage(message, status){
    let borderTextArea = document.querySelector('div.question.text-area')
    borderTextArea.classList.add(`${status}-send-question`)


    let messageForUser = document.querySelector('div.message')
    let imgMessage = document.querySelector('div.message > img')
    let textMessage = document.querySelector('div.message > span')
    let messageSpace = document.querySelector('.sheets')


    let getImg = {'success': 'yes', 'error': 'no', 'warning': 'alert'}
    
    messageSpace.style.display = 'none'
    messageForUser.style.display = 'block'
    imgMessage.setAttribute('src', `/static/admin/img/icon-${getImg[status]}.svg`)
    textMessage.innerHTML = message

    setTimeout(() => {
        clearMessage(message)
    }, 3000)
}

export function clearMessage(message){
    let textSpanMessage = document.querySelector('div.message > span')
    let borderTextAreaForClear = document.querySelector('div.question.text-area')
    let messageSpace = document.querySelector('.sheets')
    let checkMessage = document.querySelector('div.message')
    if (textSpanMessage.innerHTML === message) {
        checkMessage.style.display = 'none'
        messageSpace.style.display = 'block'
        borderTextAreaForClear.setAttribute('class', 'question text-area')
    }
}