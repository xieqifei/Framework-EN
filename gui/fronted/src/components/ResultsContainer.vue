<template>
    <el-container>
        
        <el-main>
            <el-scrollbar height="85vh">
                <div>
                    Power Flowing Through Nodes
                </div>
                <el-scrollbar>
                    <div class="scrollbar-flex-content" id="node-result-container">
                        
                    </div>
                </el-scrollbar>
                <div id="element-result-figure-container">

                </div>
            </el-scrollbar>
        </el-main>
    </el-container>   
</template>

<script setup lang="ts">


</script>

<style scoped>
.scrollbar-flex-content {
    display: flex;
}

.scrollbar-demo-item {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 50px;
    margin: 10px;
    text-align: center;
    border-radius: 4px;
    background: var(--el-color-danger-light-9);
    color: var(--el-color-danger);
}
</style>