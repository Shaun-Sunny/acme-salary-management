import apiClient from './client.js'

export async function getEmployees(params) {
  const { data } = await apiClient.get('/employees/', { params })
  return data
}

export async function getEmployee(id) {
  const { data } = await apiClient.get(`/employees/${id}`)
  return data
}

export async function createEmployee(data) {
  const response = await apiClient.post('/employees/', data)
  return response.data
}

export async function updateEmployee(id, data) {
  const response = await apiClient.put(`/employees/${id}`, data)
  return response.data
}

export async function deactivateEmployee(id) {
  const response = await apiClient.delete(`/employees/${id}`)
  return response.data
}

export async function getSalaryHistory(id) {
  const { data } = await apiClient.get(`/employees/${id}/salary-history`)
  return data
}