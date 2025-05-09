import { errorMessages } from "@vue/compiler-sfc"

export function validateFormData(formData, errors) {
    if (!formData.get('name') || formData.get('name') === 'undefined' || formData.get('name').trim() === '') {
        errors.value.push('Podaj właściwą nazwę wyceny w oknie "Nazwa projektu"')
      }
      if (!formData.get('category') || formData.get('category') === 'undefined'|| formData.get('category').trim() === '') {
        errors.value.push('Podaj właściwą nazwę w oknie "Kategoria"')
      }
      if (!formData.get('wood') || formData.get('wood') === 'undefined'|| formData.get('wood').trim() === '') {
        errors.value.push('Podaj właściwą nazwę w oknie "Materiał"')
      }
      if (!formData.get('collection') || formData.get('collection') === 'undefined'|| formData.get('collection').trim() === '') {
        errors.value.push('Podaj właściwą nazwę w oknie "Kolekcja"')
      }
      if (!formData.get('paint') || formData.get('paint') === 'undefined'|| formData.get('paint').trim() === '') {
        errors.value.push('Podaj właściwą nazwę w oknie "Malowanie"')
      }

        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1])
        }
}



export function validateNewAccesory(accesorytype, errors,accesorytypes) {

  const accesoryList = Array.isArray(accesorytype) ? accesorytype : [accesorytype]
  
  for ( let accesory of accesoryList) {

    if (accesory.name.trim() === '') {
      errors.value.push('Niewłaściwa nazwa akcesorii')
    }
    
    
    const isCorrectType = accesorytypes.includes(accesory.type)
    if (!isCorrectType) {
      errors.value.push(`Wybrano niepoprawny typ akcesorii ${accesory.type}. Wybierz z istniejących typów`,)
    }

    if (isNaN(accesory.price)) {
      errors.value.push('Niepoprawna cena')
    }

    if (isNaN(accesory.weight)) {
      errors.value.push('Niepoprawna waga')
    }
  }
  return 0
}

export function validateClientData(stepData, errors) {

  console.log(stepData.value)

  
  if (!stepData.value.projectName || stepData.value.projectName === 'undefined' || stepData.value.projectName.trim() === '') {
    errors.value.push('Podaj właściwą nazwę wyceny w oknie "Nazwa projektu"')
  }
  
  if (!errors.value.length) {
    return true
  }

  else {
    return errors, false
  }


}

// I left the validates function for future use of the bugs I dont know yet
export function validateElements(stepData) {
  return true
}

export function validateAccessoryTable(stepData) {
  return true
}

export function validateWorktimeType(stepData) {
  return true
}

export function validateSummary(stepData) {
  return true
}

export function validateChooseMode(stepData, errors, creationMode) {
  //console.log("stepData:",stepData.value)
  //console.log("creatioNmode:", creationMode)
  //console.log("Errors:", errors)

  if (stepData.value.trim() === '' && creationMode != 'newProjectMode' && creationMode!= 'newProductCatalogMode'){
    return false
  }


  return true

}

// Map step names to their corresponding validation functions
export const validationFunctions = {
  ClientData: validateClientData,
  ElementsProgressTable: validateElements,
  AccessoryTable: validateAccessoryTable,
  WorktimeType: validateWorktimeType,
  Summary: validateSummary,
  ChooseCreationMode: validateChooseMode
};


export function validateNewStage(newStageName, newStageShortcut, errors) {

  console.log(newStageName.value.trim())
  console.log(newStageName.value.length)
  console.log(newStageShortcut.value.length)
  if (newStageName.value.trim() === '' || newStageName.value.length > 20) {
    errors.value.push('Nazwa etapu zawiera błąd lub jest zbyt krótka')
  }
  if (newStageShortcut.value.lenght > 3) {
    errors.value.push('Maksymalna długość skrótu to 3 litery')
  }
  if (newStageShortcut.value.trim() ==='' ) {
    errors.value.push('Błędna nazwa skrótu')
  }

  return errors
}

export function isValidDate(date) {
  console.log(date)
  if (date instanceof(Date)) {
    return true
  }
  else {
    console.log("Not a date")
  }
}