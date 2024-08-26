<script setup>
import SimpleEditor from '@/components/Editor2/SimpleEditor.vue'
import AllExtensionsEditor from '@/components/Editor2/AllExtensionsEditor.vue'
</script>
<template>
    <el-container direction="vertical">
        <el-main><AllExtensionsEditor /></el-main>
    </el-container>
</template>

<style scoped>
.el-container {
    background: linear-gradient(to bottom, #2980b9, #6dd5fa, #ffffff);
    font-family: sans-serif;
}

.header {
    display: flex;
    justify-content: center;
    height: 20vh !important;
    padding-bottom: 20px;
    padding-top: 20px;

    .header__left {
        align-items: flex-start;
        display: flex;
        flex-direction: column;
        margin-top: 50px;

        .logo {
            height: 50px;
            margin-bottom: 20px;
        }
    }

    .header__right {
        align-items: flex-start;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 50px;
        margin-left: 10vw;
        width: 650px;

        .router-link {
            color: #fff;
            cursor: pointer;
            flex-shrink: 0;
            font-weight: 700;
            letter-spacing: 1px;
            margin: 15px;
            transition: all 0.3s ease-in-out;

            .router-link:hover {
                transform: translateY(-5px);
            }

            .router-link--active {
                border-bottom: 1px solid #fff;
                text-transform: uppercase;
            }
        }
    }
}

.el-main {
    display: flex;
    justify-content: center;
    overflow: initial;
    padding: 50px;
}

.el-tiptap-editor {
    margin-bottom: 30px;

    &__wrapper {
        width: 60vw;
    }
}

.el-footer {
    align-items: center;
    display: flex;
    font-weight: 700;
    font-size: 14px;
    justify-content: center;
}

.github-corner:hover {
    .octo-arm {
        animation: octocat-wave 560ms ease-in-out;
    }
}

@media (max-width: 500px) {
    .github-corner:hover {
        .octo-arm {
            animation: none;
        }
    }

    .github-corner {
        .octo-arm {
            animation: octocat-wave 560ms ease-in-out;
        }
    }
}

@keyframes octocat-wave {
    0%,
    100% {
        transform: rotate(0);
    }

    20%,
    60% {
        transform: rotate(-25deg);
    }

    40%,
    80% {
        transform: rotate(10deg);
    }
}
</style>
