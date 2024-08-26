<template>
    <header class="navbar">
        <div class="navbar-container">
            <div class="navbar-left">
                <div class="logo">Marker Career</div>
                <nav>
                    <a href="#" class="nav-link" @click.prevent="Methods.jump('/documentCardsList')">个人文档</a>
                    <a href="#" v-if="profileStore.eid" class="nav-link" @click.prevent="checkJump('/firmDetails')"
                        >我的企业</a
                    >
                    <a href="#" class="nav-link" @click.prevent="checkJump('/createPost')">模板</a>
                    <a href="#" class="nav-link" @click.prevent="checkJump('/chatroom')">工作台</a>
                </nav>
            </div>
            <div class="navbar-right" v-if="profileStore.username != ''">
                <a
                    href="#"
                    class="nav-link"
                    @click.prevent="toggleNotifications"
                    style="cursor: pointer; position: relative; top: 3px; margin-right: 25px"
                >
                    <el-icon size="20"><Bell /></el-icon>
                </a>
                <a style="cursor: pointer; position: relative; top: 3px; margin-right: 25px" @click="jump('/chatRoom')"
                    ><el-icon size="20"><ChatRound /></el-icon
                ></a>
                <GlobalMessage v-if="showNotificationDropdown" @close="showNotificationDropdown = false" />
                <span>
                    你好，<span class="username" @click="jump('/home')">{{ profileStore.username }}</span>
                </span>
                <div class="nav-dropdown">
                    <img :src="userAvatar" @click="jump('/home')" alt="User Avatar" class="avatar" />
                    <div class="dropdown-content">
                        <a href="#" @click.prevent="logout">退出登录</a>
                    </div>
                </div>
            </div>
            <div class="navbar-right" v-else>
                <button class="login-button" @click="jump('/loginRegister')">登录/注册</button>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProfileStore } from '@/stores/profile.ts'
import { useEnterpriseStore } from '@/stores/enterprise.ts'
import avatar from '@/assets/Global/avatar.jpg'
import Methods from '@/utils/UtilMethod.ts'
import { ElMessage } from 'element-plus'
import { Bell, ChatRound } from '@element-plus/icons-vue'

const showNotificationDropdown = ref(false)

const toggleNotifications = () => {
    showNotificationDropdown.value = !showNotificationDropdown.value
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

const profile = useProfileStore()
</script>

<style scoped>
.navbar {
    position: fixed;
    width: 100vw;
    z-index: 105;
    background-color: #1c1c1c;
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
    color: #fff;
    margin: 0 10px;
    text-decoration: none;
    position: relative;
    font-size: 14px;
}

.nav-link.active {
    color: #00b3b3;
}

.nav-link:hover {
    color: #00b3b3;
}

.nav-dropdown {
    position: relative;
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
    height: 40px;
    border-radius: 50%;
    margin-left: 10px;
    cursor: pointer;
}

.username:hover {
    color: #00b3b3;
    cursor: pointer;
}
</style>
