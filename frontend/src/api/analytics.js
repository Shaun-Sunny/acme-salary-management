import apiClient from './client.js'

export async function getSalaryStats() {
  const { data } = await apiClient.get('/analytics/salary-stats')
  return data
}

export async function getHeadcount() {
  const { data } = await apiClient.get('/analytics/headcount')
  return data
}

export async function getBandDistribution() {
  const { data } = await apiClient.get('/analytics/band-distribution')
  return data
}

export async function getTopEarners(limit = 10) {
  const { data } = await apiClient.get('/analytics/top-earners', {
    params: { limit },
  })
  return data
}