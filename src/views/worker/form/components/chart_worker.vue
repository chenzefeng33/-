<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      title="人员入职\离职对比"
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
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['入职员工', '离职员工']
  },
  toolbox: {
    feature: {
      restore: { show: true },
      saveAsImage: {}
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      boundaryGap: false,
      data: ['一月', '二月', '三月', '四月', '五月', '六月', '七月','八月','九月','十月','十一月','十二月']
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: '入职员工',
      type: 'line',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [120, 132, 101, 134, 90, 230, 210,21,90,45,90,100]
    },
    {
      name: '离职员工',
      type: 'line',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [120, 182, 191, 234, 290, 330, 310,299,30,498,890,90]
    }
  ]
};
  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
}
const { loading } = useLoading(false);

</script>

<style scoped lang="less"></style>
