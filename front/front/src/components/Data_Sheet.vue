<template>
  <a-card>
    <a-form layout="inline">
      <a-form-item label="选择条件" class="form-item">
        <a-select
          v-model:value="queryParam.selectedOption"
          placeholder="请选择"
          class="form-item-button-one"
        >
          <a-select-option value="normal">正常</a-select-option>
          <a-select-option value="Low_battery">低电量(低于20%)</a-select-option>
          <a-select-option value="maintenance">待维护</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          @click="handleSearch"
          class="form-item-button-tow"
        >
          查询
        </a-button>
      </a-form-item>
    </a-form>
  </a-card>

  <a-table
    :columns="columns"
    :data-source="getPagedData()"
    :row-key="(record) => record.id"
    :pagination="false"
    @change="handleSortChange"
  >
    <template v-slot:bodyCell="{ column, record }">
      <template v-if="column.key === 'name'">
        <a>{{ record.name }}</a>
      </template>
      <template v-else-if="column.key === 'tags'">
        <span>
          <a-tag
            v-for="tag in record.tags"
            :key="tag"
            :color="
              tag === 'loser'
                ? 'volcano'
                : tag.length > 5
                ? 'geekblue'
                : 'green'
            "
          >
            {{ tag.toUpperCase() }}
          </a-tag>
        </span>
      </template>
      <template v-else-if="column.key === 'rate'">
        <a-rate :value="record.rating" disabled allow-half />
      </template>
    </template>
  </a-table>

  <a-layout-footer>
    <a-pagination
      v-model="current"
      :total="totalItems"
      :page-size="pageSize"
      @change="handlePageChange"
      show-less-items
    />
  </a-layout-footer>
</template>

<script>
import { defineComponent, ref, onMounted, watch } from "vue";
import { getTramSorted, searchCriteria } from "@/api/tram";

export default defineComponent({
  setup() {
    // 查询参数
    const queryParam = ref({
      selectedOption: "", // 默认选项为空
    });

    // 表格数据
    const data = ref([]);
    const sortedData = ref([]); // 排序后的数据

    // 分页参数
    const current = ref(1);
    const pageSize = ref(7); // 设置每页数量为7
    const totalItems = ref(0);

    // 获取当前页数据
    const getPagedData = () => {
      const startIndex = (current.value - 1) * pageSize.value;
      const endIndex = startIndex + pageSize.value;
      return sortedData.value.slice(startIndex, endIndex); // 返回当前页数据
    };

    // 处理查询
    const handleSearch = async () => {
      try {
        console.log(queryParam.value); // 打印选中的查询条件
        const response = await searchCriteria(queryParam.value);

        if (response.data.code === 0) {
          // 数据格式化及排序
          const formattedData = response.data.data.map((item) => ({
            ...item,
            tags:
              item.tags && typeof item.tags === "string" // 确保 tags 字段存在且为字符串
                ? item.tags
                    .split(";")
                    .map((tag) => tag.trim())
                    .filter((tag, index, self) => self.indexOf(tag) === index)
                : [], // 如果没有 tags 字段，返回空数组
          }));

          // 按 id 字段升序排序
          sortedData.value = formattedData.sort((a, b) => a.id - b.id);
          totalItems.value = sortedData.value.length;
        } else {
          console.log(response.data.message || "No data found");
        }
      } catch (error) {
        console.error("Error searching data:", error);
      }
    };

    // 默认加载排序后的数据
    onMounted(async () => {
      try {
        const response = await getTramSorted();
        console.log(response.data.data);
        if (response.data.code === 0) {
          const formattedData = response.data.data.map((item) => ({
            ...item,
            tags: item.tags
              ? item.tags
                  .split(";")
                  .map((tag) => tag.trim())
                  .filter((tag, index, self) => self.indexOf(tag) === index)
              : [], // 如果没有 tags 字段，设置为空数组
          }));

          // 按 id 字段升序排序
          sortedData.value = formattedData.sort((a, b) => a.id - b.id);
          totalItems.value = sortedData.value.length;
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    });

    // 监听 selectedOption 变化，调试用
    watch(
      () => queryParam.value.selectedOption,
      (newValue, oldValue) => {
        console.log(`selectedOption changed from ${oldValue} to ${newValue}`);
      }
    );

    // 分页改变时，触发此方法
    const handlePageChange = (page) => {
      current.value = page;
    };

    // 监听排序
    const handleSortChange = (pagination, filters, sorter) => {
      // 根据 sorter 对数据进行排序
      if (sorter.field) {
        sortedData.value.sort((a, b) => {
          if (a[sorter.field] < b[sorter.field])
            return sorter.order === "ascend" ? -1 : 1;
          if (a[sorter.field] > b[sorter.field])
            return sorter.order === "ascend" ? 1 : -1;
          return 0;
        });
      }
    };

    const columns = [
      {
        title: "编号",
        dataIndex: "id",
        key: "id", // 唯一标识
        defaultSortOrder: "ascend", // 默认按升序排列
        sorter: (a, b) => a.id - b.id, // 按 id 字段升序排序
      },
      {
        title: "当前车辆所属停车点",
        dataIndex: "current_location",
        key: "current_location", // 唯一标识
      },
      {
        title: "当前车辆所属状态",
        dataIndex: "status",
        key: "status", // 唯一标识
      },
      {
        title: "当前车辆剩余电量",
        dataIndex: "remaining_battery",
        key: "remaining_battery", // 唯一标识
        defaultSortOrder: "descend",
        sorter: (a, b) => a.remaining_battery - b.remaining_battery,
      },
    ];

    return {
      queryParam,
      data,
      columns,
      current,
      pageSize,
      totalItems,
      handleSearch,
      getPagedData,
      handlePageChange,
      handleSortChange,
    };
  },
});
</script>

<style>
/* 你可以在这里添加样式 */
</style>
