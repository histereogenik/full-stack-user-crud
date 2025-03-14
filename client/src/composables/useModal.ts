import { ref } from 'vue'

export function useModal<T>() {
    const showModal = ref(false)
    const modalData = ref<T | undefined>(undefined)

    function openModal(data?: T) {
        modalData.value = data || undefined
        showModal.value = true
    }

    function closeModal() {
        showModal.value = false
        modalData.value = undefined
    }

    return {
        showModal,
        modalData,
        openModal,
        closeModal
    }
}