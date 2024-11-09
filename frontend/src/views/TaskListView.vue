<script setup>
// vue
import { ref, onMounted, computed } from "vue";

// local
import TaskDetailComponent from "@/components/TaskDetailComponent.vue";
import { getAllTasks, postTask, deleteTask } from "@/services/task.service";

// tasks object
const task = ref({
  id: Number,
  name: "",
  content: "",
  done: false,
});
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

const createTask = async () => {
  const response = await postTask(task.value);
  const newTask = response.data;
  tasks.value.unshift(newTask);
  task.value.name = "";
  task.value.content = "";
  task.value.done = false;
};

const delTask = async (id) => {
  await deleteTask(id);
  tasks.value = tasks.value.filter((t) => t.id !== id);
};

// Life cycle
onMounted(async () => {
  await listAllTasks();
});
</script>

<template>
  <div>
    <h2>Your tasks!</h2>
    <!-- toggling control -->
    <div>
      <input
        @change="displayDoneTasks = !displayDoneTasks"
        type="checkbox"
        name=""
        id="displayDone"
      />
      <label for="displayDone">Show done.</label>
    </div>
    <div>
      <form @submit.prevent="createTask">
        <!-- name control -->
        <input type="text" v-model="task.name" placeholder="name" />

        <!-- content control -->
        <input type="text" v-model="task.content" placeholder="content" />

        <!-- done control -->
        <input type="checkbox" v-model="task.done" /> done

        <!-- buttons -->
        <button type="submit">Add</button>
      </form>
    </div>
    <div>
      <template v-for="task of filteredTasks" :key="task.id">
        <TaskDetailComponent :task="task" @on-delete-task="delTask(task.id)" />
      </template>
    </div>
  </div>
</template>
