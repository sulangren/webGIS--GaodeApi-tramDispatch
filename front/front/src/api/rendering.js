//rendering,js
import myAxios from "@/request";

export const getRanderingSorted = async () => {
  return myAxios.request({
    url: "rendering/default/",
    method: "GET",
  });
};

export const getPointSorted = async () => {
  return myAxios.request({
    url: "rendering/point/",
    method: "GET",
  });
};
