<template>
    <el-drawer :value="outDrawerActive"  title="Model Test" :with-header="false" @close="onCloseDrawer" size="60%">
      <el-scrollbar height="100%">
        
      </el-scrollbar>
      <el-drawer
        v-model="innerDrawerActive"
        title=""
        :append-to-body="true"
      >
        <p>_(:зゝ∠)_</p>
      </el-drawer>
    </el-drawer>
</template>

<script setup lang="ts">import { ref } from 'vue';

    const props = defineProps({
      outDrawerActive: Boolean,
      elem: Object,
      nodes: Object
    })

    const innerDrawerActive = ref(false)
    const emit = defineEmits(['updateProperties'])
  
    // close drawer and update parameters of models
    const onCloseDrawer = (event:Event)=>{
      emit('updateProperties', props.elem)
    }

    
    
</script>

<style>

</style>