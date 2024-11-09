import axios from 'axios'

const apiBase = axios.create({
  baseURL: '127.0.0.1:8000',
})

export default apiBase
