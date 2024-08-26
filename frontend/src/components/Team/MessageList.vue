<template>
    <a-divider v-if="applications.length" />
    <h2 v-if="applications.length">申请列表</h2>
    <div class="approval-list">
        <el-card v-for="application in applications" :key="application.message.id" class="box-card" shadow="hover">
            <div class="card-header">
                <h3>{{ application.title }}</h3>
                <p>{{ application.details }}</p>
            </div>
            <div class="card-actions">
                <el-button type="success" @click="approveApplication(application.message.id)">接受</el-button>
                <el-button type="danger" @click="rejectApplication(application.message.id)">拒绝</el-button>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'
import { useCompanyStore } from '@/store/profile.ts'

const applications = ref([])
const company = useCompanyStore()

const fetchApplications = async () => {
    try {
        applications.value = await api.queryMessages(company.id)
    } catch (error) {
        console.error('获取申请列表失败', error)
    }

    applications.value.forEach((element) => {
        element.title = '申请信息'
        element.details = element.user_name + ' 申请加入团队 ' + element.team_name
    })
    console.log(`output->applicaion`, applications.value)
}

const approveApplication = async (id) => {
    try {
        await api.approveApplication(id)
        ElMessage.success('申请已接受')
        removeApplication(id)
    } catch (error) {
        ElMessage.error('接受申请失败')
    }
}

const rejectApplication = async (id) => {
    try {
        await api.rejectApplication(id)
        ElMessage.success('申请已拒绝')
        removeApplication(id)
    } catch (error) {
        ElMessage.error('拒绝申请失败')
    }
}

const removeApplication = (id) => {
    applications.value = applications.value.filter((app) => app.message.id !== id)
}

onMounted(() => {
    fetchApplications()
})
</script>

<style scoped>
.approval-list {
    display: flex;
    flex-direction: column;
}

.box-card {
    margin-bottom: 20px;
}

.card-header {
    margin-bottom: 10px;
}

.card-actions {
    display: flex;
    justify-content: space-between;
}
</style>
