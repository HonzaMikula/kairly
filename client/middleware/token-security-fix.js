import axios from 'axios'

export default function ({ app }) {
  if (process.server) {
    delete axios.defaults.headers.common['Authorization']    
  }
}
