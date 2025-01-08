// tram.js
import myAxios from "@/request";

export const getTramSorted = async () => {
  return myAxios.request({
    url: "query/list/",
    method: "GET",
  });
};

// 搜索条件
export const searchCriteria = async (queryParam) => {
  return myAxios.request({
    url: "query/query/",
    method: "GET",
    params: queryParam, // 搜索参数，如名称、地址等
  });
};
