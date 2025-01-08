// request.js

// 导入 axios 用于发起 HTTP 请求
import axios from "axios";
// 导入 Pinia store
import { useAuthStore } from "@/storage/userStorage";
// 导入 Vue Router
import router from "@/router"; // 确保路径正确

// 创建 axios 实例
const myAxios = axios.create({
  // 设置基础 URL
  baseURL: "http://localhost:8000",
  // 设置请求超时时间
  timeout: 10000,
  // 允许携带 cookie
  withCredentials: true,
});

// 添加请求拦截器
myAxios.interceptors.request.use(
  (config) => {
    // 设置请求头
    myAxios.defaults.headers.common["Content-Type"] = "application/json";
    // 获取 Pinia store 中的 token
    const authStore = useAuthStore();
    const token = authStore.user.token;
    // 如果 token 存在，则添加到请求头中
    if (token) {
      config.headers["Authorization"] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    // 处理请求错误
    return Promise.reject(error);
  }
);

// 添加响应拦截器
myAxios.interceptors.response.use(
  (response) => {
    // 处理响应数据
    return response;
  },
  (error) => {
    // 获取响应对象
    const response = error.response;
    if (response) {
      // 如果状态码为 401 或 403，处理未授权或无权限的情况
      if (response.status === 401 || response.status === 403) {
        console.log("User is not logged in or does not have permission.");
        // 重定向到登录页面，并携带重定向路径
        router.push({
          path: "/",
          query: { redirect: window.location.href },
        });
      }
      // 如果返回的错误信息为 "Invalid credentials"，则打印提示
      if (response.data.error === "Invalid credentials") {
        console.log("Invalid credentials provided.");
      }
    }
    // 处理响应错误
    return Promise.reject(error);
  }
);

// 导出 axios 实例
export default myAxios;
