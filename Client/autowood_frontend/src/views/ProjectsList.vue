<template>
    <div class="projects-list-container">
        <b-table :data="data">
            <template v-for="column in columns" :key="column.id">
                <b-table-column v-bind="column">
                    <template v-if="column.searchable && !column.numeric" #searchable="props">
                        <b-input
                            v-model="props.filters[props.column.field]"
                            :placeholder="$t('search')"
                            icon="magnify"/>
                    </template>
                    <template v-slot="props">
                        
                        <template v-if="column.field === 'nawigacja'">
                            <router-link :to="{ name: 'NewProjectDetail', params: { id: props.row.id } }">
                                <b-button icon-right="circle-info">{{$t("details")}}</b-button>                               
                            </router-link>

                            <b-button 
                            @click="toggleAddToProduction = !toggleAddToProduction, setChosenProduct(props.row)"
                             icon-right="add">{{ $t("production") }}
                            </b-button>

                            <b-button @mouseenter="hoveredProjectId = props.row.id"
                             @mouseleave="hoveredProjectId = null" 
                             @click="$emit('getElements', props.row.id)" 
                             :value=props.row.id 
                             v-if="searchModal" 
                             icon-right="file-arrow-down"
                             >{{ $t("get_elements") }}
                            </b-button>
                            
                            <teleport to="body">
                            <div 
                            v-if="hoveredProjectId === props.row.id" 
                            class="notification is-info elements-list" 
                            >
                            <ul>
                                <li v-for="element in props.row.elements" :key="element.id">
                                X: {{ element.element.dimX }} Y: {{ element.element.dimY }} Z: {{ element.element.dimZ }} {{ $t("quantity") }}: {{ element.quantity }}
                                </li>
                            </ul>
                            </div>
                            </teleport>

                        </template>
                        <template v-else>
                        {{ props.row[column.field] }}
                    </template>
                    
                </template>
                </b-table-column>
            </template>
        </b-table>
    </div>




    <div v-bind:class="{'is-active': toggleAddToProduction}" class="modal" style="--bulma-modal-content-width: 30%;">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">{{$t('add_to_production')}}</p>
            <button @click="toggleAddToProduction = !toggleAddToProduction" class="delete" aria-label="close"></button>
          </header>
          <section class="modal-card-body has-text-centered">

           <div class="card-content">
            <div class="columns">
                <div class="column">

                </div>

            </div>
        </div>
          </section>

          <footer class="modal-card-foot">
            <div class="buttons">
            </div>
          </footer>
        </div>
      </div>
    
</template>

<script setup>
import { useProjectsListStore } from '@/store/projectslist'
import { storeToRefs } from 'pinia'
import { ref} from 'vue'


const ProjectsListStore = useProjectsListStore()

const { loadProjects, loadDetailProject } = ProjectsListStore
const { projectlist, data, columns } = storeToRefs(ProjectsListStore)
const hoveredProjectId = ref(null)
const toggleAddToProduction = ref(false)
const chosenProductId = ref(null)


const propsList =  defineProps({
    searchModal: Boolean,
    default: false
})


loadProjects()


function setChosenProduct(order) {
    console.log(order);

}
</script>
<style>
.elements-list {
  position: fixed; /* Position relative to the viewport */
  width: 50%;
  top: 10%; /* Adjust based on desired position */
  left: 50%; /* Adjust based on desired position */
  transform: translate(-50%, 0); /* Center horizontally */
  z-index: 1000; /* Ensure it's on top */
  background-color: #209cee; /* Bulma's info color */
  color: white; /* Text color for better visibility */
  padding: 1rem; /* Add padding for aesthetics */
  border-radius: 5px; /* Optional: round corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add a shadow for a floating effect */
}
</style>