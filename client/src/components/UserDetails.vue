<template>
    <div class="p-4" v-if="user">
        <h2>User Details: {{ user.username }}</h2>
        <Card>
            <template #content>
                <div class="grid">
                    <div class="col-6">
                        <strong>Username:</strong> {{ user.username }}
                    </div>
                    <div class="mt-2">
                        <strong>Roles:</strong> {{ user.roles.join(', ') }}
                    </div>
                    <div class="mt-2">
                        <strong>Timezone:</strong> {{ user.preferences.timezone }}
                    </div>
                    <div class="mt-2">
                        <strong>Last Updated At:</strong> -
                    </div>
                    <div class="mt-2">
                        <strong>Active:</strong>
                        <Tag :severity="user.active ? 'success' : 'danger'">
                            {{ user.active ? 'Yes' : 'No' }}
                        </Tag>
                    </div>
                    <div class="mt-2">
                        <strong>Created At:</strong> {{ new Date(user.created_ts * 1000).toLocaleString() }}
                    </div>
                </div>

                <div class="mt-4 flex gap-2">
                    <Button label="Edit" icon="pi pi-pencil" @click="openEditModal" severity="info" outlined />
                    <Button label="Delete" icon="pi pi-trash" @click="deleteUser" severity="danger" outlined />
                    <Button label="Back" icon="pi pi-arrow-left" @click="goBack" severity="secondary" outlined />
                </div>

                <UserForm
                :visible="showEditModal"
                :userData="user"
                @close="closeModal"
                @submitted="handleUserUpdated"
                />
            </template>
        </Card>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import UserForm from './UserForm.vue'

interface User {
    _id: string
    username: string
    roles: string[]
    preferences: { timezone: string }
    active: boolean
    created_ts: number
}

const route = useRoute()
const router = useRouter()

const user = ref<User | null>(null)
const showEditModal = ref(false)

async function fetchUser() {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/users/${route.params.id}`)
        user.value = response.data
    } catch (error) {
        console.error(error)
    }
}

function openEditModal() {
    showEditModal.value = true
}

function closeModal() {
    showEditModal.value = false
}

function goBack() {
    router.push('/')
}

async function handleUserUpdated() {
    await fetchUser()
    closeModal()
}

async function deleteUser() {
    if (confirm('Are you sure you want to delete this user?')) {
        try {
            await axios.delete(`http://127.0.0.1:5000/users/${route.params.id}`)
            router.push('/')
        } catch (error) {
            console.error(error)
        }
    }
}

onMounted(fetchUser)
</script>