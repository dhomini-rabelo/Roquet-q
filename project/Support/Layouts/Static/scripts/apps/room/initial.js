document.addEventListener('DOMContentLoaded', loadMainImg)


function loadMainImg() {
    let contentMainImg = document.querySelector('.main-img')
    let mainImg = document.createElement('img')
    mainImg.src = '/static/assets/apps/room/home/person.svg'
    mainImg.alt = 'ask-person'
    contentMainImg.appendChild(mainImg)
}