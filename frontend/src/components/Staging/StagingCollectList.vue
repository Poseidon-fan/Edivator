<template>
    <div class="outer-container">
        <div class="favorites-container">
            <div class="header">
                <p style="font-size: 1.2rem">收藏的文档</p>
                <!--                <a href="#">全部文档</a>-->
            </div>
            <div style="color: #aaa" v-if="documents.length === 0">暂无收藏的文档</div>
            <a-row v-else gutter="{0}" class="documents">
                <a-col :span="8" v-for="doc in documents" :key="doc.id">
                    <a-card :hoverable="true" class="document" body-style="{ padding: '20px' }">
                        <a-card-meta :title="doc.title" class="document-info">
                            <template #description>
                                <Paragraph :ellipsis="{ rows: 2, expandable: false }" class="description-text">
                                    {{ doc.description }}
                                </Paragraph>
                            </template>
                        </a-card-meta>
                    </a-card>
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Typography } from 'ant-design-vue'
import api from '@/api'
import env from '@/utils/env'

const { Paragraph } = Typography

const documents = ref([])

onMounted(() => {
    // 获取收藏的文档
    // TODO 做分页
    api.queryFavorite().then((res) => {
        documents.value = res.map((item) => {
            return {
                ...item,
                id: item.id,
                title: item.name,
                description: item.description,
                cover: env.backEnd + item.avatar,
            }
        })
        console.log('收藏的文档', documents.value)
    })
})
</script>

<style scoped>
.outer-container {
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    border: 1px solid rgb(235, 230, 230);
}

.favorites-container {
    width: 100%;
    max-width: 1200px;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.header a {
    color: #007acc;
    text-decoration: none;
    transition: color 0.3s;
}

.header a:hover {
    color: #005bb5;
}

.documents {
    display: flex;
    flex-wrap: wrap;
}

.documents > .ant-col {
    margin-left: 10px;
}

.document {
    border: 1px solid #e8e8e8;
    border-radius: 8px; /* 添加圆角边框 */
    transition: border-color 0.3s; /* 添加边框颜色渐变效果 */
}

.document:hover {
    border-color: #d1d1d1; /* 在悬停时改变边框颜色 */
}

.document-info .description-text {
    line-height: 1.4em; /* 确保每行的高度 */
    min-height: 2.8em; /* 确保最小高度为两行 */
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
