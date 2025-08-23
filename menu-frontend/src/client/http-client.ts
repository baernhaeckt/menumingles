import axios from 'axios'

export const httpClient = axios.create({
  baseURL: 'https://menu-mingles-backend.azurewebsites.net/api/',
  timeout: 10 * 1000,
  headers: {
    'Content-Type': 'application/json',
  }
})
