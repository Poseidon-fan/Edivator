import { Node, mergeAttributes } from '@tiptap/core'

export const TextBlock = Node.create({
  name: 'textBlock',

  group: 'block',

  content: 'text*',

  parseHTML() {
    return [
      {
        tag: 'div',
        getAttrs: dom => dom.classList.contains('text-block') ? {} : false,
      },
    ]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', mergeAttributes(HTMLAttributes, { class: 'text-block' }), 0]
  },

  addNodeView() {
    return ({ node, HTMLAttributes }) => {
      const dom = document.createElement('div')
      dom.setAttribute('class', 'text-block')
      dom.setAttribute('style', 'border: 1px solid #e0e0e0; padding: 8px; margin: 4px 0;')
      dom.innerText = node.textContent
      return {
        dom,
        contentDOM: dom,
      }
    }
  },
})
