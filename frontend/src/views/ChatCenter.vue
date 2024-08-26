<script setup lang="ts">
import { ref } from 'vue';
import ChatList from '@/components/ChatCenter/ChatList.vue';
import ChatDetail from '@/components/ChatCenter/ChatDetail.vue';

const selectedGroup = ref(null);

const updateSelectedGroup = (group: any) => {
    selectedGroup.value = group;
};
</script>

<template>
    <div class="chat-center-container">
        <div class="center-left">
            <ChatList @update-selected-group="updateSelectedGroup"/>
        </div>
        <div class="center-right">
            <ChatDetail v-if="selectedGroup" :group="selectedGroup" :key="selectedGroup.id"/>
        </div>
    </div>
</template>

<style scoped>
.chat-center-container {
    padding-top: 20px;
    padding-left: 30px;
    width: 100%;
    display: flex;
    margin-top: 10px;
    margin-bottom: 10px;
    height: calc(100vh - 82px);  /* 让这个视图高度正好撑满整个屏幕*/
}
.center-left {
    width: 30%;
    border-radius: 10px;
    background-color: rgb(240, 248, 255);
}

.center-right {
    width: 70%;
    border-radius: 10px;
    background-color: rgb(240, 248, 255);
    margin-left: 10px;
    margin-right: 10px;
}
</style>