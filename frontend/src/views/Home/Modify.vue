<template>
    <div class="profile-editor">
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>个人信息修改</span>
                <el-button type="info" @click="back()" class="save-button">返回</el-button>
                <el-button type="primary" @click="save()" class="save-button">保存</el-button>
            </div>
            <el-form :model="user" ref="userForm" :rules="rules" label-width="120px">
                <el-form-item>
                    <el-upload class="avatar-uploader" :show-file-list="false" accept="image/*">
                        <div class="avatar-uploader-inner">
                            <img v-if="user.avatar" :src="user.avatar" class="avatar" />
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                        </div>
                    </el-upload>
                </el-form-item>

                <el-form-item label="用户名" prop="name">
                    <el-input v-model="user.name"></el-input>
                </el-form-item>

                <el-form-item label="电子邮件" prop="email">
                    <el-input v-model="user.email"></el-input>
                </el-form-item>

                <el-form-item label="电话号码" prop="phone">
                    <el-input v-model="user.phone"></el-input>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
// import api from '@/api'
const router = useRouter()
function save() {
    // save user data
    console.log('save user data', user)
    // api.updateUser(user.value).then((res) => {
    //     console.log('update user data', res)
    //     router.back()
    // })
    router.back()
}
function back() {
    router.back()
}
let user = ref<{
    phone: string
    name: string
    avatar: string
    email: string
}>({
    phone: '',
    name: '',
    avatar: '',
    email: '',
})

onMounted(() => {
    // fetch user data
    api.getNowUser().then((res) => {
        console.log('my user data', res)
        // user=res
        user.value = {
            phone: res.mobile || '',
            name: res.username,
            ...res,
        }
    })
})

const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        {
            pattern: /^[a-zA-Z0-9_]{3,16}$/,
            message: '用户名格式不正确',
            trigger: 'blur',
        },
    ],
    email: [
        { required: true, message: '请输入电子邮件', trigger: 'blur' },
        {
            type: 'email',
            pattern: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/,
            message: '邮箱格式不正确',
            trigger: ['blur', 'change'],
        },
    ],
    phone: [
        { required: true, message: '请输入电话号码', trigger: 'blur' },
        {
            pattern: /^[1-9]\d{9,14}$/,
            message: '电话号格式不正确',
            trigger: 'blur',
        },
    ],
}
</script>

<style scoped>
.profile-editor {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

.box-card {
    margin: 20px;
    padding: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.avatar-uploader {
    display: block;
    width: 178px;
    height: 178px;
    margin: 0 auto;
    border: 1px dashed #d9d9d9;
    border-radius: 50%;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.avatar-uploader-inner {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    position: absolute;
    top: 0;
    left: 0;
}

.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
}

.save-button {
    float: right;
    margin-right: 5px;
}
</style>
