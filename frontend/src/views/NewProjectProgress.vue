<template>


<div class="card">

  <section class="section" style="padding: 1rem">
  
    <div class="columns is-centered has-text-centered is-vcentered">

      <div class="column">
        <div class="button is-rounded is-medium" 
        @click="navigateWithButton(npSteps[0])"
        :class="returnButtonState(npSteps[0].state)">{{ $t('choose_mode') }}</div>
      </div>
      <div class="column">
      <span class="icon is-medium">
      <i class="fa-solid fa-arrow-right-long"></i>
    </span></div>

      <!-- First Column -->
      <div class="column">
        <div class="button is-rounded is-medium" 
        @click="navigateWithButton(npSteps[1])"
        :class="returnButtonState(npSteps[1].state)">{{ $t('client_data') }}</div>
      </div>
      
      <div class="column"><span class="icon is-medium">
      <i class="fa-solid fa-arrow-left-long "></i>
      </span>
      <span class="icon is-medium">
      <i class="fa-solid fa-arrow-right-long "></i>
    </span></div>
      <!-- Line Between Buttons -->

      <!-- Second Column -->
      <div class="column">
        <div class="button is-rounded is-medium" 
        @click="navigateWithButton(npSteps[2])"
        :class="returnButtonState(npSteps[2].state)"
        >{{ $t('elements_list')}}</div>
      </div>
      <div class="column"><span class="icon is-medium">
      <i class="fa-solid fa-arrow-left-long "></i>
      </span>
      <span class="icon is-medium">
      <i class="fa-solid fa-arrow-right-long "></i>
    </span></div>
      <!-- Line Between Buttons -->
  
      <!-- Third Column -->
      <div class="column">
        <div class="button is-rounded is-medium" 
        @click="navigateWithButton(npSteps[3])"
        :class="returnButtonState(npSteps[3].state)">{{$t('accessories')}}</div>
      </div>
      <!-- Line Between Buttons -->
      <div class="column"><span class="icon is-medium">
      <i class="fa-solid fa-arrow-left-long "></i>
      </span>
      <span class="icon is-medium">
      <i class="fa-solid fa-arrow-right-long "></i>
    </span></div>
      

      <!-- Fourth Column -->
      <div class="column">
        <div class="button is-rounded is-medium" 
        @click="navigateWithButton(npSteps[4])"
        :class="returnButtonState(npSteps[4].state)">{{ $t('margins')  }}</div>
      </div>
      <!-- Line Between Buttons -->
      <div class="column">
      <span class="icon is-medium">
      <i class="fa-solid fa-arrow-right-long "></i>
    </span></div>


      <!-- Fifth Column -->
      <div class="column">
        <div class="button is-rounded is-medium" 
        @click="navigateWithButton(npSteps[5])"
        :class="returnButtonState(npSteps[5].state)">{{ $t('summary')  }}</div>
      <!-- Line Between Buttons -->
      </div>
    </div>
</section>

  <div class="card-content" style="padding: 0rem;" >
    <div class="content">
    <component
      v-if="activeStep"
      :is="activeStep.component"
      :key="activeStep.name"
      @next="handleNextButton(findActiveStep)"
    ></component>
    
  </div>
  


  <footer class="card-footer" style="display: flex; justify-content: space-between; align-items: center; position: sticky; bottom: 0; width: 100%;" >

    <button @click="handleBackButton(findActiveStep)" class="card-footer-item button is-medium" :disabled="findActiveStep === 0">
    <span class="icon is-medium">
      <i class="fa-solid fa-arrow-left "></i>
    </span>
    <span>{{ $t('back') }}</span>
  </button>

  <button class="card-footer-item button is-medium">Current Step</button>
  
  
  <button v-if="findActiveStep !== npSteps.length -1" @click="handleNextButton(findActiveStep)" class="card-footer-item button is-medium" :disabled="findActiveStep === npSteps.length -1">

    <span class="text">{{ $t('next') }}</span>
    <span class="icon is-medium">
      <i class="fa-solid fa-arrow-right "></i>
    </span>

  </button>

  <button v-if="findActiveStep === npSteps.length -1" @click="saveData()" 
                                        class="card-footer-item button is-medium is-success">
                                    <i class="fa-solid fa-floppy-disk"></i>
                                    &nbsp;
                                    {{ $t('save') }}
                                </button>
  </footer>
</div>
</div>
</template>
  
<script setup>
import { useNewProjectStoreBeta } from '@/store/newproject'
import { useSummaryStore } from '@/store/summary'
import {ref, computed, onUnmounted, watch, watchEffect, shallowRef, markRaw} from 'vue'
import { storeToRefs } from 'pinia'
import {validateClientData, validateFormData} from '@/validators/Validators.js'
import { useI18n } from 'vue-i18n';
import ElementsProgressTable from '@/components/NewProjectComponents/ElementsProgressTable.vue'
import WorktimeType from '@/components/WorktimeType'
import ChooseCreationMode from '@/components/NewProjectComponents/ChooseCreationMode.vue'
import Summary from '@/components/Summary.vue'
import ClientData from '@/components/NewProjectComponents/ClientData.vue'
import { validationFunctions } from '@/validators/Validators.js'

import axios from 'axios'
import { toast } from 'bulma-toast'
import AccesoryProgressTable from '@/components/NewProjectComponents/AccesoryProgressTable.vue'
const { t } = useI18n();


// const definition section

const newProjectStore = useNewProjectStoreBeta()
const summaryStore = useSummaryStore()

const { addElement, loadData, $resetBoxes,} = newProjectStore
const {summaryCosts, elementsMargin, accesoriesMargin,
   additionalMargin,summaryCostsWithMargin, elementsCost, accesoriesCost, worktimeCost} = storeToRefs(summaryStore)

loadData()



const {elements, boxes, accesories, marginA, marginB, marginC, files, 
  customer, projectName, selectedCategory, selectedCollection,selectedFile,selectedPaint,selectedWood,chosenProductionSteps, creationMode} = storeToRefs(newProjectStore)

const errors = ref([])


const newElement = ref({
  element: {
    name: 'Przód',
    dimX: 2500,
    dimY: 250,
    dimZ: 25,
    wood_type: ''
  },
  quantity: 1
})

const npSteps = ref([
  { position: 0, name: 'ChooseCreationMode', component: markRaw(ChooseCreationMode), isValid: false, state: 'inProgress' },
  { position: 1, name: 'ClientData', component: markRaw(ClientData), isValid: false, state: 'notYetDone' },
  { position: 2, name: 'ElementsProgressTable', component: markRaw(ElementsProgressTable), isValid: false, state: 'notYetDone' },
  { position: 3, name: 'AccessoryTable', component: markRaw(AccesoryProgressTable), isValid: false, state: 'notYetDone' },
  { position: 4, name: 'WorktimeType', component: markRaw(WorktimeType), isValid: false, state: 'notYetDone' },
  { position: 5, name: 'Summary', component: markRaw(Summary), isValid: false, state: 'notYetDone' }
])



const ClientDataValidation = ref({
  projectName: projectName,
  selectedWood: selectedWood,
  selectedCategory: selectedCategory,
  selectedCollection: selectedCollection,
  selectedPaint: selectedPaint
})

const validationData = {
  ClientData: ClientDataValidation,
  ElementsProgressTable: null,
  AccessoryTable: null,
  ChooseCreationMode: creationMode


};

// comptued values section



const findActiveStep = computed (() => {
  return npSteps.value.findIndex((component) => component.state === 'inProgress')
})

const activeStep = computed (() => {
  return npSteps.value.find(step => step.state === "inProgress")
})


// functions section

function returnButtonState(state) {

  if (state === 'inProgress') {
    return 'is-primary'
  }
  else if (state === 'notYetDone') {
    return 'is-warning'
  }
  else if (state === 'done'){
    return 'is-success'
  }
  
}

function handleNextButton(index) {


  let currentStep = npSteps.value[index]
  let nextStep = npSteps.value[index+1]
  
  if (currentStep && nextStep) {
  //validation here
  
  const validate = validationFunctions[currentStep.name]

  if (validate) {
    const isValid = validate(validationData[currentStep.name], errors, creationMode)

    if (!isValid) {
      let msg = ''

        for (let i=0; i <errors.value.length; i++){
          msg += errors.value[i] += "\n"
        }
        toast({
            message: msg,
            duration: 5000,
            position: "top-center",
            type: 'is-danger',
            animate: { in: 'backInDown', out: 'backOutUp' },
          })

          errors.value = []
    }

    if(isValid) {
        currentStep.isValid = true
        currentStep.state = 'done'
        nextStep.state = 'inProgress'
    }
    
  }
  
  }
}

function handleBackButton(index) {

  let currentStep = npSteps.value[index]
  let previousStep = npSteps.value[index-1]

  if (currentStep && previousStep) {
    currentStep.state = 'notYetDone'
    previousStep.state = 'inProgress'
  }

}


function navigateWithButton(stepToActivate) {

  //maybe how many steps you skip and validate that? 

  if (activeStep.value.state = 'inProgress'){
    const validate = validationFunctions[activeStep.value.name]
    if (validate) {
      
      const isValid = validate(validationData[activeStep.value.name], errors, creationMode)
      if (!isValid) {
        let msg = ''

          for (let i=0; i <errors.value.length; i++){
            msg += errors.value[i] += "\n"
          }
          toast({
            message: 'Dokończ obecny krok',
            duration: 5000,
            position: "top-center",
            type: 'is-warning',
            animate: { in: 'backInDown', out: 'backOutUp' },
          })
          toast({
              message: msg,
              duration: 5000,
              position: "top-center",
              type: 'is-danger',
              animate: { in: 'backInDown', out: 'backOutUp' },
            })

            errors.value = []

      }
      if (isValid) {
        activeStep.value.state = 'done'
        stepToActivate.state = 'inProgress'
      }
    }
    }

    }




    async function saveData() {

const formData = new FormData();

//console.log(formData.get('name').trim())



// Add regular project data
formData.append('name', projectName.value)
formData.append('category', selectedCategory.value)
formData.append('wood', selectedWood.value)
formData.append('collection', selectedCollection.value)
formData.append('paint', selectedPaint.value)
formData.append('elements_margin', parseFloat(elementsMargin.value.toFixed(2)))
formData.append('accesories_margin', parseFloat(accesoriesMargin.value.toFixed(2)))
formData.append('additional_margin', parseFloat(additionalMargin.value.toFixed(2)))
formData.append('summary_with_margin', parseFloat(summaryCostsWithMargin.value.toFixed(2)))
formData.append('summary_without_margin', parseFloat(Number(summaryCosts.value).toFixed(2)))
formData.append('elements', JSON.stringify(elements.value))
formData.append('worktime', JSON.stringify(boxes.value))
formData.append('accesories', JSON.stringify(accesories.value))
formData.append('percent_elements_margin', marginA.value)
formData.append('percent_accesories_margin', marginB.value)
formData.append('percent_additional_margin', marginC.value)
formData.append('elements_cost', elementsCost.value)
formData.append('accesories_cost', accesoriesCost.value)
formData.append('worktime_cost', worktimeCost.value)
formData.append('customer', JSON.stringify(customer.value))
files.value.forEach((file, index) => {
formData.append(`files[${index}]`, file)
}),formData.append('production_stages', JSON.stringify(chosenProductionSteps.value))


const formDataObject = {};
formData.forEach((value, key) => {
  formDataObject[key] = value;
});

console.log(JSON.stringify(formDataObject, null, 2));





console.log(formData)

//ERROR CHECKING FUNCTIONS
validateFormData(formData, errors)

if (!errors.value.length) {

  if (creationMode.value === 'newProjectMode') {

    try {
        const response = await axios.post('api/v1/product/save', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Server response:', response)
        console.log('Project updated successfully:', response.data)
  } catch (error) {
        console.error('Error saving the project:', error)
  }
  }

    else if (creationMode.value = 'newProductCatalogMode') {
    try {
        const response = await axios.post('api/v1/production/save-product', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Server response:', response)
        console.log('Project updated successfully:', response.data)
  } catch (error) {
    console.error('Error saving the project:', error)
  }
    }


  resetInput()
} 

else {
      let msg = ''

      for (let i=0; i <errors.value.length; i++){
        msg += errors.value[i] += "\n"
      }
      toast({
          message: msg,
          duration: 5000,
          position: "top-center",
          type: 'is-danger',
          animate: { in: 'backInDown', out: 'backOutUp' },
        })

        errors.value = []
      }

}

function resetInput() {
  
    /*
    projectName.value  = ''
    selectedWood.value = ''
    selectedCategory.value = ''
    selectedCollection.value = ''
    selectedPaint.value = ''
    elements.value = []
    accesories.value = []
    $resetBoxes()
    marginA.value = 0
    marginB.value = 0
    marginC.value = 0
    */
  }
</script>



<style>
.card-content {
    background-color: transparent;
    padding: 0.5rem;
}

.line {
  width: 100px; /* Adjust the length of the line */
  height: 2px; /* Thickness of the line */
  background-color: #ccc; /* Line color */
  margin: auto; /* Center it */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>
