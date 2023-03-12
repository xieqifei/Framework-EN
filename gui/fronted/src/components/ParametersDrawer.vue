<template>
    <el-drawer :value="drawerActive"  title="Parameters" :with-header="false" @close="onCloseDrawer">
      <el-scrollbar height="100%">
        <li v-for="(param,key,index) in props.elem?.properties">
          <label name="param.value" >{{param.name}}</label>
          <el-select v-if="key.toString().startsWith('node')" v-model="param.value" class="m-2" placeholder="Select" style="width: 100%;">
            <el-option
              v-for="node in props.nodes"
              :key="node.id"
              :label="node.properties.name.value"
              :value="node.id"
            />
          </el-select>
          <el-input v-else v-model="param.value" >
            <template #append v-if="param.unit ">{{ param.unit }}</template>
          </el-input>
        </li>
      </el-scrollbar>
    </el-drawer>
</template>

<script setup lang="ts">
    const props = defineProps({
      drawerActive: Boolean,
      elem: Object,
      nodes: Object
    })

    const emit = defineEmits(['updateProperties'])
  
    // close drawer and update parameters of models
    const onCloseDrawer = (event:Event)=>{
      emit('updateProperties', props.elem)
    }

    
    
</script>

<style>

</style>