<template>
    <div class="user-management">
        <h2 class="mb-4">User Management</h2>

        <Button label="Create User" icon="pi pi-plus" class="mb-4" @click="openModal()" />

        <DataTable :value="users" paginator :rows="10">
            <Column header="Username">
                <template #body="{ data }">
                    <router-link class="user-link" :to="`/users/${data._id}`">{{
                        data.username
                    }}</router-link>
                </template>
            </Column>

            <Column header="Roles">
                <template #body="{ data }">
                    {{ data.roles.join(', ') }}
                </template>
            </Column>

            <Column header="Timezone">
                <template #body="{ data }">
                    {{ data.preferences.timezone }}
                </template>
            </Column>

            <Column header="Active">
                <template #body="{ data }">
                    <Tag :severity="data.active ? 'success' : 'danger'">
                        {{ data.active ? 'Yes' : 'No' }}
                    </Tag>
                </template>
            </Column>

            <Column header="Last Updated At">
                <template #body> - </template>
            </Column>

            <Column header="Created At">
                <template #body="{ data }">
                    {{ new Date(data.created_ts * 1000).toLocaleString() }}
                </template>
            </Column>

            <Column header="Actions">
                <template #body="{ data }">
                    <div class="action-buttons">
                        <Button
                            icon="pi pi-pencil"
                            severity="info"
                            outlined
                            @click="editUser(data)"
                        />
                        <Button
                            icon="pi pi-trash"
                            severity="danger"
                            outlined
                            @click="confirmDeleteUser(data._id)"
                        />
                    </div>
                </template>
            </Column>
        </DataTable>
        <UserForm
            :visible="showModal"
            :userData="modalData"
            @close="closeModal"
            @submitted="onFormSubmitted"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import UserForm from './UserForm.vue'
import { useModal } from '../composables/useModal'

interface User {
    _id: string
    username: string
    roles: string[]
    preferences: { timezone: string }
    active: boolean
    created_ts: number
}

const users = ref<User[]>([])
const { showModal, modalData, openModal, closeModal } = useModal<User>()

async function fetchUsers() {
    const { data } = await axios.get('http://127.0.0.1:5000/users/')
    users.value = data
}

function editUser(user: User) {
    openModal(user)
}

function confirmDeleteUser(userId: string) {
    if (confirm('Are you sure you want to delete this user?')) {
        deleteUser(userId)
    }
}

async function deleteUser(userId: string) {
    try {
        await axios.delete(`http://127.0.0.1:5000/users/${userId}`)
        await fetchUsers()
    } catch (error) {
        console.error(error)
    }
}

function onFormSubmitted() {
    closeModal()
    fetchUsers()
}

onMounted(fetchUsers)
</script>

<style scoped>
.user-link {
    color: #a0c4ff;
    text-decoration: none;
    transition: color 0.3s;
}

.user-link:hover {
    color: #90caf9;
}

.mb-4 {
    margin-bottom: 1rem;
}

.user-management {
    padding: 1rem;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
}
</style>
