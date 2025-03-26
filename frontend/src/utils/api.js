import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5173', // Your Express server port
});

export default axiosInstance;
