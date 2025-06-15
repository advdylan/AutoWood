<template>

<div class="card">


    <div class="card">
        <div class="card-content">
            <div class="columns">
                <div class="column is-full">
                    <div class="label has-text-centered is-size-5"> {{ $t('production') }}</div>
                    <div class="box">

                        <!-- HEADER -->
    <div id="columns" class="columns">
        
        <div v-for="header in headersWithSize" :key="header.id" class="column custom-column" 
        :style="{ flexBasis: header.size}">
            <div class="box custom-header">
                <div class="label has-text-centered is-size-6">{{ header.name }}</div>
            
            </div>

                        <!-- ORDERS SECTION -->
           
            <div class="section has-text-centered custom-section" v-for="(order, index) in productionList" :key="index">

                    <div
                     id="status-indicator" 
                     :class="{
                        'custom-box': order.status === 'Pending',
                        'stages-done': order.status === 'Done',
                        'stages-in-progress': order.status === 'In progress'
                    }"
                     class="box custom-box" 
                     v-if="header.name === 'Nr'">

                        {{ order.order_number }}
                    </div>

                    <div class="box has-text-centered custom-box" v-if="header.name === 'Name'">
                        {{ order.order.name }}
                    </div>

                    <div class="box has-text-centered custom-box" v-if="header.name === 'Date of order'">
                        {{ order.date_ordered }}
                    </div>

                    <div 
                    v-if="header.name === 'Delivery time'"
                    class="box has-text-centered custom-box"
                    :class="calculateDeliveryDate(order.date_ordered, order.date_of_delivery)"
                    > 
               
                        
                        <VueDatePicker 
                            v-model="order.date_of_delivery"
                            :enable-time-picker="false"
                            :menu-class="'datepicker-menu'"
                            :class="calculateDeliveryDate(order.date_ordered, order.date_of_delivery)"
                            :clearable="false"
                        />
                    </div>
                    

                    <div class="box has-text-centered custom-box" v-if="header.name === 'Stages'">
                        <nav class="level" >
                            <div class="level-left">

                                <div class="level-item" v-for="stage in order.order.production_stages">
                                    
                                    <label class="custom-checkbox">
                                        <input v-model="stage.is_done" type="checkbox" class="custom-checkbox-input">
                                        <span class="custom-checkbox-label">{{ stage.shortcut }}</span>
                                        <span class="custom-checkbox-checkmark"></span>
                                    </label>       
                                </div>
                            </div>           
                        </nav>
                    </div>

                    <div class="box has-text-centered custom-box"  v-if="header.name === 'Category'">
                        {{ order.order.category.name }}
                    </div>

                    <div class="box has-text-centered custom-box" v-if="header.name === 'Paint'">
                        {{ order.order.paints.name }}
                    </div>

                    <div 
                    class="box has-text-centered custom-box"
                    :class="{
                        'buk': order.order.wood.name === 'Buk'
                    }" 
                    v-if="header.name === 'Wood'">
                        {{ order.order.wood.name }}
                    </div>

                    <div 
                    class="box has-text-centered custom-box"
                    :class="{
                        'custom-box': order.status === 'Pending',
                        'stages-done': order.status === 'Done',
                        'stages-in-progress': order.status === 'In progress'
                    }"
                    
                    v-if="header.name === 'Status'">
                        {{ order.status }}
                    </div>

                    <div class="box custom-box" v-if="header.name === 'Notes'">
                        <input class="input custom-input" v-model="order.notes">
                    </div>
                    <div class="box custom-box" v-if="header.name === 'Nav'">
                        <router-link :to="{ name: 'NewProjectDetail', params: { id: order.order.id } }">
                                <b-button icon-right="circle-info">{{$t("details")}}</b-button>                               
                        </router-link>
                        <b-button @click="downloadEAN(order.order.id, order, order.order_number)" icon-right="circle-info">{{ $t("EAN") }}</b-button>
                        
                    </div>
            </div>
        </div>
    </div>
</div>
                </div>
            </div>

   
</div>
    </div>
        </div>


</template>

<script setup>
import axios from 'axios';
import { productionStore } from '@/store/production';
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { storeToRefs } from 'pinia';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { setTimeout } from 'core-js';

//store data 
const store = productionStore()
const {getProductionList} = store
const {productionList} = storeToRefs(store)

//const variables
const orderColor = ref('')
const containerWidth = ref(0)
const updateStagesTimeoutId = ref(null)
const updateNotesTimeoutId = ref(null)
const productionIdsWatched = ref([])
const stagesTimeoutIDs = ref(new Map)
const notesTimeoutIDS = ref(new Map)
const previousProductionList = ref([])
const datePicked = ref()





const headers = ref([
    {name: "Nr", size: '50px'},
    {name: "Name", size: '80px'},
    {name: "Date of order", size: '140px'},
    {name: "Delivery time", size: 5},
    {name: "Wood", size: 5},
    {name: "Stages", size: 5},
    {name: "Category", size: 5},
    {name: "Paint", size: 5},
    {name: "Status", size: 5},
    {name: "Notes", size: 5},
    {name: "Nav", size: 5}   
])


//computed values
const maxStages = computed(() => {return Math.max(...productionList.value.map(order => order.stages.length+1))})

const headersWithSize = computed(() => {
    return headers.value.map(header => ({
        ...header,
        size: calculateWidth(header.name)

    }))
})

const totalTextWidth = computed(() => {
    return headers.value.reduce((sum,header) => sum + calculateWidth(header.name), 0)
})



//functions

function downloadEAN(id,data,order_number) {

    console.log(`ID: ${id}`)
    console.log(`Data: ${data}`)

    try {
        let response =  axios.post(`api/v1/production/get-ean`, {
          id: id,
          data: data,
          order_number: order_number  
        },
        
         {
          responseType: 'blob',
          headers: {
            'Content-Type': 'application/json',

          },
        })
        .then((response) => {
                console.log(response)
                const href = URL.createObjectURL(response.data)

                const link = document.createElement('a')
                link.href = href
                link.setAttribute('download', `EAN_${id}.svg`)
                document.body.appendChild(link)
                link.click()

                document.body.removeChild(link)
                URL.revokeObjectURL(href)
        })


        console.log('Server response:', response)
        console.log('Project updated successfully:', response.data)
    } catch (error) {
            console.error('Error saving the project:', error)
    }
}


function isAnyStageTrue(stages) {
    if(productionList.value.length) {
        console.log(productionList.value.length)
        console.log(stages)
        return stages.some(stage => stage.is_done === true);
    }
    
}

function areAllStagesTrue(stages) {
    return stages.every(stage => stage.is_done === true);
}



function calculateDeliveryDate(dateOrder,date_of_delivery) {

    let parsedDateOfDelivery = new Date(date_of_delivery)
    let currentDate = new Date()

    //console.log(parsedDateOfDelivery)
    //console.log(`Current date: ${currentDate}`)

    let difference = (parsedDateOfDelivery - currentDate) / (1000*60*60*24)
    //console.log(difference)

    if (difference < 0.7) {
        return 'warning';
      } else if (difference <= 1) {
        return 'danger';
      } else if (difference >= 2) {
        return 'success';
      } else {
        return ''; // Default class (if needed)
      }
}

function calculateWidth(name) {
    return `${name.length * 10 + 20} px`
}

function updateOrders(id,data,order_number) {

    console.log(`Data: ${data}`)
    console.log(`Id: ${id}`)
    console.log(`order_number: ${order_number}`)
    try {
        let response =  axios.patch(`api/v1/production/update`, {
          id: id,
          data: data,
          order_number: order_number
    
        },
         {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        console.log('Project updated successfully:', response.data);
  } catch (error) {
        console.error('Error saving the project:', error.response?.data || error);
  }
}


function updateStages(id,value,order_number) {

    if (stagesTimeoutIDs.value.has(id)) {
        clearTimeout(stagesTimeoutIDs.value.get(id));
    }

    let timeoutId = setTimeout(function(){
        console.log(`Update stages fired value: ${JSON.stringify(value)} \n ID: ${id}`)
        updateOrders(id,value, order_number)
        
    }, 3000)
    stagesTimeoutIDs.value.set(id, timeoutId)
}


function updateNotes(id,value,order_number) {

    if (notesTimeoutIDS.value.has(id)) {
        clearTimeout(notesTimeoutIDS.value.get(id));
    }

    let timeoutId = setTimeout(function() {
        console.log(`Update notes fired value: ${JSON.stringify(value)}'`)
        updateOrders(id,value,order_number)

    }, 3000)
    notesTimeoutIDS.value.set(id, timeoutId)
}
function updateDateOfDelivery(id, value, order_number) {
    if (notesTimeoutIDS.value.has(id)) {
        clearTimeout(notesTimeoutIDS.value.get(id))
    }

    let timeoutId = setTimeout(function() {
        console.log(`Update date of delivery: ${JSON.stringify(value)}`)
        updateOrders(id,value,order_number)
    }, 3000)

    notesTimeoutIDS.value.set(id,timeoutId)
}


watchEffect(async() => {
    for (let order of productionList.value) {
        console.log(`Order stages: ${order.order.production_stages}`)

        if(order.order.production_stages) {
            if (isAnyStageTrue(order.order.production_stages)) {
            order.status = "In progress"
            
        }
            if(areAllStagesTrue(order.order.production_stages)) {
                order.status = "Done"
        }
            else if(!isAnyStageTrue(order.order.production_stages)) {
                order.status = "Pending"
        }

        }
        
    }
})


//watches


 
// Store previous state

watch(productionList, (newList) => {

    if (!previousProductionList.value.length) {
        console.log("First fire, do not save");
    } else {
        for (let newObject of newList) {
            let oldObject = previousProductionList.value.find(o => o.order_number === newObject.order_number);

            if (oldObject) {
                //console.log(`OldObject notes: ${oldObject.notes}`);
                //console.log(`NewObject notes: ${newObject.notes}`);
                
                if (oldObject.notes !== newObject.notes) {
                    console.log(`Notes changed from '${oldObject.notes}' to '${newObject.notes}'`)
                    console.log(`NewObject order number: ${newObject.order_number}`)
                    let note = {
                        "notes" : newObject.notes
                    }
                    updateNotes(newObject.order.id, note, newObject.order_number)
                }

                else if (JSON.stringify(oldObject.order.production_stages) !== JSON.stringify(newObject.order.production_stages)) {
                    //console.log(`Stages changes from ${JSON.stringify(oldObject.stages)} \nto ${JSON.stringify(newObject.stages)}`)
                    updateStages(newObject.order.id, newObject.order.production_stages, newObject.order_number)
                }

                else if(JSON.stringify(oldObject.date_of_delivery) !== JSON.stringify(newObject.date_of_delivery)) {
                    //console.log(`New Data of delivery: ${newObject.date_of_delivery}`)
                    updateDateOfDelivery(newObject.order.id, newObject.date_of_delivery, newObject.order_number)
                }
            }

        }
    }

    previousProductionList.value = JSON.parse(JSON.stringify(newList));
}, { deep: true });




onMounted(() => {
    getProductionList()
    containerWidth.value = document.getElementById('columns')?.offsetWidth
})
</script>



<style scoped>
.custom-section {
  padding: 3px 3px; /* Override Bulma's section padding */

}

.custom-box {
  border-style: dotted ; /* Remove default border if needed */
  border-radius: 3px;
  border-width: 1px;
  background-color: rgb(248, 248, 248);
  padding: 5px; /* Override Bulma's box padding */
  height: 40px;
  box-sizing: border-box; /* Ensure padding is included in the height */

}
.custom-box button {
    height: 30px;
    padding: 10px;
}



.custom-box .input {
  width: 100%; /* Make the input fill the container */
  height: 100%; /* Make the input fill the container */
  box-sizing: border-box; /* Ensure padding and border are included in the height */
  background-color: transparent; /* Match the background of the container */
  outline: none; /* Remove focus outline if desired */
}

.custom-header {
    border-style: solid ; /* Remove default border if needed */
    border-radius: 3px;
    border-width: 1px;
    margin: 3px;
    margin-top: 3px;
    padding: 0.5rem;
  
    
}


.custom-column {
    padding: 0.05rem;
    flex-basis: auto; /* or remove it if not needed */
    flex-grow: 0;

   
}

.custom-checkbox {
    position: relative;
    display: inline-block;
    cursor: pointer;
    font-size: 13px; /* Adjust size as needed */
    padding-left: 23px; /* Space for the custom checkbox */
    margin-right: 15px; /* Spacing between checkboxes */
}

.custom-checkbox-input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.custom-checkbox-checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 20px; /* Size of the checkbox */
    width: 20px; /* Size of the checkbox */
    background-color: #eee;
    border: 2px solid #ccc;
    border-radius: 5px; /* Rounded corners */
    transition: background-color 0.3s, border-color 0.3s;
}

.custom-checkbox-label {
    display: block;
    margin-bottom: 5px; /* Space between label and checkbox */
    font-weight: bold;
}

/* When the checkbox is checked */
.custom-checkbox-input:checked ~ .custom-checkbox-checkmark {
    background-color: #2196F3; /* Blue background */
    border-color: #2196F3;
}

/* Checkmark icon (hidden by default) */
.custom-checkbox-checkmark:after {
    content: "";
    position: absolute;
    display: none;
    left: 6.5px;
    top: 2.5px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
}


/* Show the checkmark when checked */
.custom-checkbox-input:checked ~ .custom-checkbox-checkmark:after {
    display: block;
}
.stages-done {
    background-color: rgb(97, 173, 110);
}
.stages-in-progress {
    background-color: rgb(255, 230, 169);
}
.success{
    background-color: rgb(97, 173, 110);
}
.danger{
    background-color: rgb(255, 230, 169);
}
.warning{
    background-color: hsl(348, 86%, 61%);
}

.buk {
    background-color: rgb(192, 153, 153);
}
.dab {
    background-color: rgb(124, 95, 53);
}
.sosna {
    background-color: rgb(237, 198, 152);
}

















</style>

