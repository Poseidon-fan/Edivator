<template>
    <div class="el-tiptap-editor__wrapper">
        <el-tiptap :extensions="extensions" v-model:content="content" output="html" placeholder="Write something ..." />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import {
    Doc,
    Text,
    Paragraph,
    Heading,
    Bold,
    Underline,
    Italic,
    Strike,
    Code,
    Link,
    Image,
    Blockquote,
    BulletList,
    OrderedList,
    TaskList,
    TextAlign,
    Indent,
    HardBreak,
    HorizontalRule,
    CodeView,
    Fullscreen,
    History,
} from 'element-tiptap-vue3-niyuta'

import codemirror from 'codemirror'
import 'codemirror/lib/codemirror.css' // import base style
import 'codemirror/mode/xml/xml.js' // language
import 'codemirror/addon/selection/active-line.js' // require active-line.js
import 'codemirror/addon/edit/closetag.js' // autoCloseTags
import Slash from '@/components/SlashMenu/slash.ts'
import api from '@/api'
import suggestion from '@/components/SlashMenu/suggestion'

const insertInlineEquation = ({ editor, range }) => {
    const equation = prompt('输入方程 (LaTeX 格式):', 'E=mc^2')
    if (equation) {
        editor.chain().focus().deleteRange(range).setInlineEquation(equation).run()
    }
}

const insertBlockEquation = ({ editor, range }) => {
    const equation = prompt('输入方程 (LaTeX 格式):', '\\int_{a}^{b} x^2 \\,dx')
    if (equation) {
        editor.chain().focus().deleteRange(range).setBlockEquation(equation).run()
    }
}

const insertVoiceRecognition = ({ editor, range }) => {
    editor
        .chain()
        .focus()
        .deleteRange(range)
        .insertContent({
            type: 'voiceRecognition',
            attrs: {
                editor,
            },
        })
        .run()
}

const insertCustomImage = ({ editor, range }, url) => {
    if (url) {
        editor.chain().focus().deleteRange(range).setImage({ src: url }).run()
    }
}

const slash = [
    {
        title: '普通文本',
        icon: 'mdi:format-paragraph',
        command: ({ editor, range }) => {
            console.log(`output->paragraph`)
            editor.chain().focus().deleteRange(range).setNode('paragraph').run()
        },
    },
    {
        title: '一级标题',
        icon: 'mdi:format-header-1',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('heading', { level: 1 }).run()
        },
    },
    {
        title: '二级标题',
        icon: 'mdi:format-header-2',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('heading', { level: 2 }).run()
        },
    },
    {
        title: '三级标题',
        icon: 'mdi:format-header-3',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('heading', { level: 3 }).run()
        },
    },
    {
        title: '代码块',
        icon: 'mdi:code-braces-box',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('codeBlock').run()
        },
    },
    {
        title: '无序列表',
        icon: 'mdi:format-list-bulleted',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).toggleBulletList().run()
        },
    },
    {
        title: '有序列表',
        icon: 'mdi:format-list-numbered',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).toggleOrderedList().run()
        },
    },
    {
        title: 'AI Writer',
        icon: 'mdi:robot',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('aiWriter', { content: 'Initial content' }).run()
        },
    },
    {
        title: 'AI Image',
        icon: 'mdi:robot',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('aiImage', { content: 'Initial content' }).run()
        },
    },
    {
        title: '语音识别',
        icon: 'mdi:robot',
        command: ({ editor }) => {
            const pos = editor.state.doc.content.size // 获取文档末尾位置

            editor
                .chain()
                .focus()
                .insertContentAt(pos, {
                    type: 'voiceRecognition',
                    attrs: { content: 'Initial content' },
                })
                .run()
        },
    },
    {
        title: '插入图片',
        icon: 'mdi:image',
        command: ({ editor, range }) => {
            const input = document.createElement('input')
            input.type = 'file'
            input.accept = 'image/*'
            input.onchange = async (event) => {
                const file = event.target.files[0]
                if (file) {
                    try {
                        // 创建 FormData 对象
                        const formData = new FormData()
                        formData.append('file', file)
                        formData.append('affiliated_document_id', route.params.did)

                        // 上传文件
                        const uploadUrl = await api.uploadDocumentFile(formData)

                        // 将图片转为 base64
                        const reader = new FileReader()
                        reader.onloadend = async () => {
                            const base64_img = reader.result.split(',')[1] // 去掉前缀
                            try {
                                // 调用 OCR 接口
                                const ocrResponse = await api.OCR({
                                    base64_img,
                                })

                                const ocrImageUrl = ocrResponse.data.image_url
                                const ocrTexts = ocrResponse.data.texts

                                // 插入 OCR 结果图片
                                editor.chain().focus().deleteRange(range).setImage({ src: uploadUrl }).run()

                                // 显示识别结果文字
                                console.log('识别结果文字:', ocrTexts)
                                alert(`识别结果文字: ${ocrTexts.join(', ')}`)
                            } catch (ocrError) {
                                console.error('OCR 识别失败:', ocrError)
                                // 可以添加错误处理逻辑，例如显示错误消息
                            }
                        }
                        reader.readAsDataURL(file)
                    } catch (error) {
                        console.error('上传图片失败:', error)
                        // 可以添加错误处理逻辑，例如显示错误消息
                    }
                }
            }
            input.click()
        },
    },
]

const extensions = [
    Doc,
    Text,
    Paragraph,
    Heading.configure({ level: 5 }),
    Bold.configure({ bubble: true }),
    Underline.configure({ bubble: true }),
    Italic.configure({ bubble: true }),
    Strike.configure({ bubble: true }),
    Code,
    Link.configure({ bubble: true }),
    Image,
    Blockquote,
    TextAlign,
    BulletList,
    OrderedList,
    TaskList,
    Indent,
    HardBreak,
    HorizontalRule.configure({ bubble: true }),
    CodeView.configure({
        codemirror,
        codemirrorOptions: {
            styleActiveLine: true,
            autoCloseTags: true,
        },
    }),
    Fullscreen,
    History,
    Slash.configure({
        suggestion: suggestion(slash),
    }),
]

console.log(extensions)

const content = ref(
    '<h2 style="text-align: center;">Welcome To Element Tiptap Editor Demo</h2><p>🔥 <strong>Element Tiptap Editor </strong>🔥is a WYSIWYG rich-text editor using&nbsp; <a href="https://github.com/scrumpy/tiptap" target="_blank" ref="nofollow noopener noreferrer">tiptap</a>&nbsp;and <a href="https://github.com/element-plus/element-plus" target="_blank" ref="nofollow noopener noreferrer">element-plus</a>&nbsp;for Vue3,<img src="https://i.ibb.co/nbRN3S2/undraw-upload-87y9.png" alt="" title="" height="200" data-display="right"> that\'s easy to use, friendly to developers, fully extensible and clean in design.</p><p></p><p style="text-align: right;">👉Click on the image to get started image features 👉</p><p></p><p>You can switch to <strong>Code View </strong>💻 mode and toggle <strong>Fullscreen</strong> 📺 in this demo.</p><p></p><p><strong>Got questions or need help or feature request?</strong></p><p>🚀 <strong>welcome to submit an <a href="https://github.com/Leecason/element-tiptap/issues" target="_blank" ref="nofollow noopener noreferrer">issue</a></strong> 😊</p><p>I\'m continuously working to add in new features.</p><p></p><blockquote><p>This demo is simple, switch tab for more features.</p><p>All demos source code: <a href="https://github.com/Leecason/element-tiptap/blob/master/demos/views/Index.vue" target="_blank" ref="nofollow noopener noreferrer">source code 🔗</a></p></blockquote>'
)
</script>
