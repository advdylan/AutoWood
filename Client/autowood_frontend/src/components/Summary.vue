<template>
    <div class="columns">
        <div class="column is-half">





          <div class="card">
            <header class="card-header">
              <p class="card-header-title is-size-5">{{ $t("cost_summary")}}</p>
    
            </header>
            <div class="card-content">
              <div class="content">
                

                <table class="table is-bordered is-striped is-hoverable is-fullwidth">
                  <thead>
                    <tr>
                      <th class="title is-size-6">{{ $t("elements_costs") }}</th>        
                    </tr>    
                  </thead>
                  
                  <tfoot>
     
                  </tfoot>
                  <tbody>
                    <th class="title is-size-6">{{ $t("sum") }}: {{ summElementCosts }} zł </th>
                    
                  </tbody>
                  
                </table>
  
                <table class="table is-bordered is-striped is-hoverable is-fullwidth">
                  <thead>
                    <tr>
                      <th class="title is-size-6">{{ $t("accessories_margin") }}</th>
                      </tr>
                  </thead>
                  
                  <tfoot>
  
                                 
                  </tfoot>
                  <tbody>
                    <th class="title is-size-6">{{ $t("sum") }}: {{ summAccesoriesCosts }} zł </th>
                              
                    
                  </tbody>
                  
                </table>
  
                <table class="table is-bordered is-striped is-hoverable is-fullwidth">
                  <thead>
                    <th class="title is-size-6">{{ $t("section") }}</th>
                    <th class="title is-size-6">{{ $t("time") }}</th>
                    <th class="title is-size-6">{{ $t("rate") }}</th>
                    <th class="title is-size-6">{{ $t("summary") }}</th>

                  </thead>
                  <tbody>

                      <tr v-for="worktime in worktimeCost">
                        <th> {{worktime.text}}</th>
                        <th> {{worktime.hours}} h</th>
                        <th> {{worktime.value}} zł/h</th>
                        <th> {{worktime.sum}} zł</th>
                      </tr>
                      <tr>
                        <th>{{ $t("summary") }} </th>
                        <th></th>
                        <th></th>
                        <th> {{ summWorktimeCosts }} zł</th>
                      </tr>
                  </tbody>
                </table>

                <table class="table is-bordered is-striped is-hoverable is-fullwidth">
                  <thead>
                    <tr>
                      <th class="title is-size-6">{{ $t("summary") }}</th>        
                    </tr>    
                  </thead>
                  <tbody>
                    <tr>
                      <th> {{ $t("sum") }}: {{ summaryCosts}}</th>
                    </tr>
                    <tr>
                      <th v-if="marginA"> {{ $t("elements_margin") }} : {{ parseFloat(elementsMargin).toFixed(2) }}
                      
                      </th>
                    </tr>
                    <tr>
                      <th v-if="marginB"> {{ $t("accessories_margin") }}: {{ parseFloat(accesoriesMargin).toFixed(2)}}</th>
                    </tr>
                    <tr>
                      <th v-if="marginC">{{ $t("additional_margin") }}: {{ parseFloat(additionalMargin).toFixed(2) }}</th>
                    </tr>
                    <tr>
                      <th v-if="marginC || marginB || marginA">{{ $t("summary_with_margin") }}: {{ parseFloat(summaryCostsWithMargin).toFixed(2) }}</th>
                    </tr>

                  </tbody>
                  
                </table>
                <slot>
            
                </slot>

          </div>
          
              </div>
            </div>
          
          </div>



        <div class="column">
          <div class="card">
            <header class="card-header">
              <p class="card-header-title is-size-5">{{ $t("margin_%") }}</p>           
            </header>
            <div class="card-content">
              <div class="content">
                <div class="field">
                  <label class="label">{{ $t("elements_margin") }}</label>
                  <div class="control">
                    <input v-model="marginA" class="input" type="text" :placeholder="$t('margin_%')">                  
                  </div>           
                  <label class="label">{{ $t("accessories_margin") }}</label>
                  <div class="control">
                    <input v-model="marginB" class="input" type="text" :placeholder="$t('margin_%')">                  
                  </div>
                  <label  class="label">{{ $t("additional_margin") }}<strong class="is-underlined">({{ $t("apply_warning") }})</strong></label>
                  <div class="control">
                    <input v-model="marginC" class="input" type="text" :placeholder="$t('margin_%')">                  
                  </div>
                </div>
              </div>
            </div>

          </div>

        </div>
        
    </div>
  

      
  </template>
  
  <script>
  export default {
    name: 'Summary'
  }
   
  </script>
  
  <script setup>
  import { useNewProjectStoreBeta } from '@/store/newproject'
  import { useSummaryStore } from '@/store/summary'
  import { computed, ref, watch, watchEffect } from 'vue'
  import { storeToRefs } from 'pinia'
  
  

  const props = defineProps({
    propMarginA: Number,
    propMarginB: Number,
    propMarginC: Number,
    propElements: Array,
    propAccesories: Array,
    propWorktimecosts: Array,
  })

  

  const store = useNewProjectStoreBeta()
  const summaryStore = useSummaryStore()
  

  const {elements, wood, pricedElements, accesoriesStore, worktimeCost, marginA, marginB, marginC} = storeToRefs(store)
  const { accesoriesCost, elementsCost } = storeToRefs(summaryStore)

  watch(
  () => props.propElements,
  (newElements) => {
    if (newElements && Array.isArray(newElements)) {
      store.setElements(newElements);
    }
  },
  { immediate: true }
);

watch(
  () => props.propAccesories,
  (newAccesories) => {
    if (newAccesories && Array.isArray(newAccesories)) {
      store.setAccesories(newAccesories);
    }
  },
  { immediate: true }
);


watch(
  () => props.propWorktimecosts,
  (newWorktime) => {
    store.setBoxesViaProps(newWorktime)
  }
)

if (props.propWorktimecosts) {
  store.setBoxesViaProps(props.propWorktimecosts)

}

watch(() => props.propMarginA, (newMarginA) => {
  marginA.value = newMarginA
}, { immediate: true })

watch(() => props.propMarginB, (newMarginB) => {
  marginB.value = newMarginB
}, { immediate: true })

watch(() => props.propMarginC, (newMarginC) => {
  marginC.value = newMarginC
}, { immediate: true })


 const summElementCosts = computed(() => {
  return pricedElements.value.reduce((n, {price}) => n + parseFloat(price), 0).toFixed(2)
  
 })
  
 const summAccesoriesCosts = computed(() => {
  return accesoriesStore.value.reduce((n, {sum}) => n + parseFloat(sum), 0).toFixed(2)
 })

const summWorktimeCosts = computed(() => {
  return worktimeCost.value.reduce((n, {sum}) => n + parseFloat(sum), 0).toFixed(2)
  
})

const summaryCosts = computed(() => {
  return (parseFloat(summWorktimeCosts.value) + parseFloat(summElementCosts.value) + parseFloat(summAccesoriesCosts.value)).toFixed(2)
})

const elementsMargin = computed(() => {
  let margin = ((parseFloat(summElementCosts.value) * parseInt(marginA.value)) / 100)
  return margin
})

const accesoriesMargin = computed(() => {
  let margin = ((parseFloat(summAccesoriesCosts.value) * parseInt(marginB.value)) / 100)
  return margin
})

const additionalMargin = computed(() => {
  let margin = ((parseFloat(summWorktimeCosts.value)+ parseFloat(summElementCosts.value) + parseFloat(summAccesoriesCosts.value)) * parseInt(marginC.value) / 100)
  return margin
})

const summaryCostsWithMargin = computed(() => {
  let sum = ((parseFloat(summaryCosts.value) + parseFloat(elementsMargin.value || 0) + parseFloat(accesoriesMargin.value || 0) + parseFloat(additionalMargin.value || 0)))
  return sum

})

watchEffect(() => {
summaryStore.setSummaryCosts(summaryCosts.value)
summaryStore.setElementsMargin(elementsMargin.value)
summaryStore.setAccesoriesMargin(accesoriesMargin.value)
summaryStore.setAdditionalMargin(additionalMargin.value)
summaryStore.calculateSummaryCostsWithMargin(summaryCostsWithMargin.value)
summaryStore.setElementsCost(summElementCosts.value)
summaryStore.setAccesoriesCost(summAccesoriesCosts.value)
summaryStore.setWorktimeCost(summWorktimeCosts.value)
})


  </script>
  
  
  
  