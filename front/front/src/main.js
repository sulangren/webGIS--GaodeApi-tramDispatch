import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import Antd from "../node_modules/ant-design-vue";
import "../node_modules/ant-design-vue/es/style/index.css";
import router from "./router"; // 引入路由配置
import "../node_modules/ant-design-vue/dist/antd.css";

// 使用createApp创建Vue应用实例
const pinia = createPinia();
const app = createApp(App);

// 使用app.use安装Ant Design Vue插件
app.use(Antd);
app.use(router);
app.use(pinia);

// 挂载应用实例
app.mount("#app");
