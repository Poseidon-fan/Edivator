<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'
import api from '@/api'
import { message } from 'ant-design-vue'
import env from '@/utils/env'
import DocLogList from '@/components/GlobalComponents/DocLogList.vue'
import { useProfileStore } from '@/store/profile'
import StagingCollectList from '@/components/Staging/StagingCollectList.vue'
import StagingNavi from '@/components/Staging/StagingNavi.vue'
import WordCloud from '@/components/Staging/WordCloud.vue'
import avatar from '@/assets/Global/avatar.jpg'
// import StagingChart from '@/components/Staging/StagingChart.vue'
const profileStore = useProfileStore()
const allDocumentCount = ref(0)
onMounted(() => {
    // 获取log
    getLogs()
    // 获取文档总数
    api.getTotalDocumentCounts().then((res) => {
        console.log('文档总数', res)
        allDocumentCount.value = res.total_count
    })
})

const currentTeam = ref<{
    id: number
    name: string
    description: string
    avatar: string
    cover: string
    members: { id: number; name: string; avatar: string }[]
}>({
    id: 0,
    name: '',
    description: '',
    avatar: '',
    cover: '',
    members: [],
})

const tabList = [
    {
        key: 'teamInfo',
        tab: '团队信息',
    },
    {
        key: 'teamNotification',
        tab: '最新通知',
    },
]

const activeTab = ref('teamInfo')

// 右侧卡片切换时触发
const onTabChange = (key) => {
    console.debug('change to', key)
    activeTab.value = key
    // 渲染团队信息/团队通知
}

// 添加管理员
const addAdmin = async () => {
    ElMessageBox.prompt('请输入管理员ID', '添加管理员', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
    })
        .then(({ value }) => {
            console.log('管理员ID:', value)
            api.addAdmin({
                company_id: '2',
                target_user_id: value,
            })
            ElMessage.success(`管理员 ${value} 已成功添加`)
        })
        .catch(() => {
            ElMessage.info('已取消')
        })
}

// 邀请成员
const dialogVisible = ref(false)
const inviteId = ref('')
const inviteMember = () => {
    dialogVisible.value = true
}

// 生成邀请码
const generateInviteCode = async () => {
    console.log('邀请成员ID:', inviteId.value)
    const inviteCode = await api.inviteCode({
        company_id: '2',
        user_id: inviteId.value,
    })
    ElMessageBox.alert(`邀请码为：${inviteCode}`, '邀请码', {
        confirmButtonText: '确定',
    })
    dialogVisible.value = false
}

// 添加团队
const addTeamDocDialogVisible = ref(false)
const createTeamDoc = () => {
    addTeamDocDialogVisible.value = true
}

// const confirmAddTeam = async () => {
//     console.log('新团队名称:', newTeamName.value)
//     await api.createTeam({ company_id: '2', name: newTeamName.value })
//     ElMessage.success(`团队 ${newTeamName.value} 已成功创建`)
//     addTeamDocDialogVisible.value = false
//     teams.value.push({
//         name: newTeamName.value,
//         members: [],
//     })
// }

// 向团队添加成员
const addTeamMemberDialogVisible = ref(false)
const newTeamMemberId = ref<number>(0)

// 添加团队文档
const form = ref({
    documentName: '',
    documentDescription: '',
    documentCover: [],
})

const documents = ref<
    {
        id: number
        name: string
        description: string
        cover: string
    }[]
>([])

const handleAddTeamDocCancel = () => {
    form.value.documentName = ''
    form.value.documentDescription = ''
    form.value.documentCover = []
    addTeamDocDialogVisible.value = false
}
const handleAddTeamDocOk = async () => {
    const formData = new FormData()
    formData.append('avatar', form.value.documentCover.length ? form.value.documentCover[0].url : '')
    formData.append('name', form.value.documentName)
    formData.append('description', form.value.documentDescription)
    formData.append('owner', '2')

    formData.append('owner_id', currentTeam.value.id.toString())

    try {
        const response = await api.createDocument(formData)
        if (response.status === 201) {
            message.success('文档创建成功')
            const docs = await api.queryDocuments({
                team_id: currentTeam.value.id,
            })
            documents.value = docs.map((d) => {
                return {
                    id: d.id,
                    name: d.name,
                    description: d.description,
                    cover: env.backEnd + d.avatar,
                }
            })
        } else {
            message.error('文档创建失败')
        }
    } catch (error) {
        console.error('文档创建错误:', error)
        message.error('文档创建失败，请重试')
    }
}

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
        form.value.documentCover = [{ url: e.target?.result }]
    }
    reader.readAsDataURL(file)
    return false
}

// 点击团队文档
const onClickTeamDoc = (doc) => {
    message.warn('点击团队文档还没做')
    console.log('点击了团队文档', doc)
}

// 添加团队成员
const confirmAddTeamMember = async () => {
    await api.addTeamMember({
        company_id: '2',
        team_name: currentTeam.value.name,
        user_id: newTeamMemberId.value,
    })
    ElMessage.success(`成员 ${newTeamMemberId.value} 已成员添加到团队 ${currentTeam.value.name}`)
    addTeamMemberDialogVisible.value = false
}

const logs = ref([])
// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)
const totalLogs = ref(0)

// 获取分页日志数据
const getLogs = async (page = 1, size = 10) => {
    try {
        const res = await api.queryLogs({ user_id: profileStore.id, page, size })
        logs.value = res.results
        totalLogs.value = res.count
        console.log('logs value', res, logs.value)
    } catch (err) {
        message.error('获取log失败')
        console.error('获取log失败:', err)
    }
}
// greeting time 根据实际时间更改
const greetingTime = computed(() => {
    const now = new Date()
    const hour = now.getHours()
    if (hour >= 0 && hour < 6) {
        return '凌晨好'
    } else if (hour >= 6 && hour < 12) {
        return '早上好'
    } else if (hour >= 12 && hour < 18) {
        return '下午好'
    } else {
        return '晚上好'
    }
})

const greetingName = computed(() => {
    return profileStore.username
})

const greetingWord = ref<string>('祝你开心每一天！')

const descriptionRef = ref([])

// TODO 这个是干什么的？
const truncateText = () => {
    descriptionRef.value.forEach((el) => {
        if (el) {
            const lineHeight = parseFloat(getComputedStyle(el).lineHeight)
            const maxHeight = lineHeight * 2
            el.style.height = `${maxHeight}px`
            el.style.overflow = 'hidden'

            while (el.scrollHeight > el.clientHeight) {
                el.textContent = el.textContent.slice(0, -1)
                el.textContent = el.textContent.trim() + '...'
            }
        }
    })
}

// 页码变化时触发
const handlePageChange = (page) => {
    currentPage.value = page
    getLogs(page, pageSize.value)
}

// 页大小变化时触发
const handleSizeChange = (size) => {
    pageSize.value = size
    getLogs(currentPage.value, size)
}

console.log(`output->profileStore`, profileStore)

const uploadDialogVisible = ref(false)
const file = ref(null)
const handleFileChange = (event) => {
    file.value = event.target.files[0]
}
const user = ref({ avatar: '' })
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
        profileStore.avatar = user.value.avatar
    } catch (error) {
        console.error('Error uploading avatar:', error)
        ElMessage.error('头像上传失败')
    }
}
const companyCount = ref(profileStore.companyIds.length)
</script>

<template>
    <header class="header">
        <a-layout-header class="header-info">
            <div class="header-content">
                <div class="avatar">
                    <a-avatar
                        size="large"
                        :src="profileStore.avatar ? profileStore.avatar : avatar"
                        @click="uploadDialogVisible = true"
                    />
                    <div class="avatar-overlay" @click="uploadDialogVisible = true">
                        <Edit></Edit>
                    </div>
                </div>
                <div class="content">
                    <div class="content-title">
                        <span>{{ greetingTime }}</span>
                        <span>，</span>
                        <span class="text-red">{{ greetingName }}</span>
                        <span>，</span>
                        <span class="welcome-text">{{ greetingWord }}</span>
                    </div>
                    <div class="content-bottom text-self-gray">
                        <p>{{ profileStore.email }}</p>
                    </div>
                </div>
                <div class="stats">
                    <a-statistic title="公司数" :value="companyCount" class="statistic-item" />
                    <a-statistic title="文档数" :value="allDocumentCount" class="statistic-item" />
                    <a-statistic title="动态数" :value="totalLogs" class="statistic-item" />
                    <a-statistic title="我的ID" :value="profileStore.id" class="statistic-item" />
                </div>
            </div>
        </a-layout-header>
    </header>
    <h2 style="margin-left: 60px">工作台</h2>
    <div class="container">
        <main class="left-panel">
            <div class="left-panel-1">
                <staging-collect-list />
            </div>
            <div class="left-panel-2">
                <a-card title="日志">
                    <doc-log-list :logs="logs" />
                    <el-pagination
                        v-model:currentPage="currentPage"
                        :page-size="pageSize"
                        :total="totalLogs"
                        layout="total, prev, pager, next, jumper"
                        @size-change="handleSizeChange"
                        @current-change="handlePageChange"
                    />
                </a-card>
            </div>
        </main>
        <aside class="right-panel">
            <!-- 这里显示团队信息 -->
            <div class="right-top-info"><staging-navi /></div>
            <div style="margin-top: 20px">
                <a-card title="词云图"><word-cloud :words="profileStore.keywords" /></a-card>
            </div>
            <div class="right-bottom-member">
                <a-card title="工作日历">
                    <a-calendar :fullscreen="false" />
                </a-card>
            </div>
        </aside>
    </div>
    <el-dialog title="上传头像" v-model="uploadDialogVisible" width="550px">
        <input type="file" @change="handleFileChange" accept="image/*" />
        <template slot="footer" style="margin-left: 10px">
            <el-button @click="uploadDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="uploadAvatar">确 定</el-button>
        </template>
    </el-dialog>
</template>

<style scoped>
.avatar-overlay {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    height: 40%;
    width: 100%;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0 0 50% 50%;
    opacity: 0;
    transition: opacity 0.3s ease;
    cursor: pointer;
}

.avatar:hover .avatar-overlay {
    opacity: 1;
}

.avatar-overlay svg {
    color: white;
    width: 24px;
    height: 24px;
}
.text-red {
    --un-text-opacity: 1;
    color: rgba(248, 113, 113, var(--un-text-opacity));
    box-sizing: border-box;
}

.clickable {
    cursor: pointer;
}

.text-self-gray {
    color: #595959;
}

.header {
    display: flex;
    margin-top: 50px;
    margin-left: 100px;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;

    .header-info {
        padding: 16px 24px;
        display: flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
        border-radius: 8px;
    }

    .header-content {
        display: flex;
    }

    .avatar {
        position: relative;
        width: 80px;
        height: 80px;
        transition: transform 0.3s;
        border-radius: 50%;
        overflow: hidden;
        cursor: pointer;
    }

    .avatar > span {
        width: 100%;
        height: 100%;
        border: 1px solid rgba(102, 102, 102, 0.44);
    }

    .avatar:hover {
        transform: scale(1.1); /* Scale up the avatar slightly on hover */
    }

    .content {
        position: relative;
        top: 4px;
        flex: 1 1 auto;
        margin-left: 24px;
        line-height: 22px;
        margin-top: 4px;

        .content-title {
            margin-bottom: 12px;
            font-weight: 500;
            font-size: 20px;
            line-height: 28px;
            box-sizing: border-box;
            width: 500px;

            .welcome-text {
                box-sizing: border-box;
            }
        }

        .content-bottom {
            box-sizing: border-box;
            padding-bottom: 10px;
        }
    }

    .stats {
        width: 300px;
        margin-left: 400px;
        text-align: right;
        display: flex;
        flex: 0 1 auto;

        .statistic-item {
            margin-left: 20px;

            .ant-statistic-title {
                font-size: 12px;
                color: #666;
            }
        }

        .statistic-item:hover {
            transform: translateY(-1px); /* Lift up slightly on hover */
            transition: transform 0.3s;
        }
    }
}

.ant-statistic-content {
    font-size: 20px;
    text-align: center !important;
    color: #1890ff; /* Vibrant color for the numbers */
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle text shadow for depth */
}
.container {
    overflow-x: hidden;
    /* border: 1px solid red; */
    display: flex;
    width: 90%;
    margin: 20px 140px 20px 50px;
    padding: 20px;
    justify-content: space-between;
    .left-panel {
        /* border: 1px solid blue; */
        width: 60%;
        height: 100%;
        margin-right: 20px;
        /* 让团队卡片自动换行 */
        flex-wrap: wrap;
        flex-direction: row;

        .left-panel-1 {
            /* border: 1px solid red; */
            width: 100%;
            margin-bottom: 20px;
        }

        .left-panel-2 {
            width: 100%;
        }
    }

    .right-panel {
        /* border: 1px solid green; */
        width: 40%;
        height: 100%;

        .right-top-info {
            /* border: 1px solid yellow; */
            width: 100%;
        }

        .right-bottom-member {
            /* border: 1px solid pink; */
            height: calc(100% - 200px);
            margin-top: 20px;
        }
    }
}

:deep(.ant-statistic-content) {
    text-align: center;
}
</style>
