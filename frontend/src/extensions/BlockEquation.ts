import { Node, mergeAttributes } from '@tiptap/core'
import katex from 'katex'
import 'katex/dist/katex.min.css'

export const BlockEquation = Node.create({
  name: 'blockEquation',

  group: 'block',
  content: 'text*',

  addAttributes() {
    return {
      equation: {
        default: '',
      },
    }
  },

  parseHTML() {
    return [
      {
        tag: 'div[data-type="block-equation"]',
      },
    ]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', mergeAttributes(HTMLAttributes, { 'data-type': 'block-equation' }), 0]
  },

  addNodeView() {
    return ({ node }) => {
      const dom = document.createElement('div')
      dom.setAttribute('data-type', 'block-equation')
      const equation = node.attrs.equation
      katex.render(equation, dom, {
        displayMode: true,
        throwOnError: false,
      })
      return {
        dom,
      }
    }
  },

  addCommands() {
    return {
      setBlockEquation: equation => ({ commands }) => {
        return commands.insertContent({
          type: this.name,
          attrs: { equation },
        })
      },
    }
  },
})
