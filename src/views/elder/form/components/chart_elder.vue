<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      title="年龄统计"
    >
      <div ref="main" style="width: 100%; height: 400px"></div>
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
import useLoading from '../../../../hooks/loading';
import useChartOption from '../../../../hooks/chart-option';
import { ref, onMounted } from "vue";
//  按需引入 echarts
import * as echarts from "echarts";
const main = ref() // 使用ref创建虚拟DOM引用，使用时用main.value
onMounted(
  () => {
    init()
  }
)
function init() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(main.value);
  // 指定图表的配置项和数据
  var option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: '#999'
      }
    }
  },
  toolbox: {
    feature: {
      dataView: { show: true, readOnly: false },
      magicType: { show: true, type: ['line', 'bar'] },
      restore: { show: true },
      saveAsImage: { show: true }
    }
  },
  legend: {
    data: ['男', '女']
  },
  xAxis: [
    {
      type: 'category',
      data: ['60-65', '65-70', '70-75', '75-80', '80-85', '85-90', '90-95','95-100','100-105'],
      axisPointer: {
        type: 'shadow'
      }
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '数量',
      min: 0,
      max: 30,
      interval: 5,
      axisLabel: {
        formatter: '{value} 人'
      }
    }
  ],
  series: [
    {
      name: '男',
      type: 'bar',
      tooltip: {
        valueFormatter: function (value) {
          return value + ' 人';
        }
      },
      data: [
        2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3
      ]
    },
    {
      name: '女',
      type: 'bar',
      tooltip: {
        valueFormatter: function (value) {
          return value + ' 人';
        }
      },
      data: [
        2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3
      ]
    }
  ]
};
  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
}
const { loading } = useLoading(false);

</script>

<style scoped lang="less"></style>
