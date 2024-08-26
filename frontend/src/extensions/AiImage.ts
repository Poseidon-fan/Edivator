import { Node, mergeAttributes } from '@tiptap/core'
import { Plugin, PluginKey } from '@tiptap/pm/state'
import { createApp, ref } from 'vue'
import AiImage from '@/components/AI/AiImage.vue'
import api from '@/api'

const toneRef = ref('二次元')

// 示例事件处理函数
function changeStyle(style) {
    console.log(`Change style to ${style}`)
    toneRef.value = style
}

const generateImage = async (editor, getPos) => {

    const url = await api.generateImage({
        text: document.querySelector('.ai-image>.input-container').textContent,
        style: toneRef.value,
        resolution: "512*512"
    })
    console.log(`output->url`,url)

    let pos = getPos()

    // 删除当前节点
    const { tr } = editor.state
    const nodeSize = editor.state.doc.nodeAt(pos).nodeSize;
    tr.delete(pos, pos + nodeSize)
    editor.view.dispatch(tr)

    pos = getPos()

    const { selection } = editor.state

    // 如果光标不可用，将图片插入到文档末尾
    if (!selection || selection.empty === false) {
        pos = editor.state.doc.content.size
    }

    // 创建新的图片节点
    const node = editor.schema.nodes.image.create({ src: url })

    // 使用 transaction 插入图片节点
    editor.view.dispatch(
        editor.state.tr
            .replaceWith(pos, pos, node)
            .scrollIntoView()
    )


    console.log('Generate image clicked')
}

export default Node.create({
    name: 'aiImage',
    group: 'block',
    content: 'inline*',

    addOptions() {
        return {
            HTMLAttributes: {},
        }
    },

    addAttributes() {
        return {
            content: {
                default: '',
            },
        }
    },

    parseHTML() {
        return [
            {
                tag: 'div[data-type="ai-image"]',
            },
        ]
    },

    renderHTML({ HTMLAttributes }) {
        return [
            'div',
            mergeAttributes(HTMLAttributes, { 'data-type': 'ai-image' }),
            0,
        ]
    },

    addNodeView() {
        return ({ node, getPos, editor }) => {
            const dom = document.createElement('div')
            dom.setAttribute('data-type', 'ai-image')

            // 创建 Vue 实例并挂载到 DOM 上
            const app = createApp(AiImage, {
                content: node.attrs.content,
                placeholder: 'Describe the image that you want me to generate.',
                onUpdate: (content) => {
                    const { tr } = editor.state
                    tr.setNodeMarkup(getPos(), undefined, { content })
                    editor.view.dispatch(tr)
                },
            })

            const instance = app.mount(dom)

            const label = document.createElement('label')
            label.innerText = 'Prompt'
            label.classList.add('prompt-textarea')
            dom.querySelector('.ai-image').insertBefore(
                label,
                dom.querySelector('.ai-image').children[0]
            )

            // 创建根 div 元素
            const buttonGroup = document.createElement('div')
            buttonGroup.className = 'button-group'

            // 创建下拉菜单
            const dropdownSelect = document.createElement('select')
            dropdownSelect.className = 'change-style-select'

            const styles = [
                { value: '二次元', text: '二次元' },
                { value: '写实风格', text: '写实风格' },
                { value: '古风', text: '古风' },
                { value: '赛博朋克', text: '赛博朋克' },
                { value: '水彩画', text: '水彩画' },
                { value: '油画', text: '油画' },
                { value: '卡通画', text: '卡通画' },
            ]

            styles.forEach(option => {
                const optionElement = document.createElement('option')
                optionElement.value = option.value
                optionElement.text = option.text
                dropdownSelect.appendChild(optionElement)
            })

            // 监听下拉菜单变化
            dropdownSelect.addEventListener('change', (event) => {
                changeStyle(event.target.value)
            })

            // 创建生成图像按钮
            const generateImageButton = document.createElement('button')
            generateImageButton.className = 'generate-image-button'
            generateImageButton.innerHTML =
                '<i class="el-icon-picture"></i> Generate image'
            generateImageButton.addEventListener('click', () => {
                console.log(`output->editor, getPos`,editor, getPos)
                generateImage(editor, getPos)
            })

            // 将元素添加到 button-group
            buttonGroup.appendChild(dropdownSelect)
            buttonGroup.appendChild(generateImageButton)

            // 将 button-group 添加到页面中的某个位置
            dom.appendChild(buttonGroup)

            console.log('Button group created:', buttonGroup)
            dom.querySelector('.ai-image').appendChild(buttonGroup)

            console.log(
                `output->instance`,
                dom.querySelector('.ai-image').childNodes[0]
            )

            // 添加事件监听器
            dom.addEventListener('change-style', (item) => {
                changeStyle(item)
            })
            dom.addEventListener('generate-image', () => {
                console.log(`output->editor, getPos`,editor, getPos)
                generateImage(editor, getPos)
            })

            return {
                dom,
                contentDOM: dom.querySelector('.input-container') || dom,
                update: (updatedNode) => {
                    if (updatedNode.type.name !== this.name) {
                        return false
                    }
                    instance.content = updatedNode.attrs.content
                    return true
                },
            }
        }
    },

    addCommands() {
        return {
            setAiImage:
                (attributes) =>
                ({ commands }) => {
                    return commands.setNode(this.name, attributes)
                },
            toggleAiImage:
                (attributes) =>
                ({ commands }) => {
                    return commands.toggleNode(
                        this.name,
                        'paragraph',
                        attributes
                    )
                },
        }
    },

    addKeyboardShortcuts() {
        return {
            'Mod-Alt-i': () => this.editor.commands.toggleAiImage(),

            Backspace: () => {
                const { empty, $anchor } = this.editor.state.selection
                const isAtStart = $anchor.pos === 1

                if (!empty || $anchor.parent.type.name !== this.name) {
                    return false
                }

                if (isAtStart || !$anchor.parent.textContent.length) {
                    return this.editor.commands.clearNodes()
                }

                return false
            },
        }
    },

    addProseMirrorPlugins() {
        return [
            new Plugin({
                key: new PluginKey('aiImageHandler'),
                props: {
                    handleDOMEvents: {
                        input(view, event) {
                            const target = event.target
                            if (
                                target &&
                                target.closest &&
                                target.closest('[data-type="ai-image"]')
                            ) {
                                const { tr } = view.state
                                const { from } = view.state.selection
                                const value = target.value
                                tr.setNodeMarkup(from - 1, undefined, {
                                    content: value,
                                })
                                view.dispatch(tr)
                                return true
                            }
                            return false
                        },
                    },
                },
            }),
        ]
    },
})
