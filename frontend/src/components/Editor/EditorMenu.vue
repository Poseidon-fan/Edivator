<template>
    <div>
        <template v-for="(item, index) in items">
            <div class="divider" v-if="item.type === 'divider'" :key="`divider${index}`" />
            <MenuItem v-else :key="index" v-bind="item" />
        </template>
    </div>
</template>

<script setup lang="ts">
import { Editor } from '@tiptap/vue-3'
import MenuItem from '@/components/Editor/MenuItem.vue'

const props = defineProps<{ editor: Editor }>()

const items = [
    {
        icon: 'bold',
        title: 'Bold',
        action: () => props.editor?.chain().focus().toggleBold().run(),
        isActive: () => props.editor?.isActive('bold'),
    },
    {
        icon: 'italic',
        title: 'Italic',
        action: () => props.editor?.chain().focus().toggleItalic().run(),
        isActive: () => props.editor?.isActive('italic'),
    },
    {
        icon: 'strikethrough',
        title: 'Strike',
        action: () => props.editor?.chain().focus().toggleStrike().run(),
        isActive: () => props.editor?.isActive('strike'),
    },
    {
        icon: 'code-view',
        title: 'Code',
        action: () => props.editor?.chain().focus().toggleCode().run(),
        isActive: () => props.editor?.isActive('code'),
    },
    {
        icon: 'mark-pen-line',
        title: 'Highlight',
        action: () => props.editor?.chain().focus().toggleHighlight().run(),
        isActive: () => props.editor?.isActive('highlight'),
    },
    {
        type: 'divider',
    },
    {
        icon: 'h-1',
        title: 'Heading 1',
        action: () => props.editor?.chain().focus().toggleHeading({ level: 1 }).run(),
        isActive: () => props.editor?.isActive('heading', { level: 1 }),
    },
    {
        icon: 'h-2',
        title: 'Heading 2',
        action: () => props.editor?.chain().focus().toggleHeading({ level: 2 }).run(),
        isActive: () => props.editor?.isActive('heading', { level: 2 }),
    },
    {
        icon: 'h-3',
        title: 'Heading 3',
        action: () => props.editor?.chain().focus().toggleHeading({ level: 3 }).run(),
        isActive: () => props.editor?.isActive('heading', { level: 3 }),
    },
    {
        icon: 'h-4',
        title: 'Heading 4',
        action: () => props.editor?.chain().focus().toggleHeading({ level: 4 }).run(),
        isActive: () => props.editor?.isActive('heading', { level: 4 }),
    },
    {
        icon: 'paragraph',
        title: 'Paragraph',
        action: () => props.editor?.chain().focus().setParagraph().run(),
        isActive: () => props.editor?.isActive('paragraph'),
    },
    {
        icon: 'list-unordered',
        title: 'Bullet List',
        action: () => props.editor?.chain().focus().toggleBulletList().run(),
        isActive: () => props.editor?.isActive('bulletList'),
    },
    {
        icon: 'list-ordered',
        title: 'Ordered List',
        action: () => props.editor?.chain().focus().toggleOrderedList().run(),
        isActive: () => props.editor?.isActive('orderedList'),
    },
    {
        icon: 'list-check-2',
        title: 'Task List',
        action: () => props.editor?.chain().focus().toggleTaskList().run(),
        isActive: () => props.editor?.isActive('taskList'),
    },
    {
        icon: 'code-box-line',
        title: 'Code Block',
        action: () => props.editor?.chain().focus().toggleCodeBlock().run(),
        isActive: () => props.editor?.isActive('codeBlock'),
    },
    {
        type: 'divider',
    },
    {
        icon: 'double-quotes-l',
        title: 'Blockquote',
        action: () => props.editor?.chain().focus().toggleBlockquote().run(),
        isActive: () => props.editor?.isActive('blockquote'),
    },
    {
        icon: 'separator',
        title: 'Horizontal Rule',
        action: () => props.editor?.chain().focus().setHorizontalRule().run(),
    },
    {
        type: 'divider',
    },
    {
        icon: 'text-wrap',
        title: 'Hard Break',
        action: () => props.editor?.chain().focus().setHardBreak().run(),
    },
    {
        icon: 'format-clear',
        title: 'Clear Format',
        action: () => props.editor?.chain().focus().clearNodes().unsetAllMarks().run(),
    },
    {
        type: 'divider',
    },
    {
        icon: 'arrow-go-back-line',
        title: 'Undo',
        action: () => props.editor?.chain().focus().undo().run(),
    },
    {
        icon: 'arrow-go-forward-line',
        title: 'Redo',
        action: () => props.editor?.chain().focus().redo().run(),
    },
]
</script>

<style>
.divider {
    background-color: rgba(255, 255, 255, 0.25);
    height: 1.25rem;
    margin-left: 0.5rem;
    margin-right: 0.75rem;
    width: 1px;
    display: inline-block;
}
</style>
