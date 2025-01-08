// function.js
import myAxios from "@/request";

// bufferRegister 函数，确保 URL 路径正确
export const bufferRegister = async (params) => {
  return myAxios.request({
    url: "function/buffer/", // 确保路径正确
    method: "POST",
    data: params,
  });
};

export const getCenterPointRegister = async () => {
  return myAxios.request({
    url: "function/centerPoint/", // 确保路径正确
    method: "get",
  });
};

export const topPathRegister = async (params) => {
  return myAxios.request({
    url: "function/pathPlanning/", // 确保路径正确
    method: "POST",
    data: params,
  });
};
