<template>
    <div class="el-tiptap-editor__wrapper">
        <el-tiptap ref="tiptapRef" lang="zh" output="json" :extensions="allExtensions" v-model:content="content1" />
    </div>
</template>
<script lang="ts" setup>
import { ref, defineProps, watch } from 'vue'
import {
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

const content1 = ref('')
const content2 = ref('')
const tiptapRef = ref(null)

watch(content1, (newValue) => {
    console.log(`output->newValue`, tiptapRef.value.editor.getHTML())
    props.editor.innerHTML = tiptapRef.value.editor.getHTML()
})

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
        title: '任务列表',
        icon: 'mdi:checkbox-marked-outline', // 可以使用合适的图标，例如带勾选框的图标
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
        title: '文本块',
        icon: 'mdi:code-tags',
        command: ({ editor, range }) => {
            editor.chain().focus().deleteRange(range).setNode('textBlock', { content: 'Initial content' }).run()
        },
    },
    {
        title: '内联公式',
        icon: 'mdi:pi',
        command: insertInlineEquation,
    },
    {
        title: '块公式',
        icon: 'mdi:pi',
        command: insertBlockEquation,
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
        icon: 'mdi:microphone',
        command: insertVoiceRecognition,
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
                        formData.append('affiliated_document_id', route.params.did)

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

const getSuggestionItems = () => {
    return slash
}

import { VueRenderer } from '@tiptap/vue-3'
import tippy from 'tippy.js'
import CommandsList from '@/components/SlashMenu/CommandsList.vue'
import { TextBlock } from '@/extensions/TextBlock.ts'
import { InlineEquation } from '@/extensions/InlineEquation.ts'
import { BlockEquation } from '@/extensions/BlockEquation.ts'
import { CustomImage } from '@/extensions/CustomImage.ts'
import AiWriter from '@/extensions/AiWriter.ts'
import AiImage from '@/extensions/AiImage.ts'
import VoiceRecognition from '@/extensions/voiceRecognition.ts'
import { useRoute } from 'vue-router'
import api from '@/api'

const route = useRoute()

const renderItems = () => {
    let component
    let popup

    return {
        onStart: (props) => {
            component = new VueRenderer(CommandsList, {
                props,
                editor: props.editor,
            })
            const { $cursor } = props.editor.view.state.selection
            const selection = props.editor.state.selection

            const context = selection.$from.depth ? selection.$from.node(selection.$from.depth - 1) : null
            const listItem = context && context.type.name === 'listItem'
            const isCursorInParagraph = $cursor && $cursor.parent.type.name === 'paragraph'
            if (!props.clientRect || !isCursorInParagraph || listItem) {
                return
            }
            popup = tippy('body', {
                getReferenceClientRect: props.clientRect,
                appendTo: () => document.body,
                content: component.element,
                showOnCreate: true,
                interactive: true,
                trigger: 'manual',
                placement: 'bottom-start',
            })
        },

        onUpdate(props) {
            console.log(`output->up`)
            component.updateProps(props)
            if (!props.clientRect || props.text !== '/') {
                popup[0].hide()
                return
            }
            if (props.text === '/') {
                popup[0].show()
            }
            popup[0].setProps({
                getReferenceClientRect: props.clientRect,
            })
        },

        onKeyDown(props) {
            if (props.event.key === 'Escape') {
                popup[0].hide()
                return true
            }
            return component.ref?.onKeyDown(props)
        },

        onExit() {
            popup[0].destroy()
            component.destroy()
        },
    }
}

const textExtensions = [
    Doc,
    Text,
    Paragraph,
    Bold,
    Underline,
    Italic,
    Strike,
    Code,
    FontFamily,
    FontSize,
    Color.configure({ bubble: true }),
    Highlight.configure({ bubble: true }),
    FormatClear,
    History,
]

const paragraphExtensions = [
    Doc,
    Text,
    Paragraph,
    Heading.configure({ level: 5 }),
    BulletList,
    OrderedList,
    TaskList,
    TextAlign,
    LineHeight,
    Indent,
    Blockquote,
    CodeBlock,
    History,
]

const richAndToolsExtensions = [
    Doc,
    Text,
    Paragraph,
    Link,
    Image,
    Iframe,
    Table.configure({ resizable: true }),
    HorizontalRule,
    Print,
    SelectAll,
    Fullscreen,
    CodeView.configure({
        codemirror,
        codemirrorOptions: {
            styleActiveLine: true,
            autoCloseTags: true,
        },
    }),
    // Gapcursor,
    History,
]
const allExtensions = [
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
    History.configure({ depth: 10 }),
    Heading.configure({ level: 5, bubble: true }),
    BulletList.configure({ bubble: true }),
    OrderedList.configure({ bubble: true }),
    TaskList.configure({ bubble: true }),
    TextAlign.configure({ bubble: true }),
    LineHeight.configure({ bubble: true }),
    Indent.configure({ bubble: true }),
    Blockquote.configure({ bubble: true }),
    CodeBlockLowlight.configure({ lowlight }),
    Link.configure({ bubble: true, addLinkPlaceholder: 'add link', editLinkPlaceholder: 'edit link' }),
    Commands.configure({
        suggestion: {
            items: getSuggestionItems,
            render: renderItems,
        },
    }),
    TextBlock,
    InlineEquation,
    BlockEquation,
    AiImage,
    AiWriter,
    VoiceRecognition,
    CustomImage,
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
    CodeView.configure({
        bubble: true,
        codemirror,
        codemirrorOptions: {
            styleActiveLine: true,
            autoCloseTags: true,
        },
    }),
    Gapcursor,
    CodeBlock,
    Dropcursor,
]
</script>
<style>
/* Basic editor styles */
.ProseMirror {
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
</style>
