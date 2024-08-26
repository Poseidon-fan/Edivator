<template>
    <header class="navbar">
        <div class="navbar-container">
            <div class="navbar-left">
                <div class="logo">
                    <img style="height: 50px" src="@/assets/logo2.png" alt="" />
                </div>
                <nav>
                    <a @click.prevent="Methods.jump('/panel')" class="nav-link">工作台</a>
                    <a @click.prevent="Methods.jump('/documentCardsList')" class="nav-link">个人文档</a>
                    <a @click.prevent="Methods.jump('/team/manage')" v-if="companyStore.id" class="nav-link"
                        >我的企业</a
                    >
                    <a @click.prevent="Methods.jump('/doc/template')" class="nav-link">模板</a>
                </nav>
            </div>
            <div class="navbar-right" v-if="profileStore.username !== ''">
                <a
                    href="#"
                    class="nav-link bell"
                    @click.prevent="toggleNotifications"
                    style="cursor: pointer; position: relative; top: 3px; margin-right: 25px"
                    aria-label="bell-icon"
                >
                    <el-icon size="20"><Bell /></el-icon>
                    <span v-show="hasUnreadMessages" class="red-dot"></span>
                </a>
                <GlobalMessage
                    @allMessageRead="hasUnreadMessages = false"
                    @unreadMessage="hasUnreadMessages = true"
                    v-show="showNotificationDropdown"
                    @close="showNotificationDropdown = false"
                />
                <span>
                    你好，<span class="username">{{ profileStore.username }}</span>
                </span>
                <div class="nav-dropdown">
                    <a-popover :overlayStyle="{ position: fixed }">
                        <template #content>
                            <div class="avatar-hover-dropdown-card">
                                <!-- Card Content Start -->
                                <div class="card-header">
                                    <img
                                        :src="profile.avatar ? profile.avatar : avatar"
                                        alt="User Avatar"
                                        class="avatar"
                                        style="border: 1px solid #66666670"
                                    />
                                </div>
                                <a-divider />
                                <div class="card-body">
                                    <p>我的 E 币：{{ profile.money + '.0' }}</p>
                                    <a @click="Methods.jumpToUserHome()">个人设置</a>
                                    <a @click="logout()">退出登录</a>
                                    <a @click="openRechargeDialog">充值</a>
                                    <!-- 充值按钮 -->
                                </div>
                                <a-divider />
                                <div class="card-footer">
                                    <p>当前企业</p>
                                    <div class="company">
                                        <span class="company-name">{{ companyName }}</span>
                                        <a class="switch-company" @click="switchCompany">切换 <RightOutlined /></a>
                                    </div>
                                    <!--                                    <a href="#" class="admin-link">企业管理后台</a>-->
                                </div>
                                <!-- Card Content End -->
                            </div>
                        </template>
                        <img
                            :src="profile.avatar ? profile.avatar : avatar"
                            alt=""
                            class="avatar"
                            style="border: 1px solid #66666670"
                        />
                    </a-popover>
                </div>
            </div>
            <div class="navbar-right" v-else>
                <button class="login-button" @click="Methods.jump('/loginRegister')">登录/注册</button>
            </div>
        </div>

        <el-dialog
            title="充值"
            v-model="rechargeDialogVisible"
            width="30%"
            @close="handleRechargeDialogClose"
            class="recharge-dialog"
        >
            <el-row justify="center" class="recharge-options">
                <el-col :span="6">
                    <el-button type="primary" size="large" @click="recharge(20)" class="recharge-button">
                        充值 20 E 币
                    </el-button>
                </el-col>
                <el-col :span="6">
                    <el-button type="success" size="large" @click="recharge(50)" class="recharge-button">
                        充值 50 E 币
                    </el-button>
                </el-col>
                <el-col :span="6">
                    <el-button type="warning" size="large" @click="recharge(100)" class="recharge-button">
                        充值 100 E 币
                    </el-button>
                </el-col>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="rechargeDialogVisible = false">取消</el-button>
            </span>
        </el-dialog>
    </header>
</template>

<script setup>
import { ref, onMounted, computed, defineAsyncComponent } from 'vue'
import { useProfileStore, useCompanyStore } from '@/store/profile.ts'
import avatar from '@/assets/Global/avatar.jpg'
import router from '@/router'
import { Bell } from '@element-plus/icons-vue'
import Methods from '@/utils/UtilMethod.ts'
import { RightOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import axios from 'axios'
import env from '@/utils/env'
const api = axios.create({
    baseURL: env.backEnd,
    withCredentials: false,
    timeout: 50000,
})

const GlobalMessage = defineAsyncComponent(() => import('@/components/GlobalComponents/GlobalMessage.vue'))

const profile = useProfileStore()
const companyStore = useCompanyStore()
const showNotificationDropdown = ref(false)
const hasUnreadMessages = ref(true) // 示例：假设有未读消息
const companyName = computed(() => companyStore.name || `您还未选择企业`)
const logout = () => {
    profileStore.$reset()
    localStorage.removeItem('token')
    message.success('登出成功！')
    setTimeout(() => {
        Methods.jump('/loginRegister')
    }, 200)
}

const toggleNotifications = () => {
    const bellDom = document.querySelector('.bell')
    const tem = bellDom.getBoundingClientRect().left
    showNotificationDropdown.value = !showNotificationDropdown.value
    const notification = document.querySelector('.notification-dropdown')
    notification.style.left = tem - 190 + 'px'
}

const handleClickOutside = (event) => {
    const dropdown = document.querySelector('.notification-dropdown')
    const bellIcon = document.querySelector('.nav-link[aria-label="bell-icon"]')
    if (dropdown && !dropdown.contains(event.target) && !bellIcon.contains(event.target)) {
        showNotificationDropdown.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

// 示例：假设有函数来更新未读消息状态
// const updateUnreadMessages = () => {
//   hasUnreadMessages.value = // 获取未读消息状态
// }

const profileStore = useProfileStore()

const switchCompany = () => {
    Methods.jump('/company/switch')
}

const rechargeDialogVisible = ref(false) // 控制充值弹窗的显示与隐藏

const openRechargeDialog = () => {
    rechargeDialogVisible.value = true
}

const handleRechargeDialogClose = () => {
    rechargeDialogVisible.value = false
}

const recharge = async (amount) => {
    profileStore.money += amount
    message.success(`充值成功，已充值 ${amount} E 币`)
    await api.post(
        `users/recharge/`,
        { point: amount },
        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        }
    )
    rechargeDialogVisible.value = false
}
</script>

<style scoped>
.navbar {
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 105;
    background-color: #ffffff;
    padding: 10px 0;
    color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
}

.navbar-left,
.navbar-right {
    display: flex;
    align-items: center;
    color: #0d0d0d;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    color: #00b3b3;
    margin-right: 20px;
}

nav {
    display: flex;
    align-items: center;
}

.nav-link {
    color: #4f4c4d;
    margin: 0 10px;
    text-decoration: none;
    position: relative;
    font-size: 14px;
    cursor: pointer;
}

.nav-link.active {
    color: #00b3b3;
}

.nav-link:hover {
    color: #00b3b3;
}

.nav-dropdown {
    width: 100px;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: rgb(100, 100, 100);
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
    right: 0;
}

.nav-dropdown:hover .dropdown-content {
    display: block;
}

.dropdown-content a {
    color: white;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {
    background-color: #ddd;
    color: black;
}

.login-button {
    border: 1px solid #00b3b3;
    background-color: transparent;
    color: #00b3b3;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
}

.login-button:hover {
    background-color: #00b3b3;
    color: #fff;
}

.avatar {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    margin-left: 10px;
    cursor: pointer;
}

.username:hover {
    color: #00b3b3;
    cursor: pointer;
}

.avatar-hover-dropdown-card {
    width: 250px;
    background-color: white;
    border-radius: 4px;
    padding: 2px;

    .card-header {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #ddf1ff;
        border-radius: 7px;

        .avatar {
            position: relative;
            top: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 20px;
            font-weight: bold;
        }
    }

    .card-body {
        margin-top: 10px;
        display: flex;
        flex-direction: column;

        a {
            color: #4f4c4d;
            text-decoration: none;
            padding: 5px 0;
        }

        a:hover {
            color: #00b3b3;
        }
    }

    .card-footer {
        margin-top: 10px;
        display: flex;
        flex-direction: column;

        .company {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 0;
            margin-bottom: 10px;
            background: #eff6fc;
            width: 100%;
            border-radius: 7px;

            .company-name {
                margin-left: 5px;
            }
        }

        .switch-company {
            color: #777174;
            margin-right: 8px;
        }

        .admin-link {
            color: #4f4c4d;
            text-decoration: none;
            padding: 5px 0;
        }

        .admin-link:hover {
            color: #00b3b3;
        }
    }
}

.red-dot {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 8px;
    height: 8px;
    background-color: red;
    border-radius: 50%;
}

.recharge-dialog {
    border-radius: 8px;
}

.recharge-options {
    margin-top: 20px;
    gap: 30px;
}

.recharge-button {
    width: 100%;
    margin-bottom: 10px;
    border-radius: 4px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.dialog-footer {
    display: flex;
    justify-content: right;
    margin-top: 15px;
}

.dialog-footer .el-button {
    border-radius: 4px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
