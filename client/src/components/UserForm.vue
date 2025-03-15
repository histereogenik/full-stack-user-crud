<template>
    <Dialog
        :visible="visible"
        :header="isEdit ? 'Edit User' : 'Create User'"
        modal
        class="user-dialog"
        @hide="handleClose"
    >
        <div class="form-container">
            <div class="field">
                <label for="username">Username</label>
                <InputText id="username" v-model="form.username" class="input-field" />
            </div>

            <div class="field" v-if="!isEdit">
                <label for="password">Password</label>
                <InputText
                    id="password"
                    type="password"
                    v-model="form.password"
                    class="input-field"
                />
            </div>

            <div class="field">
                <label for="roles">Roles (comma-separated)</label>
                <InputText id="roles" v-model="rolesInput" class="input-field" />
            </div>

            <div class="field">
                <label for="timezone">Timezone</label>
                <InputText id="timezone" v-model="form.preferences.timezone" class="input-field" />
            </div>

            <div class="field-checkbox">
                <Checkbox v-model="form.active" inputId="active" binary />
                <label for="active">Active</label>
            </div>

            <div class="form-actions">
                <Button label="Cancel" severity="secondary" @click="handleClose" />
                <Button :label="isEdit ? 'Update' : 'Create'" @click="submitForm" />
            </div>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Checkbox from 'primevue/checkbox'

interface UserForm {
    username: string
    password?: string
    roles: string[]
    preferences: { timezone: string }
    active: boolean
}

const props = defineProps<{
    visible: boolean
    userData?: UserForm & { _id: string }
}>()

const emit = defineEmits(['close', 'submitted'])

const isEdit = computed(() => !!props.userData)

const form = ref<UserForm>({
    username: '',
    password: '',
    roles: [],
    preferences: { timezone: '' },
    active: true
})

const rolesInput = ref('')

watch(
    () => props.userData,
    (userData) => {
        if (userData) {
            form.value = { ...userData }
            rolesInput.value = userData.roles.join(', ')
        } else {
            resetForm()
        }
    },
    { immediate: true }
)

function handleClose() {
    emit('close')
}

function resetForm() {
    form.value = {
        username: '',
        password: '',
        roles: [],
        preferences: { timezone: '' },
        active: true
    }
    rolesInput.value = ''
}

async function submitForm() {
    form.value.roles = rolesInput.value.split(',').map((role) => role.trim())

    const confirmMessage = props.userData?._id
        ? 'Are you sure you want to update this user?'
        : 'Are you sure you want to create this user?'

    if (!confirm(confirmMessage)) {
        return // Stop submission if the user cancels
    }

    // Create a safe copy of the form to avoid modifying the original
    const payload = { ...form.value }

    // Remove fields not allowed by backend
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    delete (payload as any)._id
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    delete (payload as any).created_ts

    try {
        if (props.userData?._id) {
            // Edit mode
            await axios.put(`http://127.0.0.1:5000/users/${props.userData._id}`, payload)
        } else {
            // Create mode
            await axios.post('http://127.0.0.1:5000/users/', payload)
        }
        emit('submitted')
    } catch (error) {
        console.error(error)
    }
}
</script>

<style scoped>
.user-dialog {
    max-width: 500px;
}

.form-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.field {
    display: flex;
    flex-direction: column;
}

.input-field {
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-radius: 5px;
}

.field-checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}
</style>
