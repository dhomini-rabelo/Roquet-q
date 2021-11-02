let buttonsWhiteAndBlue = document.querySelectorAll('.button-blue-white')
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
    field = field.toString().substring(36)
    
    if (field in fields){
        let blueImg = document.querySelector(`.${field} .blue-img`)
        let whiteImg = document.querySelector(`.${field} .white-img`)   
        
        if (whiteImg.style.display === '' || whiteImg.style.display === 'block'){
            blueImg.style.display = 'block'
            whiteImg.style.display = 'none'
        }else if (whiteImg.style.display == 'none'){
            blueImg.style.display = 'none'
            whiteImg.style.display = 'block'            
        }
    }
}
