<template>
  <div id="container" style="width: 100%; height: 100%">
    <!-- 提示区域 -->
    <div class="warning-tips">
      <div class="tip">
        <span class="color-box" style="background-color: #ffff33"></span>
        <span class="tip-text">警戒区域</span>
      </div>
      <div class="tip">
        <span class="color-box" style="background-color: #ff4500"></span>
        <span class="tip-text">危险区域</span>
      </div>
    </div>

    <div class="button-container">
      <Button type="primary" @click="showDrawer"> 火灾预警 </Button>

      <!-- 使用 v-model 来控制 Drawer 的显示和隐藏 -->
      <Drawer
        title="火灾预警界面"
        :width="400"
        v-model:visible="open"
        @close="onClose"
        :style="{ zIndex: 999 }"
      >
        <Form :model="form" @finish="buffer">
          <Row :gutter="16">
            <a-form-item label="火灾车辆编号" name="vehicleCount" hasFeedback>
              <Input v-model:value="form.vehicleCount" placeholder="电车编号" />
            </a-form-item>
          </Row>
          <Row>
            <a-form-item>
              <button>生成缓冲区预警</button>
            </a-form-item>
          </Row>
        </Form>
      </Drawer>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { getRanderingSorted, getPointSorted } from "@/api/rendering";
import { functionAuthStore } from "@/storage/functionStorage";
import { Button, Drawer, Form, Input, Row, message } from "ant-design-vue";

export default {
  name: "MapWindow",
  components: {
    Button,
    Drawer,
    Form,
    Input,
    Row,
    "a-form-item": Form.Item,
  },
  setup() {
    const map = ref(null);
    const polygons = ref([]);
    const open = ref(false); // 控制 Drawer 显示与否
    const markers = ref([]);

    const bufferMarkers = ref([]); // 用来存储红色点的标记
    const circles = ref([]); // 用来存储所有的圆

    const authStore = functionAuthStore();

    // 初始化表单对象
    const form = ref({
      vehicleCount: "", // 火灾车辆
    });

    const showDrawer = () => {
      open.value = true; // 打开 Drawer
    };

    const onClose = () => {
      open.value = false; // 关闭 Drawer
    };

    // 提交表单时的操作
    const onSubmit = (values) => {
      console.log("Form Submitted:", values);
    };

    // 加载并初始化地图
    const loadAMapApi = () => {
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src = "";
      document.head.appendChild(script);

      script.onload = () => {
        initMap();
      };
    };

    const initMap = () => {
      const layer = new AMap.createDefaultLayer({
        zooms: [3, 20],
        visible: true,
        opacity: 1,
        zIndex: 0,
      });

      map.value = new AMap.Map("container", {
        viewMode: "2D",
        zoom: 16.3,
        center: [],
        layer: [layer],
      });
    };

    // 获取并渲染数据
    onMounted(async () => {
      try {
        const response = await getRanderingSorted();
        console.log("Response:", response.data);

        if (response.data.code === 0 && Array.isArray(response.data.data)) {
          const formattedPolygons = response.data.data.map((item) => {
            const coordinates = item.coordinates;
            // 创建 AMap.Polygon 实例时，确保它没有被响应式包裹
            const polygon = new AMap.Polygon({
              path: coordinates,
              fillColor: "#ccebc5",
              strokeOpacity: 1,
              fillOpacity: 0.5,
              strokeColor: "#2b8cbe",
              strokeWeight: 1,
              strokeStyle: "dashed",
              strokeDasharray: [5, 5],
            });

            return polygon;
          });

          polygons.value = formattedPolygons; // 更新 polygons

          // 延迟添加多边形到地图
          setTimeout(() => {
            addPolygonsToMap(polygons.value);
          }, 500);
        } else {
          console.error("Invalid data format", response.data);
        }
      } catch (error) {
        console.error("Error fetching polygons:", error);
      }
    });

    // 获取并渲染自行车点数据
    const fetchBicyclePoints = async () => {
      try {
        const response = await getPointSorted();
        // console.log("Bicycles Response:", response.data);

        if (response.data.code === 0 && Array.isArray(response.data.data)) {
          const bicycles = response.data.data;
          console.log(bicycles);
          // 延迟添加点到地图
          setTimeout(() => {
            addMarkersToMap(bicycles);
          }, 500);
        } else {
          console.error("Invalid bicycle data format", response.data);
        }
      } catch (error) {
        console.error("Error fetching bicycles:", error);
      }
    };

    // 将多边形添加到地图
    const addPolygonsToMap = (polygons) => {
      if (Array.isArray(polygons)) {
        polygons.forEach((polygon) => {
          // 确保每个 polygon 是 AMap.Polygon 实例
          if (polygon instanceof AMap.Polygon) {
            map.value.add(polygon); // 添加有效的 AMap.Polygon 实例到地图
          } else {
            console.error("Invalid polygon item", polygon);
          }
        });
      } else {
        console.error("Polygons is not an array:", polygons);
      }
    };

    // 将自行车点添加到地图
    const addMarkersToMap = (bicycles) => {
      if (Array.isArray(bicycles)) {
        bicycles.forEach((bicycle) => {
          const { id, coordinates } = bicycle;
          const marker = new AMap.Marker({
            position: new AMap.LngLat(coordinates[0], coordinates[1]), // 设置点的坐标
            title: `Bicycle ID: ${id}`, // 设置点的标题为 ID
          });
          markers.value.push(marker); // 将每个点标记保存到 markers 数组
          map.value.add(marker); // 添加标记到地图
        });
      }
    };

    // 加载并初始化地图 API
    onMounted(() => {
      loadAMapApi();
      fetchBicyclePoints(); // 获取并渲染自行车点数据
    });

    const buffer = async () => {
      try {
        const response = await authStore.bufferRegisters({
          id: form.value.vehicleCount,
        });

        if (response.code === 0 && Array.isArray(response.data)) {
          const bicycles = response.data;
          console.log(bicycles);

          // 先删除之前的红色点
          deletePreviousBufferMarkers();
          // 先删除之前的圆
          deletePreviousCircles();

          // 延迟添加新点到地图
          setTimeout(() => {
            addBufferMarkersPointToMap(bicycles); // 添加新的红色点
            console.log("添加成功");
          }, 500);

          console.log(form.value.vehicleCount);
          // 查找与 form.vehicleCount 匹配的自行车点
          const bicycle = bicycles.find(
            (bike) => bike.id === Number(form.value.vehicleCount)
          );
          console.log(bicycle);

          if (bicycle) {
            const { coordinates } = bicycle;
            console.log("Selected Bicycle:", bicycle);

            // 绘制缓冲区圆（50米和100米）
            drawHundredBufferCircles(coordinates, 100); // 绘制100米圆
            drawFiftyBufferCircles(coordinates, 50); // 绘制50米圆
          }
          open.value = false; // 关闭 Drawer
        } else {
          // 后端返回无记录时弹出提示
          message.info("电车编号无效");
        }
      } catch (error) {
        console.error("Error fetching bicycles:", error);
      }
    };

    // 删除之前的红色点
    const deletePreviousBufferMarkers = () => {
      // 清空 markers 数组中存储的所有红色点标记
      bufferMarkers.value.forEach((marker) => {
        map.value.remove(marker); // 从地图上移除标记
      });

      // 清空 bufferMarkers 数组
      bufferMarkers.value = [];
    };

    // 将新的红色点标记添加到地图
    const addBufferMarkersPointToMap = (bicycles) => {
      if (Array.isArray(bicycles)) {
        bicycles.forEach((bicycle) => {
          const { id, coordinates } = bicycle;

          // 创建新的标记
          const marker = new AMap.Marker({
            position: new AMap.LngLat(coordinates[0], coordinates[1]), // 设置点的坐标
            title: `Bicycle ID: ${id}_buffer`, // 设置点的标题为 ID
            offset: new AMap.Pixel(-9.5, -31.8), //偏移量
            icon: "https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png", // 设置图标
          });

          // 将新的红色点标记保存到 bufferMarkers 数组
          bufferMarkers.value.push(marker);

          // 将新标记添加到地图
          map.value.add(marker);
        });
      }
    };

    const drawFiftyBufferCircles = (center, radius) => {
      const circle = new AMap.Circle({
        center: new AMap.LngLat(center[0], center[1]), // 圆心位置
        radius: radius, // 圆的半径（单位：米）
        strokeColor: "#F00", // 边框颜色
        strokeOpacity: 1, // 边框透明度
        strokeWeight: 2, // 边框宽度
        fillColor: "#FF4500", // 填充颜色
        fillOpacity: 0.5, // 填充透明度
      });

      circles.value.push(circle); // 将圆添加到数组中
      map.value.add(circle); // 将圆添加到地图中
    };

    const drawHundredBufferCircles = (center, radius) => {
      const circle = new AMap.Circle({
        center: new AMap.LngLat(center[0], center[1]), // 圆心位置
        radius: radius, // 圆的半径（单位：米）
        strokeColor: "#F00", // 边框颜色
        strokeOpacity: 1, // 边框透明度
        strokeWeight: 2, // 边框宽度
        strokeStyle: "dashed", //线样式
        fillColor: "#FFFF33", // 填充颜色
        fillOpacity: 0.3, // 填充透明度
      });

      circles.value.push(circle); // 将圆添加到数组中
      map.value.add(circle); // 将圆添加到地图中
    };

    // 删除之前绘制的所有圆
    const deletePreviousCircles = () => {
      // 清空 circles 数组中存储的所有圆
      circles.value.forEach((circle) => {
        map.value.remove(circle); // 从地图上移除圆
      });

      // 清空 circles 数组
      circles.value = [];
    };

    return {
      map,
      polygons,
      onClose,
      showDrawer,
      open, // 需要返回给模板以便使用
      form,
      onSubmit,
      buffer,
    };
  },
};
</script>

<style>
html,
body,
#container {
  width: 100%;
  height: 100%;
}

/* 提示区域样式 */
.warning-tips {
  position: absolute;
  bottom: 40px; /* 距离底部 10px */
  left: 40px; /* 距离左边 10px */
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.7); /* 背景半透明 */
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.tip {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.color-box {
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border-radius: 50%; /* 圆形颜色框 */
}

.tip-text {
  font-size: 14px;
  color: #333;
}

/* 按钮容器的样式 */
.button-container {
  position: absolute;
  top: 50px; /* 按钮距离顶部 50px */
  right: 70px; /* 按钮距离右边 70px */
  z-index: 99; /* 确保按钮位于地图的顶部 */
}

/* 确保 Drawer 的 z-index 比 Button 的 z-index 小 */
.ant-drawer {
  z-index: 1000 !important;
}
</style>
