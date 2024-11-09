import apiBase from "./base.service";

const baseTasksListUrl = "/tasks-list";
const baseTasksDetailUrl = "/tasks-detail";

export const getAllTasks = async () =>
  await apiBase.get(`${baseTasksListUrl}/`);

export const getPendingTasks = async () =>
  await apiBase.get(`${baseTasksListUrl}-pending/`);

export const postTask = async (task) =>
  await apiBase.post(`${baseTasksListUrl}/`, task);

export const deleteTask = async (id) =>
  await apiBase.delete(`${baseTasksDetailUrl}/${id}/`);
