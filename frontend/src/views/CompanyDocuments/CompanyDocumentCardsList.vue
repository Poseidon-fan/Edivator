<template>
    <h2 style="margin-left: 40px; margin-top: 50px; margin-bottom: 0">企业文档</h2>
    <div class="flexContainer">
        <a-card
            hoverable
            class="flexItem"
            v-for="(ele, i) in filteredDocuments"
            :key="i"
            @click="Methods.jump(`/editor/${ele.id}`)"
        >
            <template #cover>
                <img
                    alt="example"
                    :src="ele.avatar ? `${env.backEnd.slice(0, -1)}${ele.avatar}` : cover"
                    style="height: 180px"
                />
            </template>
            <template #actions>
                <star-outlined
                    @click.stop="toggleFavorite(ele)"
                    :class="{ favorite: ele.isFavorite }"
                    key="favorite"
                    style="font-size: 14px"
                />
            </template>
            <a-card-meta :title="ele.name">
                <template #avatar>
                    <a-avatar :src="avatar" size="large"></a-avatar>
                </template>
                <template #description>
                    <Paragraph :ellipsis="{ rows: 2, expandable: false }" style="white-space: pre-wrap">
                        {{ ele.description + '\n\n' }}
                    </Paragraph>
                </template>
            </a-card-meta>
        </a-card>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { Card, Avatar, Typography, message, Button, Input } from 'ant-design-vue'
const { Paragraph } = Typography
import { StarOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import Methods from '@/utils/UtilMethod.ts'
import { useProfileStore } from '@/store/profile.ts'
import api from '@/api'
import env from '@/utils/env'
import cover from '@/assets/images/card.png'
import avatar from '@/assets/images/avatar.png'
import { useCompanyStore } from '@/store/profile.ts'

const router = useRouter()
const companyStore = useCompanyStore()

const profile = useProfileStore()
import { ElMessage } from 'element-plus'

const form = ref({
    documentName: '',
    documentDescription: '',
    documentCover: [] as any[],
})

const settingsForm = ref({
    id: '',
    documentName: '',
    documentDescription: '',
    documentCover: [] as any[],
})

const editForm = ref({
    documentContent: '',
})

const documents = ref([])
const filteredDocuments = ref([])
const favoriteDocuments = ref([])

const searchValue = ref('')

const toggleFavorite = (doc) => {
    doc.isFavorite = !doc.isFavorite
    message.success(`文档已${doc.isFavorite ? '收藏' : '取消收藏'}`)
    api.toggleFavorite({ doc_id: doc.id })
    console.log(`output->documents.value`, documents.value)
}

const beforeUploadSettings = (file: File) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
    if (!isJpgOrPng) {
        message.error('你只能上传 JPG/PNG 文件!')
        return false
    }
    const isLt2M = file.size / 1024 / 1024 < 4
    if (!isLt2M) {
        message.error('图片必须小于 4MB!')
        return false
    }
    const reader = new FileReader()
    reader.onload = (e) => {
        settingsForm.value.documentCover = [
            {
                url: e.target?.result as string,
                originFileObj: file,
            },
        ]
    }
    reader.readAsDataURL(file)
    return false // 不进行默认的上传行为
}

const handleSettingsCancel = () => {
    isSettingsVisible.value = false
}

const handleEditOk = () => {
    console.log('Edit form data:', editForm.value)
    isEditVisible.value = false
}

const handleEditCancel = () => {
    isEditVisible.value = false
}

const dialogVisible = ref(false)
const currentDocumentIndex = ref(null)

const onSearch = async (value) => {
    try {
        const response = await api.searchDocuments({ search: value, company_id: companyStore.id })
        if (response.status === 200) {
            filteredDocuments.value = response.data
        } else {
            message.error('搜索失败')
        }
    } catch (error) {
        console.error('搜索错误:', error)
        message.error('搜索失败，请重试')
    }
}

const clearSearch = () => {
    searchValue.value = ''
    filteredDocuments.value = documents.value
}

onMounted(async () => {
    documents.value = await api.queryDocuments({
        company_id: companyStore.id,
    })

    favoriteDocuments.value = await api.queryFavorite()
    console.log(`output->favoriteDocuments`, favoriteDocuments.value)

    for (let i = 0; i < documents.value.length; i++) {
        documents.value[i].isFavorite = false
        for (let j = 0; j < favoriteDocuments.value.length; j++) {
            if (favoriteDocuments.value[j].id == documents.value[i].id) {
                documents.value[i].isFavorite = true
                break
            }
        }
    }

    filteredDocuments.value = documents.value

    console.log(`output->documents.value`, documents.value)
})
</script>

<style scoped>
.flexItem {
    flex: 0 0 22.5%; /* 固定宽度为 300px */
    height: 324px; /* 固定高度为 324px */
}

.flexContainer {
    display: flex;
    flex-wrap: wrap; /* 换行 */
    width: 90%;
    margin: 0 auto;
    padding-top: 30px;
    padding-bottom: 60px;
    row-gap: 40px;
    column-gap: 3%;
    /* row-gap: 4%; */
}

:deep(.ant-card-body) {
    padding: 12px 24px !important;
    padding-bottom: 0 !important;
}

.document-cover-preview {
    width: 300px;
    height: 180px; /* 固定高度为 200px */
    object-fit: cover;
    margin-top: 10px;
}

.favorite {
    color: gold !important;
}

.dialog-content {
    font-size: 16px;
    color: #606266;
    margin-bottom: 20px;
    display: block;
}

.dialog-footer {
    text-align: right;
    margin: 0;
    padding: 10px 0;
    border-top: 1px solid #ebeef5;
}

.el-dialog {
    border-radius: 8px;
    padding: 20px;
}

.el-button {
    margin-left: 10px;
}

:deep(.el-dialog__body) {
    padding-top: 20px;
    font-size: 16px;
}
.search-bar {
    padding: 10px;
}
</style>
