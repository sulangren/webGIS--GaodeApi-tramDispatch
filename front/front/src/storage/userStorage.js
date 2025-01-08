// userStore.js

// 导入 Pinia 的 defineStore 用于定义状态管理 store
import { defineStore } from "pinia";
// 导入 Vue 的 ref 响应式引用
import { ref } from "vue";
// 导入用户相关的 API 函数
import {
  getCurrentUser,
  userLogin,
  deleteUser,
  userRegister,
} from "@/api/user";

import { bufferRegister } from "@/api/function";

// 定义名为 "auth" 的 Pinia store
export const useAuthStore = defineStore("auth", () => {
  // 创建一个响应式引用，存储用户信息
  const user = ref({
    username: "未登录",
    token: "",
  });

  // 异步函数，用于获取当前登录用户信息
  async function fetchLoginUser() {
    try {
      const token = user.value.token; // 从 Pinia store 获取 Token
      if (!token) {
        console.error("No token available for fetching user data");
        return;
      }
      const res = await getCurrentUser();
      if (res.data.code === 0 && res.data.data) {
        user.value = { ...res.data.data, token: res.data.token }; // 更新用户信息
        console.log(res.data.data);
      } else {
        // 如果获取用户信息失败，不设置默认用户
      }
    } catch (error) {
      console.log(error);
    }
  }

  // 函数，用于设置登录用户信息
  function setLoginUser(newLoginUser) {
    user.value = newLoginUser;
  }

  // 异步函数，用于注册新用户
  async function register(credentials) {
    try {
      const res = await userRegister(credentials);
      console.log(res);
      if (res.data.code === 0 && res.data.data) {
        user.value = { ...res.data.data, token: "" };
        user.value.username = "";
        console.log(res.data);
        return res.data;
      } else {
        throw new Error(res.data.message || "注册失败");
      }
    } catch (error) {
      console.error("Register failed:", error);
      throw error;
    }
  }

  // 异步函数，用于用户登录
  async function login(credentials) {
    try {
      const res = await userLogin(credentials);
      if (res.data.code === 0 && res.data.data) {
        user.value = { ...res.data.data, token: res.data.token };
        return res.data;
      }
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  }

  // 函数，用于用户注销
  function logout() {
    // 清除用户状态和 Token
    user.value = { username: "未登录", token: "" };
    // 调用登出 API
    deleteUser(user.value.token);
  }

  async function bufferRegisters(id) {
    try {
      const response = await bufferRegister(id);
      if (response.data.code === 0 && response.data.data) {
        user.value = { ...response.data.data, token: response.data.token };
        return response.data;
      } // 假设后端返回的数据结构为 { data: [[113.268774, 35.18784], [113.269978, 35.188001]] }
    } catch (error) {
      console.error("Failed to fetch point data:", error);
      throw error; // 可以根据需要进行进一步处理
    }
  }

  // 返回 store 中的所有响应式属性和函数
  return {
    user,
    fetchLoginUser,
    setLoginUser,
    login,
    logout,
    register,
    bufferRegisters,
  };
});
