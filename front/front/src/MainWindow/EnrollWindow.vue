<template>
  <a-layout class="layout">
    <a-layout-content style="padding: 24px">
      <a-card title="新用户注册" :bordered="false">
        <a-form :model="registerForm" :rules="rules" @finish="logins">
          <a-form-item
            name="username"
            label="新用户名"
            :labelCol="{ span: 24 }"
            :wrapperCol="{ span: 24 }"
            hasFeedback
          >
            <a-input v-model:value="registerForm.username" />
          </a-form-item>
          <a-form-item
            name="password"
            label="密码"
            :labelCol="{ span: 24 }"
            :wrapperCol="{ span: 24 }"
            hasFeedback
          >
            <a-input-password v-model:value="registerForm.password" />
          </a-form-item>
          <a-form-item
            name="confirm"
            label="确认密码"
            :labelCol="{ span: 24 }"
            :wrapperCol="{ span: 24 }"
            hasFeedback
          >
            <a-input-password v-model:value="registerForm.confirm" />
          </a-form-item>
          <a-form-item
            name="employeeKey"
            label="员工密钥（可选）"
            :labelCol="{ span: 24 }"
            :wrapperCol="{ span: 24 }"
          >
            <a-input v-model:value="registerForm.employeeKey" />
          </a-form-item>
          <a-form-item
            name="phone"
            label="手机号（可选）"
            :labelCol="{ span: 24 }"
            :wrapperCol="{ span: 24 }"
          >
            <a-input v-model:value="registerForm.phone" />
          </a-form-item>
          <a-form-item :wrapperCol="{ span: 24, offset: 0 }">
            <a-button type="primary" htmlType="submit">提交注册</a-button>
            <a-button style="margin-left: 8px" @click="handleCancel"
              >取消注册</a-button
            >
          </a-form-item>
        </a-form>
      </a-card>
    </a-layout-content>
  </a-layout>
</template>

<script>
import { reactive } from "vue";
import { useAuthStore } from "@/storage/userStorage";
import { useRouter } from "vue-router";
import {
  Form,
  Input,
  Button,
  Card,
  Layout,
  InputPassword,
  message,
} from "ant-design-vue";

export default {
  components: {
    "a-layout": Layout,
    "a-layout-content": Layout.Content,
    "a-card": Card,
    "a-form-item": Form.Item,
    "a-input": Input,
    "a-input-password": InputPassword,
    "a-button": Button,
  },

  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    // 这里直接在 setup 中使用 reactive
    const registerForm = reactive({
      username: "",
      password: "",
      confirm: "",
      employeeKey: "",
      phone: "",
    });

    const rules = {
      username: [
        {
          required: false,
          message: "请输入正确的用户名",
          trigger: /^\S{4,10}$/,
        },
      ],
      password: [
        {
          required: false,
          message: "请输入正确的密码",
          pattern: /^\S{8,16}$/,
        },
      ],
      confirm: [
        { required: false, message: "请确认密码", trigger: "blur" },
        {
          validator: (_, value) => {
            if (!value || value === registerForm.password) {
              return Promise.resolve();
            }
            return Promise.reject(new Error("两次输入的密码不一致"));
          },
        },
      ],
      employeeKey: [{ required: false }],
      phone: [
        {
          required: false,
          pattern: /^\S{11,11}$/,
          message: "请输入正确的手机号",
        },
      ],
    };

    const logins = async () => {
      console.log("staff_username:", registerForm.username);
      console.log("staff_password:", registerForm.password);
      console.log("staff_phone:", registerForm.phone);
      try {
        await authStore.register({
          staff_username: registerForm.username, // 使用后端需要的字段名
          staff_password: registerForm.password,
          staff_telephone: registerForm.phone || null, // 可选字段
        });
        message.success("注册成功");
        await router.push("/"); // 注册成功后跳转到登录页面
      } catch (error) {
        message.error("注册失败");
      }
    };

    return { registerForm, rules, logins };
  },

  methods: {
    handleCancel() {
      this.$router.push("/");
      this.isModalVisible = false; // 关闭模态框
    },
  },
};
</script>

<style scoped>
.layout {
  height: 100vh;
}
</style>
