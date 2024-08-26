import { Node, mergeAttributes } from '@tiptap/core'
import katex from 'katex'
import 'katex/dist/katex.min.css'

export const InlineEquation = Node.create({
  name: 'inlineEquation',

  inline: true,
  group: 'inline',
  atom: true,

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
        tag: 'span[data-equation]',
      },
    ]
  },

  renderHTML({ HTMLAttributes }) {
    return ['span', mergeAttributes(HTMLAttributes, { 'data-equation': HTMLAttributes.equation })]
  },

  addNodeView() {
    return ({ node }) => {
      const dom = document.createElement('span')
      const equation = node.attrs.equation
      dom.setAttribute('data-equation', equation)
      katex.render(equation, dom, {
        throwOnError: false,
      })
      return {
        dom,
      }
    }
  },

  addCommands() {
    return {
      setInlineEquation: equation => ({ commands }) => {
        return commands.insertContent({
          type: this.name,
          attrs: { equation },
        })
      },
    }
  },
})
