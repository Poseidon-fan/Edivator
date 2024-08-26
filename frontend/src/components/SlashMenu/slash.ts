import { Extension } from '@tiptap/core'
import suggestion from '@tiptap/suggestion'

export default Extension.create({
    name: 'slash',
    addOptions() {
        return {
            suggestion: {
                char: '/',
                command: ({ editor, range, props }) => {
                    props.command({ editor, range })
                },
            },
        }
    },

    addProseMirrorPlugins() {
        return [
            suggestion({
                editor: this.editor,
                ...this.options.suggestion,
            }),
        ]
    },
})
