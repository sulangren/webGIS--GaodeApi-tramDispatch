<template>
  <div class="map-container">
    <!-- 地图容器 -->
    <div id="container" class="map"></div>

    <!-- 右侧面板容器 -->
    <div class="right-sidebar">
      <Form :model="form" @finish="handleButtonClick">
        <Row :gutter="16">
          <a-form-item label="运输车辆容量" name="vehicleCount" hasFeedback>
            <Input
              v-model:value="form.vehicleCount"
              placeholder="输入大于5的整数"
            />
          </a-form-item>
        </Row>
        <Row>
          <a-form-item>
            <button class="action-button">生成运输方案</button>
          </a-form-item>
        </Row>
      </Form>

      <!-- 表格展示调度数据 -->
      <table class="data-table">
        <thead>
          <tr>
            <th>调度ID</th>
            <th>起始点</th>
            <th>终点</th>
            <th>调度数量</th>
            <th>开始调度</th>
          </tr>
        </thead>
        <tbody>
          <!-- 动态渲染表格数据 -->
          <tr v-for="(row, index) in currentPageData" :key="index">
            <td>{{ row.dispatchId }}</td>
            <td>{{ row.startPoint }}</td>
            <td>{{ row.endPoint }}</td>
            <td>{{ row.scheduleAmount }}</td>
            <td>
              <button
                @click="startDispatch(row.dispatchId)"
                class="start-dispatch-button"
              >
                开始调度
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页控件 -->
      <div class="pagination">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage <= 1"
        >
          上一页
        </button>
        <span>第 {{ currentPage }} 页</span>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
        >
          下一页
        </button>
      </div>
    </div>
    <!-- 小地图容器 -->
    <div
      id="overview-map"
      style="
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 200px;
        height: 150px;
        border: 1px solid #000;
        z-index: 100;
      "
    ></div>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick } from "vue";
import { getRanderingSorted } from "@/api/rendering"; // 假设你的接口方法
import { getCenterPointRegister, topPathRegister } from "@/api/function";
import { Form, Input, Row } from "ant-design-vue";

export default {
  name: "MapWindow",
  components: {
    "a-form-item": Form.Item,
    Form,
    Input,
    Row,
  },

  setup() {
    const map = ref(null);
    const polygons = ref([]); // 存储多边形
    const tableData = ref([]); // 存储表格数据
    const markers = ref([]); // 存储标记
    const navigationData = ref([]); // 存储导航数据
    const one = ref([]);
    let overviewMap = null; // 小地图变量
    let overviewRect = null; // 用于小地图中的框

    // 分页参数
    const currentPage = ref(1); // 当前页
    const pageSize = ref(5); // 每页显示的数量

    // 初始化表单对象
    const form = ref({
      vehicleCount: "", // 表单中的运输车辆容量
    });

    // 加载并初始化地图
    const loadAMapApi = () => {
      window._AMapSecurityConfig = {
        securityJsCode: "", // 替换为你的安全密钥
      };
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src = ""; // 请替换为有效的高德地图API Key
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

      // 加载驾车插件
      AMap.plugin(["AMap.Driving"], () => {
        console.log("Driving plugin loaded successfully");
      });
    };

    // 获取并渲染数据
    onMounted(async () => {
      try {
        const response = await getRanderingSorted();
        if (response.data.code === 0 && Array.isArray(response.data.data)) {
          const formattedPolygons = response.data.data.map((item) => {
            const coordinates = item.coordinates;
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

          polygons.value = formattedPolygons;

          // 延迟添加多边形到地图
          setTimeout(() => {
            addPolygonsToMap(polygons.value);
          }, 500);

          // 初始化鹰眼图
          nextTick(() => {
            initOverviewMap();
          });
        } else {
          console.error("Invalid data format", response.data);
        }
      } catch (error) {
        console.error("Error fetching polygons:", error);
      }
    });

    // 初始化小地图（鹰眼图）
    const initOverviewMap = () => {
      overviewMap = new AMap.Map("overview-map", {
        zoom: 13.5, // 设置鹰眼图缩放级别
        center: map.value.getCenter(), // 设置小地图中心点为大地图中心
        viewMode: "2D", // 小地图模式
        zooms: [3, 15], // 小地图缩放级别
      });

      // 小地图上的框，用于显示大地图的显示区域
      overviewRect = new AMap.Rectangle({
        bounds: map.value.getBounds(),
        strokeColor: "#F00",
        strokeWeight: 2,
        fillOpacity: 0.3,
        fillColor: "#FF0",
      });
      overviewMap.add(overviewRect);

      // 监听大地图的移动事件，更新小地图视图
      map.value.on("move", () => {
        const center = map.value.getCenter();
        overviewMap.setCenter(center); // 更新小地图中心
        updateOverviewRect(); // 更新小地图的显示框
      });

      // 监听大地图的缩放事件，更新小地图的框
      map.value.on("zoomend", () => {
        updateOverviewRect(); // 更新显示框
      });

      // 监听鼠标的移动事件
      map.value.on("mousemove", () => {
        updateOverviewRect(); // 鼠标移动时，更新小地图框
      });
    };

    // 更新小地图上的显示框
    const updateOverviewRect = () => {
      const bounds = map.value.getBounds();
      overviewRect.setBounds(bounds); // 设置小地图上的框为大地图当前显示区域
    };

    const centerPointRegisters = async () => {
      try {
        const response = await getCenterPointRegister();
        if (response.data.code === 0 && Array.isArray(response.data.data)) {
          const bicycles = response.data.data;
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
          if (polygon instanceof AMap.Polygon) {
            map.value.add(polygon);
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
          const { id, polygon_center } = bicycle;
          const marker = new AMap.Marker({
            position: new AMap.LngLat(polygon_center[0], polygon_center[1]), // 设置点的坐标
            title: `Bicycle ID: ${id}`, // 设置点的标题为 ID
          });
          markers.value.push(marker); // 将每个点标记保存到 markers 数组
          map.value.add(marker); // 添加标记到地图
        });
      }
    };

    const handleButtonClick = async () => {
      try {
        const response = await topPathRegister({
          capacity: form.value.vehicleCount, // 从表单获取车辆容量
        });

        console.log("API Response:", response.data); // 打印返回的数据

        // 检查 response.data.data 是否是数组
        if (response.data && Array.isArray(response.data.data)) {
          const allData = response.data.data;

          // 更新表格数据
          tableData.value = allData.map((item) => ({
            dispatchId: item.dispatch_count, // 调度数量
            startPoint: item.from, // 起始点
            endPoint: item.to, // 终点
            scheduleAmount: item.transfer_amount, // 调度数量
          }));

          // 更新导航数据
          navigationData.value = allData.map((item) => ({
            dispatchId: item.dispatch_count,
            startCoords: item.fromPoint, // 起始点坐标
            endCoords: item.toPoint, // 终止点坐标
          }));
        } else {
          console.error("response.data.data is not an array:", response.data);
        }
      } catch (error) {
        console.error("Error fetching schedule data:", error);
      }
    };

    // 开始调度
    const startDispatch = async (dispatchId) => {
      try {
        console.log("dispatchId:", dispatchId);
        console.log("navigationData.value:", navigationData.value); // 打印导航数据

        // 清除上一次的路线和标记
        clearLastRoute();

        // 找到对应的导航数据
        const navigation = navigationData.value.find(
          (item) => item.dispatchId === dispatchId
        );

        if (navigation) {
          const { startCoords, endCoords } = navigation;

          // 检查坐标是否有效
          if (!startCoords || !endCoords) {
            console.error("起点或终点坐标无效:", navigation);
            return;
          }

          // 确保坐标为有效的 [longitude, latitude] 数组
          if (
            !Array.isArray(startCoords) ||
            !Array.isArray(endCoords) ||
            startCoords.length !== 2 ||
            endCoords.length !== 2
          ) {
            console.error("坐标数据无效:", navigation);
            return;
          }

          const startLngLat = new AMap.LngLat(startCoords[0], startCoords[1]);
          const endLngLat = new AMap.LngLat(endCoords[0], endCoords[1]);

          // 确保高德地图插件已加载
          if (window.AMap && window.AMap.Driving) {
            const driving = new AMap.Driving({
              map: map.value, // 地图对象
              panel: null, // 可以设置为显示信息的面板
              policy: AMap.DrivingPolicy.LEAST_TIME, // 选择最短时间路线
            });

            // 设置起点和终点
            driving.search(startLngLat, endLngLat, (status, result) => {
              if (status === "complete") {
                console.log("导航成功:", result);
                one.value.push(driving);
                console.log(one.value);
              } else {
                console.error("导航失败:", result);
              }
            });
          } else {
            console.error("AMap.Driving 插件未加载.");
          }
        } else {
          console.error("未找到对应的导航数据:", dispatchId);
        }
      } catch (error) {
        console.error("调度启动失败", error);
      }
    };

    // 分页：计算当前页的数据
    const currentPageData = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = currentPage.value * pageSize.value;
      return tableData.value.slice(start, end);
    });

    // 计算总页数
    const totalPages = computed(() => {
      return Math.ceil(tableData.value.length / pageSize.value);
    });

    // 改变页面
    const changePage = (newPage) => {
      if (newPage >= 1 && newPage <= totalPages.value) {
        currentPage.value = newPage;
      }
    };

    // 清除上一次的导航路径和标记
    function clearLastRoute() {
      if (Array.isArray(one.value) && one.value.length > 0) {
        one.value.forEach((driving) => {
          if (driving && map.value) {
            driving.clear(); // 清理路线
            console.log("Cleared route:", driving);
          }
        });
      }
      one.value = []; // 清理完毕后再重置
    }

    // 加载并初始化地图 API
    onMounted(() => {
      loadAMapApi();
      centerPointRegisters();
    });

    return {
      map,
      polygons,
      tableData, // 表格数据
      handleButtonClick,
      startDispatch,
      form,
      currentPageData,
      currentPage,
      totalPages,
      changePage,
    };
  },
};
</script>

<style scoped>
html,
body,
#container {
  margin: 0;
  padding: 0;
  height: 100%;
  position: relative; /* 确保父容器是相对定位 */
}

.map-container {
  display: flex;
  width: 100%;
  height: 100%;
  position: relative; /* 将整个地图容器设置为相对定位 */
}

.map {
  flex-grow: 1;
  height: 100%;
}

.right-sidebar {
  width: 450px;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
}

.action-button {
  width: 100%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 10px;
}

.action-button:hover {
  background-color: #45a049;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.data-table th {
  background-color: #f2f2f2;
}

.start-dispatch-button {
  padding: 5px 10px;
  background-color: #008cba;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.start-dispatch-button:hover {
  background-color: #007b9f;
}

/* 分页器样式 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.pagination button {
  padding: 5px 10px;
  margin: 0 10px;
  background-color: #007b9f;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button[disabled] {
  background-color: #d3d3d3;
  cursor: not-allowed;
}

.map-control button {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  color: #000;
}

.map-control button:hover {
  background-color: #f0f0f0;
}

.map-control button.active {
  background-color: #2b8cbe;
  color: #fff;
  border-color: #2b8cbe;
}

#overview-map {
  position: absolute;
  top: 10px;
  right: 10px; /* 保持右上角 */
  width: 200px;
  height: 150px;
  border: 1px solid #000;
  z-index: 100;
}
</style>
