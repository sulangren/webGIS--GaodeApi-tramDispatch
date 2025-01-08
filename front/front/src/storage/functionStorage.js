// userStore.js
import { defineStore } from "pinia";
import { bufferRegister, topPathRegister } from "@/api/function"; // 确保导入的是正确的 bufferRegister 函数

export const functionAuthStore = defineStore("auth", () => {
  async function bufferRegisters(params) {
    try {
      const response = await bufferRegister(params); // 确保传递正确的参数结构
      if (response.data.code === 0 && response.data.data) {
        return response.data;
      }
    } catch (error) {
      console.error("Failed to fetch point data:", error);
      throw error;
    }
  }

  async function topPathRegisters(params) {
    try {
      const response = await topPathRegister(params); // 确保传递正确的参数结构
      if (response.data.code === 0 && response.data.data) {
        return response.data;
      }
    } catch (error) {
      console.error("Failed to fetch point data:", error);
      throw error;
    }
  }

  return {
    bufferRegisters,
    topPathRegisters,
  };
});
