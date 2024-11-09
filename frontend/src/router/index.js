import { createRouter, createWebHistory } from 'vue-router'
import TaskListView from '@/views/TaskListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'tasks',
      component: TaskListView,
    },
  ],
})

export default router
