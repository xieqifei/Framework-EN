<template>
    <el-drawer :value="drawerActive" @input="$emit('onDrawerChange', $event.target.value)" title="I am the title" :with-header="false" @close="onCloseDrawer">
      <el-scrollbar height="100%">
        <li v-for="(param,key,index) in props.model?.properties">
          <label name="param.value" >{{param.name}}</label>
          <el-select v-if="key.toString().indexOf('node') !== -1" v-model="param.value" class="m-2" placeholder="Select" style="width: 100%;">
            <el-option
              v-for="edge in props.edges"
              :key="edge.id"
              :label="edge.properties.name.value"
              :value="edge.id"
            />
          </el-select>
          <el-input v-else v-model="param.value" >
            <template #append v-if="param.unit ">{{ param.unit }}</template>
          </el-input>
        </li>
      </el-scrollbar>
    </el-drawer>
</template>

<script setup lang="ts">import { ref } from 'vue';

    const props = defineProps({
      drawerActive: Boolean,
      model: Object,
      edges: Object
    })

    const active = ref<boolean>(false)

    const emit = defineEmits(['updateProperties'])
    
    // close drawer and update parameters of models
    const onCloseDrawer = (event:Event)=>{
      emit('updateProperties', props.model)
    }

</script>

<style>

</style>