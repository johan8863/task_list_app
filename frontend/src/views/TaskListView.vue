<script setup>
// vue
import { ref, onMounted } from 'vue'

// local
import TaskDetailComponent from '@/components/TaskDetailComponent.vue'
import { getAllTasks } from '@/services/task.service'

// tasks object
const tasks = ref([])

// API consuming
const listAllTasks = async () => {
  const response = await getAllTasks()
  tasks.value = response.data
}

// Life cycle
onMounted(async () => {
  await listAllTasks()
})
</script>

<template>
  <div>
    <h2>Your tasks!</h2>
    <div>
      <template v-for="task of tasks" :key="task.id">
        <TaskDetailComponent :task="task" />
      </template>
    </div>
  </div>
</template>
