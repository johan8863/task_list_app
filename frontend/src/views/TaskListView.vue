<script setup>
// vue
import { ref, onMounted, computed } from "vue";

// local
import TaskDetailComponent from "@/components/TaskDetailComponent.vue";
import {
  getAllTasks,
  postTask,
  deleteTask,
  putTask,
} from "@/services/task.service";

// tasks object
const task = ref({
  id: Number,
  name: "",
  content: "",
  done: false,
});

const tasks = ref([]);

const taskBackendError = ref({
  id: 0,
  name: "",
  content: "",
  done: false,
  response: "",
  request: "",
});

// handlers
const displayDoneTasks = ref(false);
const updatingTask = ref(false);
const updatedTask = ref({});
const updatedTaskIndex = ref(-1);

// functions
const filteredTasks = computed(() => {
  return displayDoneTasks.value
    ? tasks.value
    : tasks.value.filter((task) => task.done === false);
});

const startUpdate = (payload) => {
  updatedTask.value = { ...payload.task };
  updatedTaskIndex.value = payload.index;
  updatingTask.value = true;
};

const cancelUpdate = () => {
  updatingTask.value = false;
  updatedTask.value = {};
};

const clearTaskBackendErrors = () => {
  taskBackendError.value.id = 0;
  taskBackendError.value.name = "";
  taskBackendError.value.content = "";
  taskBackendError.value.done = false;
  taskBackendError.value.response = "";
  taskBackendError.value.request = "";
};

// API consuming
const listAllTasks = async () => {
  try {
    const response = await getAllTasks();
    tasks.value = response.data;
  } catch (error) {
    if (error.response) {
      taskBackendError.value.response = error.response.data;
    } else if (error.request) {
      taskBackendError.value.request = "Server not responding.";
    } else {
      console.error("Backend error:", error);
    }
  }
};

const createTask = async () => {
  try {
    const response = await postTask(task.value);
    const newTask = response.data;

    tasks.value.unshift(newTask);

    task.value.name = "";
    task.value.content = "";
    task.value.done = false;

    clearTaskBackendErrors();
  } catch (error) {
    if (error.response) {
      taskBackendError.value = error.response.data;
    } else if (error.request) {
      taskBackendError.value.request = "Server not responding.";
    } else {
      console.error("Backend error", error);
    }
  }
};

const updateTask = async () => {
  try {
    const searchIndex = updatedTaskIndex.value;

    if (searchIndex === -1) {
      console.error("No valid task selected");
      return;
    }

    const response = await putTask(updatedTask.value);
    const savedTask = response.data;

    clearTaskBackendErrors();

    // updated tasks should be moved to the top, to highlight importance
    tasks.value.splice(searchIndex, 1);
    tasks.value.unshift(savedTask);

    // reset components properties values to be ready
    // to get new tasks updating
    updatingTask.value = false;
    updatedTaskIndex.value = -1;
    updatedTask.value = {};
  } catch (error) {
    if (error.response.data) {
      taskBackendError.value = error.response.data;
    } else if (error.response.status === 404) {
      taskBackendError.value.response = "Person not found.";
    } else if (error.request) {
      taskBackendError.value.request = error.request;
    } else {
      console.error("Backend error", error);
    }
  }
};

const delTask = async (id) => {
  try {
    await deleteTask(id);
    tasks.value = tasks.value.filter((t) => t.id !== id);
    clearTaskBackendErrors();
  } catch (error) {
    if (error.response) {
      console.log(error.response);
      taskBackendError.value.response = error.response.data.detail;
    } else if (error.request) {
      console.error(error.request);
      taskBackendError.value.request = "Server not responding.";
    }
  }
};

// Life cycle
onMounted(async () => {
  await listAllTasks();
});
</script>

<template>
  <div>
    <h2>Your tasks!</h2>
    <div v-if="!taskBackendError.response && !taskBackendError.request">
      <!-- main content -->
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
      <!-- create task -->
      <div v-if="!updatingTask">
        <form @submit.prevent="createTask">
          <!-- name control -->
          <input type="text" v-model="task.name" placeholder="name" />
          <span v-if="taskBackendError.name">{{ taskBackendError.name }}</span>

          <!-- content control -->
          <input type="text" v-model="task.content" placeholder="content" />
          <span v-if="taskBackendError.content">{{
            taskBackendError.content
          }}</span>

          <!-- done control -->
          <input type="checkbox" v-model="task.done" /> done

          <!-- buttons -->
          <button type="submit">Add</button>
        </form>
      </div>
      <!-- update task -->
      <div v-else="updatingTask">
        <!-- name control -->
        <input type="text" v-model="updatedTask.name" placeholder="name" />
        <span v-if="taskBackendError.name">{{ taskBackendError.name }}</span>

        <!-- content control -->
        <input
          type="text"
          v-model="updatedTask.content"
          placeholder="content"
        />
        <span v-if="taskBackendError.content">{{
          taskBackendError.content
        }}</span>

        <!-- done control -->
        <input type="checkbox" v-model="updatedTask.done" /> done

        <!-- buttons -->
        <button type="button" @click="updateTask">update</button>
        <button type="button" @click="cancelUpdate">cancel</button>
      </div>
      <div>
        <template v-for="(task, index) of filteredTasks" :key="task.id">
          <TaskDetailComponent
            :task="task"
            :index="index"
            @on-delete-task="delTask(task.id)"
            @on-update-task="startUpdate"
          />
        </template>
      </div>
    </div>
    <div v-else>
      <div v-if="taskBackendError.request">
        <span>{{ taskBackendError.request }}</span>
      </div>
      <div v-if="taskBackendError.response">
        <span>{{ taskBackendError.response }}</span>
      </div>
    </div>
  </div>
</template>
