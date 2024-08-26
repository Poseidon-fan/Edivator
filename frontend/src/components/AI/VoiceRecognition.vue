<template>
    <node-view-wrapper class="voice-recognition">
        <div v-if="!isUploaded" class="voice-recognition">
            <el-upload
                class="upload-demo"
                action=""
                :http-request="uploadFile"
                :on-success="handleSuccess"
                :on-error="handleError"
                :before-upload="beforeUpload"
                drag
                accept=".pcm,.wav,.amr,.m4a"
            >
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
                <div class="tip">The maximum size per file is 5 MB. Allowed formats: .pcm, .wav, .amr, .m4a</div>
            </el-upload>
        </div>
        <p v-else>{{ recognitionResult }}</p>
    </node-view-wrapper>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NodeViewWrapper } from '@tiptap/vue-3'
import { ElMessage } from 'element-plus'
import api from '@/api'

const props = defineProps<{
    onUpdate?: (result: string) => void
    content: string
    editor: any
}>()

const isUploaded = ref(false)
const recognitionResult = ref('')

const uploadFile = async (request: any) => {
    try {
        const file = request.file
        console.log('Uploading file:', file)
        const base64 = await convertToBase64(file)
        const pureBase64 = base64.split(',')[1] // 去掉前缀
        const result = await api.voiceRecognize({
            file_format: 'pcm',
            dev_pid: '1537',
            speech: pureBase64,
        })
        handleSuccess(result)
    } catch (error) {
        handleError(error)
    }
}

const convertToBase64 = (file: File) => {
    return new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result as string)
        reader.onerror = (error) => reject(error)
    })
}

const handleSuccess = (result: any) => {
    ElMessage.success('File uploaded successfully')
    recognitionResult.value = result.data.result.join(' ')
    isUploaded.value = true
    replaceNodeWithResult(recognitionResult.value)
}

const handleError = (error: any) => {
    ElMessage.error(`File upload failed: ${error}`)
}

const beforeUpload = (file: File) => {
    const isLt5M = file.size / 1024 / 1024 < 5
    if (!isLt5M) {
        ElMessage.error('File size must be less than 5MB!')
    }
    return isLt5M
}

const replaceNodeWithResult = (result: string) => {
    const { state, view } = props.editor
    const tr = state.tr
    console.log(`output->props.editor`, props.editor)
    console.log(`output->state, view, tr`, state, view, tr)
    const { from, to } = state.selection

    const node = state.schema.text(result)
    tr.replaceWith(from, to, node)
    view.dispatch(tr)
}
</script>

<style scoped>
.voice-recognition {
    width: 100%;
    max-width: 500px;
    margin: 20px auto;
}

.upload-demo {
    border: 2px dashed #d9d9d9;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: border-color 0.3s ease;
}

.upload-demo:hover {
    border-color: #409eff;
}

.el-upload__text {
    font-size: 16px;
    color: #606266;
}

.el-upload__text em {
    color: #409eff;
    font-style: normal;
    cursor: pointer;
}

.tip {
    margin-top: 10px;
    font-size: 14px;
    color: #909399;
}

.voice-recognition-result {
    font-size: 16px;
    color: #606266;
    margin-top: 20px;
}
</style>
