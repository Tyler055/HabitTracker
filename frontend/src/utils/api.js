import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/api', // Or whatever your backend URL is
});

export default axiosInstance;
