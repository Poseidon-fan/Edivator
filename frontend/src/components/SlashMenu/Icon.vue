<script setup>
import { Icon } from '@iconify/vue'
defineProps(['icon', 'height', 'inline', 'color'])
</script>

<template>
    <div>
        <Icon
            :icon="icon"
            :height="height ? height : '18'"
            :inline="inline ? true : false"
            :color="color ? color : ''"
        />
    </div>
</template>
