// src/store/profile.js

import { defineStore } from 'pinia'

interface ProfileState {
    username: string
    id: string
    mobile: string
    email: string
    avatar: string
    companyIds: Array<number>
    did: string
    keywords: Array<Array<string>>,
    money: number
}

export const useProfileStore = defineStore('profile', {
    state: (): ProfileState => ({
        username: '',
        id: '0',
        mobile: '',
        email: '',
        avatar: '',
        companyIds: [],
        did: '0',
        keywords: [],
        money: 0
    }),

    actions: {
        updateProfile(profile: {
            username: string
            id: string
            mobile: string
            email: string
            avatar: string
            company_ids: Array<number>
            keywords: Array<Array<string>>
            point: number
        }) {
            console.log(`output->profile`,profile)
            this.username = profile.username
            this.id = profile.id
            this.mobile = profile.mobile
            this.email = profile.email
            this.avatar = profile.avatar
            this.companyIds = profile['company_ids']
            this.keywords = profile['keywords']
            this.money = profile['point']
        },
    },

    persist: {
        key: 'profile-store',
        storage: window.sessionStorage,
        paths: ['username', 'id', 'mobile', 'email', 'avatar', 'companyIds', 'keywords', 'money'],
    },
})

interface CompanyState {
    id: number
    name: string
    admin: number
    users: Array<number>
    administrators: Array<number>
}

export const useCompanyStore = defineStore('company', {
    state: (): CompanyState => ({
        id: 0,
        name: '',
        admin: 0,
        users: [],
        administrators: [],
    }),

    actions: {
        updateCompany(company: {
            id: number
            name: string
            admin: number
            users: Array<number>
            administrators: Array<number>
        }) {
            this.id = company.id
            this.name = company.name
            this.admin = company.admin
            this.users = company.users
            this.administrators = company.administrators
        },
        isAdmin() {
            // profile store中id是否在company store中的administrators中
            const profileStore = useProfileStore()
            return this.administrators.includes(Number(profileStore.id))
        },
    },

    persist: {
        key: 'company-store',
        storage: window.sessionStorage,
        paths: ['id', 'name', 'admin', 'users', 'administrators'],
    },
})
