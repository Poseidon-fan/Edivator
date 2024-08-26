<template>
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
            v-for="(ele, i) in documents"
            :key="i"
            @click="Methods.jump(`/editor/${ele.id}`)"
        >
            <template #cover>
                <img alt="example" :src="cover" style="height: 180px" />
            </template>
            <template #actions>
                <setting-outlined @click.stop="showSettings(ele)" key="setting" />
                <edit-outlined @click.stop="editDocument" key="edit" />
                <delete-outlined @click.stop="confirmDelete(i)" key="delete" />
            </template>
            <a-card-meta :title="ele.name">
                <template #avatar>
                    <a-avatar :src="avatar" size="large"></a-avatar>
                </template>
                <template #description>
                    <Paragraph :ellipsis="{ rows: 2, expandable: false }">
                        {{ ele.description }}
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
                    {{ settingsForm.documentName }}
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
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { Card, Avatar, Modal, Form, Input, Typography, Upload, Button, message } from 'ant-design-vue'

const { Paragraph } = Typography
import {
    SettingOutlined,
    EditOutlined,
    DeleteOutlined,
    PlusCircleOutlined,
    UploadOutlined,
} from '@ant-design/icons-vue'
import AvatarImg from '@/assets/images/avatar.png'
import { useRouter } from 'vue-router'
import Methods from '@/utils/UtilMethod.ts'
import { useProfileStore, useCompanyStore } from '@/store/profile.ts'
import api from '@/api'
import cover from '@/assets/images/card.png'
import avatar from '@/assets/images/avatar.png'

const router = useRouter()

const isModalVisible = ref(false)
const isSettingsVisible = ref(false)
const isEditVisible = ref(false)
const profile = useProfileStore()
const company = useCompanyStore()

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

const templates = ref([])

const documents = ref<
    {
        id: string
        name: string
        description: string
        cover: string
    }[]
>([])

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

const editDocument = () => {
    isEditVisible.value = true
}

const handleOk = async () => {
    const formData = new FormData()
    formData.append('avatar', form.value.documentCover.length ? form.value.documentCover[0].url : '')
    formData.append('name', form.value.documentName)
    formData.append('description', form.value.documentDescription)
    formData.append('owner', '3')
    formData.append('owner_id', company.companyId)
    formData.append('template', form.value.templateId)

    try {
        const response = await api.createDocument(formData)
        if (response.status === 201) {
            documents.value.push(response.data)
            form.value.documentName = ''
            form.value.documentDescription = ''
            form.value.documentCover = []
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

const confirmDelete = (index: number) => {
    Modal.confirm({
        title: '确认删除',
        content: '你确定要删除这个文档吗？',
        onOk: () => {
            documents.value.splice(index, 1)
        },
    })
}

onMounted(async () => {
    documents.value = await api.queryDocuments({
        company_id: company.companyId,
    })

    templates.value = await api.queryPublicTemplates()
    form.value.templateId = templates.value[0].id
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
    const reader = new FileReader()
    reader.onload = (e) => {
        form.value.documentCover = [{ url: e.target?.result as string }]
    }
    reader.readAsDataURL(file)
    return false
}
</script>

<style scoped>
.flexItem {
    flex: 0 0 300px; /* 固定宽度为 300px */
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
</style>
