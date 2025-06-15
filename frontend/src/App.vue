<template>
  
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/animate.css@4.0.0/animate.min.css"
  />  
  
  <div class='container is-fluid is-fullheight'>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link to="/"><a class="navbar-item" href="http://localhost:8080/">
        <div class="is-size-3"> 
           | Auto-Wood |
        </div>
      </a> </router-link>
      
  
      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" @click="showMobile = !showMobile">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
  
    <div id="navbarBasicExample" class="navbar-menu" v-bind:class="{'is-active': showMobile}">
      <div class="navbar-start">
        
        <router-link to="/production" class="navbar-item">      
            <i class="fa-solid fa-hammer fa-lg"></i>
            <div class="is-size-5">
              &nbsp;{{ $t("production")}}
            </div>
          </router-link>

          <div class="navbar-item has-dropdown is-hoverable">

            <router-link to="/projects-list" class="navbar-link">
              <i class="fa-solid fa-book fa-lg"></i>
            <div class="is-size-5"> 
              &nbsp; {{ $t("catalog")}}         
            </div>
            </router-link>

            <div class="navbar-dropdown is-dark fa-lg">
            <router-link to="/new-project" class="navbar-item">
              {{ $t("new_product")}}   
            </router-link>
            <hr class="navbar-divider">
            <router-link to="/catalog-list" class="navbar-item">
              {{ $t("catalog_list")}}   
            </router-link>

          </div>       
          </div>

        <div class="navbar-item has-dropdown is-hoverable">


          <router-link to="/projects-list" class="navbar-link">
          <i class="fa-solid fa-file-pen fa-lg">
          </i>
          <div class="is-size-5"> 
            &nbsp; {{ $t("projects")}}         
          </div>
        </router-link>

        <div class="navbar-dropdown is-dark fa-lg">
          <router-link to="/new-project" class="navbar-item">
            {{ $t("new_project")}}   
          </router-link>
          <hr class="navbar-divider">
          <router-link to="/projects-list" class="navbar-item">
            {{ $t("projects_list")}}   
          </router-link>
        </div>       
        </div>
  
  
        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">
            <i class="fa-solid fa-coins fa-lg">
            </i>
            <div class="is-size-5"> 
              &nbsp; {{ $t("prices_setup")}}
            </div>
          </a>
          <div class="navbar-dropdown">            
              <router-link to="/prices-setup" class="navbar-item">
                {{ $t("labor_costs")}}
              </router-link>

          </div>
          
        </div>
        <router-link to="/accessories" class="navbar-item">      
          <i class="fa-solid fa-screwdriver-wrench fa-lg"></i>
          <div class="is-size-5">
            &nbsp;{{ $t("accesories")}}
          </div>
        </router-link>

       
        <router-link to="/warehouse" class="navbar-item">  
          <i class="fa-solid fa-warehouse fa-lg"></i>
          <div class="is-size-5">
            &nbsp;{{ $t("warehouse")}}
          </div>
        </router-link>

        
        
        
      </div>
      
      <div class="navbar-end">
        <div class="navbar-item has-dropdown is-hoverable">
          <router-link to="/projects-list" class="navbar-link">
          
          <div class="is-size-5"> 
             {{ $t("tools")}}  &nbsp;       
          </div>

        </router-link>
        <div class="navbar-dropdown is-dark fa-lg">
          <router-link to="/cut-optimizer" class="navbar-item">
            {{ $t("cut-optimizer")}}   
          </router-link>

        </div>       
        </div>
        <div class="navbar-item">
          <figure class="image is-32x32">
            <img  @click="changeLanguage('pl')" class="is-rounded" :src="`${publicPath}poland.png`"/>
          </figure>
        </div>
        <div class="navbar-item">
          <figure class="image is-32x32">
            <img @click="changeLanguage('en')" class="is-rounded" :src="`${publicPath}united-kingdom.png`"/>
          </figure>
        </div>
        
        

      </div>
  
      
    </div>
  </nav>

  <section class="section">
    <router-view/>
  </section>

  
  <footer class="footer">
    <div class="content has-text-centered">
      <p>
        <strong>| Auto-Wood |</strong> by Dylan.
        The source code is licensed
        <a href="https://opensource.org/license/mit">MIT</a>. The
        website content is licensed
        <a href="https://creativecommons.org/licenses/by-nc-sa/4.0//"
          >CC BY NC SA 4.0</a
        >.
      </p>
    </div>
  </footer>

</div>

 
</template>

<script>
import { useI18n } from 'vue-i18n'

export default {
  metaInfo: {
    title: 'Auto-Wood - Your Woodworking Solution',
    titleTemplate: '%s | Auto-Wood'
  },
  
  data() {
    
    const { locale } = useI18n()

    function changeLanguage(language) {
      locale.value = language
    }
    

    return {
      showMobile: false,
      publicPath: process.env.BASE_URL,
      changeLanguage
    }
  }
}


</script>



<style lang="scss">




</style>

