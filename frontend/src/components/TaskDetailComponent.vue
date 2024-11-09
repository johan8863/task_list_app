<script setup>
// vue

defineProps({
  task: {
    name: String,
    content: String,
    done: Boolean,
  },
})
</script>

<template>
  <div>
    <h4>{{ task.name }}</h4>
    <p>{{ task.content }}</p>
  </div>
</template>
