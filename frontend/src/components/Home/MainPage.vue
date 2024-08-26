<template>
    <!-- 版心 -->
    <div class="mainPage-container">
        <!-- 选项按钮 -->
        <div class="tabs">
            <button @click="activeTab = 'collects'" :class="{ active: activeTab === 'collects' }">
                <i></i> 收藏文档
            </button>
            <button @click="activeTab = 'pictures'" :class="{ active: activeTab === 'pictures' }"><i></i> 图床</button>
            <button @click="activeTab = 'empty'" :class="{ active: activeTab === 'empty' }"><i></i> todo</button>
            <button @click="activeTab = 'empty'" :class="{ active: activeTab === 'empty' }"><i></i> todo</button>
        </div>
        <!-- 选项具体内容 -->
        <div class="tab-content">
            <CollectList v-if="activeTab === 'collects'" />
        </div>
        <div class="tab-content">
            <PictureList v-if="activeTab === 'pictures'" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CollectList from './CollectList.vue'
import PictureList from './PictureList.vue'

const activeTab = ref<'empty' | 'pictures' | 'collects'>('empty')
</script>

<style scoped>
.mainPage-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    padding-top: 0;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Arial', sans-serif;
    border: black solid 1px;
}

.tabs {
    width: 100%;
    display: flex;
    justify-content: space-around;
    margin: 20px 0;
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 10px;
}

.tabs button {
    background: none;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    color: #666;
    transition: color 0.3s, transform 0.3s;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.tabs button i {
    font-size: 24px;
    margin-bottom: 5px;
}

.tabs button.active {
    color: rgb(0, 150, 150);
    transform: scale(1.1);
}

.tabs button:hover {
    color: rgb(0, 180, 180);
}
</style>
