<template>
    <div class="company-switch-card">
        <h1 class="title">进入应用</h1>
        <p class="subtitle">我们将在企业中为您提供全新的文档与团队服务</p>
        <a-divider />
        <a-list item-layout="horizontal" :data-source="companies">
            <template #renderItem="{ item }">
                <a-list-item @click="switchCompany(item)">
                    <a-list-item-meta :description="item.description">
                        <template #title>
                            <a>{{ item.name }}</a>
                        </template>
                        <template #avatar>
                            <a>
                                <a-avatar>{{ item.name[0] }}</a-avatar>
                            </a>
                        </template>
                    </a-list-item-meta>
                </a-list-item>
            </template>
        </a-list>
        <div class="create-new" @click="createNewCompany">
            <a-icon type="plus" class="new-icon" />
            <span class="company-name">创建新的企业</span>
            <span class="company-subtitle">可用于企业、组织或团队</span>
        </div>
        <div class="create-new" @click="showJoinCompanyDialog">
            <a-icon type="plus" class="new-icon" />
            <span class="company-name">加入企业</span>
        </div>
    </div>

    <el-dialog title="加入企业" v-model="joinCompanyDialogVisible" width="30%">
        <el-input v-model="inviteCode" placeholder="请输入邀请码" style="margin-bottom: 20px"></el-input>
        <el-input v-model="companyName" placeholder="请输入企业名称"></el-input>
        <div slot="footer" class="dialog-footer">
            <el-button @click="joinCompanyDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="attemptJoinCompany">确 定</el-button>
        </div>
    </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { ElMessage } from 'element-plus'
import api from '@/api'
import { useCompanyStore, useProfileStore } from '@/store/profile'
import UtilMethod from '@/utils/UtilMethod'

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

const companyStore = useCompanyStore()
const profileStore = useProfileStore()

const companies = ref([])

const switchCompany = (company) => {
    companyStore.updateCompany(company)
    console.log('Switch to Company', company)
    message.success('切换企业成功！')
    UtilMethod.jumpToHome()
}

const createNewCompany = () => {
    console.log('jump to create company')
    UtilMethod.jump('/company/create')
}

onMounted(async () => {
    // 重新获取companyId
    const nowUser = await api.getNowUser()
    profileStore.updateProfile(nowUser)

    const companyIds = nowUser.company_ids

    // 遍历所有companyIds, 获取公司信息
    for (const companyId of companyIds) {
        const companyInfo = (await api.queryCompany(companyId)).data
        companies.value.push({
            id: companyInfo.id,
            name: companyInfo.name,
            description: companyInfo.description,
            create_time: companyInfo.create_time,
            update_time: companyInfo.update_time,
            is_deleted: companyInfo.is_deleted,
            admin: companyInfo.admin,
            users: companyInfo.users,
            administrators: companyInfo.administrators,
            // avatar: `https://api.multiavatar.com/${companyInfo.data.name}` TODO 提供接口
        })
    }
})
</script>

<style scoped>
.company-switch-card {
    width: 400px;
    height: 300px;
    margin: 50px auto;

    .title {
        font-size: 35px;
        font-weight: bold;
        margin: 20px 0;
    }
}

.subtitle {
    color: #888;
    margin-bottom: 20px;
}

.company-item {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 10px;
}

.company-item:hover {
    background-color: #f0f0f0;
}

.create-new {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 10px;
    margin-top: 20px;
}

.create-new:hover {
    background-color: #f0f0f0;
}

.new-icon {
    font-size: 24px;
    margin-right: 10px;
}

.company-name {
    font-weight: bold;
    margin-right: auto;
}

.company-subtitle {
    color: #888;
    font-size: 12px;
}

.create-company-card {
    z-index: 500;
}

.dialog-footer {
    margin-top: 20px;
}
</style>
