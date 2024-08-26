import { Image as TiptapImage, mergeAttributes } from '@tiptap/extension-image'
import api from '@/api'

export const CustomImage = TiptapImage.extend({
  name: 'customImage',

  addNodeView() {
    return ({ node, getPos, editor }) => {
      const dom = document.createElement('img')
      const { src, alt, title } = node.attrs
      dom.setAttribute('src', src)
      dom.setAttribute('alt', alt || '')
      dom.setAttribute('title', title || '')

      dom.addEventListener('click', (event) => {
        event.preventDefault()
        handleImageClick(node, getPos, editor)
      })

      return {
        dom,
      }
    }
  },
})

const handleImageClick = (node, getPos, editor) => {
    const action = prompt('选择操作: 1. OCR 2. 目标检测', '1')
    if (action === '1') {
      performOCR(node, getPos, editor)
    } else if (action === '2') {
      performObjectDetection(node, getPos, editor)
    }
}
  

const performOCR = (node, getPos, editor) => {
    // 将图片转为 base64
    const url = node.attrs.src
    fetch(url)
      .then(res => res.blob())
      .then(blob => {
        const reader = new FileReader()
        reader.onloadend = async () => {
          const base64_img = reader.result.split(',')[1] // 去掉前缀
          console.log(`output->base64_img`, base64_img)
          try {
            // 调用 OCR 接口
            const ocrResponse = await api.OCR({
              base64_img,
            })
            
            console.log(`output->ocrResponse`,ocrResponse.data)
            const ocrImageUrl = ocrResponse.data.image_url
            const ocrTexts = ocrResponse.data.texts.join(', ')
            
            console.log(`output->ocrImageUrl`,ocrImageUrl)
            // 插入 OCR 结果图片
            editor.chain().focus().deleteRange({ from: getPos(), to: getPos() + node.nodeSize }).setImage({ src: ocrImageUrl }).run()
  
            // 插入识别结果文字
            editor.chain().focus().insertContent(`<p>${ocrTexts}</p>`).run()
          } catch (ocrError) {
            console.error('OCR 识别失败:', ocrError)
          }
        }
        reader.readAsDataURL(blob)
    })
}
  
  
const performObjectDetection = (node, getPos, editor) => {
    // 将图片转为 base64
    const url = node.attrs.src
    fetch(url)
      .then(res => res.blob())
      .then(blob => {
        const reader = new FileReader()
        reader.onloadend = async () => {
          const base64_img = reader.result.split(',')[1] // 去掉前缀
          console.log(`output->base64_img`, base64_img)
          try {
            // 调用 OCR 接口
            const ocrResponse = await api.objectDetect({
              base64_img,
            })
            
            console.log(`output->ocrResponse`,ocrResponse.data)
          } catch (ocrError) {
            console.error('OCR 识别失败:', ocrError)
          }
        }
        reader.readAsDataURL(blob)
    })
}