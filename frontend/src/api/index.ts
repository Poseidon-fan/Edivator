import axios from 'axios'
import env from '@/utils/env'
import { message } from 'ant-design-vue'
import UtilMethods from '@/utils/UtilMethod'
import { useCompanyStore, useProfileStore } from '@/store/profile'

const profile = useProfileStore()
const companyStore = useCompanyStore()
// 创建 Axios 实例
const api = axios.create({
    baseURL: env.backEnd,
    withCredentials: false,
    timeout: 50000,
})

// 延时函数
function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {
    // 获取当前用户
    getNowUser: async function () {
        const user = await api.get(`users/me`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
        console.log('update user profile after login', user.data)
        profile.updateProfile(user.data)
        return user.data
    },
    // 注册函数
    register: async function (params: { username: string; email: string; password: string }) {
        try {
            const isSuccess = (await api.post(`users/register/`, params)).status == 201
            if (isSuccess) {
                message.success('注册成功')
                const ret = await this.login({
                    username: params.username,
                    password: params.password,
                })
                if (ret) {
                    message.success('登录成功')
                    profile.updateProfile(ret)
                    setTimeout(() => {
                        UtilMethods.jump('/panel')
                    }, 500)
                }
            } else message.error('注册失败')
        } catch (error) {
            console.log(`output->error`, error)
            message.error(error.response.data.error)
        }
    },
    // 登录函数
    login: async function (params: { username: string; password: string }) {
        console.log(`output->login`)
        try {
            const user = await api.post(`users/login/`, params)
            localStorage.setItem('token', user.data.token)
            localStorage.setItem('refresh', user.data.refresh)
            const nowUser = await this.getNowUser()
            if (nowUser.company_ids.length > 0) {
                const company = await this.queryCompany(nowUser.company_ids[0])
                companyStore.updateCompany(company.data)
            }

            return nowUser
        } catch (error) {
            console.log(`output->error`, error)
            message.error(error.response.data.error[0])
            return null
        }
    },
    // 文本摘要
    abstract: async function (params: object) {
        return (await api.post(`ai/chat/summarize/`, params)).data.summary
    },
    // 文本修饰
    polish: async function (params: object) {
        return (await api.post(`ai/chat/polish/`, params)).data.polished
    },
    // 翻译
    translate: async function (params: object) {
        return (await api.post(`ai/chat/translate/`, params)).data.translated
    },
    // 续写
    continueWrite: async function (params: object) {
        return (await api.post(`ai/chat/continue_write/`, params)).data.continued
    },
    // 文本改错
    correct: async function (params: object) {
        return (await api.post(`ai/correct/`, params)).data.response
    },
    // 创建企业
    createCompany: async function (params: { name: string; description: string }) {
        return await api.post(`companies/create/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
    },
    // 添加企业管理员
    addAdmin: async function (params: object) {
        await api.post(`companies/appoint_admin/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
    },
    // 生成邀请码
    inviteCode: async function (params: object) {
        return (
            await api.post(`/invitations/generate/`, params, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data.token
    },
    // 查询团队详情
    queryTeam: async function (team_id: number): Promise<{
        name: string
        description: string
        avatar: string
        cover: string
        id: number
    }> {
        return (
            await api.get(`teams/query_detail/${team_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },
    // 查询团队成员
    queryTeamMembers: async function (team_id: number): Promise<
        {
            id: number
            username: string
            email: string
            mobile: string
            avatar: string
        }[]
    > {
        return (
            await api.get(`teams/query_users/${team_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },

    // 创建团队
    createTeam: async function (params: { name: string; company_id: number; description: string }) {
        return await api.post(`teams/create/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
    },
    // 添加团队成员
    addTeamMember: async function (params: object) {
        console.log(`output->params`, params)
        await api.post(`teams/add_user/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
    },
    // 获取用户信息
    getUserInfo: async function (uid: string) {
        return (
            await api.get(`users/${uid}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },
    // 加入企业
    joinCompany: async function (params: object) {
        return await api.post(`users/join_company/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 验证 token 是否有效，返回一个 Boolean
    validToken: async function (params: object) {
        return (await api.post(`users/token/verify/`, params)).status == 200
    },
    // 刷新 token
    refreshToken: async function (params: object) {
        const ret = (await api.post(`users/token/refresh/`, params)).data.access
        localStorage.setItem('token', ret)
    },
    // 上传头像
    uploadAvatar: async function (params: object) {
        // 正常情况下 id 从 pinia 中获取
        return (
            await api.post(`users/${profile.id}/avatar/upload/`, params, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'multipart/form-data',
                },
            })
        ).data.url
    },
    // 查询文档
    queryDocuments: async function (params: object): Promise<
        {
            id: number
            user: number
            team: number
            company: number
            template: number
            create_time: string
            update_time: string
            is_delete: boolean
            name: string
            description: string
            owner: number
            avatar: string
            version_counts: number
            creator: number
        }[]
    > {
        return (
            await api.get(`documents/query_doc/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
                params,
            })
        ).data
    },
    // 创建文档
    createDocument: async function (params: object) {
        return await api.post(`documents/create/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 修改文档的基本信息
    updateDocument: async function (id: string, params: object) {
        return await api.put(`documents/update/${id}/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 获取一个文档的全部版本
    queryVersions: async function (params: object) {
        return (
            await api.get(`documents/query_version/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
                params,
            })
        ).data
    },
    // 创建文档的新版本
    createVersion: async function (params: object) {
        return (
            await api.post(`documents/versions/create/`, params, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },
    // 更新版本内容
    updateVersion: async function (pk: string, params: object) {
        return (
            await api.put(`documents/versions/update/${pk}/`, params, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },
    // 查询企业的创建者
    queryCreator: async function (company_id: string) {
        const ret = await api.get(`/companies/query_admin/${company_id}/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
        console.log(`output->ret`, ret)
        return ret.data
    },
    // 查询企业的所有管理员
    queryAdmins: async function (company_id: string) {
        const ret = await api.get(`/companies/query_administrators/${company_id}/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
        console.log(`output->ret`, ret)
        return ret.data
    },
    // 查找企业中所有团队
    queryCompanyTeams: async function (company_id: number) {
        return (
            await api.get(`/companies/query_teams/${company_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 查找企业中所有团队简略信息
    queryCompanyTeamsShort: async function (company_id: number) {
        return (
            await api.get(`/companies/query_teams_short/${company_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 查询企业中的所有用户
    queryCompanyMembers: async function (company_id: string) {
        return (
            await api.get(`/companies/query_users/${company_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 查询某团队的具体信息
    queryTeamDetail: async function (team_id: string) {
        return (
            await api.get(`/teams/query_detail/${team_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 查询某公司的具体信息
    queryCompanyDetail: async function (company_id: number) {
        return (
            await api.get(`/companies/query_detail/${company_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 上传文档中的文件到后端
    uploadDocumentFile: async function (params: object) {
        // 正常情况下 id 从 pinia 中获取
        return (
            env.backEnd.slice(0, -1) +
            (
                await api.post(`documents/inner_files/create/`, params, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'multipart/form-data',
                    },
                })
            ).data.file
        )
    },
    // 调用 OCR
    OCR: async function (params: object) {
        console.log(`output->params`, params)
        return await api.post(`ai/ocr/infer/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 普通大模型对话
    chat: async function (params: object) {
        return await api.post(`ai/chat/common_chat/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 提取样式
    extractStyle: async function (params: object) {
        return await api.post(`ai/extract_style/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 上传用户对话
    uploadAiChat: async function (params: object) {
        await api.post(`ai/dialogs/create/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 查询用户对话
    queryAiChat: async function (params: object) {
        return (
            await api.get(`ai/dialogs/query/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
                params,
            })
        ).data
    },
    // 以特定的风格生成文本
    generateText: async function (params: object) {
        return (
            await api.post(`ai/chat/styled_ggenerate/`, params, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data.response
    },
    // 查询企业信息
    queryCompany: async function (company_id: number) {
        return await api.get(`/companies/query_detail/${company_id}/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        })
    },
    // 申请加入团队
    applyJoinTeam: async function (team_id: number) {
        return await api.post(
            `/teams/messages/applicate/`,
            {
                team: team_id,
            },
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            }
        )
    },
    // 查询我在公司的团队
    queryMyTeams: async function (companyID: number): Promise<
        {
            team_detail: {
                name: string
                description: string
                avatar: string
                cover: string
                id: number
            }
            members: {
                id: number
                username: string
                email: string
                mobile: number
                avatar: string
            }[]
        }[]
    > {
        return (
            await api.get(`/teams/query_belonged_teams/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
                params: {
                    company_id: companyID,
                },
            })
        ).data
    },
    // 获取所有的通知
    getAllNotifications: async function (params: Object) {
        return (
            await api.get(`/teams/notifications/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },
    // 获取日志
    queryLogs: async function (param: object) {
        return (
            await api.get(`/documents/query_logs/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
                params: param,
            })
        ).data
    },
    // 获取所有等待处理的消息
    queryMessages: async function (company_id: string) {
        return (
            await api.get(`/teams/messages/query_pendings/?company_id=${company_id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            })
        ).data
    },
    // 批准加入团队
    approveApplication: async function (id: string) {
        await api.post(`/teams/messages/approve/${id}/`, null, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 拒绝加入团队
    rejectApplication: async function (id: string) {
        await api.post(`/teams/messages/reject/${id}/`, null, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 将通知标记为已读
    markAsRead: async function (params: Object) {
        await api.post(`/teams/notifications/mark-as-read/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 生成图片
    generateImage: async function (params: Object) {
        const taskId = (
            await api.post(`ai/pictures/generate/`, params, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data.data.primaryTaskId

        console.log(`output->taskId`, taskId)
        await delay(5000)

        return (
            await api.post(
                `ai/pictures/get_img/`,
                { taskId },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                }
            )
        ).data.img
    },
    // 语音识别
    voiceRecognize: async function (params: object) {
        return await api.post(`ai/speeches/recognize/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 图片目标检测
    objectDetect: async function (params: object) {
        return await api.post(`ai/ocr/pattern/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 获取用户收藏的所有文档
    queryFavorite: async function () {
        return (
            await api.get(`documents/collects/query/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 收藏 / 取消收藏文档
    toggleFavorite: async function (params: object) {
        await api.post(`documents/collects/do/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 解散团队
    deleteTeam: async function (team_id: string) {
        return await api.delete(`/teams/delete/${team_id}/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 删除文档
    deleteDocument: async function (id: string) {
        return await api.delete(`documents/delete/${id}/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 退出团队
    leaveTeam: async function (team_id: string) {
        return await api.post(`/teams/exit/${team_id}/`, null, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 查询所有公共模板
    queryPublicTemplates: async function () {
        return (
            await api.get(`documents/templates/query_public/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 获取用户所有的个人模板
    qeuryPersonalTemplates: async function () {
        return (
            await api.get(`documents/templates/query_private/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 创建文件模板
    createTemplate: async function () {
        return await api.post(`documents/templates/create/`, null, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    // 根据 id 查询指定文档
    queryDocumentById: async function (doc_id: string) {
        return (
            await api.get(`documents/query_single_doc/${doc_id}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 更新文档关键词
    updateKeywords: async function (document_id: string, params: object) {
        return await api.put(`documents/update_keywords/${document_id}/`, params, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'multipart/form-data',
            },
        })
    },
    // 查找文档
    searchDocuments: async function (params: Object) {
        return await api.get(`documents/search_by_keyword/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
            params,
        })
    },
    // 获取用户文档总数
    getTotalDocumentCounts: async function () {
        return (
            await api.get(`users/get_doc_num/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            })
        ).data
    },
    // 充值 E 币
    recharge: async function (point) {
        await api.post(`users/recharge/`, {point}, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
    },
    getMessages: async function (group_id: number) {
        try {
            const res = await api.get('messages/query/?group_id=' + group_id, {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                }
            })
            return res.data
        } catch (e) {
            console.log('error when get messages', e)
            return null
        }
    },
}
