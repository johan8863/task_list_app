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
  // in case the user decides to change from updating or creating and
  // errors have already been trigered, they must be cleared
  clearTaskBackendErrors();
  updatedTask.value = { ...payload.task };
  updatedTaskIndex.value = payload.index;
  updatingTask.value = true;
};

const cancelUpdate = () => {
  // in case the user decides to change from updating or creating and
  // errors have already been trigered, they must be cleared
  clearTaskBackendErrors();
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
    // in case the user decides to change from updating or creating and
    // errors have already been trigered, they must be cleared
    clearTaskBackendErrors();
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
    // in case the user decides to change from updating or creating and
    // errors have already been trigered, they must be cleared
    clearTaskBackendErrors();
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
  <div class="bg-light">
    <div class="container">
      <h2 class="text-primary mb-4">Your tasks!</h2>
      <div v-if="!taskBackendError.response && !taskBackendError.request">
        <!-- main content -->

        <!-- toggling control -->
        <div class="form-check mb-3">
          <input
            @change="displayDoneTasks = !displayDoneTasks"
            type="checkbox"
            name=""
            id="displayDone"
            class="form-check-input"
          />
          <label class="form-check-label" for="displayDone">Show done.</label>
        </div>
        <!-- create task -->
        <div v-if="!updatingTask">
          <form @submit.prevent="createTask" class="row g-3 mb-4">
            <!-- name control -->
            <div class="col-auto">
              <input
                type="text"
                v-model="task.name"
                placeholder="task name"
                class="form-control"
              />
              <!-- backend errors -->
              <div v-if="taskBackendError.name" class="form-text text-danger">
                <span
                  v-for="(error, index) in taskBackendError.name"
                  :key="index"
                  >{{ error }}</span
                >
              </div>
            </div>

            <!-- content control -->
            <div class="col-auto">
              <input
                type="text"
                v-model="task.content"
                placeholder="task content"
                class="form-control"
              />
              <!-- backend errors -->
              <div
                v-if="taskBackendError.content"
                class="form-text text-danger"
              >
                <span
                  v-for="(error, index) in taskBackendError.content"
                  :key="index"
                  >{{ error }}</span
                >
              </div>
            </div>

            <!-- done control -->
            <div class="col-auto form-check">
              <input
                type="checkbox"
                v-model="task.done"
                class="form-check-input"
                id="done"
              />
              <label for="done" class="form-check-lab">done</label>
            </div>

            <div class="col-auto">
              <!-- buttons -->
              <button type="submit" class="btn btn-primary btn-sm">Add</button>
            </div>
          </form>
          <!-- end create task -->
        </div>

        <!-- update task -->
        <div v-else="updatingTask">
          <form class="row g-3 mb-4">
            <!-- name control -->
            <div class="col-auto">
              <input
                type="text"
                v-model="updatedTask.name"
                placeholder="task name"
                class="form-control"
              />
              <!-- backend errors -->
              <div v-if="taskBackendError.name" class="form-text text-danger">
                <span
                  v-for="(error, index) in taskBackendError.name"
                  :key="index"
                  >{{ error }}</span
                >
              </div>
            </div>

            <!-- content control -->
            <div class="col-auto">
              <input
                type="text"
                v-model="updatedTask.content"
                placeholder="task content"
                class="form-control"
              />
              <!-- backend errors -->
              <div
                v-if="taskBackendError.content"
                class="form-text text-danger"
              >
                <span
                  v-for="(error, index) in taskBackendError.content"
                  :key="index"
                  >{{ error }}</span
                >
              </div>
            </div>

            <!-- done control -->
            <div class="col-auto form-check">
              <input
                type="checkbox"
                v-model="updatedTask.done"
                class="form-check-input"
                id="done"
              />
              <label for="done" class="form-check-label">done</label>
            </div>

            <!-- buttons -->
            <div class="col-auto">
              <button
                type="button"
                @click="updateTask"
                class="btn btn-primary btn-sm me-2"
              >
                Update
              </button>
              <button
                type="button"
                @click="cancelUpdate"
                class="btn btn-secondary btn-sm"
              >
                Cancel
              </button>
            </div>
          </form>
          <!-- end update task -->
        </div>
        <!-- tasks list -->
        <div>
          <template v-for="(task, index) of filteredTasks" :key="task.id">
            <TaskDetailComponent
              :task="task"
              :index="index"
              @on-delete-task="delTask(task.id)"
              @on-update-task="startUpdate"
            />
          </template>
          <!-- end tasks list -->
        </div>
      </div>
      <div v-else>
        <div v-if="taskBackendError.request">
          <span class="alert alert-danger">{{ taskBackendError.request }}</span>
        </div>
        <div v-if="taskBackendError.response">
          <span class="alert alert-danger">{{
            taskBackendError.response
          }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
