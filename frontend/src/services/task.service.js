import apiBase from './base.service'

const baseTasksListUrl = '/tasks-list'

export const getAllTasks = async () => await apiBase.get(`${baseTasksListUrl}/`)

export const getPendingTasks = async () => await apiBase.get(`${baseTasksListUrl}-pending/`)
