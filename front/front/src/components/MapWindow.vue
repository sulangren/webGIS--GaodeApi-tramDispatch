<template>
  <div id="container" style="width: 100%; height: 100%"></div>
</template>

<script>
export default {
  name: "MapWindow",
  data() {
    return {
      map: null,
      polygon: null,
    };
  },
  mounted() {
    this.loadAMapApi();
  },
  methods: {
    loadAMapApi() {
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src = "";
      document.head.appendChild(script);

      script.onload = () => {
        this.initMap();
      };
    },
    initMap() {
      const layer = new AMap.createDefaultLayer({
        zooms: [3, 20], //可见级别
        visible: true, //是否可见
        opacity: 1, //透明度
        zIndex: 0, //叠加层级
      });
      this.map = new AMap.Map("container", {
        viewMode: "2D", //默认使用 2D 模式
        zoom: 16.3, //地图级别
        center: [], //地图中心点
        layer: [layer],
      });

      const Valid_area = [[[]]];
      this.polygon = new AMap.Polygon({
        path: Valid_area, //多边形路径
        fillColor: "#ccebc5", //多边形填充颜色
        strokeOpacity: 1, //线条透明度
        fillOpacity: 0.5, //填充透明度
        strokeColor: "#2b8cbe", //线条颜色
        strokeWeight: 1, //线条宽度
        strokeStyle: "dashed", //线样式
        strokeDasharray: [5, 5], //轮廓的虚线和间隙的样式
      });
      this.polygon.on("mouseover", () => {
        this.polygon.setOptions({
          fillOpacity: 0.1, //多边形填充透明度
          fillColor: "#7bccc4",
        });
      });
      this.map.add(this.polygon);
    },
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
</style>
