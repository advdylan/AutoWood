<template>
  
  
<form @submit.prevent="submitForm">
            
            <nav class="level">

 
          <div class="field">
            <label class="label has-text-centered">{{ $t("name")}}</label>
            <div class="control">
              <input class="input is-small"  v-model="newElement.element.name">             
            </div>
          </div>

          <div class="field">
            <label class="label has-text-centered">X</label>
            <div class="control">
              <input class="input is-small"  v-model="newElement.element.dimX">           
            </div>
          </div>

          <div class="field">
            <label class="label has-text-centered">Y</label>
            <div class="control">
              <input class="input is-small" v-model="newElement.element.dimY" >             
            </div>
          </div>

          <div class="field">
            <label class="label has-text-centered">Z</label>
            <div class="control">
              <input class="input is-small"   v-model="newElement.element.dimZ">             
            </div>
          </div>

          <div class="field">
            <label class="label has-text-centered">{{ $t("quantity")}}</label>
            <div class="control">
              <input class="input is-small"   v-model="newElement.quantity" >             
            </div>
          </div>

          <div class="field">
            <label class="label has-text-centered">{{ $t("wood_type")}}</label>
            <div class="control">
              <div class="select is-small">
                <select v-model="newElement.element.wood_type">
                  <option v-for="woodItem in wood" :key="woodItem.id" :value="woodItem">
                    {{ woodItem.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

            <div class="field" style="padding-top: 1.15rem;">
              <button type="submit"  class="button is-success is-small"><i class="fa-solid fa-plus"></i></button>
           
            </div>
            </nav>    
          
      </form>
      <section v-if="elements.length">
  
    <div class="columns">
      <div class="column is-half is-centered">
        
      </div>
    </div>
  
</section>

  <div v-if="elements.length">
  <b-table :key="tableKey" :data="elements" :paginated="isPaginated" :per-page="perPage" :current-page.sync="currentPage" :pagination-simple="isPaginationSimple" :pagination-position="paginationPosition" :default-sort-direction="defaultSortDirection" :pagination-rounded="isPaginationRounded" :sort-icon="sortIcon" :sort-icon-size="sortIconSize" default-sort="user.first_name" aria-next-label="Next page" aria-previous-label="Previous page" aria-page-label="Page" aria-current-label="Current page" :page-input="hasInput" :pagination-order="paginationOrder" :page-input-position="inputPosition" :debounce-page-input="inputDebounce">

  <b-table-column > 
    <template  #default="props">
      <input class="input is-small"  v-model="props.row.element.name"/>
    </template> 

  </b-table-column>

  <b-table-column >
    <template  #default="props">
      <input class="input is-small"  v-model="props.row.element.dimX"/>
    </template> 
  </b-table-column>

  <b-table-column >
    <template #default="props">
      <input class="input is-small"  v-model="props.row.element.dimY"/>
    </template> 
  </b-table-column>
  
  <b-table-column >
    <template #default="props">
      <input class="input is-small"  v-model="props.row.element.dimZ"/>
    </template> 

  </b-table-column>

  <b-table-column >
    <template #default="props">
      <div class="select is-small">
        <select v-model="props.row.element.wood_type" :placeholder="$t('wood_type')">
        <option
          v-for="woodItem in wood"
          :value="woodItem"
          :key="woodItem.id">
        {{ woodItem.name }}</option>
      </select>
      </div>
    </template>

  </b-table-column>

  <b-table-column >
    <template #default="props">
      <input class="input is-small"  v-model="props.row.quantity"/>
    </template> 
  </b-table-column>

  <b-table-column >
    <template #default="props">
      <b-button @click="handleDeleteButton(props.row)" type="is-danger is-small" icon-left="x">    
      </b-button>
    </template>
 


  </b-table-column>
</b-table>                            
</div>

</template>



<script>
export default {
  name: 'ElementsTable', 
}
</script>


<script setup>
import { computed, ref } from 'vue'
import { useNewProjectStoreBeta } from '@/store/newproject'
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { toast } from 'bulma-toast';

const store = useNewProjectStoreBeta()
const { elements,wood} = storeToRefs(store)
const {deleteElement, addElement} = store

//table variables
const editMode = ref(false)
const errors = ref([])
let isPaginated = false
let isPaginationSimple = false
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
const tableKey = ref(0)
const hoveredRow = ref()

const props = defineProps({
  elements: Array,
  default: () => [],
  required: true
})

const { t } = useI18n();

const columns = computed(() => [
  { field: 'element.name', label: t('name'), sortable: true, searchable: true, },
  { field: 'element.dimX', label: t("length"), sortable: true, searchable: true, },
  { field: 'element.dimY', label: t("width"), sortable: true, searchable: true, },
  { field: 'element.dimZ', label: t('thickness'), sortable: true, searchable: true, },
  { field: 'element.wood_type.name', label: t('wood_type'), sortable: true, searchable: true, },
  { field: 'quantity', label: t('quantity'), sortable: true },
  { field: 'nav', label: 'nav', sortable: false, centered: true },
]);

// why didnt I use Pinia here?
const sendValueToParent = () => {
      emit('updateValue', childValue.value);
    };

function handleDeleteButton(row){
      console.log(row)
      const index = elements.value.findIndex(item => item.element.name === row.element.name)
      elements.value.splice(index, 1)
      tableKey.value += 1 //refreshing the table
    }


    const submitForm = () => {

 

if( elements.value.length > 0) {
  for ( let accName of elements.value){
    if(newElement.value.element.name === accName.element.name) {
      errors.value.push('Projekt zawiera element o takiej nazwie. Zmień nazwę')
    }
  }
} 


if (newElement.value.element.dimX <= 0) {
  errors.value.push('Podaj długość większą niż 0')
}
if (typeof newElement?.value?.element?.name !== 'string' || newElement.value.element.name.trim() === '') {
  errors.value.push('Podaj właściwą nazwę')
}
if (newElement.value.element.dimY <= 0) {
  errors.value.push('Podaj wysokość większą niż 0')
}
if (newElement.value.element.dimZ <= 0) {
  errors.value.push('Podaj grubość większą niż 0')
}
console.log(newElement.value.element.wood_type)
if (newElement.value.element.wood_type == '') {
  errors.value.push('Wybierz materiał')
}

if (!errors.value.length) {
  addElement(newElement.value);
newElement.value = {
  element: {
    name: 'Przód',
    dimX: 2500,
    dimY: 250,
    dimZ: 25,
    wood_type: ''
          },
  quantity: 1
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


const newElement = ref({
      element: {
      name: 'Przód',
      dimX: 200,
      dimY: 250,
      dimZ: 25,
      wood_type: ''
      },
      quantity: 7
})
</script>
<style>

.delete-column {
  width: 10px; 
  text-align: center;
}

.delete-column b-button {
  padding: 0;
}

.rectangle-title {
  height: 50px;
  width: 500px;
  background-image: linear-gradient(khaki, rgb(93, 139, 115) );
}

.hero.is-primary {
  background-color:rgb(141, 188, 164);
  border-radius: 5px;
}

.control {
  padding-left: 0.3rem;
  padding-right: 0.75rem;
}




</style>


