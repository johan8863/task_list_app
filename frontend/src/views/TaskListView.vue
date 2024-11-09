<script setup>
// vue
import { ref, onMounted, computed } from "vue";

// local
import TaskDetailComponent from "@/components/TaskDetailComponent.vue";
import { getAllTasks } from "@/services/task.service";

// tasks object
const tasks = ref([]);

// handlers
const displayDoneTasks = ref(false);

// functions
const filteredTasks = computed(() => {
  return displayDoneTasks.value
    ? tasks.value
    : tasks.value.filter((task) => task.done === false);
});

// API consuming
const listAllTasks = async () => {
  const response = await getAllTasks();
  tasks.value = response.data;
};

// Life cycle
onMounted(async () => {
  await listAllTasks();
});
</script>

<template>
  <div>
    <h2>Your tasks!</h2>
    <div>
      <form>
        <input
          @change="displayDoneTasks = !displayDoneTasks"
          type="checkbox"
          name=""
          id=""
        />
        Show done.
        <input type="text" />
      </form>
    </div>
    <div>
      <template v-for="task of filteredTasks" :key="task.id">
        <TaskDetailComponent :task="task" />
      </template>
    </div>
  </div>
</template>
