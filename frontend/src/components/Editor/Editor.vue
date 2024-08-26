<template>
    <AiContextMenu
        :visiblemenu="visiblemenu"
        :position="position"
        :content="selectedText"
        @updateDialog="showDialog"
        @closeMenu="notsee"
    />
    <div class="EditMain" ref="filecont" @mousedown="notsee">
        <div class="lefttools">
            <VersionControl
                :keywords="keyWords"
                :templateName="templateName"
                @changeDocument="handleChangeDocument"
                @newDocument="handleNewDocument"
            />
        </div>
        <div class="editor">
            <div class="el-tiptap-editor__wrapper">
                <el-tiptap
                    @useAI="useAI"
                    ref="editor"
                    lang="zh"
                    output="html"
                    :extensions="allExtensions"
                    v-model="content"
                />
            </div>
        </div>
        <!--        <div class="righttools">-->
        <!--            <Outline />-->
        <!--        </div>-->
    </div>

    <el-dialog v-model="dialogVisible" title="显示" width="50%">
        <p>{{ dialogContent }}</p>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="dialogVisible = false">确定</el-button>
        </span>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, onUnmounted } from 'vue'
import { useRoute, onBeforeRouteLeave } from 'vue-router'
import { useEditor } from '@tiptap/vue-3'
import Simple from '@/components/Editor2/AllExtensionsEditor.vue'

import AiContextMenu from './AiContextMenu.vue'
import VersionControl from '@/components/Editor/VersionControl.vue'
import EditorMenu from '@/components/Editor/EditorMenu.vue'
import Outline from '@/components/Editor/Outline.vue'
import api from '@/api'
import { useEditorStore } from '@/store'
import { useEditorUpdateStore } from '@/store/editorUpdate'
import TaskItem from '@tiptap/extension-task-item'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import CharacterCount from '@tiptap/extension-character-count'
import { TableExtensions } from '@/extensions/Table.ts'
import 'jsmind/style/jsmind.css'
import jsMind from 'jsmind'

const route = useRoute()
// 用来存各个版本的内容
const documentContents = ref({})
// 保存当前的版本
const activeDocument = ref(1)
const visiblemenu = ref(false)
const position = ref({ top: 0, left: 0 })
const selectedText = ref('')
const dialogVisible = ref(false)
const dialogContent = ref('')
const filecont = ref(null)

const editorStore = useEditorStore()
const editorUpdateStore = useEditorUpdateStore()
const editor = ref(null)

const useAI = () => {
    profile.money -= 1
}

import {
    AiContext,
    // InlineEquation,
    BlockEquation,
    Doc,
    Text,
    Paragraph,
    // text extensions
    Bold,
    Underline,
    Italic,
    Strike,
    Code,
    FontFamily,
    FontSize,
    Color,
    Highlight,
    FormatClear,
    // paragraph extensions
    Heading,
    BulletList,
    OrderedList,
    TaskList,
    TextAlign,
    LineHeight,
    Indent,
    Blockquote,
    CodeBlock,
    // rich and tools extensions
    Link,
    Image,
    Table,
    Iframe,
    HorizontalRule,
    Fullscreen,
    Print,
    SelectAll,
    History,
    CodeView,
    Gapcursor,
    Commands,
    Dropcursor,
    CodeBlockLowlight,
    getSuggestionItems,
    renderItems,
} from 'element-tiptap-vue3-niyuta'
import codemirror from 'codemirror'
import 'codemirror/lib/codemirror.css' // import base style
import 'codemirror/mode/xml/xml.js' // language
import 'codemirror/addon/selection/active-line.js' // require active-line.js
import 'codemirror/addon/edit/closetag.js'
// autoCloseTags
import css from 'highlight.js/lib/languages/css'
import js from 'highlight.js/lib/languages/javascript'
import ts from 'highlight.js/lib/languages/typescript'
import html from 'highlight.js/lib/languages/xml'
// load all highlight.js languages
import { lowlight } from 'lowlight'
lowlight.registerLanguage('html', html)
lowlight.registerLanguage('css', css)
lowlight.registerLanguage('js', js)
lowlight.registerLanguage('ts', ts)

const content = ref('')

import { useProfileStore } from '@/store/profile.ts'
import { ElMessage } from 'element-plus'
const profile = useProfileStore()

window.addEventListener(
    'keydown',
    function (e) {
        //可以判断是不是mac，如果是mac,ctrl变为花键
        //event.preventDefault() 方法阻止元素发生默认的行为。
        if (e.keyCode == 83 && e.ctrlKey) {
            e.preventDefault()
        }
    },
    false
)

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

const slashArr = [
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
        title: '任务列表',
        icon: 'mdi:checkbox-marked-outline',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).toggleTaskList().run()
        },
    },
    {
        title: '引用',
        icon: 'mdi:format-quote-open',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).toggleBlockquote().run()
        },
    },
    {
        title: '表格',
        icon: 'mdi:table',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()
        },
    },
    {
        title: '水平线',
        icon: 'mdi:minus',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setHorizontalRule().run()
        },
    },
    {
        title: '图片',
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
                        formData.append('affiliated_document_id', profile.did)

                        // 上传文件
                        const uploadUrl = await api.uploadDocumentFile(formData)

                        insertCustomImage({ editor, range }, uploadUrl)
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

import slash from '@/components/SlashMenu/suggestion.ts'

const Slash = slash(slashArr)

console.log(`output->Slash`, Slash)
const allExtensions = [
    AiContext.configure({ bubble: true }),
    History.configure({ depth: 10 }),
    // InlineEquation,
    BlockEquation,
    Doc,
    Text,
    Paragraph,
    Bold.configure({ bubble: true }),
    Underline.configure({ bubble: true }),
    Italic.configure({ bubble: true }),
    Strike.configure({ bubble: true }),
    Code.configure({ bubble: true }),
    FontFamily.configure({ bubble: true }),
    FontSize.configure({ bubble: true }),
    Color.configure({ bubble: true }),
    Highlight.configure({ bubble: true }),
    FormatClear.configure({ bubble: true }),
    Heading.configure({ level: 5, bubble: true }),
    BulletList.configure({ bubble: true }),
    OrderedList.configure({ bubble: true }),
    TaskList.configure({ bubble: true }),
    TextAlign.configure({ bubble: true }),
    LineHeight.configure({ bubble: true }),
    Indent.configure({ bubble: true }),
    Blockquote.configure({ bubble: true }),
    CodeBlockLowlight.configure({ lowlight }),
    Link.configure({
        bubble: true,
        addLinkPlaceholder: 'add link',
        editLinkPlaceholder: 'edit link',
    }),
    Commands.configure({
        suggestion: {
            items: Slash.items,
            render: Slash.render,
        },
    }),
    Image.configure({
        bubble: true,
        defaultWidth: 400,
        draggable: true,
    }),
    Iframe.configure({ bubble: true }),
    Table.configure({ resizable: true }),
    HorizontalRule.configure({ bubble: true }),
    Print.configure({ bubble: true }),
    SelectAll.configure({ bubble: true }),
    Fullscreen.configure({ bubble: true }),
    Gapcursor,
    Dropcursor,
]

import env from '@/utils/env'

const loadHeadings = () => {
    const headings = []
    console.log(`output->editor.value`, editor.value)
    if (!editor.value) return
    const transaction = editor.value.state.tr
    if (!transaction) return

    editor.value.state.doc.descendants((node, pos) => {
        if (node.type.name === 'heading') {
            const start = pos
            const end = pos + node.nodeSize
            const id = `heading-${headings.length + 1}`
            if (node.attrs.id !== id) {
                transaction.setNodeMarkup(pos, undefined, { ...node.attrs, id })
            }

            headings.push({
                level: node.attrs.level,
                text: node.textContent,
                start,
                end,
                id,
            })
        }
    })

    transaction.setMeta('addToHistory', false)
    transaction.setMeta('preventUpdate', true)
    editor.value.view.dispatch(transaction)
    editorStore.setHeadings(headings)
}

import { useEditorUpdateStore } from '@/store/editorUpdate'

// 切换版本，传进来一个对象，代表切换后的版本
const handleChangeDocument = async (doc) => {
    if (activeDocument.value) {
        // 切换版本之前，保存当前版本的内容
        documentContents.value[activeDocument.value] = document.querySelector('.ProseMirror').getHTML()
        await api.updateVersion(activeDocument.value, {
            document_id: profile.did,
            content: document.querySelector('.ProseMirror').getHTML(),
        })
        ElMessage.success('文档已保存')
    }
    if (doc) {
        activeDocument.value = doc.version
        editor.value.setContent(documentContents.value[doc.version] || '')
    }
}

const handleNewDocument = async ({ name, base }) => {
    // 保存当前的更改
    documentContents.value[activeDocument.value] = document.querySelector('.ProseMirror').getHTML()
    await api.updateVersion(activeDocument.value, {
        document_id: profile.did,
        content: document.querySelector('.ProseMirror').getHTML(),
    })
    ElMessage.success('文档已保存')

    documentContents.value[name] = documentContents.value[base]
    // 将文本改为新版本的内容
    editor.value.setContent(documentContents.value[name] || '')
}

function loadExternalCss(url) {
    return new Promise((resolve, reject) => {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.type = 'text/css'
        console.log(`output->url`, url)
        link.href = url

        link.onload = () => resolve(link) // 返回 link 元素
        link.onerror = () => reject(new Error(`Failed to load CSS from ${url}`))

        document.head.appendChild(link)
    })
}

const keyWords = ref([])
const title = ref([])
const templateName = ref('')
let cssLinkElement = null

onMounted(async () => {
    profile.did = route.params.did
    const versions = await api.queryVersions({
        document_id: profile.did,
    })
    versions.forEach((version) => {
        documentContents.value[version.version] = version.content || ''
    })
    activeDocument.value = versions[0].version
    editor.value.setContent(documentContents.value[activeDocument.value])

    // 模版和关键词功能
    const ret = await api.queryDocumentById(profile.did)
    let template = ''
    console.log(`output->ret`, ret)
    if (ret.template) template = ret.template.content
    if (ret.template) templateName.value = ret.template.name
    console.log(`output->templateName`, templateName.value)
    keyWords.value = ret.keywords
    title.value = ret.description

    if (ret.template) cssLinkElement = await loadExternalCss(env.backEnd.slice(0, -1) + template)
})

window.onbeforeunload = async (event) => {
    event.preventDefault()
    event.returnValue = ''
    handleChangeDocument(null)
    alert('你所做的更改可能未保存')
    await api.updateKeywords(profile.did, {
        content: document.querySelector('.ProseMirror').textContent,
        title: title.value,
    })
}

onBeforeRouteLeave(async (event) => {
    handleChangeDocument(null)
    await api.updateKeywords(profile.did, {
        content: document.querySelector('.ProseMirror').textContent,
        title: title.value,
    })
})

onUnmounted(() => {
    if (cssLinkElement) {
        document.head.removeChild(cssLinkElement)
    }
})

const selecttext = (e) => {
    const selection = window.getSelection()
    if (selection && selection.toString()) {
        selectedText.value = selection.toString()
        const range = selection.getRangeAt(0)
        const rects = range.getClientRects()
        const lastRect = rects[rects.length - 1] // 获取最后一个矩形
        const editorRect = filecont.value.getBoundingClientRect()

        // 将菜单位置设置为选中文本的最后一个字符的右下角
        position.value.top = lastRect.bottom - editorRect.top + filecont.value.scrollTop + 10
        position.value.left = lastRect.right - editorRect.left + filecont.value.scrollLeft + 10
        visiblemenu.value = true
    }
}

const notsee = () => {
    visiblemenu.value = false
}

const showDialog = (content) => {
    dialogContent.value = content
    dialogVisible.value = true
}
</script>

<style>
.editcont {
    line-height: 1.5;
}

.EditMain {
    position: relative;
    width: 100vw;
    height: 100vh;
}

.editorcard {
    position: relative;
    height: 100%;
}

.lefttools {
    position: fixed;
    width: 300px;
    height: 80vh;
    background-color: #fff;
    box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow-y: auto;
    left: 2px;
    top: 100px;
    transition: all 0.3s ease;
    z-index: 1000;
}

.lefttools:hover {
    left: 2px;
}

.el-tiptap-editor__right-sidebar {
    left: 2px;
}

.el-tiptap-editor__right-sidebar .sidebar {
    right: 2px;
}

.righttools {
    position: fixed;
    width: 300px;
    height: 80vh;
    background-color: #fff;
    box-shadow: 0 2px 8px #00000026;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow-y: auto;
    right: -290px;
    top: 100px;
    transition: all 0.3s ease;
    z-index: 1000;
}

.righttools:hover {
    right: 2px;
}

.editor {
    position: relative;
    width: 60%;
    height: 95%;
    top: 2.5%;
    margin: 0 auto;
    border: 1px solid #4f5c5700;
}

.editor .editor {
    position: relative;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    grid-template-rows: 10% 90%;
}

.history-block {
    border: 1px solid #eaeaea;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.history-block h3 {
    margin: 0 0 10px 0;
    font-size: 1.2em;
    font-weight: bold;
}

.content-box {
    border: 1px solid #dcdcdc;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    background-color: #f9f9f9;

    p {
        white-space: pre-wrap; /* 保持换行符 */
        font-size: 16px;
        color: #333;
        line-height: 1.5;
        word-break: break-all; /* 确保单词在容器边界换行 */
    }
}

.button-group {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
}

.button-group .el-button {
    flex: 1;
}

.outline__title {
    font-size: 16px;
    margin-bottom: 10px;
    margin-top: 10px;
}

.sidebarTree {
    height: 400px;
    overflow: auto;
}

.shortcut-keys {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: auto auto;
    gap: 5px 10px;
}

.shortcut-keys li {
    display: contents;
}

.key-combination {
    font-weight: bold;
    margin-top: 15px;
    color: rgb(80, 80, 80);
}

.key-description {
    color: rgb(90, 90, 90);
    margin-top: 15px;
}

.ai-history-block {
    margin-bottom: 10px;
}

.toptools {
    background-color: rgba(207, 220, 245, 0.199);
    border-bottom: 1px dashed #9ca19f65;
    height: 3vh;
}

.bottomcount {
    position: absolute;
    bottom: 0;
    background-color: rgba(207, 220, 245);
    border-top: 1px dashed #9ca19f65;
    height: 5vh;
    width: 100%;
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 100%;
    justify-items: center;
    align-items: center;
}

.editcont {
    position: relative;
    width: 100%;
    height: calc(92vh - 40px);
    overflow-y: scroll;
}

b {
    font-weight: bold;
}

.ProseMirror {
    p {
        margin: 0;
    }

    h1,
    h2,
    h3 {
        margin-top: 0;
        margin-bottom: 0;
        line-height: 1.2;
    }

    pre {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 20px 0;
        overflow-x: auto;
        font-family: 'JetBrainsMono', monospace;
        color: #333;

        code {
            display: block;
            white-space: pre-wrap; /* 保持代码的换行格式 */
            font-size: 16px;
            line-height: 1.5;
        }
    }

    ul {
        padding: 0 2rem;
    }

    ol {
        padding: 0 2rem;
        list-style: decimal;
    }

    ul[data-type='taskList'] div {
        display: inline-block;
    }

    ul[data-type='taskList'] {
        padding-left: 0.75rem;
    }

    ul[data-type='taskList'] li[data-checked='false'] label,
    ul[data-type='taskList'] li[data-checked='true'] label {
        margin-right: 10px;
    }

    ul[data-type='taskList'] li::marker {
        content: none;
    }

    blockquote {
        border-left: 3px solid rgb(231, 228, 226);
        margin: 0.75rem 0;
        padding-left: 1rem;
        color: rgb(150, 150, 150);
    }

    hr {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    hr.ProseMirror-selectednode {
        border-width: 1px 0 0;
        border-color: rgba(0, 0, 0, 0.2);
        background-color: rgba(0, 0, 0, 0.8);
        border-top-color: rgba(0, 0, 0, 0.3);
    }

    img {
        transition: all 200ms;
        min-width: 200px;
        margin-top: 20px;
        margin-bottom: 20px;
        margin-left: 20px;
        margin-right: 20px;
        height: auto;
        cursor: pointer;
    }

    img:hover {
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
        border: 1px solid #0050b3;
    }

    table {
        border-collapse: collapse;
        table-layout: fixed;
        width: 100%;
        margin: 0;
        overflow: hidden;
    }
}

.ProseMirror:focus {
    outline: none;
}

.tiptap p.is-editor-empty:first-child::before {
    color: #adb5bd;
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
}

.tiptap > * + * {
    margin-top: 0.75em;
}

.tiptap .tiptap td,
.tiptap th {
    min-width: 1em;
    border: 2px solid #ced4da;
    padding: 3px 5px;
    vertical-align: top;
    box-sizing: border-box;
    position: relative;
}

.tiptap th {
    font-weight: bold;
    text-align: left;
    background-color: #f1f3f5;
}

.tiptap .selectedCell:after {
    z-index: 2;
    position: absolute;
    content: '';
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    background: rgba(200, 200, 255, 0.4);
    pointer-events: none;
}

.tiptap .column-resize-handle {
    position: absolute;
    right: -2px;
    top: 0;
    bottom: -2px;
    width: 4px;
    background-color: #adf;
    pointer-events: none;
}

.tiptap table p {
    margin: 0;
}

.tiptap pre .hljs-quote {
    color: #616161;
}

.tiptap pre .hljs-variable,
.tiptap pre .hljs-template-variable,
.tiptap pre .hljs-attribute,
.tiptap pre .hljs-tag,
.tiptap pre .hljs-name,
.tiptap pre .hljs-regexp,
.tiptap pre .hljs-link,
.tiptap pre .hljs-selector-id,
.tiptap pre .hljs-selector-class {
    color: #f98181;
}

.tiptap pre .hljs-number,
.tiptap pre .hljs-meta,
.tiptap pre .hljs-built_in,
.tiptap pre .hljs-builtin-name,
.tiptap pre .hljs-literal,
.tiptap pre .hljs-type,
.tiptap pre .hljs-params {
    color: #fbbc88;
}

.tiptap pre .hljs-string,
.tiptap pre .hljs-symbol,
.tiptap pre .hljs-bullet {
    color: #b9f18d;
}

.tiptap pre .hljs-title,
.tiptap pre .hljs-section {
    color: #faf594;
}

.tiptap pre .hljs-keyword,
.tiptap pre .hljs-selector-tag {
    color: #70cff8;
}

.tiptap pre .hljs-emphasis {
    font-style: italic;
}

.tiptap pre .hljs-strong {
    font-weight: 700;
}

.tableWrapper {
    overflow-x: auto;
}

.resize-cursor {
    cursor: ew-resize;
    cursor: col-resize;
}

.editor {
    background-color: white;
}

.contextmenu {
    width: 180px;
    margin: 0;
    background: #fff;
    z-index: 3000;
    position: fixed;
    list-style-type: none;
    padding: 5px;
    padding-left: 15px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 400;
    color: #333;
    box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, 0.3);
    display: grid;
    grid-template-columns: 50% 50%;
}

.contextmenu .item {
    height: 35px;
    width: 100%;
    line-height: 35px;
    color: rgb(29, 33, 41);
    cursor: pointer;
}

.contextmenu .item:hover {
    background: rgb(229, 230, 235);
}

.ai-writer {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 8px;
    color: #ffffff;
    width: 500px;
    margin: auto;
}

.prompt-label {
    font-size: 14px;
    margin-bottom: 8px;
    display: block;
}

.prompt-textarea {
    width: 100%;
    height: 100px;
    background-color: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #ffffff;
    padding: 10px;
    font-size: 14px;
    resize: none;
}

.controls {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.change-tone-button {
    background-color: #4a4a4a;
    border: none;
    color: #ffffff;
}

.change-tone-button:hover {
    background-color: #5a5a5a;
}

.generate-text-button {
    background-color: #4caf50;
    border: none;
    color: #ffffff;
}

.generate-text-button:hover {
    background-color: #45a049;
}

.el-icon-cpu {
    margin-right: 5px;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
}

.ProseMirror img:hover {
}

.text-block {
    border: 1px solid #e0e0e0; /* 浅灰色边框 */
    background-color: #f9f9f9; /* 浅色背景 */
    border-radius: 4px; /* 圆角边框 */
    padding: 8px; /* 内部填充 */
    margin: 4px 0; /* 外部间距 */
    font-family: 'Arial', sans-serif; /* 字体 */
    color: #333; /* 文本颜色 */
}

.ai-writer {
    width: 100%;
    margin: auto;
    padding: 10px;
    border: 1px solid #333;
    border-radius: 8px;
    background: #1a1a1a;
    color: #f5f5f5;

    .input-container {
        display: flex;
        flex-direction: column;
    }

    .prompt-textarea {
        width: 100%;
        border: 1px solid #444;
        border-radius: 4px;
        padding: 10px;
        background: #2b2b2b;
        color: #f5f5f5;
        resize: none;
        min-height: 100px;
    }

    .button-group {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }

    .change-tone-button,
    .generate-text-button {
        flex-grow: 1;
        margin-right: 10px;
    }

    .change-tone-button {
        background: #444;
        border: none;
    }

    .generate-text-button {
        background: #1abc9c;
        border: none;
    }

    .change-tone-button:hover,
    .generate-text-button:hover {
        background: #16a085;
    }
}

.ProseMirror {
    > * + * {
        margin-top: 0.75em;
    }

    pre {
        background: #0d0d0d;
        border-radius: 0.5rem;
        color: #fff;
        font-family: 'JetBrainsMono', monospace;
        padding: 0.75rem 1rem;

        code {
            background: none;
            color: inherit;
            font-size: 0.8rem;
            padding: 0;
        }

        .hljs-comment,
        .hljs-quote {
            color: #616161;
        }

        .hljs-variable,
        .hljs-template-variable,
        .hljs-attribute,
        .hljs-tag,
        .hljs-name,
        .hljs-regexp,
        .hljs-link,
        .hljs-name,
        .hljs-selector-id,
        .hljs-selector-class {
            color: #f98181;
        }

        .hljs-number,
        .hljs-meta,
        .hljs-built_in,
        .hljs-builtin-name,
        .hljs-literal,
        .hljs-type,
        .hljs-params {
            color: #fbbc88;
        }

        .hljs-string,
        .hljs-symbol,
        .hljs-bullet {
            color: #b9f18d;
        }

        .hljs-title,
        .hljs-section {
            color: #faf594;
        }

        .hljs-keyword,
        .hljs-selector-tag {
            color: #70cff8;
        }

        .hljs-emphasis {
            font-style: italic;
        }

        .hljs-strong {
            font-weight: 700;
        }
    }
}

.el-tiptap-editor *[class^='el-tiptap-editor'] {
    left: auto !important;
}

.el-tiptap-editor__voice-recognition {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #e3f2fd; /* Light blue background color */
    border: 1px solid #90caf9; /* Light blue border color */
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    width: 500px;
    max-width: 100%;
    padding: 10px;
    animation: border-animation 2s infinite;

    .voice-recognition {
        width: 100%;
        max-width: 500px;
        margin: 20px auto;
    }

    .upload-demo {
        /* border: 2px dashed #d9d9d9; */
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: border-color 0.3s ease;
    }

    .upload-demo:hover {
        border-color: #409eff;
    }

    .el-upload__text {
        font-size: 16px;
        color: #606266;
    }

    .el-upload__text em {
        color: #409eff;
        font-style: normal;
        cursor: pointer;
    }

    .tip {
        margin-top: 10px;
        font-size: 14px;
        color: #909399;
    }

    .voice-recognition-result {
        font-size: 16px;
        color: #606266;
        margin-top: 20px;
    }

    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
    }
}

.el-tiptap__od-dialog-visible {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 500px;
    max-width: 100%;
    display: flex;
    padding: 10px;
    z-index: 1000;
    max-height: 400px;
    overflow: auto;

    custom-dialog {
        background-color: #e3f2fd; /* Light blue background color */
        border: 1px solid #90caf9; /* Light blue border color */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 10px;
    }

    .dialog-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        color: #333;
    }

    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

    .loading-spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-top: 4px solid #007bff;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
    }

    .ocr-content {
        width: 100%;
    }

    .ocr-item {
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        padding: 10px;
        margin-bottom: 10px;
        width: 100%;
    }

    .ocr-item-header {
        display: flex;
        justify-content: space-between;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .ocr-score {
        color: #007bff;
    }

    .ocr-keyword {
        color: #626aef;
    }

    .ocr-item-content {
        margin-top: 10px;
    }

    .ocr-image {
        max-width: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    }

    .dialog-footer {
        display: flex;
        justify-content: flex-end;
        margin-top: 5px;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
}

.el-tiptap__ocr-dialog-visible {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 500px;
    max-width: 100%;
    display: flex;
    padding: 10px;
    z-index: 1000;
    height: 400px;

    .dialog-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        color: #333;
        height: 100%;
    }

    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

    .loading-spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-top: 4px solid #007bff;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
    }

    .ocr-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .ocr-image {
        max-width: 100%;
        margin-bottom: 10px;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .text-container {
        width: 100%;
        text-align: left;
        padding: 10px;
        background-color: #ffffff; /* White background for text container */
        border-radius: 5px;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
        max-height: 200px;
        overflow: auto;
    }

    .dialog-footer {
        display: flex;
        justify-content: flex-end;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
}

.image-view {
    border: solid 1px rgba(0, 0, 0, 0.3);
}
</style>
