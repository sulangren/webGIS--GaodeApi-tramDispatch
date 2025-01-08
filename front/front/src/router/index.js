import { createRouter, createWebHistory } from "vue-router";
import MainPage from "@/components/MainPageWindow.vue";
import DataSheet from "@/components/Data_Sheet.vue"; // 假设组件名为 DataSheet
import WarningWindow from "@/components/WarningWindow.vue";
import EnrollWindow from "@/MainWindow/EnrollWindow.vue";
import MainWindow from "@/MainWindow/MainWindow.vue";
import NearbyTramsWindow from "@/components/NearbyTramsWindow.vue";
import LocationWindow from "@/components/LocationWindow.vue";

const routes = [
  {
    path: "", // 根路径不需要重复的 component 配置
    component: MainWindow, // 根路径的组件
    children: [
      { path: "", component: MainPage }, // 子路由的路径应该是相对路径
      { path: "/data", component: DataSheet }, // 确保组件名和文件名一致
      { path: "/warning", component: WarningWindow },
      { path: "/nearby", component: NearbyTramsWindow },
      { path: "/location", component: LocationWindow },
    ],
  },
  { path: "/enroll", component: EnrollWindow }, // 确保路径以斜杠开头
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
