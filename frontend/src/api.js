import axios from "axios"

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
})

export async function uploadFile(file) {
  const userId = localStorage.getItem("user_id")

  const formData = new FormData()
  formData.append("file", file)
  formData.append("user_id", userId)

  const response = await api.post("/upload", formData)

  return response.data
}

export async function getJobStatus(jobId) {
  const response = await api.get(`/job/${jobId}`)

  return response.data
}

export default api

export async function sendChat(query) {
  const userId = localStorage.getItem("user_id")

  const response = await api.post("/chat", {
    query: query,
    user_id: userId,
  })

  return response.data
}

export async function getUserFiles() {
  const userId = localStorage.getItem("user_id")

  const response = await api.get(`/files/${userId}`)

  return response.data
}