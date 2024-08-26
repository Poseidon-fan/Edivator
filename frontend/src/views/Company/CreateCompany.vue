<template>
    <div class="devops-container">
        <div class="left-side">
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
        <div class="right-side">
            <h1 class="title">立即开启 Edivator Cloud</h1>
            <p class="subtitle">你的团队，可以在企业内协作，免费试用！</p>
            <div class="company-form">
                <a-form class="company-form-sub" :model="companyInfo" name="basic" autocomplete="off">
                    <a-form-item
                        label="公司名称"
                        name="companyName"
                        :rules="[{ required: true, message: '请输入公司名称' }]"
                    >
                        <a-input v-model:value="companyInfo.companyName" />
                    </a-form-item>

                    <a-form-item
                        label="公司简介"
                        name="companyDescription"
                        :rules="[{ required: true, message: '请输入公司简介' }]"
                    >
                        <a-input v-model:value="companyInfo.companyDescription" />
                    </a-form-item>

                    <a-form-item>
                        <a-button
                            style="width: 100%; height: 40px"
                            type="primary"
                            html-type="submit"
                            @click="createCompany"
                        >
                            立即创建
                        </a-button>
                    </a-form-item>
                </a-form>
            </div>
            <p class="existing-company">已有其他企业？<a @click.prevent="joinCompany">查看我的企业</a></p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/api'
import UtilMethod from '@/utils/UtilMethod'
import { useRouter } from 'vue-router'
import { useCompanyStore } from '@/store/profile.ts'
const companyInfo = ref({
    companyName: '',
    companyDescription: '',
    organizationScale: '',
})

const router = useRouter()
const company = useCompanyStore()
const createCompany = async () => {
    // 创建公司逻辑
    const ret = await api.createCompany({
        name: companyInfo.value.companyName,
        description: companyInfo.value.companyDescription,
    })
    console.log(`output->ret`, ret)
    if (ret.status === 201) {
        message.success('创建成功！')
        await router.push('/company/switch')
    } else {
        message.error('创建失败，请重试')
    }
}

const joinCompany = () => {
    UtilMethod.jump('/company/switch')
}
</script>

<style scoped>
.devops-container {
    display: flex;
    height: 100vh;
}

.left-side {
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

.right-side {
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

    .company-form {
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
