<script setup>
// vue

defineProps({
  task: {
    id: Number,
    name: String,
    content: String,
    done: Boolean,
  },
});

defineEmits(["onDeleteTask"]);
</script>

<template>
  <div>
    <h4>{{ task.name }}</h4>
    <p>{{ task.content }}</p>
    <span>{{ task.done }}</span>
    <button type="button" @click="$emit('onDeleteTask', task.id)">
      delete
    </button>
  </div>
</template>
