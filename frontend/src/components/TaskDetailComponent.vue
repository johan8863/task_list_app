<script setup>
// vue

const props = defineProps({
  task: {
    id: Number,
    name: String,
    content: String,
    done: Boolean,
  },
  index: Number,
});

const emit = defineEmits(["onDeleteTask", "onUpdateTask"]);

const updateTask = () =>
  emit("onUpdateTask", {
    task: props.task,
    index: props.index,
  });
</script>

<template>
  <div>
    <h4>{{ task.name }}</h4>
    <p>{{ task.content }}</p>
    <span>{{ task.done }}</span> <br />
    <button type="button" @click="updateTask">update</button>
    <button type="button" @click="$emit('onDeleteTask', task.id)">
      delete
    </button>
  </div>
</template>
