<template>
    <div class="document-list">
        <div v-for="document in documents" :key="document.id" class="document-item" @click="goToDocument(document.url)">
            <img :src="document.icon" alt="Document Icon" class="document-icon" />
            <div class="document-details">
                <h3>{{ document.name }}</h3>
                <p>{{ document.description }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Document {
    id: number
    icon: string
    name: string
    description: string
    url: string
}

const documents = ref<Document[]>([
    {
        id: 1,
        icon: '/src/assets/images/card.png', // 替换为实际的图标URL
        name: 'Document 1',
        description: 'This is the description for Document 1.',
        url: 'https://www.baidu.com',
    },
    {
        id: 2,
        icon: '/src/assets/images/card.png', // 替换为实际的图标URL
        name: 'Document 2',
        description: 'This is the description for Document 2.',
        url: 'https://www.baidu.com',
    },
])

const goToDocument = (url: string) => {
    window.location.href = url
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.document-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 1000px;
    margin: 0 auto;
}

.document-item {
    display: flex;
    align-items: center;
    cursor: pointer;
    border: 1px solid #ddd;
    padding: 16px;
    border-radius: 8px;
    transition: background-color 0.3s, box-shadow 0.3s;
    box-sizing: border-box;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    color: #333;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 0 10px;
}

.document-item:hover {
    background: linear-gradient(135deg, #e2e6ea, #dee2e6);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.document-icon {
    width: 64px;
    height: 64px;
    margin-right: 16px;
    border-radius: 50%;
    border: 2px solid #ccc;
}

.document-details h3 {
    margin: 0;
    font-size: 1.5em;
    font-family: 'Roboto', sans-serif;
    font-weight: 700;
}

.document-details p {
    margin: 4px 0 0;
    color: #666;
    font-family: 'Roboto', sans-serif;
    font-weight: 400;
}
</style>
