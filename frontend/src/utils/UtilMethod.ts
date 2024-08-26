import router from '@/router'
import env from './env'
function catAvatarUrl(avatar: string) {
    return env.backEnd + avatar
}

function jump(path: string) {
    router.push(path)
}

function jumpToHome() {
    router.push('/documentCardsList')
}

function jumpToUserHome() {
    router.push('/home')
}

export default {
    jump,
    jumpToHome,
    jumpToUserHome,
}
