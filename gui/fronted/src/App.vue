<script setup lang="ts">

import MyFooter from './views/MyFooter.vue';
import CanvasContainer from './components/CanvasContainer.vue'
import {ref} from 'vue'
import ResultsContainer from './components/ResultsContainer.vue';
// startSSE()
const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

</script>

<template>

  <div class="common-layout">
    <el-container>
      <el-header class="header">
        <!-- Logo -->
        <div class="header__logo">
          <img src="./assets/logo.png" alt="My App" />
        </div>
        <div class="header_title">
          <h1>
            Battery Sizing Optimization
          </h1>
        </div>

       
    </el-header>
      <el-container>
        <el-tabs :tab-position="'left'"  class="tabs">
          <el-tab-pane label="Modeling"><CanvasContainer/></el-tab-pane>
          <el-tab-pane label="Simulation Result"><ResultsContainer/></el-tab-pane>
          <el-tab-pane label="Model Test">Sensitivity Analysis</el-tab-pane>
      </el-tabs>
      </el-container>
      <MyFooter/>
    </el-container>
  </div>
</template>
<style scoped>
/* .aside{
  height: 100%;
  width: 200px; 
} */
.tabs{
  width: 100%;
}
.header {
  display: flex;
  /* justify-content: space-between; */
  align-items: center; 
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24); 
}
.header_title{
  margin-left: 50px;
  text-align: center;
}
.header__logo {
  margin-left: 1rem;
  font-size: 1.5rem;
}

.header__logo img {
  height: 40px;
}
</style>
