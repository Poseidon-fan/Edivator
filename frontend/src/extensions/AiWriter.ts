import { Node, mergeAttributes } from '@tiptap/core'
import { Plugin, PluginKey } from '@tiptap/pm/state'
import { createApp, ref } from 'vue'
import AiWriter from '@/components/AI/AiWriter.vue'
import api from '@/api'

const toneRef = ref('')

// 示例事件处理函数
function changeTone(tone) {
    console.log(`Change tone to ${tone}`)
    toneRef.value = tone
}

const generateText = async () => {
    console.log(`output->`, document.querySelector('.ai-writer>.input-container').textContent)
    alert(
        await api.generateText({
            content: document.querySelector('.ai-writer>.input-container').textContent,
            style: toneRef.value,
        })
    )
    console.log('Generate text clicked')
}

export default Node.create({
    name: 'aiWriter',
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
                tag: 'div[data-type="ai-writer"]',
            },
        ]
    },

    renderHTML({ HTMLAttributes }) {
        return ['div', mergeAttributes(HTMLAttributes, { 'data-type': 'ai-writer' }), 0]
    },

    addNodeView() {
        return ({ node, getPos, editor }) => {
            const dom = document.createElement('div')
            dom.setAttribute('data-type', 'ai-writer')

            // 创建 Vue 实例并挂载到 DOM 上
            const app = createApp(AiWriter, {
                content: node.attrs.content,
                placeholder: 'Tell me what you want me to write about.',
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
            dom.querySelector('.ai-writer').insertBefore(label, dom.querySelector('.ai-writer').children[0])

            // 创建根 div 元素
            const buttonGroup = document.createElement('div')
            buttonGroup.className = 'button-group'

            // 创建下拉菜单
            const dropdownSelect = document.createElement('select')
            dropdownSelect.className = 'change-tone-select'

            const formalOption = document.createElement('option')
            formalOption.value = 'Academic'
            formalOption.text = 'Academic'

            const informalOption = document.createElement('option')
            informalOption.value = 'Business'
            informalOption.text = 'Business'

            const friendlyOption = document.createElement('option')
            friendlyOption.value = 'Humorous'
            friendlyOption.text = 'Humorous'

            // 添加选项到下拉菜单
            dropdownSelect.appendChild(formalOption)
            dropdownSelect.appendChild(informalOption)
            dropdownSelect.appendChild(friendlyOption)

            // 监听下拉菜单变化
            dropdownSelect.addEventListener('change', (event) => {
                changeTone(event.target.value)
            })

            // 创建生成文本按钮
            const generateTextButton = document.createElement('button')
            generateTextButton.className = 'generate-text-button'
            generateTextButton.innerHTML = '<i class="el-icon-s-promotion"></i> Generate text'
            generateTextButton.addEventListener('click', generateText)

            // 将元素添加到 button-group
            buttonGroup.appendChild(dropdownSelect)
            buttonGroup.appendChild(generateTextButton)

            // 将 button-group 添加到页面中的某个位置
            document.body.appendChild(buttonGroup)

            // 控制台日志
            console.log('Button group created:', buttonGroup)
            dom.querySelector('.ai-writer').appendChild(buttonGroup)

            console.log(`output->instance`, dom.querySelector('.ai-writer').childNodes[0])

            // 添加事件监听器
            dom.addEventListener('change-tone', (item) => {
                changeTone(item)
            })
            dom.addEventListener('generate-text', () => {
                generateText()
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
            setAiWriter:
                (attributes) =>
                ({ commands }) => {
                    return commands.setNode(this.name, attributes)
                },
            toggleAiWriter:
                (attributes) =>
                ({ commands }) => {
                    return commands.toggleNode(this.name, 'paragraph', attributes)
                },
        }
    },

    addKeyboardShortcuts() {
        return {
            'Mod-Alt-w': () => this.editor.commands.toggleAiWriter(),

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
                key: new PluginKey('aiWriterHandler'),
                props: {
                    handleDOMEvents: {
                        input(view, event) {
                            const target = event.target
                            if (target && target.closest && target.closest('[data-type="ai-writer"]')) {
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
