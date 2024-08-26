import { VueRenderer } from '@tiptap/vue-3'
import tippy from 'tippy.js'
import CommandsList from './CommandsList.vue'

export default function set(items) {
    return {
        items: () => {
            return items
                ? items
                : [
                      {
                          title: '一级标题',
                          icon: 'mdi:format-header-1',
                          command: ({ editor, range }) => {
                              editor.chain().focus().deleteRange(range).setNode('heading', { level: 1 }).run()
                          },
                      },
                  ]
        },
        render: () => {
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
        },
    }
}
