<template>
    <div class="picture-container">
        <img v-for="(imageUrl, index) in pictures" :key="index" :src="imageUrl" class="picture" />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const pictures = ref([
    'https://th.bing.com/th/id/OIP.WBCnEx4vqWbQ24NUxhC6JwHaE7?rs=1&pid=ImgDetMain',
    'https://img2.baidu.com/it/u=4284680107,1075571090&fm=253&fmt=auto&app=120&f=JPEG?w=1422&h=800',
])
</script>

<style scoped>
.picture-container {
    width: 1000px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
}

.picture {
    margin: 10px;
    width: 200px;
    height: 200px;
    border: 2px solid transparent;
    transition: border-color 0.3s ease;
}

.picture:hover {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    transition: transform 0.5s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
</style>
