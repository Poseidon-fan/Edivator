<template>
    <div class="team-container">
        <div class="header">
            <h1>企业</h1>
        </div>
        <div class="buttons">
            <el-button type="primary" @click="addAdmin">添加管理员</el-button>
            <el-button type="success" @click="inviteMember"> 邀请成员 </el-button>
        </div>

        <!-- 邀请成员弹窗 -->
        <el-dialog title="邀请成员" v-model="dialogVisible" width="30%">
            <el-input v-model="inviteId" placeholder="请输入成员ID"></el-input>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="generateInviteCode"> 生成邀请码 </el-button>
            </div>
        </el-dialog>

        <!-- 添加管理员弹窗 -->
        <el-dialog title="添加管理员" v-model="addAdminDialogVisible" width="30%">
            <el-select v-model="selectedAdminId" placeholder="请选择成员">
                <el-option v-for="member in availableAdmins" :key="member.id" :label="member.name" :value="member.id">
                    <template #default="{ name }">
                        <a-avatar :src="avatar">{{ name }}</a-avatar>
                        <span>{{ member.name }}</span>
                    </template>
                </el-option>
            </el-select>
            <div slot="footer" class="dialog-footer">
                <el-button @click="addAdminDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="confirmAddAdmin">确 定</el-button>
            </div>
        </el-dialog>

        <!-- 添加团队成员弹窗 -->
        <el-dialog title="添加成员" v-model="addTeamMemberDialogVisible" width="30%">
            <el-select v-model="selectedMemberId" placeholder="请选择成员">
                <el-option v-for="member in availableMembers" :key="member.id" :label="member.name" :value="member.id">
                    <template #default="{ name }">
                        <a-avatar :src="avatar">{{ name }}</a-avatar>
                        <span>{{ member.name }}</span>
                    </template>
                </el-option>
            </el-select>
            <div slot="footer" class="dialog-footer">
                <el-button @click="addTeamMemberDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="confirmAddTeamMember">确 定</el-button>
            </div>
        </el-dialog>

        <MessageList />

        <a-divider />
        <h2>企业文档</h2>
        <div class="company-doc-region">
            <div class="left-panel">
                <!--      添加新团队文档的卡片      -->
                <div class="team-card-brief">
                    <a-card hoverable class="flexItem" @click="createTeamDoc" style="height: 100%">
                        <template #cover>
                            <plus-circle-outlined
                                style="position: relative; top: 30px; height: 230px; color: #1890ff; font-size: 120px"
                            />
                        </template>
                        <a-card-meta title="创建企业文档" description="点击此处创建企业文档" />
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
                        <a-card-meta :title="doc.name">
                            <template #avatar>
                                <a-avatar :src="doc.cover" size="large"></a-avatar>
                            </template>
                            <template #description>
                                <Paragraph :ellipsis="{ rows: 2, expandable: false }">
                                    {{ doc.description }}
                                </Paragraph>
                            </template>
                        </a-card-meta>
                    </a-card>
                </div>
            </div>
            <div class="right-panel" v-show="showRightPanel">
                <a-card :bordered="false" class="log-card" title="企业动态">
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
        </div>
        <a-divider />
        <div class="header">
            <h2>全部团队</h2>
            <a-tooltip title="企业管理员可操作" placement="top" trigger="click">
                <a-button type="primary" :disabled="!companyStore.isAdmin()" @click="createTeam">创建团队</a-button>
            </a-tooltip>
        </div>
        <div class="tabs">
            <a-tabs v-model:activeKey="activeTab">
                <a-tab-pane key="all" tab="公司团队">
                    <a-table :columns="columns" :dataSource="teamsInCompany">
                        <template #bodyCell="{ column, record }">
                            <!--          团队名          -->
                            <template v-if="column.key === 'name'">
                                <a-avatar
                                    class="teamAvatar"
                                    shape="square"
                                    size="large"
                                    :src="record.avatar ? record.avatar : teamAvatar"
                                />
                                <a style="margin-left: 10px" @click="onClickTeamName(record)">{{ record.name }} </a>
                            </template>
                            <template v-else-if="column.key === 'description'">
                                {{ record.description || '这个团队很懒，没有写描述:(' }}
                            </template>
                            <template v-else-if="column.key === 'members'">
                                <!--          团队成员          -->
                                <a-avatar-group
                                    :max-count="2"
                                    size="large"
                                    :max-style="{
                                        color: '#f56a00',
                                        backgroundColor: '#fde3cf',
                                    }"
                                >
                                    <a-tooltip
                                        v-for="(member, index) in record.members"
                                        :key="index"
                                        :title="member.username"
                                        placement="top"
                                    >
                                        <a-avatar
                                            :src="
                                                member.avatar ? `${env.backEnd.slice(0, -1)}${member.avatar}` : avatar
                                            "
                                        ></a-avatar>
                                    </a-tooltip>
                                </a-avatar-group>
                            </template>
                            <template v-else-if="column.key === 'action'">
                                <a-popconfirm
                                    title="确定向管理员申请加入该团队吗？"
                                    ok-text="是"
                                    cancel-text="否"
                                    @confirm="applyEnterTeam(record.id)"
                                >
                                    <a-button type="link" v-if="!record.isMember">
                                        <template #icon>
                                            <user-add-outlined />
                                        </template>
                                        申请加入
                                    </a-button>
                                </a-popconfirm>

                                <a-divider type="vertical" />
                                <a-tooltip title="企业管理员可操作" placement="top" trigger="click">
                                    <a-dropdown :disabled="!isAdmin">
                                        <a class="ant-dropdown-link" @click.prevent>
                                            <TeamOutlined />
                                            管理团队
                                            <DownOutlined />
                                        </a>
                                        <template #overlay>
                                            <a-menu>
                                                <a-menu-item>
                                                    <a-button type="link" @click="addUser(record.id, record)">
                                                        <template #icon>
                                                            <UsergroupAddOutlined />
                                                        </template>
                                                        添加成员
                                                    </a-button>
                                                </a-menu-item>
                                                <a-menu-item>
                                                    <a-popconfirm
                                                        title="确定解散该团队吗？"
                                                        ok-text="是"
                                                        cancel-text="否"
                                                        @confirm="deleteTeam(record.id)"
                                                    >
                                                        <a-button style="color: #ec0b0b" type="link">
                                                            <template #icon>
                                                                <UsergroupDeleteOutlined />
                                                            </template>
                                                            解散团队
                                                        </a-button>
                                                    </a-popconfirm>
                                                </a-menu-item>
                                            </a-menu>
                                        </template>
                                    </a-dropdown>
                                </a-tooltip>
                            </template>
                        </template>
                    </a-table>
                </a-tab-pane>
                <a-tab-pane key="joined" tab="我加入的">
                    <a-table :columns="myColumns" :dataSource="teamsOfMine">
                        <template #bodyCell="{ column, record }">
                            <!--          团队名          -->
                            <template v-if="column.key === 'name'">
                                <a-avatar
                                    class="teamAvatar"
                                    shape="square"
                                    size="large"
                                    :src="record.avatar ? record.avatar : teamAvatar"
                                />
                                <a style="margin-left: 10px" @click="onClickTeamName(record)">{{ record.name }} </a>
                            </template>
                            <template v-else-if="column.key === 'description'">
                                {{ record.description || '这个团队很懒，没有写描述:(' }}
                            </template>
                            <template v-else-if="column.key === 'members'">
                                <!--          团队成员          -->
                                <!-- TODO 示例图片 -->
                                <a-avatar-group
                                    :max-count="2"
                                    size="large"
                                    :max-style="{
                                        color: '#f56a00',
                                        backgroundColor: '#fde3cf',
                                    }"
                                >
                                    <a-tooltip
                                        v-for="(member, index) in record.members"
                                        :key="index"
                                        title="member.username"
                                        placement="top"
                                    >
                                        <a-avatar
                                            :src="
                                                member.avatar ? `${env.backEnd.slice(0, -1)}${member.avatar}` : avatar
                                            "
                                        ></a-avatar>
                                    </a-tooltip>
                                </a-avatar-group>
                            </template>
                            <template v-else-if="column.key === 'action'">
                                <a-popconfirm
                                    title="确定退出该团队吗？"
                                    ok-text="是"
                                    cancel-text="否"
                                    @confirm="leaveTeam(record.id)"
                                >
                                    <a-button style="color: #ec0b0b" type="link">
                                        <template #icon>
                                            <user-add-outlined />
                                        </template>
                                        退出团队
                                    </a-button>
                                </a-popconfirm>
                            </template>
                        </template>
                    </a-table>
                </a-tab-pane>
            </a-tabs>
        </div>

        <a-divider />
        <h2>企业成员</h2>
        <div class="company-members">
            <a-table :columns="memberColumns" :dataSource="companyUsers">
                <template #bodyCell="{ column, record }">
                    <template v-if="column.key === 'avatar'">
                        <a-avatar class="memberAvatar" :src="record.avatar ? record.avatar : avatar" />
                    </template>
                    <template v-else-if="column.key === 'name'">
                        <span :class="{ 'admin-label': record.isAdmin }">{{ record.name }}</span>
                    </template>
                    <template v-else-if="column.key === 'email'">
                        {{ record.email }}
                    </template>
                    <template v-else-if="column.key === 'mobile'">
                        {{ record.mobile }}
                    </template>
                </template>
            </a-table>
        </div>

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
                    <div v-if="form.documentCover.length" style="width: 472px">
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
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import DocLogList from '@/components/GlobalComponents/DocLogList.vue'
import api from '@/api'
import { useCompanyStore } from '@/store/profile'
import {
    UserOutlined,
    AntDesignOutlined,
    EditOutlined,
    SettingOutlined,
    PlusCircleOutlined,
    EllipsisOutlined,
    UploadOutlined,
} from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import {
    DownOutlined,
    UserAddOutlined,
    UsergroupAddOutlined,
    UsergroupDeleteOutlined,
    TeamOutlined,
} from '@ant-design/icons-vue'
import { message, Card, Avatar, Modal, Form, Input, Typography, Upload, Button } from 'ant-design-vue'
import MessageList from '@/components/Team/MessageList.vue'
import { useProfileStore } from '@/store/profile.ts'
import { ElMessageBox, ElMessage, ElPagination } from 'element-plus'
const profile = useProfileStore()
import env from '@/utils/env'
const { Paragraph } = Typography
import avatar from '@/assets/Global/avatar.jpg'
import teamAvatar from '@/assets/images/teamAvatar.png'

// 企业文档相关
const logs = ref([])

const getURL = (url) => {
    console.log(`output->url`, url)
    URL.createObjectURL(url)
}

// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)
const totalLogs = ref(0)

// 获取分页日志数据
const getLogs = async (page = 1, size = 10) => {
    try {
        const res = await api.queryLogs({ company_id: companyStore.id, page, size })
        logs.value = res.results
        totalLogs.value = res.count
        console.log('logs value', res, logs.value)
    } catch (err) {
        message.error('获取log失败')
        console.error('获取log失败:', err)
    }
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
    form.value.documentCover = [file]
    form.value.documentCover[0].url = URL.createObjectURL(file)
    return false
}
const form = ref({
    documentName: '',
    documentDescription: '',
    documentCover: [],
    templateId: null,
})
const handleAddTeamDocCancel = () => {
    form.value.documentName = ''
    form.value.documentDescription = ''
    form.value.documentCover = []
    addTeamDocDialogVisible.value = false
}
const handleAddTeamDocOk = async () => {
    const formData = new FormData()
    if (!form.value.documentCover.length) {
        message.error('请先上传封面')
        return
    }
    console.log(`output->form.value.documentCover`, form.value.documentCover[0])
    formData.append('avatar', form.value.documentCover[0].originFileObj)
    formData.append('name', form.value.documentName)
    formData.append('description', form.value.documentDescription)
    formData.append('owner', '3')
    formData.append('owner_id', companyStore.id.toString())
    formData.append('template', form.value.templateId)

    try {
        const response = await api.createDocument(formData)
        if (response.status === 201) {
            message.success('文档创建成功')
            const docs = await api.queryDocuments({
                company_id: companyStore.id,
            })
            documents.value = docs.map((d) => {
                return {
                    id: d.id,
                    name: d.name,
                    description: d.description,
                    cover: d.avatar
                        ? env.backEnd.slice(0, -1) + d.avatar
                        : 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
                }
            })
            addTeamDocDialogVisible.value = false
        } else {
            message.error('文档创建失败')
        }
    } catch (error) {
        console.error('文档创建错误:', error)
        message.error(error.response.data.error)
    }
}
import Methods from '@/utils/UtilMethod.ts'
const showRightPanel = ref(true)
const onClickTeamDoc = (doc) => {
    Methods.jump(`/editor/${doc.id}`)
}
const documents = ref<
    {
        id: number
        name: string
        description: string
        cover: string | null
    }[]
>([])
const addTeamDocDialogVisible = ref(false)
const createTeamDoc = () => {
    addTeamDocDialogVisible.value = true
}

const companyStore = useCompanyStore()
const vueRouter = useRouter()
const activeTab = ref<string>('all')
const createTeam = () => {
    vueRouter.push('/team/create')
}
const onClickTeamName = (team) => {
    vueRouter.push(`/doc/team/${team.id}`)
}

const isAdmin = computed(() => {
    return companyStore.isAdmin()
})

const columns = [
    {
        title: '团队名称',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '团队描述',
        dataIndex: 'description',
        key: 'description',
    },
    {
        title: '团队成员',
        dataIndex: 'members',
        key: 'members',
    },
    {
        title: '操作',
        key: 'action',
    },
]

const myColumns = [
    {
        title: '团队名称',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '团队描述',
        dataIndex: 'description',
        key: 'description',
    },
    {
        title: '团队成员',
        dataIndex: 'members',
        key: 'members',
    },
    {
        title: '操作',
        key: 'action',
    },
]

const memberColumns = [
    {
        title: '头像',
        dataIndex: 'avatar',
        key: 'avatar',
    },
    {
        title: '姓名',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '邮箱',
        dataIndex: 'email',
        key: 'email',
    },
    {
        title: '手机号',
        dataIndex: 'mobile',
        key: 'mobile',
    },
]

type Team = {
    team_detail: {
        name: string
        description: string
        avatar: string
        cover: string
        id: number
    }
    members: Array<{
        id: number
        username: string
        email: string
        mobile: number
        avatar: string
    }>
}
const teamsInCompany = ref([])
const teamsOfMine = ref([])

// 随机头像
const randomAvatar = (key) => {
    return `https://xsgames.co/randomusers/avatar/${key}`
}

const pullTeamsInCompany: () => Promise<Team[]> = async () => {
    const companyID = companyStore.id
    const farTeams: Team[] = await api.queryCompanyTeams(companyID)
    console.log(`output->farTeams`, farTeams)
    for (let i = 0; i < farTeams.length; i++) {
        let flag = false
        for (let j = 0; j < farTeams[i].members.length; j++) {
            if (farTeams[i].members[j].id == profile.id) {
                flag = true
                break
            }
        }
        farTeams[i]['team_detail'].isMember = flag
    }
    return farTeams
}

const applyEnterTeam = (teamID: number) => {
    console.log('申请加入团队', teamID)
    api.applyJoinTeam(teamID)
        .then((res) => {
            console.log('申请成功', res)
            if (res.status === 201) {
                message.success('申请成功，等待管理员审批')
            }
        })
        .catch((err) => {
            console.error('申请失败', err)
            message.error('申请失败：' + err.response.data.detail || '请稍后重试')
        })
}

const deleteTeam = (teamID: number) => {
    console.log('解散团队', teamID)
    api.deleteTeam(teamID)
        .then((res) => {
            console.log('解散成功', res)
            if (res.status === 204) {
                message.success('解散成功')
            }
            console.log(`output->teamsInCompany.value`, teamsInCompany.value.length)
            for (let i = 0; i < teamsInCompany.value.length; i++) {
                if (teamsInCompany.value[i].id == teamID) {
                    teamsInCompany.value.splice(i, 1)
                    break
                }
            }
        })
        .catch((err) => {
            console.error('解散失败', err)
            message.error('解散失败，请稍后重试')
        })
}

const leaveTeam = (teamID: number) => {
    api.leaveTeam(teamID)
        .then((res) => {
            if (res.status === 204) {
                message.success('退出成功')
            }
            for (let i = 0; i < teamsOfMine.value.length; i++) {
                if (teamsOfMine.value[i].id == teamID) {
                    teamsOfMine.value.splice(i, 1)
                    break
                }
            }
        })
        .catch((err) => {
            console.error('退出失败', err)
            message.error('退出失败，请稍后重试')
        })
}

const teams = ref([])
const companyUsers = ref([])
const companyState = useCompanyStore()
const selectedTeam = ref(
    teams.value.length > 0
        ? teams.value[0]
        : {
              team_detail: {
                  id: 0,
                  name: '您还没有团队',
                  description: '快去创建团队吧！',
                  avatar: 'https://joeschmoe.io/api/v1/random',
                  cover: 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
              },
              members: [],
          }
)
const activeTeamId = ref(0)

const addUser = (id, team) => {
    addTeamMemberDialogVisible.value = true
    activeTeamId.value = id
    selectedTeam.value = team
    addTeamMember()
}

const templates = ref([])

onMounted(async () => {
    // 拉取企业文档
    const docs = await api.queryDocuments({
        company_id: companyStore.id,
    })
    console.log(`output->docs`, docs)
    documents.value = docs.map((d) => {
        return {
            id: d.id,
            name: d.name,
            description: d.description,
            cover: d.avatar
                ? env.backEnd.slice(0, -1) + d.avatar
                : 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
        }
    })

    templates.value = await api.queryPublicTemplates()
    form.value.templateId = templates.value[0].id
    console.log(`output->templates`, templates)

    // 拉取公司团队
    const pulledTeamsInCompany = await pullTeamsInCompany()
    teamsInCompany.value = pulledTeamsInCompany.map((t) => {
        return {
            ...t.team_detail,
            members: t.members,
        }
    })
    teams.value = teamsInCompany.value
    companyUsers.value = await api.queryCompanyMembers(companyStore.id)
    console.log('teamsInCompany', companyUsers.value, teams.value)

    // 拉取我所在的团队
    const pulledMyTeams = await api.queryMyTeams(companyStore.id)
    teamsOfMine.value = pulledMyTeams.map((t) => {
        return {
            ...t.team_detail,
            members: t.members,
        }
    })

    api.queryMessages(companyStore.id)
    // 获取logs
    getLogs()
})

// 添加管理员
const addAdminDialogVisible = ref(false)
const selectedAdminId = ref(null)
const availableAdmins = ref([])
const addAdmin = async () => {
    availableAdmins.value = []
    const tem = await api.queryAdmins(companyStore.id)
    for (let i = 0; i < companyUsers.value.length; i++) {
        let flag = false
        for (let j = 0; j < tem.length; j++) {
            if (companyUsers.value[i].id == tem[j].id) {
                flag = true
                break
            }
        }
        if (!flag) availableAdmins.value.push(companyUsers.value[i])
    }
    addAdminDialogVisible.value = true
}

const confirmAddAdmin = async () => {
    if (selectedAdminId.value) {
        await api.addAdmin({
            company_id: companyStore.id,
            target_user_id: selectedAdminId.value,
        })
        ElMessage.success(`管理员已成功添加`)
        addAdminDialogVisible.value = false
    }
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
        company_id: profile.companyIds[0],
        user_id: inviteId.value,
    })
    ElMessageBox.alert(`邀请码为：${inviteCode}`, '邀请码', {
        confirmButtonText: '确定',
    })
    dialogVisible.value = false
}

// 向团队添加成员
const addTeamMemberDialogVisible = ref(false)
const newTeamMemberId = ref('')
const availableMembers = ref([])
const selectedMemberId = ref(null)
const selectedMember = ref(null)
const addTeamMember = async () => {
    availableMembers.value = []
    const tem = await api.queryTeamMembers(activeTeamId.value)
    console.log(`output->tem`, tem)
    for (let i = 0; i < companyUsers.value.length; i++) {
        let flag = false
        for (let j = 0; j < tem.length; j++) {
            if (companyUsers.value[i].id == tem[j].id) {
                flag = true
            }
            if (flag) break
        }
        console.log(`output->i, flag`, i, flag)
        if (!flag) availableMembers.value.push(companyUsers.value[i])
    }
    addTeamMemberDialogVisible.value = true
}

const confirmAddTeamMember = async () => {
    if (selectedMemberId.value) {
        for (let i = 0; i < availableMembers.value.length; i++) {
            if (availableMembers.value[i].id == selectedMemberId.value) {
                selectedMember.value = availableMembers.value[i]
                break
            }
        }

        console.log(`output->selectedTeam.value`, selectedTeam.value)
        await api.addTeamMember({
            company_id: profile.companyIds[0],
            team_name: selectedTeam.value.name,
            user_id: selectedMemberId.value,
        })
        ElMessage.success(`成员 ${selectedMember.value.name} 已添加到团队 ${selectedTeam.value['team_detail'].name}`)
        addTeamMemberDialogVisible.value = false
        selectedTeam.value.members.push(selectedMember.value)
        selectedMemberId.value = 0
        selectedMember.value = null
    }
}
</script>

<style scoped>
.team-container {
    margin: 40px;
    margin-top: 50px;
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.tabs {
    margin-bottom: 20px;
}

.common-teams {
    height: 200px;
}

.common-teams-placeholder {
    background: #fff;
    padding: 20px;
    text-align: center;
    color: #888;
}

.all-teams-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.all-teams-header a-button {
    margin-right: 10px;
}

.company-doc-region {
    /* border: 1px solid blue; */
    height: 100%;
    margin-right: 20px;
    display: flex;
    /* 让团队卡片自动换行 */
    flex-wrap: wrap;
    flex-direction: row;
    padding: 20px;

    .team-card-brief {
        margin: 20px 20px 0 0;
        width: 295px;
        max-width: 300px;
        flex-grow: 1;
    }

    .left-panel {
        /* border: 1px solid blue; */
        width: 70%;
        height: 100%;
        display: flex;
        /* 让团队卡片自动换行 */
        flex-wrap: wrap;
        flex-direction: row;
    }

    .right-panel {
        height: 100%;
        width: 30%;
        max-width: 400px;

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

.document-cover-preview {
    display: inline-block;
    width: 400px;
    margin-left: 36px;
    margin-top: 20px;
}

.dialog-footer {
    margin-top: 20px;
}

:deep(.ant-card-cover > img) {
    height: 200px;
}

.admin-label {
    font-weight: bold;
    color: red;
}

.memberAvatar {
    transform: scale(1.5);
}

.teamAvatar {
    border: #eee solid 1px;
}
</style>
