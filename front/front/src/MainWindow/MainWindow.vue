<template>
  <a-layout class="layout">
    <a-layout-header class="header-one">
      <a-row align="middle" justify="space-between" class="header-one-layout">
        <a-col :span="4">
          <img src="../image/logo.png" class="header-one-image" />
        </a-col>
        <a-col :span="16">
          <div class="logo-text">GIS校园共享单车调度系统</div>
        </a-col>
        <a-col :span="2">
          <div>
            <!-- 显示用户名或登录按钮 -->
            <div
              v-if="
                authStore.user.username && authStore.user.username !== '未登录'
              "
              class="a-button-div"
            >
              {{ authStore.user.username }}
            </div>
            <div v-else>
              <a-button class="a-button-logIn" @click="isModalVisible = true"
                >注册/登入</a-button
              >
            </div>
          </div>
        </a-col>
        <a-col :span="2">
          <a-button class="a-button-help">关于我们</a-button>
        </a-col>
      </a-row>
    </a-layout-header>

    <a-layout-header class="header-tow">
      <a-row align="middle" justify="space-between" class="header-one-layout">
        <a-col :span="24" class="header-tow-button">
          <a-button
            key="1"
            @click="setActiveTab(1)"
            class="a-button-Map"
            :class="{ 'active-tab': activeTab === 1 }"
          >
            首页
          </a-button>
          <a-button
            key="2"
            @click="setActiveTab(2)"
            class="a-button-Data"
            :class="{ 'active-tab': activeTab === 2 }"
          >
            车辆情况统计
          </a-button>
          <a-button
            key="3"
            @click="setActiveTab(3)"
            class="a-button-user"
            :class="{ 'active-tab': activeTab === 3 }"
          >
            车辆位置总览
          </a-button>
          <a-button
            key="4"
            @click="setActiveTab(4)"
            class="a-button-user"
            :class="{ 'active-tab': activeTab === 4 }"
          >
            车辆位置调度系统
          </a-button>
          <a-button
            key="5"
            @click="setActiveTab(5)"
            class="a-button-user"
            :class="{ 'active-tab': activeTab === 5 }"
          >
            火灾预警
          </a-button>
        </a-col>
      </a-row>
    </a-layout-header>

    <a-layout-content class="content">
      <router-view></router-view>
    </a-layout-content>
  </a-layout>

  <!-- 登录/注册模态框 -->
  <a-modal v-model:visible="isModalVisible" title="注册" :footer="null">
    <a-layout-content>
      <a-form
        :model="form"
        :rules="rules"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 16 }"
        style="max-width: 600px"
        @finish="logins"
        @finish-failed="onFinishFailed"
      >
        <a-form-item label="用户名" name="username" hasFeedback>
          <a-input v-model:value="form.username" />
        </a-form-item>

        <a-form-item label="密码" name="password" hasFeedback>
          <a-input-password v-model:value="form.password" />
        </a-form-item>

        <a-layout-Footer class="a-modal-button-tow">
          <a-form-item>
            <a-button
              class="a-model-button-logIn"
              type="primary"
              html-type="submit"
              >登入</a-button
            >
          </a-form-item>
        </a-layout-Footer>
        <a-layout-Footer class="a-modal-button-one">
          <a-button class="a-model-button-enroll" @click="goToRegisterPage"
            >点我注册</a-button
          >
        </a-layout-Footer>
      </a-form>
    </a-layout-content>
  </a-modal>
</template>

<script>
import { reactive, nextTick, ref } from "vue"; // 引入ref和reactive
import { useRouter } from "vue-router";
import { useAuthStore } from "@/storage/userStorage";
import {
  Layout,
  Button,
  Modal,
  Form,
  Input,
  InputPassword,
  message,
} from "ant-design-vue";

export default {
  components: {
    "a-layout": Layout,
    "a-layout-header": Layout.Header,
    "a-layout-content": Layout.Content,
    // "a-layout-footer": Layout.Footer,
    "a-row": Layout.Row,
    "a-col": Layout.Col,
    "a-button": Button,
    "a-modal": Modal,
    "a-form-item": Form.Item,
    "a-input": Input,
    "a-input-password": InputPassword,
  },

  setup() {
    // 获取路由和用户认证 store
    const router = useRouter();
    const authStore = useAuthStore();

    // 定义响应式数据
    const activeTab = ref(null); // 当前选中的 tab，初始为 null
    const isModalVisible = ref(false); // 控制模态框显示与隐藏

    // 表单数据和验证规则
    const form = reactive({
      username: "",
      password: "",
    });

    const rules = {
      username: [
        {
          required: true,
        },
        { min: 4, max: 10, message: "请输入正确的用户名", trigger: "blur" },
      ],
      password: [
        {
          required: true,
        },
        { min: 8, max: 16, message: "请输入正确的密码", trigger: "blur" },
      ],
    };

    // 登录方法
    const logins = async () => {
      try {
        const data = await authStore.login({
          staff_username: form.username,
          staff_password: form.password,
        });
        console.log(data);
        authStore.user.username = data.data;
        authStore.user.token = data.token;
        await nextTick(); // 确保 DOM 更新完成
        // 登录成功后跳转到首页
        message.success("登录成功");
        await router.push({
          path: "/",
          replace: true,
        });
        isModalVisible.value = false; // 关闭模态框
      } catch (error) {
        console.error("Login failed:", error);
        message.error("用户名或密码不正确");
      }
    };

    const goToRegisterPage = () => {
      router.push("/enroll");
      isModalVisible.value = false; // 关闭模态框
    };

    // 设置活动的 tab
    const setActiveTab = (tabIndex) => {
      activeTab.value = tabIndex;

      if (!authStore.user.username || authStore.user.username === "未登录") {
        showMessageAndRedirect(tabIndex);
        activeTab.value = 1;
      } else {
        switch (tabIndex) {
          case 1:
            router.push({ path: "/" });
            break;
          case 2:
            router.push({ path: "/data" });
            break;
          case 3:
            router.push({ path: "/nearby" });
            break;
          case 4:
            router.push({ path: "/location" });
            break;
          case 5:
            router.push({ path: "/warning" });
            break;
          default:
            router.push({ path: "/" });
        }
      }
    };

    // 显示消息并跳转
    const showMessageAndRedirect = () => {
      message.warning("您未登录，请您登入", 2, () => {});
    };

    return {
      activeTab,
      isModalVisible,
      form,
      logins,
      rules,
      goToRegisterPage,
      setActiveTab,
      authStore,
      showMessageAndRedirect,
    };
  },
};
</script>

<style scoped>
.layout {
  height: 100vh;
  background: #f0f2f5;
}

.header-one {
  background: #001529;
  padding: 0 16px;
  height: 50px;
}

.logo-text {
  position: relative;
  font-size: 20px; /* 根据需要调整字体大小 */
  color: #fff; /* 文字颜色 */
  margin-left: 3%; /*根据需要调整左边距*/
  top: -8px;
}

.header-one-image {
  margin-bottom: 18px;
  width: 60px;
  height: 40px;
  float: right;
}

.a-button-logIn {
  position: relative;
  border: none;
  background: #001529;
  color: #fff;
  box-shadow: none; /* 去除阴影 */
  top: -6px;
}

.a-button-div {
  position: relative;
  color: white;
  top: -6px;
}

.a-button-help {
  position: relative;
  border: none;
  background: #001529;
  color: #fff;
  box-shadow: none; /* 去除阴影 */
  top: -6px;
}

.header-one-dropdown {
  margin-left: 16px;
  margin-bottom: 15%;
}

.content {
  padding: 16px;
}

.header-tow {
  background: #ededed;
  padding: 0 16px;
  height: 50px;
}

.header-tow-button {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-tow-button .a-button-Map,
.header-tow-button .a-button-Data,
.header-tow-button .a-button-user {
  margin-left: 10px;
  margin-right: 10px;
  position: relative;
  border: none;
  background: #ededed;
  box-shadow: none; /* 去除阴影 */
}

.active-tab::after {
  content: "";
  display: block;
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: #1890ff;
}

/* 弹窗样式 */
.a-modal-button-one {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  background-color: white; /* 设置背景颜色为白色 */
}
.a-modal-button-tow {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white; /* 设置背景颜色为白色 */
}
.a-model-button-logIn {
  margin-left: 10px;
  margin-right: 10px;
  width: 300px;
}
.a-model-button-enroll {
  margin-left: 10px;
  margin-right: 10px;
  border: none;
  background: #fff;
  box-shadow: none; /* 去除阴影 */
}
</style>
