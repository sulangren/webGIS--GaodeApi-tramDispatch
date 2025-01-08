<template>
  <div id="container" style="width: 100%; height: 100%">
    <!-- 地图容器 -->
    <div id="map-container"></div>

    <!-- 左上角的图层切换按钮 -->
    <div class="map-control">
      <a-dropdown
        :visible="isDropdownVisible"
        @visibleChange="toggleDropdown"
        trigger="click"
      >
        <!-- 触发按钮 -->
        <a-button type="primary" shape="round" @click="toggleDropdown">
          图层切换
        </a-button>

        <!-- 下拉菜单 -->
        <template #overlay>
          <a-menu>
            <a-menu-item key="vector" @click="switchToVector">
              <span :class="{ active: currentLayer === 'vector' }"
                >矢量地图</span
              >
            </a-menu-item>
            <a-menu-item key="satellite" @click="switchToSatellite">
              <span :class="{ active: currentLayer === 'satellite' }"
                >卫星地图</span
              >
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>

      <a-dropdown
        :visible="operationDropdownVisible"
        @visibleChange="handleOperationDropdown"
        trigger="click"
      >
        <!-- 触发按钮 -->
        <a-button type="primary" shape="round" @click="handleOperationDropdown">
          距离测量
        </a-button>

        <!-- 下拉菜单 -->
        <template #overlay>
          <a-menu>
            <a-menu-item key="drawLine" @click="startDrawing">
              <span>画线</span>
            </a-menu-item>
            <a-menu-item key="measureDistance" @click="calculateDistance">
              <span>测距</span>
            </a-menu-item>
            <a-menu-item key="clearLine" @click="clearDrawing">
              <span>清除线</span>
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
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

  <a-modal
    v-model:visible="isModalVisible"
    title="距离信息"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <p>{{ distanceInfo }}</p>
  </a-modal>
</template>

<script>
import { ref, onMounted, nextTick } from "vue";
import { getRanderingSorted, getPointSorted } from "@/api/rendering";

export default {
  name: "MapWindow",
  setup() {
    const map = ref(null);
    const polygons = ref([]); // 存储多边形对象
    const markers = ref([]); // 存储标记点对象
    const currentLayer = ref("vector"); // 当前图层（矢量或卫星）
    const isDropdownVisible = ref(false); // 下拉菜单是否显示
    const operationDropdownVisible = ref(false); // 操作下拉菜单是否显示
    let vectorLayer = null;
    let satelliteLayer = null;
    let overviewMap = null; // 小地图变量
    let overviewRect = null; // 用于小地图中的框
    let rangingTool = null; // 定义测距工具变量

    let polyline = null; // 声明画线对象
    const linePath = ref([]); // 画线的路径
    const drawingMode = ref(false); // 是否开启画线模式

    const isModalVisible = ref(false); // 控制Modal显示
    const distanceInfo = ref(""); // 存储距离信息

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
      if (!AMap) {
        console.error("AMap is not defined!");
        return;
      }

      // 初始化图层
      vectorLayer = new AMap.createDefaultLayer({
        zooms: [3, 20],
        visible: true,
        opacity: 1,
        zIndex: 0,
      }); // 矢量图层
      satelliteLayer = new AMap.TileLayer.Satellite(); // 卫星图层

      // 初始化地图
      map.value = new AMap.Map("container", {
        viewMode: "2D",
        zoom: 16.3,
        center: [113.266949, 35.188365], // 地图中心
        layers: [vectorLayer], // 默认加载矢量图层
      });

      // 加载工具条控件
      AMap.plugin(["AMap.ToolBar"], () => {
        const toolBarControl = new AMap.ToolBar();
        map.value.addControl(toolBarControl);
      });

      // 加载测距工具插件
      AMap.plugin("AMap.RangingTool", () => {
        rangingTool = new AMap.RangingTool(map.value); // 初始化测距工具
        rangingTool.on("end", (event) => {
          console.log("测距结束:", event);
        });

        // 点击右键时，停止测距工具
        map.value.on("rightclick", () => {
          rangingTool.turnOff(); // 关闭测距工具
        });
      });

      // 获取并渲染多边形和标记点数据
      fetchPolygons();
      fetchBicyclePoints();

      // 初始化鹰眼图
      nextTick(() => {
        initOverviewMap();
      });

      // 监听地图点击事件以绘制路径
      map.value.on("click", (e) => {
        if (!drawingMode.value) return;

        const { lng, lat } = e.lnglat;
        linePath.value.push([lng, lat]);
        console.log("添加点到路径:", [lng, lat]);

        if (polyline) {
          polyline.setPath(linePath.value);
        } else {
          polyline = new AMap.Polyline({
            path: linePath.value,
            strokeColor: "#FF0000",
            strokeWeight: 3,
          });
          map.value.add(polyline);
        }
      });

      map.value.on("dblclick", () => {
        console.log(
          "Double click event triggered, drawingMode:",
          drawingMode.value
        );
        if (drawingMode.value) {
          drawingMode.value = false;
          console.log("Ending drawing mode");
        } else {
          console.log("Drawing mode is already false");
        }
      });
    };

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

    // 控制下拉菜单的显示状态
    const toggleDropdown = (visible) => {
      isDropdownVisible.value =
        visible !== undefined ? visible : !isDropdownVisible.value;
    };

    const handleOperationDropdown = (visible) => {
      operationDropdownVisible.value =
        visible !== undefined ? visible : !operationDropdownVisible.value;
    };

    // 图层切换逻辑
    const switchToVector = () => {
      if (currentLayer.value !== "vector") {
        map.value.setLayers([vectorLayer]);
        currentLayer.value = "vector";
      }
    };

    const switchToSatellite = () => {
      if (currentLayer.value !== "satellite") {
        map.value.setLayers([satelliteLayer]);
        currentLayer.value = "satellite";
      }
    };

    // 获取并渲染多边形数据
    const fetchPolygons = async () => {
      try {
        const response = await getRanderingSorted();
        console.log("Polygons Response:", response.data);

        if (response.data.code === 0 && Array.isArray(response.data.data)) {
          const formattedPolygons = response.data.data.map((item) => {
            const coordinates = item.coordinates;
            console.log(coordinates);
            const polygon = new AMap.Polygon({
              path: coordinates,
              fillColor: "#efebe2",
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
        } else {
          console.error("Invalid polygon data format", response.data);
        }
      } catch (error) {
        console.error("Error fetching polygons:", error);
      }
    };

    // 获取并渲染自行车点数据
    const fetchBicyclePoints = async () => {
      try {
        const response = await getPointSorted();
        console.log("Bicycles Response:", response.data);

        if (response.data.code === 0 && Array.isArray(response.data.data)) {
          const bicycles = response.data.data;

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
      polygons.forEach((polygon) => map.value.add(polygon));
    };

    // 将自行车点添加到地图
    const addMarkersToMap = (bicycles) => {
      bicycles.forEach((bicycle) => {
        const { id, coordinates } = bicycle;
        const marker = new AMap.Marker({
          position: new AMap.LngLat(coordinates[0], coordinates[1]),
          title: `Bicycle ID: ${id}`,
        });
        markers.value.push(marker);
        map.value.add(marker);
      });
    };

    // 功能按钮逻辑
    const resetView = () => {
      map.value.setZoomAndCenter(16.3, [113.266949, 35.188365]);
    };

    const clearPolygons = () => {
      polygons.value.forEach((polygon) => map.value.remove(polygon));
      polygons.value = [];
    };

    const clearMarkers = () => {
      markers.value.forEach((marker) => map.value.remove(marker));
      markers.value = [];
    };

    // 开始画线
    const startDrawing = () => {
      console.log("开始画线被点击");
      drawingMode.value = true;
      linePath.value = []; // 清空之前的路径
      if (polyline) {
        map.value.remove(polyline);
        polyline = null;
      }
      console.log("开始画线");
    };

    // 计算路径长度
    const calculateDistance = () => {
      if (linePath.value.length < 2) {
        console.log("路径点不足，无法计算距离");
        return;
      }
      const totalLength = AMap.GeometryUtil.distanceOfLine(linePath.value);
      distanceInfo.value = `路径总长度：${totalLength.toFixed(2)} 米`; // 设置距离信息
      isModalVisible.value = true; // 显示Modal
    };

    const handleOk = () => {
      isModalVisible.value = false;
    };

    const handleCancel = () => {
      isModalVisible.value = false;
    };

    const clearDrawing = () => {
      if (polyline) {
        polyline.setMap(null); // 从地图中移除线
        polyline = null; // 清空对象
        linePath.value = []; // 清空路径
        console.log("已清除画线");
      }
    };

    // 初始化时加载地图
    onMounted(() => {
      loadAMapApi();
    });

    return {
      currentLayer,
      switchToVector,
      switchToSatellite,
      resetView,
      clearPolygons,
      clearMarkers,
      toggleDropdown,
      map,
      isDropdownVisible,
      handleOperationDropdown,
      startDrawing,
      calculateDistance,
      isModalVisible,
      distanceInfo,
      handleOk,
      handleCancel,
      clearDrawing,
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

.map-control {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 5px;
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

.map-functions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.map-functions button {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.map-functions button:hover {
  background-color: #f0f0f0;
}

.map-control-container {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1000;
  width: 160px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  font-family: Arial, sans-serif;
  overflow: hidden;
}

.map-control-header {
  background: #2b8cbe;
  color: #fff;
  padding: 8px;
  text-align: center;
  font-weight: bold;
  border-bottom: 1px solid #ccc;
}

.map-control-buttons {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 8px;
}

.map-control-buttons button {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s, color 0.3s;
}

.map-control-buttons button:hover {
  background-color: #f0f0f0;
}

.map-control-buttons button.active {
  background-color: #2b8cbe;
  color: #fff;
  border-color: #2b8cbe;
}

#overview-map {
  position: absolute;
  top: 10px;
  left: 10px; /* 放在左上角 */
  width: 200px;
  height: 150px;
  border: 1px solid #000;
  z-index: 100;
}
</style>
