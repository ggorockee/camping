<template>
  <button
    :class="buttonClasses"
    :disabled="!canClick || loading"
    class="text-lg font-medium focus:outline-none text-white py-4 transition-colors"
  >
    {{ loading ? 'Loading...' : actionText }}
  </button>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface Props {
  canClick: boolean
  loading: boolean
  actionText: string
}

const props = defineProps<Props>()

const buttonClasses = computed(() => {
  if (props.loading) {
    // Optional: Could style differently when loading
    return 'bg-gray-300 pointer-events-none'
  }
  return props.canClick ? 'bg-lime-600 hover:bg-lime-700' : 'bg-gray-300 pointer-events-none'
})
</script>
