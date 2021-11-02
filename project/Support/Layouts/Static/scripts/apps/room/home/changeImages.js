let buttonsWhiteAndBlue = document.querySelectorAll('.button-white-blue')
let fields = {'enter': 0, 'group': 0}

//* Events
buttonsWhiteAndBlue.forEach((button) => {
    button.addEventListener('mouseover', changeImgColor)
    button.addEventListener('mouseout', changeImgColor)
    }
)


//* Functions

function changeImgColor(event) {
    let field = event.currentTarget.getAttribute('class')
    field = field.toString().substring(18)

    if (field in fields){
        let blueImg = document.querySelector(`.${field} .blue-img`)
        let whiteImg = document.querySelector(`.${field} .white-img`)   
        
        if (blueImg.style.display === '' || blueImg.style.display === 'block'){
            blueImg.style.display = 'none'
            whiteImg.style.display = 'block'
        }else if (blueImg.style.display == 'none'){
            blueImg.style.display = 'block'
            whiteImg.style.display = 'none'            
        }
    }
}
