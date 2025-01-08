// user.js
// 导入 axios 实例，用于发起 HTTP 请求
import myAxios from "@/request";

// 用户注册
export const userRegister = async (params) => {
  // 发起 POST 请求到 /api/user/register 路由，传递用户数据
  return myAxios.request({
    url: "user/register/",
    method: "POST",
    data: params,
  });
};

// 用户登录
export const userLogin = async (params) => {
  // 发起 POST 请求到 /api/user/login 路由，传递用户登录数据
  return myAxios.request({
    url: "user/login/",
    method: "POST",
    data: params,
  });
};

// 用户注销
export const userLogout = async (params) => {
  // 发起 POST 请求到 /api/user/logout 路由，传递注销数据
  return myAxios.request({
    url: "/api/user/logout",
    method: "POST",
    data: params,
  });
};

// 获取当前用户
export const getCurrentUser = async () => {
  // 发起 GET 请求到 /api/user/current 路由，获取当前用户信息
  return myAxios.request({
    url: "/api/user/current",
    method: "GET",
  });
};

// 获取用户列表
export const searchUsers = async (username) => {
  // 发起 GET 请求到 /api/user/search 路由，根据用户名搜索用户
  return myAxios.request({
    url: "/api/user/search",
    method: "GET",
    params: {
      username,
    },
  });
};

// 删除用户
export const deleteUser = async (id) => {
  // 发起 POST 请求到 /api/user/delete/:id 路由，传递用户 ID 进行删除
  return myAxios.request({
    url: `/api/user/delete/${id}`,
    method: "POST",
    data: id,
  });
};
