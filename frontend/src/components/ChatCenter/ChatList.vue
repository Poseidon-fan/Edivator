<script setup lang="ts">
import { defineEmits, onMounted, ref } from 'vue'
import { MessageTwoTone, SearchOutlined } from '@ant-design/icons-vue'
import api from '@/api'
import { message } from 'ant-design-vue'
import { useCompanyStore } from '@/store/profile'
import teamAvatar from '@/assets/images/teamAvatar.png'

const companyStore = useCompanyStore()

const groups = ref([])

onMounted(async () => {
    groups.value = await api.queryCompanyTeamsShort(companyStore.id)
})

const selectedGroup = ref(null)
const emit = defineEmits(['update-selected-group'])
const searchVisible = ref(false)
const searchQuery = ref('')
const searchResults = ref([])

const selectGroup = (group: any) => {
    selectedGroup.value = group
    emit('update-selected-group', group)
}

const showSearchModal = () => {
    searchVisible.value = true
}

const handleSearch = async () => {
    searchResults.value = await api.searchGroup(searchQuery.value)
}

const handleCancel = () => {
    searchVisible.value = false
}

const handleJoinGroup = async (group: any) => {
    const res = await api.applyJoinGroup({
        target: group.id,
    })
    if (res != null) {
        message.success('申请成功')
    }
}
</script>

<template>
    <div class="chat-list-container">
        <div class="chat-list-header">
            <MessageTwoTone style="font-size: 20px" />
            <span>我的群组</span>
        </div>
        <div class="list-content">
            <a-list class="group-list" item-layout="horizontal" :data-source="groups">
                <template #renderItem="group">
                    <a-list-item
                        :class="['user-list-item', { selected: group.item === selectedGroup }]"
                        @click="selectGroup(group.item)"
                    >
                        <a-list-item-meta>
                            <template #avatar>
                                <a-avatar
                                    class="teamAvatar"
                                    :src="group.item.avatar ? group.item.avatar : teamAvatar"
                                />
                            </template>
                            <template #title>
                                {{ group.item.name }}
                            </template>
                            <template #description>
                                <a-typography-text ellipsis :content="group.item.description" />
                            </template>
                        </a-list-item-meta>
                    </a-list-item>
                </template>
            </a-list>
        </div>
        <a-modal
            v-model:visible="searchVisible"
            title="搜索群组"
            @ok="handleSearch"
            @cancel="handleCancel"
            width="600px"
        >
            <a-input-search
                v-model:value="searchQuery"
                placeholder="请输入群组名或ID"
                enter-button="搜索"
                @search="handleSearch"
                style="margin-bottom: 20px"
            />
            <a-list v-if="searchResults.length > 0" :data-source="searchResults" item-layout="horizontal">
                <template #renderItem="group">
                    <a-list-item>
                        <a-list-item-meta>
                            <template #avatar>
                                <a-avatar
                                    :src="group.item.avatar || 'https://www.antdv.com/assets/logo.1ef800a8.svg'"
                                />
                            </template>
                            <template #title>
                                {{ group.item.name }}
                            </template>
                            <template #description>
                                {{ group.item.description }}
                            </template>
                        </a-list-item-meta>
                        <a-button type="primary" @click="handleJoinGroup(group.item)">申请加入</a-button>
                    </a-list-item>
                </template>
            </a-list>
            <a-empty v-if="searchResults.length === 0" description="暂无搜索结果" />
        </a-modal>
    </div>
</template>

<style scoped>
.chat-list-container {
    width: 100%;
    padding: 20px;
    border-radius: 10px;
}

.chat-list-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.chat-list-header > span {
    font-size: 16px;
    line-height: 24px;
    margin-left: 10px;
    font-weight: 500;
}

.list-content {
    margin-top: 20px;
}

.user-list-item {
    transition: background-color 0.3s;
    border-radius: 10px;
    cursor: pointer;
}

.user-list-item:hover {
    background-color: #f5f5f5;
}

.user-list-item.selected {
    background-color: #e6f7ff;
    border-left: 4px solid #1890ff;
}

.a-button {
    margin-left: 10px;
}

.teamAvatar {
    transform: scale(1.2);
    position: relative;
    top: 10px;
    border: solid 1px rgba(0, 0, 0, 0.4);
}
</style>
