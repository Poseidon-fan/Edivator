<template>
    <a-card title="快速开始 / 便捷导航">
        <a-row :gutter="[16, 16]">
            <a-col v-for="(operation, index) in operations" :key="index" :span="8">
                <a-button block @click="() => handleClick(operation.url)">{{ operation.name }}</a-button>
            </a-col>
            <!--            <a-col :span="8">-->
            <!--                <a-button type="primary" block @click="addOperation"-->
            <!--                    >+ 添加</a-button-->
            <!--                >-->
            <!--            </a-col>-->
        </a-row>
    </a-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

interface Operation {
    name: string
    url: string
}

const operations = ref<Operation[]>([
    { name: '文档列表', url: '/documentCardsList' },
    { name: '文档模板', url: '/doc/template' },
    { name: '我的企业', url: '/team/manage' },
])

const handleClick = (url: string) => {
    router.push(url)
}
</script>

<style scoped>
.operations {
    margin-top: 10px;
}
</style>
