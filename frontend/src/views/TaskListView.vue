<script setup>
// vue
import { ref } from 'vue'

// tasks object
const tasks = ref([
  {
    id: 1,
    name: 'Kitchen',
    content: 'Wash the dishes, dry the sink.',
    done: true,
  },
  {
    id: 2,
    name: 'Groceries',
    content: 'Chicken drums.',
    done: true,
  },
  {
    id: 3,
    name: 'Painting',
    content: 'Paint the rooms ASAP.',
    done: false,
  },
  {
    id: 1,
    name: 'Accounting',
    content: 'Transfer 10% to saving credit card.',
    done: true,
  },
])
</script>

<template>
  <div>
    <h2>Your tasks!</h2>
    <div>
      <template v-for="task of tasks" :key="task.id">
        <h4>{{ task.name }}</h4>
        <p>{{ task.content }}</p>
      </template>
    </div>
  </div>
</template>
