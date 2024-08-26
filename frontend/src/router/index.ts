import { createRouter, createWebHistory, RouteRecordRaw, createWebHashHistory } from 'vue-router'

const LoginRegister = () => import('@/views/Login&Register/LoginRegister.vue')
const MainStaging = () => import('@/views/Panel/MainStaging.vue')
const DocumentCardsList = () => import('@/views/PersonalDocuments/DocumentCardsList.vue')
const CompanyDocumentCardsList = () => import('@/views/CompanyDocuments/CompanyDocumentCardsList.vue')
const Editor = () => import('@/views/Editor/Editor.vue')
const TeamDoc = () => import('@/views/Team/TeamDoc.vue')
const TeamCreate = () => import('@/views/Team/TeamCreate.vue')
const TeamManage = () => import('@/views/Team/TeamManage.vue')
const Home = () => import('@/views/Home/Home.vue')
const Modify = () => import('@/views/Home/Modify.vue')
const CreateCompany = () => import('@/views/Company/CreateCompany.vue')
const DocTemplate = () => import('@/views/DocTemplate/DocTemplate.vue')
const SwitchCompany = () => import('@/views/Company/SwitchCompany.vue')
const ChatCenter = () => import('@/views/ChatCenter.vue')

const routes: Array<RouteRecordRaw> = [
    {
        path: '/editor2',
        name: 'Editor2',
        component: () => import('@/components/Editor2/Editor.vue'),
    },
    {
        path: '/panel',
        name: 'ControlPanel',
        component: MainStaging,
    },
    {
        path: '/loginRegister',
        name: 'LoginRegister',
        component: LoginRegister,
    },
    {
        path: '/documentCardsList',
        name: 'DocumentCardsList',
        component: DocumentCardsList,
    },
    {
        path: '/doc/team/:tid',
        name: 'TeamDoc',
        component: TeamDoc,
    },
    {
        path: '/team/manage',
        name: 'TeamManage',
        component: TeamManage,
    },
    {
        path: '/team/create',
        name: 'TeamCreate',
        component: TeamCreate,
    },
    {
        // 这个 params 参数是编辑器对应文档的 id
        path: '/editor/:did',
        name: 'Editor',
        component: Editor,
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
    },
    {
        path: '/modify',
        name: 'Modify',
        component: Modify,
    },
    {
        path: '/company/create',
        name: 'CreateCompany',
        component: CreateCompany,
    },
    {
        path: '/doc/template',
        name: 'DocTemplate',
        component: DocTemplate,
    },
    {
        path: '/company/switch',
        name: 'SwitchCompany',
        component: SwitchCompany,
    },
    {
        path: '/companyDocumentCardsList',
        name: 'CompanyDocumentCardsList',
        component: CompanyDocumentCardsList,
    },
    {
        path: '/chat-center',
        name: 'ChatCenter',
        component: ChatCenter,
    }
]

const router = createRouter({
    // history: createWebHistory(process.env.BASE_URL),
    history: createWebHashHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    sessionStorage.setItem('preRoute', to.path)
    next()
})

export default router
