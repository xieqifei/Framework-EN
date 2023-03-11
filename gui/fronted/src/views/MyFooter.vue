<template>
    <footer class="footer">
        <span class="footer__item">Copyright - Qifei</span>
    </footer>
  </template>
  
  <style scoped>
  /* 样式仅适用于此组件 */
  .footer {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    height: 60px;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 9;
  }
  
  .footer__logo img {
    height: 40px;
  }
  
  .footer__nav {
    margin-right: 1rem;
  }
  
  .footer__list {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
  }
  
  .footer__item {
    margin-left: 1rem;
  }
  
  .footer__link {
    color: #333;
    text-decoration: none;
    transition: color 0.2s ease-in-out;
  }
  
  .footer__link:hover {
    color: #777;
  }
  </style>
  
  
  <script lang="ts" setup>

 
  
  </script>