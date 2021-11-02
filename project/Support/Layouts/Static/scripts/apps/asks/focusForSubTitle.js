import  {getInitialThemeQuestion} from './selectForTheme.js'



let subLinks = document.querySelectorAll('.sub-link')
let apps = document.querySelectorAll('.app')

document.addEventListener('DOMContentLoaded', focusForSubTitles)
subLinks.forEach(
    (link) => link.addEventListener('click', () => setTimeout(focusForSubTitles, 200))
)
    
function focusForSubTitles() {
    let url = document.URL
    let focus = url.substring(url.indexOf('#')+1)
    if (focus === url){
        subLinks[0].classList.add('sub-title-active')
        apps[0].classList.add('visible')
        return
    }
    subLinks.forEach((link, index) => {
        if (link.getAttribute('focus') === focus) {
            link.classList.add('sub-title-active')
            apps[index].classList.add('visible')
        } else if (link.classList.contains('sub-title-active')){
            link.classList.remove('sub-title-active')
            if (apps[index].classList.contains('visible')){
                apps[index].classList.remove('visible')
            }
        }
    })
}

