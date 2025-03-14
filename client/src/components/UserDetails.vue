<template>
    <div class="user-details" v-if="user">
        <h2 class="page-title">User Details</h2>
        <Card class="user-card">
            <template #content>
                <div class="details-grid">
                    <div><strong>Username:</strong> {{ user.username }}</div>
                    <div><strong>Roles:</strong> {{ user.roles.join(', ') }}</div>
                    <div><strong>Timezone:</strong> {{ user.preferences.timezone }}</div>
                    <div>
                        <strong>Active:</strong>
                        <Tag class="active-m" :severity="user.active ? 'success' : 'danger'">
                            {{ user.active ? 'Yes' : 'No' }}
                        </Tag>
                    </div>
                    <div><strong>Created At:</strong> {{ new Date(user.created_ts * 1000).toLocaleString() }}</div>
                </div>

                <div class="actions">
                        <Button label="Edit" icon="pi pi-pencil" severity="info" outlined @click="openEditModal" />
                        <Button label="Delete" icon="pi pi-trash" severity="danger" outlined @click="deleteUser" />
                        <Button label="Back" icon="pi pi-arrow-left" severity="secondary" outlined @click="goBack" />
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

<style scoped>
.user-details {
    max-width: 600px;
    margin: 2rem auto;
    padding: 1.5rem;
    background-color: #1e1e1e;
    border-radius: 8px;
}

.page-title {
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 1rem;
}

.user-card {
    padding: 1rem;
    border-radius: 8px;
    background-color: #242424;
}

.details-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding: 1rem;
}
.active-m {
    margin-left: 0.3rem
}
.actions {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
}

</style>