// src/utils/request.ts
import axios from "axios";
import { ElMessage } from 'element-plus'

let request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 5000
});


request.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


request.interceptors.response.use((response) => {
    return response.data;
}, (error) => {
    let message = "";
    let status = error.response.status;
    switch (status) {
        case 401:
            message = 'TOKEN过期'
            break
        case 403:
            message = '无权访问'
            break
        case 404:
            message = '请求地址错误'
            break
        case 500:
            message = '服务器出现问题'
            break
        default:
            message = '网络出现问题'
            break
    }
    ElMessage({
        type: "error",
        message
    });

    return Promise.reject(error);
})

export default request;