<template>
    <div class="version-control">
        <h2>文档标签</h2>
        <div class="tag-container">
            <span v-for="(keyword, index) in keywords" :key="index" class="tag">{{ keyword }}</span>
        </div>
        <div class="template-info">
            <h2 v-if="templateName">文档模板</h2>
            <span style="color: #333; font-size: 20px">{{ templateName }}</span>
        </div>
        <a-divider></a-divider>
        <button class="new-document-button" @click="startNewDocument">新建版本</button>
        <div
            v-for="(doc, index) in documents"
            :key="doc.id"
            :class="{ active: doc === activeDocument }"
            class="document-item"
            @click="setActiveDocument(doc)"
        >
            <span>{{ doc.description }}</span>
            <el-icon-edit class="edit-icon" @click.stop="openEditDialog(doc)"></el-icon-edit>
        </div>
        <el-dialog v-model="dialogVisible" title="选择版本">
            <el-select v-model="selectedBaseDocument" placeholder="选择版本">
                <el-option
                    v-for="(doc, index) in documents"
                    :key="doc.version"
                    :label="doc.description"
                    :value="doc.version"
                />
                <el-option label="空白版本" :value="0"></el-option>
            </el-select>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="createDocumentFromVersion">确认</el-button>
            </span>
        </el-dialog>
        <el-dialog v-model="editDialogVisible" title="编辑版本名称">
            <el-input v-model="editDocument.description" placeholder="请输入新的版本名称"></el-input>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="updateDocumentDescription">确认</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, onMounted } from 'vue'
import { ElDialog, ElButton, ElSelect, ElOption, ElInput } from 'element-plus'
import { Edit as ElIconEdit } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'
import api from '@/api'

const documents = ref([])
// 当前的版本对象
let activeDocument = ref(null)
const dialogVisible = ref(false)
// 选中的原始版本的值
const selectedBaseDocument = ref(0)
const emit = defineEmits(['changeDocument', 'newDocument'])
const editDialogVisible = ref(false)
const editDocument = ref({ id: null, description: '' })

const props = defineProps({
    keywords: Array,
    templateName: String,
})

// 切换版本时调用, doc 传的是一个对象
const setActiveDocument = (doc: (typeof documents.value)[0]) => {
    activeDocument.value = doc
    emit('changeDocument', doc)
}

const startNewDocument = () => {
    dialogVisible.value = true
}

const route = useRoute()

// 新建版本时调用
const createDocumentFromVersion = async () => {
    if (selectedBaseDocument.value !== null) {
        // 自行推断出 version
        const newDocumentName = `新文档-${documents.value.length + 1}`
        // 既保存了当前编辑的版本，又创建了新版本

        const newVersion = await api.createVersion({
            description: newDocumentName,
            document_id: route.params.did,
            source_version: selectedBaseDocument.value,
        })

        emit('newDocument', {
            name: newVersion.version,
            base: selectedBaseDocument.value ? selectedBaseDocument.value : null,
        })
        // 新的 version 对象
        documents.value.push(newVersion)
        activeDocument.value = newVersion
        dialogVisible.value = false
        selectedBaseDocument.value = 0
        // 这一步是为了重置 editor 的 active
        emit('changeDocument', newVersion)
    }
}

const openEditDialog = (doc: (typeof documents.value)[0]) => {
    editDocument.value = { ...doc }
    editDialogVisible.value = true
}

const updateDocumentDescription = async () => {
    const updatedDoc = await api.updateVersion(editDocument.value.version, {
        description: editDocument.value.description,
        document_id: route.params.did,
    })
    const index = documents.value.findIndex((doc) => doc.id === editDocument.value.id)
    if (index !== -1) {
        documents.value[index].description = updatedDoc.description
    }
    editDialogVisible.value = false
}

onMounted(async () => {
    documents.value = await api.queryVersions({
        document_id: route.params.did,
    })
    activeDocument.value = documents.value[0] ? documents.value[0] : null
})
</script>

<style scoped>
.version-control {
    padding: 20px;
    background: #f9f9f9;
    border-radius: 10px;
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 100%;
    height: 100%;
}

.template-info {
    margin-top: 20px;
    margin-bottom: 20px;
}

.new-document-button {
    display: block;
    width: 100%;
    padding: 12px;
    margin-bottom: 20px;
    background: #87ceeb;
    border: none;
    border-radius: 6px;
    color: #fff;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s, transform 0.3s;
}

.new-document-button:hover {
    background: #6ca6cd;
    transform: scale(1.05);
}

.document-item {
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 6px;
    margin-bottom: 12px;
    background-color: #fff;
    color: #333;
    cursor: pointer;
    transition: background-color 0.3s, box-shadow 0.3s, transform 0.3s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.document-item:hover {
    background-color: #f0f0f0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transform: translateX(5px);
}

.document-item.active {
    background-color: #cad8ea;
    border-color: #a0a0a0;
    color: #333;
    box-shadow: 0 4px 12px rgba(176, 196, 222, 0.4);
}

.edit-icon {
    font-size: 16px;
    width: 24px;
    cursor: pointer;
    margin-left: 10px;
    color: #87ceeb;
    transition: color 0.3s;
}

.edit-icon:hover {
    color: #6ca6cd;
}

.tag-container {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 10px;
}

.tag {
    background-color: #87ceeb;
    color: white;
    font-size: 14px;
    padding: 6px 10px;
    border-radius: 12px;
    margin-right: 10px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.tag:hover {
    background-color: #6ca6cd;
}

:deep(.ant-divider) {
    margin-top: 12px;
}

.dialog-footer {
    margin-top: 20px;
}
</style>
