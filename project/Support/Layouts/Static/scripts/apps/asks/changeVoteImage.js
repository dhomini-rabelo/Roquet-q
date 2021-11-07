export function activeChangeVoteImage(){
    let voteImages = document.querySelectorAll('.edit-question button.action')

    voteImages.forEach((voteImage) => {
        voteImage.addEventListener('mouseover', changeImgColor)
    })

    voteImages.forEach((voteImage) => {
        voteImage.addEventListener('mouseout', changeImgColor)
    })
}


function changeImgColor(event){
    let currentImg = event.currentTarget.children[1]
    let altImg = currentImg.getAttribute('alt')
    if(altImg.slice(0, 4) !== 'none'){
        currentImg.src = `/static/assets/apps/asks/vote/none-${altImg}.png`
        currentImg.alt = `none-${altImg}`
    }else{
        currentImg.src = `/static/assets/apps/asks/vote/${altImg.substring(5)}.png`
        currentImg.alt = `${altImg.substring(5)}`
    }
}