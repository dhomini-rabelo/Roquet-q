export function renderData(data) {
    let themes = data['themes']
    renderThemesForApp1(themes)
    renderMainDataForApp2(data, themes)
}

function renderThemesForApp1(themes) {
    let renderArea = document.querySelector('.state-themes')
    let activeThemes = []
    let disabledThemes = []
    themes.forEach((theme) => {
        if(theme.active){
            activeThemes.unshift(theme.name)
        }else{
            disabledThemes.unshift(theme.name)
        }
    })
    if (activeThemes.length !== 0){
        renderArea.innerHTML += '<h1>Ativos</h1>'
    }
    activeThemes.forEach((theme) => {
        renderArea.innerHTML += `
        <div class="theme">
            <span>${theme}</span>
        </div>
        <br>
        `
    })
    if (disabledThemes.length !== 0){
        renderArea.innerHTML += '<h1>Inativos</h1>'
    }
    disabledThemes.forEach((theme) => {
        renderArea.innerHTML += `
        <div class="theme">
            <span>${theme}</span>
        </div>
        <br>
        `
    })
}


function renderMainDataForApp2(data, themes){
    let renderArea = document.querySelector('.main-data')
    renderArea.innerHTML += `
    <div class="theme" style="font-weight: bold;">
        <span>Criador:</span>
        <span>${data.creator}</span>
    </div>
    <br>
    <div class="theme" style="font-weight: bold;">
        <span>Total de perguntas:</span>
        <span>${data.all_questions}</span>
    </div>
    <br>
    <div class="theme" style="font-weight: bold;">
        <span>Visitas:</span>
        <span>${data.visits}</span>
    </div>
    <br>    
    `
    if (themes.length === 0) {
        return
    }
    renderArea.innerHTML += '<h1>Dados de temas</h1>'
    themes.forEach((theme) => {
        renderArea.innerHTML += `
        <h2>${theme.name}</h2>
    <div class="theme" style="font-weight: bold;">
        <span>Criador:</span>
        <span>${theme.creator}</span>
    </div>
    <br>
    <div class="theme" style="font-weight: bold;">
        <span>Total de perguntas:</span>
        <span>${theme.questions}</span>
    </div>
        `
    })
}