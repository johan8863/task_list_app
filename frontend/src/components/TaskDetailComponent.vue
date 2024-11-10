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
  <div class="card mb-2">
    <!-- body -->
    <div class="card-body">
      <!-- task info -->
      <h4 class="card-title">{{ task.name }}</h4>
      <p class="card-text">{{ task.content }}</p>
      <span class="badge" :class="task.done ? 'bg-success' : 'bg-warning'">
        {{ task.done ? "Completed" : "Pending" }}
      </span>

      <!-- buttons -->
      <div class="mt-3">
        <button
          type="button"
          @click="updateTask"
          class="btn btn-outline-primary btn-sm me-2"
        >
          Update
        </button>
        <button
          type="button"
          @click="$emit('onDeleteTask', task.id)"
          class="btn btn-outline-danger btn-sm"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>
