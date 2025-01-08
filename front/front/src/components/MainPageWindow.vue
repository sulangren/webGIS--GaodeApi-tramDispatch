<template>
  <a-carousel autoplay>
    <!-- 第一张图片 -->
    <div>
      <img src="../image/one.jpg" :style="imageStyle" alt="Slide 1" />
    </div>
    <!-- 第二张图片 -->
    <div>
      <img src="../image/tow.jpg" :style="imageStyle" alt="Slide 2" />
    </div>
    <!-- 第三张图片 -->
    <div>
      <img src="../image/three.jpg" :style="imageStyle" alt="Slide 3" />
    </div>
  </a-carousel>
</template>

<script>
import { Carousel } from "ant-design-vue";

export default {
  name: "App",
  components: {
    "a-carousel": Carousel,
  },
  setup() {
    // 图片样式，使用 objectFit: "fill" 以允许图片变形来填充容器
    const imageStyle = {
      width: "100%", // 图片宽度100%
      height: "90%", // 图片高度100%，使其填充容器
      objectFit: "fill", // 允许图片发生变形，完全填充容器
    };

    return {
      imageStyle,
    };
  },
};
</script>

<style scoped>
/* 设置 carousel 容器的宽度和高度 */
.a-carousel {
  width: 100%; /* 设置宽度为父容器的100% */
  height: 300px; /* 设置固定高度为300px，你可以根据需求调整 */
}
</style>
