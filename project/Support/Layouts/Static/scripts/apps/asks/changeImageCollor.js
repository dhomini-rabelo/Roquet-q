let button = document.querySelector('.white-and-blue')

button.addEventListener('mouseover', changeImgColor)
button.addEventListener('mouseout', changeImgColor)

function changeImgColor(){
    let imgs = document.querySelectorAll('.copy img')
    imgs.forEach((img) => {
        if(img.style.display === 'inline-block'){
            img.style.display = 'none'
        }else if(img.style.display === 'none'){
            img.style.display = 'inline-block'
        }
    })
}