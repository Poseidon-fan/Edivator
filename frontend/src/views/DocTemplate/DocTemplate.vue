<template>
    <div class="container">
        <!-- 模板推荐 -->
        <div class="template-recommendations">
            <h2>文档模板</h2>
            <div class="my-template-list">
                <div
                    class="my-template-card"
                    v-for="(template, index) in publicTemplateList"
                    :key="template.id"
                    @click="showImageModal(template.avatar, template.name)"
                >
                    <a-card :bordered="false" :hoverable="true">
                        <div class="image-container">
                            <img :src="template.avatar" alt="模板图片" />
                        </div>
                        <div class="card-title">{{ template.name }}</div>
                    </a-card>
                </div>
            </div>
        </div>
        <!-- 图片预览弹窗 -->
        <a-modal
            :title="previewName"
            v-model:visible="isImageModalVisible"
            @cancel="handleImageModalCancel"
            @ok="handleImageModalCancel"
        >
            <img :src="previewImageUrl" alt="模板图片" class="preview-image" />
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/api'

const searchValue = ref<string>('')

const myTemplateList = ref([
    { id: '1', title: '模板1', imageUrl: '', category: 'category1' },
    { id: '2', title: '模板2', imageUrl: '', category: 'category2' },
])

const publicTemplateList = ref([])

const isUploadModalVisible = ref<boolean>(false)
const uploadedFile = ref<File | null>(null)
const previewName = ref('')

const showUploadModal = () => {
    isUploadModalVisible.value = true
}

const handleUploadOk = () => {
    if (uploadedFile.value) {
        api.extractStyle({ doc: uploadedFile.value })
    }
    isUploadModalVisible.value = false
}

const handleUploadCancel = () => {
    isUploadModalVisible.value = false
}

const beforeUpload = (file: File) => {
    const isWord =
        file.type === 'application/msword' ||
        file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    if (!isWord) {
        message.error('只允许上传 Word 文件!')
        return false
    }
    uploadedFile.value = file
    return false
}

const isImageModalVisible = ref<boolean>(false)
const previewImageUrl = ref<string>('')
const defaultImage = 'https://img1.baidu.com/it/u=3351025822,1475188484&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=708'

const showImageModal = (url: string, name: string) => {
    previewName.value = name
    previewImageUrl.value = url
    isImageModalVisible.value = true
}

const handleImageModalCancel = () => {
    isImageModalVisible.value = false
}

onMounted(async () => {
    publicTemplateList.value = await api.queryPublicTemplates()
    myTemplateList.value = await api.qeuryPersonalTemplates()
})
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    padding: 30px;
    background-color: #f4f4f4;
}

.template-recommendations {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.template-recommendations h2 {
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: bold;
    color: #333333;
    text-align: center;
    border-bottom: 2px solid #eaeaea;
    padding-bottom: 10px;
}

.my-template-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: space-between;
}

.my-template-card {
    width: calc(33.333% - 20px);
    background-color: #ffffff;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #dadada;
    transition: transform 0.3s ease, box-shadow 0.3s ease;

    &:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border-color: #d9d9d9;
    }
}

.image-container {
    width: 100%;
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    border-bottom: 1px solid #eaeaea;
}

.image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
}

.card-title {
    padding: 15px 10px;
    font-size: 16px;
    font-weight: 500;
    color: #555555;
    text-align: center;
}

.preview-image {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #eaeaea;
}
</style>
