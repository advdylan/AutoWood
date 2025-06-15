import { createRouter, createWebHistory } from 'vue-router'

import ProjectsList from '../views/ProjectsList.vue'
import NewProjectDetail from '../views/NewProjectDetail.vue'
import PricesSetup from '@/views/PricesSetup.vue'
import Accessories from '@/views/Accessories.vue'
import Home from '@/views/Home.vue'
import NewProjectProgress from '@/views/NewProjectProgress.vue'
import CutOptimizer from '@/views/CutOptimizer.vue'
import Warehouse from '@/views/Warehouse.vue'
import Production from '@/views/Production.vue'
import CatalogList from '@/views/CatalogList.vue'
import CatalogProductDetail from '@/views/CatalogProductDetail.vue'


const routes = [
  
  {
    path: '/new-project',
    name: 'NewProject',
    component: NewProjectProgress,
  },
  {
    path: '/new-project-progress',
    name: 'NewProjectProgress',
    component: NewProjectProgress,

  },

  {
    path: '/new-project/:id',
    name: 'NewProjectDetail',
    component: NewProjectDetail
  },

  {
    path: '/catalog-product/:id',
    name: 'CatalogProductDetail',
    component: CatalogProductDetail
  },

  {
    path: '/projects-list',
    name: 'ProjectsList',
    component: ProjectsList
  },
  {
    path: '/catalog-list',
    name: 'CatalogList',
    component: CatalogList
  },
  {
    path: '/prices-setup',
    name: 'PriceSetup',
    component: PricesSetup
  },
  {
    path: '/accessories',
    name: 'Accessories',
    component: Accessories
  },
  {
    path: '/cut-optimizer',
    name: 'CutOptimizer',
    component: CutOptimizer
  },
  {
    path: '/warehouse',
    name: 'Warehouse',
    component: Warehouse
  },
  {
    path: '/production',
    name: 'Production',
    component: Production
  },
  {
    path: '/',
    name: 'Home',
    component: Home,

  }
  
 
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
