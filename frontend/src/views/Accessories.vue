<template>
    <div class=columns>
        <div class="column is-10 is-offset-1">
            <div class="notification is-primary">
                <div class="title is-centered is-size-4">
                    {{ $t('accessory_management') }}
                </div>
                <div class="text">
                    {{ $t('cost_change_info') }}
                </div>
            </div>
        </div>
    </div>
    <div class="column is-10 is-offset-1 ">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title is-centered is-size-4">
                    {{ $t('accessories') }}
                    <span>&nbsp;<i class="fa-solid fa-screwdriver-wrench fa-lg"></i></span>
                </p>
            </header>
            <div class="card-content">
                <div class="content">
                    <div class="projects-list-container">
                        <b-table :key="tableKey" :data="filteredAccessories" :paginated="isPaginated" :per-page="perPage" :current-page.sync="currentPage" :pagination-simple="isPaginationSimple" :pagination-position="paginationPosition" :default-sort-direction="defaultSortDirection" :pagination-rounded="isPaginationRounded" :sort-icon="sortIcon" :sort-icon-size="sortIconSize" default-sort="user.first_name" aria-next-label="Next page" aria-previous-label="Previous page" aria-page-label="Page" aria-current-label="Current page" :page-input="hasInput" :pagination-order="paginationOrder" :page-input-position="inputPosition" :debounce-page-input="inputDebounce">
                            <template v-for="(column, index) in columns" :key="column.id">
                                <b-table-column v-bind="column">
                                    <template v-if="column.searchable && !column.numeric" #searchable="props">
                                        <b-input v-model="props.filters[props.column.field]" :placeholder="$t('search')" icon="magnify"/>
                                    </template>
                                    <template v-if="column.field === 'nawigacja'" #header>
                                    <b-switch v-model="editMode">
                                        {{  $t('edit_mode') }}
                                    </b-switch>
                                    <b-switch v-model="showActiveAcc">
                                        {{ $t('archive_acc')}}
 
                                    </b-switch>
                                    </template>
                                    <template v-slot="props">
                                        <template v-if="column.field === 'nawigacja'">
                                            <b-button @click="handleDeleteButton(props.row)" type="is-danger" icon-left="x">
                                                
                                            </b-button>
                                        </template>
                                        
                                        <template v-if="editMode && column.searchable">
                                            <b-input @input="markAsEdited(props.row)"  v-model="props.row[column.field]"></b-input>
                                        </template>
                                        

                                        <template v-else>
                                            {{ props.row[column.field] }}
                                        </template>

                                    </template>
                                </b-table-column>
                                
                            </template>
                        </b-table>
                        <button @click="handleUpdateAccesories(accesorytype);" 
                                        class="button is-success">
                                    <i class="fa-solid fa-floppy-disk"></i>
                                    &nbsp;
                                    {{ $t('save') }}
                                </button>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="column is-10 is-offset-1">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title is-centered is-size-4">
                    {{ $t('add_new_accessories') }}
                    <span>&nbsp;<i class="fa-solid fa-plus"></i></span>
                </p>
            </header>
            <div class="card-content">
                <div class="content">
                    <div class="columns">
                        <div class="column is-half is-offset-one-quarter">
                    
                    <nav class="level">
                        <div class="level-item has-text-centered">
                            <input v-model="accesory.name" class="input" :placeholder="$t('name')"/>
                        </div>
                        <div class="level-item has-text-centered">
                            <div class="select">
                                <select v-model="accesory.type">
                                    <option v-for="type in accesorytypes" :value="type">
                                        {{ type }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="level-item has-text-centered">
                            <input v-model="accesory.weight" class="input" :placeholder="$t('weight')"/>
                        </div>
                        <div class="level-item has-text-centered">
                            <input v-model="accesory.price" class="input" :placeholder="$t('price')"/>
                        </div>
                        <div class="level-item has-text-centered">
                            <button @click="showAccModal = !showAccModal" class="button is-success">
                                
                                <i class="fa-solid fa-plus"></i>
                                &nbsp;
                                {{ $t('add') }}
                                
                            </button>
                        </div>
                    </nav>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal" v-bind:class="{'is-active': showAccModal}" id="newelement-modal" style="--bulma-modal-content-width: 50%;">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title is-centered is-size-2">{{ $t('confirm_add_accessory') }}</p>
                    <button class="delete" aria-label="close" @click="showAccModal = false"></button>
                </header>
                <section class="modal-card-body has-text-centered">
                    <div class="notification is-success">
                        <button class="delete"></button>
                        {{ $t('check_correctness') }}
                    </div>
                    <nav class="level">
                        <div class="level-item has-text-centered">
                            <input v-model="accesory.name" class="input" :placeholder="$t('name')"/>
                        </div>
                        <div class="level-item has-text-centered">
                            <div class="select">
                                <select v-model="accesory.type">
                                    <option v-for="type in accesorytypes" :value="type">
                                        {{ type }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="level-item has-text-centered">
                            <input v-model="accesory.weight" class="input" :placeholder="$t('weight')"/>
                        </div>
                        <div class="level-item has-text-centered">
                            <input v-model="accesory.price" class="input" :placeholder="$t('price_pln')"/>
                        </div>
                    </nav>

                    <div class="label">{{ $t('description') }}</div>
                    <textarea v-model="accesory.description" :placeholder="$t('description')" class="textarea"></textarea>
                </section>

                <footer class="modal-card-foot">
                    <div class="buttons">
                        <button @click="handleAddButton();" class="button is-success">
                            <i class="fa-solid fa-plus"></i>
                            &nbsp;
                            {{ $t('add') }}
                        </button>
                        <button @click="showAccModal = !showAccModal;" class="button">
                            <i class="fa-solid fa-ban"></i>
                            &nbsp;
                            {{ $t('cancel') }}
                        </button>
                    </div>
                </footer>
            </div>
        </div>
    </div>

    <div class="modal" v-bind:class="{'is-active': saveReminder}" id="newelement-modal" style="--bulma-modal-content-width: 40%;">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title is-centered is-size-3">Zanim wyjdziesz!</p>
                    <button class="delete" aria-label="close" @click="saveReminder = false"></button>
                </header>
                <section class="modal-card-body has-text-centered is-size-5">
                    <div class="notification is-warning">
                        <button class="delete"></button>
                        Masz niezapisane zmiany w dziale akcesorii.
                        <br>
                        Poniższe akcesoria zostały zmienione:
                        
                    </div>

                   
                        <b-table :data="editedRowsArray" :columns="columns_reminder"></b-table>
                    
                    
                    



                </section>

                <footer class="modal-card-foot">
                    <nav class="level is-mobile" style="width: 100%;">

                        <!-- Left Section -->
                        <div class="level-left">
                            <div class="level-item">
                                <button @click="handleUpdateAccesories(accesorytype);" 
                                        class="button is-success">
                                    <i class="fa-solid fa-floppy-disk"></i>
                                    &nbsp;
                                    {{ $t('save') }}
                                </button>
                            </div>
                            <div class="level-item">
                                <button @click="saveReminder = !saveReminder;" class="button">
                                    <i class="fa-solid fa-ban"></i>
                                    &nbsp;
                                    {{ $t('cancel') }}
                                </button>
                            </div>
                        </div>
                
                        <!-- Right Section -->
                        <div class="level-right">
                            <div class="level-item">
                                <button @click="discardChanges()" class="button is-danger">
                                    Nie zapisuj i wyjdź&nbsp;
                                    <i class="fa-solid fa-arrow-right"></i>
                                </button>
                            </div>
                        </div>
                    </nav>
                </footer>
            </div>
        </div>
    </div>





</template>


<script setup>
import { useNewProjectStoreBeta } from '@/store/newproject'
import { storeToRefs } from 'pinia'
import { onMounted, ref, watch, onBeforeUnmount,computed} from 'vue'
import axios from 'axios'
import { toast } from 'bulma-toast'
import {validateFormData, validateNewAccesory} from '@/validators/Validators.js'

import { useRouter, useRoute, onBeforeRouteLeave } from 'vue-router'

const router = useRouter()

const showActiveAcc = ref(false)
const editMode = ref(false)
const showAccModal = ref(false)
const saveReminder = ref(false)
const newProjectStore = useNewProjectStoreBeta()
const tableKey = ref(0)
const accesory = ref({
  description: '',
  name: '',
  price: '',
  type: '',
  weight: ''
})
const typeChoices = ref([])
const errors = ref([])



//table variables
let isPaginated = true
let isPaginationSimple = true
let isPaginationRounded = false
let paginationPosition = 'bottom'
let defaultSortDirection = 'asc'
let sortIcon= 'arrow-up'
let sortIconSize= 'is-small'
let currentPage= 1
let perPage= 10
let hasInput= false
let paginationOrder= ''
let inputPosition= ''
let inputDebounce= ''

const filteredAccessories = computed(() => {
    return accesorytype.value.filter(acc => acc.is_active !== showActiveAcc.value)
})





const {loadData, addAccesorytype, updateAccesories} = newProjectStore
const {accesories, accesorytype} = storeToRefs(newProjectStore)


function getAccessoryTypes(accesoryList) {
  return [...new Set(accesoryList.flatMap(item => item.type_choices.map(choice => choice[0])))];
}

const accesorytypes = getAccessoryTypes(accesorytype.value)

function handleUpdateAccesories(accesorytype) {

const accesorytypes = getAccessoryTypes(accesorytype)
validateNewAccesory(accesorytype,errors,accesorytypes)

/* for ( let accesory of accesorytype) {
  console.log(accesory.name)
}
 */




if(!errors.value.length) {      


  const result = updateAccesories(accesorytype)
  

  if (result) {
    toast({
          message: `Poprawnie dodane nowe akcesoria`,
          duration: 5000,
          position: "top-center",
          type: 'is-success',
          animate: { in: 'backInDown', out: 'backOutUp' },
        })
        saveReminder.value = false
  }

  else {
    toast({
          message: `Czasy pracy nie zaktualizowane poprawnie`,
          duration: 5000,
          position: "top-center",
          type: 'is-danger',
          animate: { in: 'backInDown', out: 'backOutUp' },
        })
  }
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

function handleAddButton() {      

    let tempId = -1 //temporary ID for frontend new accesories
    const allTypeChoices = accesorytype.value.flatMap(item => item.type_choices) 
    const uniqueTypeChoices = [...new Set(allTypeChoices.map(JSON.stringify))].map(JSON.parse)

      const newAccesory = {
        description: accesory.value.description,
        id: tempId--,
        name: accesory.value.name,
        price: accesory.value.price,
        type: accesory.value.type,
        weight: accesory.value.weight,
        type_choices: uniqueTypeChoices,
        is_active: true
    }
    /* console.log("Accesorytype: ", accesorytype.value)
    console.log("NewAcc:" , newAccesory) */

    //error CHECKING HERE
    console.log(accesorytypes)
    validateNewAccesory(newAccesory,errors,accesorytypes)

    if (newAccesory.name.trim() === '') {
      errors.value.push("Błędna nazwa")
    }
    if (newAccesory.type.trim() === '') {
      errors.value.push("Błędna typ")
    }
    if (newAccesory.weight.trim() === '' || newAccesory.weight.trim() <= 0) {
      errors.value.push("Błędna waga")
    }
    if (newAccesory.price.trim() === '' || newAccesory.price.trim() <= 0) {
      errors.value.push("Błędna cena")
    }

    if (!errors.value.length) {
      addAccesorytype(newAccesory)
      tableKey.value += 1 //Refreshing table data 
      showAccModal.value = false
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

    function handleDeleteButton(row){
      const index = accesorytype.value.findIndex(item => item.id === row.id)
      accesorytype.value[index].is_active = false
      //accesorytype.value.splice(index, 1)
      tableKey.value += 1 //refreshing the table
    }






let originalArray = [...accesorytype.value]

const editedRows = ref(new Set())
const pendingRoute = ref(null)

const editedRowsArray = computed(()=> [...editedRows.value])
const markAsEdited = (row) => {
    editedRows.value.add(row)
}





onBeforeRouteLeave(async (to, from) => {

//console.log("editedRows value:", editedRows.value);
//console.log("Before if",editedRows.value.size)

if (editedRows.value.size > 0) 
{
console.log("After if ", editedRows.value.size)
saveReminder.value = true // open modal
pendingRoute.value = to;
return new Promise((resolve, reject) => {
    const unwatch = watch(saveReminder, (val)=> {
        if (!val) {
            unwatch()
            reject()
            editedRows.value = new Set()
            router.push(pendingRoute.value.fullPath)
            pendingRoute.value = null

            console.log("CLEARING if!val")
        } else {
            unwatch()
            resolve()
            editedRows.value = new Set()
            router.push(pendingRoute.value.fullPath)
            console.log("CLEARING else")
        }
    })
}) 
}  

/* else if(editedRows.value.size === 0) {
editedRows.value = new Set()
console.log("CLEARING elif")

} */

})

function discardChanges() {

console.log('Discarding changes')
saveReminder.value = false
router.push(pendingRoute.value.fullPath)

}

const preventNavigation = (event) => {
    if (editedRows.value) {
        event.preventDefault();
        event.returnValue = ''; // Trigger browser confirmation dialog
    }
};

onMounted(() => {
    loadData()
    /* window.addEventListener('beforeunload', preventNavigation); */
})

onBeforeUnmount (() => {
   /*  window.removeEventListener('beforeunload', preventNavigation); */
    console.log("Before unmount")
})


let columns = [
    { 
    field: 'name', 
    label: 'Nazwa',
    searchable: true,
    sortable: true
    },
    { 
    field: 'type', 
    label: 'Typ',
    searchable: true,
    sortable: true
    },
    { 
    field: 'weight', 
    label: 'Waga',
    searchable: true,
    sortable: true
    },
    {  
    field: 'price', 
    label: 'Cena',
    searchable: true,
    sortable: true
    },
    {
    field: 'nawigacja',
    label: 'Nawigacja',
    centered: true
    }
]

let columns_reminder = [
    { 
    field: 'name', 
    label: 'Nazwa',
 
    },
    { 
    field: 'type', 
    label: 'Typ',

    },
    { 
    field: 'weight', 
    label: 'Waga',

    },
    {  
    field: 'price', 
    label: 'Cena',
    sortable: true

    },


]
</script>
<style>

</style>