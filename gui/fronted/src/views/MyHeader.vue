<template>
  <el-header class="header">
      <!-- Logo -->
      <div class="header__logo">
        <img src="../assets/logo.svg" alt="My App" />
      </div>
      Header
      <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        :ellipsis="false"
        @select="handleSelect"
      >
      <el-menu-item index="0">Dashboard</el-menu-item>
      <el-menu-item index="1">Result</el-menu-item>
    </el-menu>
  </el-header>
</template>

<style>
/* 样式仅适用于此组件 */
.header {
  /* display: flex;
  justify-content: space-between;
  align-items: center;  */
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24); 
}

/* .header__logo {
  margin-left: 1rem;
  font-size: 1.5rem;
} */

/* .header__logo img {
  height: 100%;
} */
</style>


<script lang="ts" setup>
import {ref} from 'vue'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}



</script>