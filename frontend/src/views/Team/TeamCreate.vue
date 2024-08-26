<template>
    <div class="devops-container">
        <div class="left-side">
            <h1 class="title">立即开启 Edivator 团队协作</h1>
            <p class="subtitle">你的文档，可以在团队内自由协作，免费试用！</p>
            <div class="team-form">
                <a-form class="company-form-sub" :model="teamInfo" name="basic" autocomplete="off">
                    <a-form-item
                        label="团队名称"
                        name="teamName"
                        :rules="[{ required: true, message: '请输入团队名称' }]"
                    >
                        <a-input v-model:value="teamInfo.teamName" />
                    </a-form-item>

                    <a-form-item
                        label="团队简介"
                        name="teamDescription"
                        :rules="[{ required: true, message: '请输入团队简介' }]"
                    >
                        <a-input v-model:value="teamInfo.teamDescription" />
                    </a-form-item>

                    <a-form-item>
                        <a-button
                            style="width: 100%; height: 40px"
                            type="primary"
                            html-type="submit"
                            @click="createTeam"
                        >
                            立即创建
                        </a-button>
                    </a-form-item>
                </a-form>
            </div>
        </div>
        <div class="right-side">
            <div class="overlay">
                <img src="@/assets/logo2.png" alt="logo" />
                <ul class="features-list">
                    <li>文档协作</li>
                    <li>团队管理</li>
                    <li>智能写作</li>
                    <li>模板生成</li>
                    <li>AI洞察</li>
                    <li>云端同步</li>
                    <li>企业级管理</li>
                    <li>多模态OCR</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/api'
import UtilMethod from '@/utils/UtilMethod'
import { useRouter } from 'vue-router'
import { useCompanyStore } from '@/store/profile'

const teamInfo = ref({
    teamName: '',
    teamDescription: '',
    organizationScale: '',
})

const router = useRouter()
const companyStore = useCompanyStore()
const createTeam = async () => {
    const companyID = companyStore.id
    const ret = await api.createTeam({
        name: teamInfo.value.teamName,
        description: teamInfo.value.teamDescription,
        company_id: companyID,
    })

    console.log(`output->ret`, ret)
    if (ret.status === 201) {
        message.success('团队创建成功')
        await router.push('/team/manage')
    } else {
        console.error('团队创建失败', ret)
        message.error('团队创建失败，请重试')
    }
}
</script>

<style scoped>
.devops-container {
    display: flex;
    height: 100vh;
}

.right-side {
    position: relative;
    width: 50%;
    background: url('@/assets/yunxiao.png') no-repeat center center;
    background-size: cover;
    color: #000000;

    .features-list {
        list-style: none;
        padding: 0;
        font-size: 18px;
        text-align: left;
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* 两列布局 */
        gap: 20px; /* 列之间的间距 */

        li {
            display: flex;
            align-items: center;

            &:before {
                content: '✔';
                margin-right: 10px;
                color: #4caf50;
            }
        }
    }
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.logo {
    display: flex;
    align-items: center;
    margin-bottom: 50px;

    img {
        width: 40px;
        height: 40px;
        margin-right: 10px;
    }

    .logo-title {
        font-size: 45px;
        font-weight: bold;
    }
}

.left-side {
    width: 50%;
    padding: 50px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: white;

    .title {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .subtitle {
        font-size: 16px;
        color: #888;
        margin-bottom: 30px;
    }

    .team-form {
        .company-form-sub {
            width: 90%;
        }
    }

    .existing-company {
        margin-top: 20px;
        color: #888;

        a {
            color: #1890ff;
        }
    }
}
</style>
