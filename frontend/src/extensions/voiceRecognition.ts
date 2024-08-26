import { Node, mergeAttributes, NodeViewRenderer } from '@tiptap/core'
import { VueNodeViewRenderer } from '@tiptap/vue-3'
import VoiceRecognition from '@/components/AI/VoiceRecognition.vue'

export default Node.create({
  name: 'voiceRecognition',

  group: 'block',

  atom: true,

  addAttributes() {
    return {
      content: {
        default: '',
      },
      editor: {
        default: null,
      },
    }
  },

  parseHTML() {
    return [
      {
        tag: 'voice-recognition',
      },
    ]
  },

  renderHTML({ HTMLAttributes }) {
    return ['voice-recognition', mergeAttributes(HTMLAttributes)]
  },

  addNodeView() {
    return VueNodeViewRenderer(VoiceRecognition)
  },
})
