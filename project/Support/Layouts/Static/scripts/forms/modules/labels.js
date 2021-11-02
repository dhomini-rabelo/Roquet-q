export function adaptLabels(optionals){
    let weLabels = document.querySelectorAll('label');

    weLabels.forEach((label) => {
        if ('span' === label.innerHTML.slice(label.innerHTML.length - 6, label.innerHTML.length - 2)){
            label.innerHTML = label.innerHTML.slice(0, label.innerHTML.length - 35);
        }else{
            label.innerHTML = label.innerHTML.slice(0, label.innerHTML.length - 13);
        }

        if(label.getAttribute('for') in optionals){
            label.innerHTML += '(opcional):';
        }else{
            label.innerHTML += ':';
        }
    });
}