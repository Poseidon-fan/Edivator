import Blockquote from '@tiptap/extension-blockquote'

export default Blockquote.extend({
  addCommands() {
    return {
      setBlockquote: () => ({ commands }) => {
        return commands.setNode('blockquote')
      },
      toggleBlockquote: () => ({ commands }) => {
        return commands.toggleNode('blockquote', 'paragraph')
      },
      unsetBlockquote: () => ({ commands }) => {
        return commands.lift('blockquote')
      },
    }
  },
})
