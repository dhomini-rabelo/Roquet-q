
export function adaptTextAreas(columns, rows){
    let weTextAreas = document.querySelectorAll('textarea');
    
    weTextAreas.forEach((weTextArea) => {
        weTextArea.setAttribute('rows', rows);
        if (columns !== 0){weTextArea.setAttribute('cols', columns);}
    });
}