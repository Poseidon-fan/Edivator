<template>
    <h2 style="margin-left: 40px; margin-top: 50px; margin-bottom: 0">个人文档</h2>
    <div class="search-bar" style="position: relative; width: 90%; left: 4.5%; margin-top: 20px">
        <a-input-search
            v-model:value="searchValue"
            placeholder="搜索文档"
            enter-button="搜索"
            size="large"
            @search="onSearch"
        />
        <a-button style="right: 0; top: 0; margin-top: 15px" @click="clearSearch">清除搜索</a-button>
    </div>
    <div class="flexContainer">
        <a-card hoverable class="flexItem" @click="showModal">
            <template #cover>
                <plus-circle-outlined
                    style="position: relative; top: 30px; height: 180px; color: #1890ff; font-size: 120px"
                />
            </template>
            <a-card-meta title="添加新文档" description="点击此处添加新文档" />
        </a-card>

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
                <edit-outlined @click.stop="showSettings(ele)" key="setting" />
                <star-outlined
                    @click.stop="toggleFavorite(ele)"
                    :class="{ favorite: ele.isFavorite }"
                    key="favorite"
                    style="font-size: 14px"
                />
                <delete-outlined @click.stop="confirmDelete(i)" key="delete" />
            </template>
            <a-card-meta :title="ele.name">
                <template #avatar>
                    <a-avatar
                        style="border: #606266 1px solid"
                        :src="profile.avatar ? profile.avatar : avatar"
                        size="large"
                    ></a-avatar>
                </template>
                <template #description>
                    <Paragraph :ellipsis="{ rows: 2, expandable: false }" style="white-space: pre-wrap">
                        {{ ele.description + '\n\n' }}
                    </Paragraph>
                </template>
            </a-card-meta>
        </a-card>

        <a-modal v-model:visible="isModalVisible" title="新建文档" centered @ok="handleOk" @cancel="handleCancel">
            <a-form layout="vertical">
                <a-form-item label="文档名">
                    <a-input v-model:value="form.documentName" />
                </a-form-item>
                <a-form-item label="文档描述">
                    <a-textarea v-model:value="form.documentDescription" />
                </a-form-item>
                <a-form-item label="文档封面">
                    <a-upload
                        :show-upload-list="false"
                        :before-upload="beforeUpload"
                        v-model:file-list="form.documentCover"
                    >
                        <a-button>
                            <template v-slot:icon>
                                <UploadOutlined />
                            </template>
                            点击上传封面
                        </a-button>
                    </a-upload>
                    <div v-if="form.documentCover.length">
                        <img :src="form.documentCover[0].url" alt="Document Cover" class="document-cover-preview" />
                    </div>
                </a-form-item>
                <a-form-item label="文档模板">
                    <a-select v-model:value="form.templateId" placeholder="选择模板">
                        <a-select-option v-for="template in templates" :key="template.id" :value="template.id">
                            {{ template.name }}
                        </a-select-option>
                    </a-select>
                </a-form-item>
            </a-form>
        </a-modal>

        <!-- 文档设置模态框 -->
        <a-modal
            v-model:visible="isSettingsVisible"
            title="文档设置"
            centered
            @ok="handleSettingsOk"
            @cancel="handleSettingsCancel"
        >
            <a-form layout="vertical">
                <a-form-item label="文档名">
                    <a-input v-model:value="settingsForm.documentName" />
                </a-form-item>
                <a-form-item label="文档描述">
                    <a-textarea v-model:value="settingsForm.documentDescription" />
                </a-form-item>
                <a-form-item label="文档封面">
                    <a-upload
                        :show-upload-list="false"
                        :before-upload="beforeUploadSettings"
                        v-model:file-list="settingsForm.documentCover"
                    >
                        <a-button>
                            <template v-slot:icon>
                                <UploadOutlined />
                            </template>
                            点击上传封面
                        </a-button>
                    </a-upload>
                    <div v-if="settingsForm.documentCover.length">
                        <img
                            v-if="settingsForm.documentCover[0].url"
                            :src="settingsForm.documentCover[0].url"
                            alt="Document Cover"
                            class="document-cover-preview"
                        />
                    </div>
                </a-form-item>
            </a-form>
        </a-modal>

        <!-- 文档编辑模态框 -->
        <a-modal
            v-model:visible="isEditVisible"
            title="编辑文档"
            centered
            @ok="handleEditOk"
            @cancel="handleEditCancel"
        >
            <a-form layout="vertical">
                <a-form-item label="文档内容">
                    <a-textarea v-model:value="editForm.documentContent" rows="10" />
                </a-form-item>
            </a-form>
        </a-modal>

        <!-- 文档删除拟态框 -->
        <el-dialog v-model="dialogVisible" title="确认删除" width="30%">
            <div>你确定要删除这个文档吗？</div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="handleDelete">确认</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { Card, Avatar, Modal, Form, Input, Typography, Upload, Button, message, Select, Option } from 'ant-design-vue'
const { Paragraph } = Typography
import {
    SettingOutlined,
    EditOutlined,
    DeleteOutlined,
    PlusCircleOutlined,
    UploadOutlined,
    StarOutlined,
} from '@ant-design/icons-vue'
import AvatarImg from '@/assets/images/avatar.png'
import { useRouter } from 'vue-router'
import Methods from '@/utils/UtilMethod.ts'
import { useProfileStore } from '@/store/profile.ts'
import api from '@/api'
import env from '@/utils/env'
import cover from '@/assets/images/card.png'
import avatar from '@/assets/images/avatar.png'

const router = useRouter()

const isModalVisible = ref(false)
const isSettingsVisible = ref(false)
const isEditVisible = ref(false)
const profile = useProfileStore()
import { ElMessage } from 'element-plus'

const form = ref({
    documentName: '',
    documentDescription: '',
    documentCover: [] as any[],
    templateId: null,
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
const templates = ref([])

const searchValue = ref('')

const showModal = () => {
    isModalVisible.value = true
}

const showSettings = (doc) => {
    settingsForm.value.id = doc.id
    settingsForm.value.documentName = doc.name
    settingsForm.value.documentDescription = doc.description
    settingsForm.value.documentCover = [{ url: doc.cover }]
    isSettingsVisible.value = true
}

const toggleFavorite = (doc) => {
    doc.isFavorite = !doc.isFavorite
    message.success(`文档已${doc.isFavorite ? '收藏' : '取消收藏'}`)
    api.toggleFavorite({ doc_id: doc.id })
}

const handleOk = async () => {
    const formData = new FormData()
    if (form.value.documentCover.length) {
        formData.append('avatar', form.value.documentCover[0].originFileObj)
    }
    formData.append('name', form.value.documentName)
    formData.append('description', form.value.documentDescription)
    formData.append('owner', '1')
    formData.append('template', form.value.templateId)

    try {
        const response = await api.createDocument(formData)
        if (response.status === 201) {
            documents.value.push(response.data)
            filteredDocuments.value = documents.value
            form.value.documentName = ''
            form.value.documentDescription = ''
            form.value.documentCover = []
            form.value.templateId = null
            isModalVisible.value = false
            message.success('文档创建成功')
        } else {
            message.error('文档创建失败')
        }
    } catch (error) {
        console.error('文档创建错误:', error)
        message.error('文档创建失败，请重试')
    }
}

const handleCancel = () => {
    isModalVisible.value = false
}

const handleSettingsOk = async () => {
    const formData = new FormData()
    formData.append('name', settingsForm.value.documentName)
    formData.append('description', settingsForm.value.documentDescription)
    if (settingsForm.value.documentCover.length) {
        formData.append('avatar', settingsForm.value.documentCover[0].originFileObj)
    }

    try {
        const response = await api.updateDocument(settingsForm.value.id, formData)
        if (response.status === 200) {
            const updatedDoc = response.data
            const index = documents.value.findIndex((doc) => doc.id === updatedDoc.id)
            if (index !== -1) {
                documents.value[index] = updatedDoc
                filteredDocuments.value = documents.value
            }
            isSettingsVisible.value = false
            message.success('文档更新成功')
        } else {
            message.error('文档更新失败')
        }
    } catch (error) {
        console.error('文档更新错误:', error)
        message.error('文档更新失败，请重试')
    }
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

const jump2PersonalDocument = () => {
    router.push('/documents/personalDocument')
}

const dialogVisible = ref(false)
const currentDocumentIndex = ref(null)

const confirmDelete = (index) => {
    currentDocumentIndex.value = index
    dialogVisible.value = true
}

const handleDelete = () => {
    const index = currentDocumentIndex.value
    if (index !== null) {
        api.deleteDocument(documents.value[index].id)
            .then(() => {
                ElMessage.success('删除成功')
                documents.value.splice(index, 1)
                filteredDocuments.value = documents.value
                dialogVisible.value = false
            })
            .catch((error) => {
                ElMessage.error('删除失败')
                console.error(error)
            })
    }
}

const onSearch = async (value) => {
    try {
        const response = await api.searchDocuments({ search: value })
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
    documents.value = await api.queryDocuments({ user_id: profile.id })
    filteredDocuments.value = documents.value

    favoriteDocuments.value = await api.queryFavorite()

    templates.value = await api.queryPublicTemplates()
    form.value.templateId = templates.value[0].id

    for (let i = 0; i < documents.value.length; i++) {
        documents.value[i].isFavorite = false
        for (let j = 0; j < favoriteDocuments.value.length; j++) {
            if (favoriteDocuments.value[j].id == documents.value[i].id) {
                documents.value[i].isFavorite = true
                break
            }
        }
    }
})

const beforeUpload = (file: File) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
    if (!isJpgOrPng) {
        message.error('你只能上传JPG/PNG文件!')
        return false
    }
    const isLt2M = file.size / 1024 / 1024 < 4
    if (!isLt2M) {
        message.error('图片必须小于4MB!')
        return false
    }
    form.value.documentCover = [{ originFileObj: file }]
    form.value.documentCover[0].url = URL.createObjectURL(form.value.documentCover[0].originFileObj)
    return false
}
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
}

:deep(.ant-card-body) {
    padding: 12px 24px !important;
    padding-bottom: 0 !important;
}

:deep(.ant-card-cover) {
    border: 1px solid #e0e0e0;
}

.document-cover-preview {
    width: 300px;
    height: 180px;
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
