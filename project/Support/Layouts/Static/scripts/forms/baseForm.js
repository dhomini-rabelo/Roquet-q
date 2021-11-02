import {adaptTextAreas} from './modules/textAreas';
import {adaptLabels} from './modules/labels';
import {setRequiredInputs, setValueForInput, changeTypeInput} from './modules/input';
import { addMask } from './modules/masks';
import { forMoneyBRMask, strMask, forDateBRMask } from './modules/functions';
import { inputValidator } from './modules/validateInput';
import {strDate} from './modules/utils';

//! write ->  type = "module" in tag script
// test use class needs-validation



document.addEventListener('load', adaptForm);
// DOMContentLoaded


function adaptForm(){




    let useValuesForInputs = false;
    let editTypeOfInputs = false;
    let useRequiredInputs = false;
    let editLabels = false;
    let editTextAreas = false;
    let useMasks = false;
    let useInputValidator = false;
    let useInputsInARow = false;
    



    //*--------------------------------------------------------------




    if (useValuesForInputs){
        /* 
        Edita o valor do input, como colocar um valor padrão para datas
        */
        let modifications = [
           //('id_field', value),
        ];//using id

        for (let i in modifications){
           setValueForInput(modifications[i][0], modifications[i][1]);
        }
    }



    if (editTypeOfInputs){
        /* 
        Edita o tipo do input, como trocar text para date ou number para text,
        caso queira usar máscaras
        */
        let modifications = [
            //('id_field', newType),
         ];//using id
 
         for (let i in modifications){
            changeTypeInput(modifications[i][0], modifications[i][1]);
         }        
    }



    let optionalFields  = {
        // 'id_name': 0 -> initialIndex
    }// using id

    if (useRequiredInputs){
        /* 
        Define os campos que são requeridos
        */
        setRequiredInputs(optionalFields);
    }



    if (editLabels){
        /* 
        Edita o texto do label
        */
       adaptLabels(optionalFields);
    }
    


    if (editTextAreas){
        /* 
        Controla tamanho da tag textarea no form, se
        columns = 0, ele utiliza o valor padrão do form
        */
        let rows = 2;
        let columns = 0;
        adaptTextAreas(columns, rows);
    }


    
    if (useMasks){
        //! <script src="https://cdn.jsdelivr.net/npm/cleave.js@1.6.0/dist/cleave.min.js"></script>
        //! Adaptado para uso com input do tipo text
        let modifications = [
            //('id_field', mask),
        ];//using id
        let allowedMasks = ['cpf', 'cnpj', 'phoneBR', 'dateBR', 'moneyBR', 'card', 'numericOnly', 'numericPositiveOnly', 'securityPasswordCard']
        for (let i in modifications){
            addMask(modifications[i][0], modifications[i][1]);
        }  
        //* Functions
        // case mask for string --> strMask(idInput, False)
        // case moneyBR in modifications  --> forMoneyBRMask(idInput);
        // case dateBR in modifications  --> forDateBRMask(idInput); use valor 01/01/2000 como inicial
    }



    if (useInputValidator){
        let idInputs = [
            //'id'
        ];
        let inputs = [];
        for(let idInput in idInputs) {
            let input = document.getElementById(idInput);
            inputs.push(input);
        }
        inputs.forEach((input) => {
            input.addEventListener('blur', inputValidator);
        });
    }



    if (useInputsInARow){
        //! use div.row para abranger esses inputs
        let minorInputs = document.querySelector("div.row > div");
        minorInputs.forEach((input) => {
            currentClass = input.getAttribute("class");
            input.setAttribute("class", `col-md-6 ${currentClass}`);
        });
    }
}

