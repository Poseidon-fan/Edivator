<template>
    <div class="container">
        <main class="left-team-panel">
            <!-- 这里放所有团队文档卡片 -->
            <!--      添加新团队文档的卡片      -->
            <div class="team-card-brief">
                <a-card hoverable class="flexItem" @click="createTeamDoc">
                    <template #cover>
                        <plus-circle-outlined
                            style="position: relative; top: 30px; height: 230px; color: #1890ff; font-size: 120px"
                        />
                    </template>
                    <a-card-meta title="创建团队文档" description="点击此处创建团队文档" />
                </a-card>
            </div>
            <div class="team-card-brief" v-for="doc in documents" :key="doc.id">
                <!-- 单个团队文档卡片 -->
                <a-card hoverable @click="onClickTeamDoc(doc)">
                    <!-- 团队封面 -->
                    <template #cover>
                        <img
                            alt="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
                            :src="doc.cover"
                        />
                    </template>
                    <template #actions>
                        <setting-outlined key="setting" />
                        <edit-outlined key="edit" />
                        <ellipsis-outlined key="ellipsis" />
                    </template>
                    <a-card-meta :title="doc.name" :description="doc.description">
                        <template #avatar>
                            <a-avatar :src="doc.cover" />
                        </template>
                    </a-card-meta>
                </a-card>
            </div>
        </main>
        <aside class="right-panel">
            <!-- 这里显示团队信息 -->
            <div class="right-top-info">
                <div class="team-card-detailed">
                    <a-card
                        :title="currentTeam.name"
                        :tab-list="tabList"
                        :active-tab-key="activeTab"
                        @tabChange="(key) => onTabChange(key)"
                    >
                        <!--                        <template #extra>-->
                        <!--                            <a href="#">查看团队文档</a>-->
                        <!--                        </template>-->
                        <!-- tab标签页头 -->
                        <template #customTab="item">
                            <span v-if="item.key === 'teamInfo'">
                                <home-outlined />
                                {{ item.tab }}
                            </span>
                            <span v-if="item.key === 'teamNotification'">
                                <notification-outlined />
                                {{ item.tab }}
                            </span>
                        </template>
                        <!-- 内容区域 -->
                        <div class="team-content">
                            <div v-if="activeTab === 'teamInfo'">
                                <p>团队ID: {{ currentTeam.id }}</p>
                                <p>团队名称: {{ currentTeam.name }}</p>
                                <p>
                                    团队描述:
                                    {{ currentTeam.description || '暂无描述' }}
                                </p>
                            </div>
                            <div v-if="activeTab === 'teamNotification'">
                                <p>团队通知</p>
                            </div>
                        </div>
                    </a-card>
                </div>
            </div>
            <div class="right-bottom-member">
                <a-card title="成员信息">
                    <template #extra>
                        <a-dropdown>
                            <a class="ant-dropdown-link" @click.prevent>
                                成员管理
                                <UserOutlined />
                            </a>
                            <template #overlay>
                                <a-menu>
                                    <a-menu-item>
                                        <div @click="addTeamDocDialogVisible = true">添加成员</div>
                                    </a-menu-item>
                                    <a-menu-item>
                                        <div @click="addAdmin">添加管理员</div>
                                    </a-menu-item>
                                    <a-menu-item @click="inviteMember">邀请成员 </a-menu-item>
                                </a-menu>
                            </template>
                        </a-dropdown>
                    </template>
                    <!--                    <el-button-->
                    <!--                        type="success"-->
                    <!--                        @click="addTeamMemberDialogVisible = true"-->
                    <!--                    >-->
                    <!--                        拉人进团队-->
                    <!--                    </el-button>-->
                    <div class="member-card" v-for="member in currentTeam.members" :key="member.id">
                        <a-avatar :src="currentTeam.avatar">
                            {{ member.name }}
                        </a-avatar>
                        <span>{{ member.name }}</span>
                    </div>
                </a-card>
            </div>
        </aside>

        <!-- 邀请成员弹窗 -->
        <el-dialog title="邀请成员" v-model="dialogVisible" width="30%">
            <el-input v-model="inviteId" placeholder="请输入成员ID"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="generateInviteCode"> 生成邀请码 </el-button>
                </div>
            </template>
        </el-dialog>

        <!-- 添加团队文档弹窗 -->
        <a-modal
            v-model:visible="addTeamDocDialogVisible"
            title="新建文档"
            centered
            @ok="handleAddTeamDocOk"
            @cancel="handleAddTeamDocCancel"
        >
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
            </a-form>
        </a-modal>

        <!-- 添加团队成员弹窗 -->
        <el-dialog title="添加团队成员" v-model="addTeamMemberDialogVisible" width="30%">
            <el-input v-model="newTeamMemberId" placeholder="请输入新团队成员 Id"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="addTeamMemberDialogVisible = false"> 取 消 </el-button>
                    <el-button type="primary" @click="confirmAddTeamMember"> 确定 </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import {
    SettingOutlined,
    EditOutlined,
    EllipsisOutlined,
    HomeOutlined,
    NotificationOutlined,
    PlusCircleOutlined,
    UserOutlined,
    UploadOutlined,
} from '@ant-design/icons-vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import api from '@/api'
import { message } from 'ant-design-vue'
import env from '@/utils/env'

const vueRouter = useRouter()

onMounted(async () => {
    // 队伍信息
    const teamID = Number(vueRouter.currentRoute.value.params.tid)
    console.log('获取到团队ID:', teamID)
    const teamDetail = await api.queryTeam(teamID)
    const teamMembersInfo = await api.queryTeamMembers(teamID)
    console.log('团队（和成员）详情:', teamDetail, teamMembersInfo)
    currentTeam.value = {
        id: teamDetail.id,
        name: teamDetail.name,
        description: teamDetail.description,
        avatar: teamDetail.avatar,
        cover: teamDetail.cover,
        members: teamMembersInfo.map((m) => {
            return {
                id: m.id,
                name: m.username,
                avatar: m.avatar,
                email: m.email,
                mobile: m.mobile,
            }
        }),
    }
    // 文档信息
    const docs = await api.queryDocuments({
        team_id: teamID,
    })
    console.log('团队文档:', docs)
    documents.value = docs.map((d) => {
        return {
            id: d.id,
            name: d.name,
            description: d.description,
            cover: env.backEnd + d.avatar,
        }
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
</script>

<style scoped>
.container {
    /* border: 1px solid red; */
    display: flex;
    height: 90vh;
    width: 90%;
    margin: 20px 140px 20px 100px;
    padding: 20px;

    .left-team-panel {
        /* border: 1px solid blue; */
        width: 70%;
        height: 100%;
        margin-right: 20px;
        display: flex;
        /* 让团队卡片自动换行 */
        flex-wrap: wrap;
        flex-direction: row;
    }

    .right-panel {
        /* border: 1px solid green; */
        width: 30%;
        height: 100%;

        .right-top-info {
            /* border: 1px solid yellow; */
            height: 200px;
            width: 100%;
        }

        .right-bottom-member {
            /* border: 1px solid pink; */
            height: calc(100% - 200px);
            margin-top: 200px;
        }
    }
}

.team-card-brief {
    margin: 20px 20px 0 0;
    width: 300px;
    max-width: 300px;
    flex-grow: 1;
}

.team-card-detailed {
    width: 100%;
    height: 100%;

    .team-content {
        overflow-y: auto;
    }
}

.member-card {
    margin: 0 0 20px 0;

    span {
        margin: 0 0 0 10px;
    }
}

.buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}
</style>
