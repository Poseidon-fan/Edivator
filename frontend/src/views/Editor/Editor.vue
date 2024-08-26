<template>
    <div class="EditMain">
        <Editor />
    </div>
</template>

<script setup lang="ts">
import Editor from '@/components/Editor/Editor.vue'
</script>

<style>
.EditMain {
    position: relative;
    width: 90vw;
    height: 100vh;
    margin: 20px auto;
    grid-template-columns: 20% 60% 20%;
}
</style>
