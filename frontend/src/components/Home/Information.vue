<template>
    <div class="user-profile">
        <!-- 版心 -->
        <div class="container">
            <div class="profile-header clearfix">
                <div class="avatar-container leftfix">
                    <img
                        :src="user.avatar ? user.avatar : avatar"
                        alt="Avatar"
                        class="avatar"
                        @click="showUploadDialog"
                    />
                    <div class="avatar-overlay" @click="showUploadDialog">
                        <span>修改头像</span>
                    </div>
                </div>
                <div class="profile-info leftfix">
                    <h2>{{ user.name }}</h2>
                    <div class="user-details">
                        <span>ID：{{ user.id }}</span>
                    </div>
                    <div class="user-details">
                        <span>昵称：{{ user.username }}</span>
                    </div>
                    <div class="user-details">
                        <span>邮箱：{{ user.email }}</span>
                    </div>
                </div>
                <div class="modify rightfix">
                    <span @click="jump('/modify')">编辑</span>
                </div>
                <div class="modify rightfix">
                    <span @click="jump('/company/create')">创建企业</span>
                </div>
                <div class="modify rightfix">
                    <span @click="showJoinCompanyDialog">加入企业</span>
                </div>
                <div class="modify rightfix">
                    <span @click="showUploadDialog">上传头像</span>
                </div>
            </div>

            <div class="profile-body">
                <div class="profile-details">
                    <p><span @click="jump('#')">我的企业</span></p>
                    <p><span @click="jump('#')">我的团队</span></p>
                </div>
                <div class="profile-details">
                    <p><strong>个人简介：</strong>我是摩卡</p>
                </div>
            </div>
        </div>

        <!-- 加入企业弹窗 -->
        <el-dialog title="加入企业" v-model="joinCompanyDialogVisible" width="30%">
            <el-input v-model="inviteCode" placeholder="请输入邀请码" style="margin-bottom: 20px"></el-input>
            <el-input v-model="companyName" placeholder="请输入企业名称"></el-input>
            <div slot="footer" class="dialog-footer">
                <el-button @click="joinCompanyDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="attemptJoinCompany">确 定</el-button>
            </div>
        </el-dialog>

        <!-- 上传头像弹窗 -->
        <el-dialog title="上传头像" v-model="uploadDialogVisible" width="30%">
            <input type="file" @change="handleFileChange" accept="image/*" />
            <div slot="footer" class="dialog-footer">
                <el-button @click="uploadDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="uploadAvatar">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/store/profile'
import avatar from '@/assets/Global/avatar.jpg'
import api from '@/api'
import env from '@/utils/env'

const router = useRouter()
const jump = (path: string) => {
    router.push(path)
}

const user = ref<{
    id: number
    username: string
    name: string
    email: string
    avatar: string
}>({})
const profile = useProfileStore()

onMounted(async () => {
    user.value = await api.getUserInfo(profile.id)
    console.log(`output->user.value`, user.value)
    await api.validToken({ token: localStorage.getItem('token') })
    await api.refreshToken({ refresh: localStorage.getItem('refresh') })
})

const joinCompanyDialogVisible = ref(false)
const inviteCode = ref('')
const companyName = ref('')

const showJoinCompanyDialog = () => {
    joinCompanyDialogVisible.value = true
}

const attemptJoinCompany = async () => {
    try {
        const ret = await api.joinCompany({
            token: inviteCode.value,
            company_name: companyName.value,
        })
        joinCompanyDialogVisible.value = false
        if (ret.status == '200') ElMessage.success('成功加入企业')
        else ElMessage.error('加入企业失败，请检查邀请码和企业名称')
    } catch (error) {
        ElMessage.error('加入企业失败，请检查邀请码和企业名称')
    }
}

const uploadDialogVisible = ref(false)
const file = ref(null)

const showUploadDialog = () => {
    uploadDialogVisible.value = true
}

const handleFileChange = (event) => {
    file.value = event.target.files[0]
}

const uploadAvatar = async () => {
    if (!file.value) {
        ElMessage.error('请先选择一个文件')
        return
    }

    if (file.value.size > 2097152) {
        ElMessage.error('文件大小超过 2MB 限制')
        return
    }

    const formData = new FormData()
    formData.append('avatar', file.value)

    try {
        user.value.avatar = env.backEnd + 'files/' + (await api.uploadAvatar(formData))
        ElMessage.success('头像上传成功')
        uploadDialogVisible.value = false
        profile.avatar = user.value.avatar
    } catch (error) {
        console.error('Error uploading avatar:', error)
        ElMessage.error('头像上传失败')
    }
}
</script>

<style scoped>
.user-profile {
    margin-top: 20px;
    max-height: 300px;
    margin-bottom: 10px;
}

.container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    flex-direction: column;
    font-family: 'Arial', sans-serif;
}

.profile-header {
    border-bottom: 1px solid #f0f0f0;
    margin-bottom: 5px;
}

.avatar-container {
    position: relative;
    display: inline-block;
}

.avatar {
    height: 80px;
    width: 80px;
    display: block;
    border-radius: 50%;
    border: 2px solid #555;
    margin: 10px;
    cursor: pointer;
}

.avatar-overlay {
    position: absolute;
    top: 10%;
    left: 10%;
    height: 80%;
    width: 80%;
    background: rgba(0, 0, 0, 0.4);
    border-radius: 50%;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
    cursor: pointer;
}

.avatar-container:hover .avatar-overlay {
    opacity: 1;
}

.modify {
    color: rgb(0, 120, 120);
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 18px;
    cursor: pointer;
    margin-top: 40px;
    margin-right: 20px;
}

.user-details {
    color: #666;
    margin: 5px 0;
    margin-top: 10px;
}

.profile-body {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.profile-details {
    flex: 1;
}

.profile-details p {
    margin: 5px 0;
    color: #555;
}

.resume-link {
    margin-left: 20px;
}

.resume-link a {
    color: rgb(0, 160, 159);
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
}

.resume-link a:hover {
    text-decoration: underline;
}

p > span {
    background: linear-gradient(to right, #6c5ce7, #a29bfe);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    border: 2px solid transparent;
    border-radius: 5px;
    padding: 5px 10px;
    transition: color 0.3s ease, border-bottom 0.3s ease;
    cursor: pointer;
    position: relative;
    display: inline-block;
}

p > span:hover {
    color: #0056b3; /* 悬浮时的颜色 */
    /*border-color: #a29bfe;*/
}

p > span:before {
    content: '';
    position: absolute;
    width: 100%;
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: #007bff;
    visibility: hidden;
    transform: scaleX(0);
    transition: all 0.3s ease-in-out;
}

p > span:hover:before {
    visibility: visible;
    transform: scaleX(1);
}

.leftfix {
    float: left;
}

.rightfix {
    float: right;
}

.clearfix::after {
    content: '';
    display: block;
    clear: both;
}

.dialog-footer {
    margin-top: 20px;
}
</style>
