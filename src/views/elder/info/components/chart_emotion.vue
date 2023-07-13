<template>
    <a-spin :loading="loading" style="width: 100%">
      <a-card
        class="general-card"
        title="情绪分析"
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
  title: {
    text: 'Referer of a Website',
    subtext: 'Fake Data',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
  }
  const { loading } = useLoading(false);
  
  </script>
  
  <style scoped lang="less"></style>
  