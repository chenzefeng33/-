<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      title="人员统计"
    >
      <Chart style="width: 100%; height: 300px" :option="chartOption" />
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import useLoading from '../../../../hooks/loading';
  import useChartOption from '../../../../hooks/chart-option';

  const { chartOption } = useChartOption((isDark) => {
    const graphicElementStyle = {
      textAlign: 'center',
      fill: isDark ? 'rgba(255,255,255,0.7)' : '#4E5969',
      fontSize: 14,
      lineWidth: 10,
      fontWeight: 'bold',
    };
    return {
      legend: {
        left: 'center',
        data: ['老人', '工作人员', '义工'],
        bottom: 0,
        icon: 'circle',
        itemWidth: 8,
        textStyle: {
          color: isDark ? 'rgba(255,255,255,0.7)' : '#4E5969',
        },
        itemStyle: {
          borderWidth: 0,
        },
      },
      tooltip: {
        show: true,
        trigger: 'item',
      },
      graphic: {
        elements: [
          {
            type: 'text',
            left: 'center',
            top: 'center',
            style: {
              text: '人员统计',
              ...graphicElementStyle,
            },
          }
        ],
      },
      series: [
        {
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '50%'],
          label: {
            formatter: '{d}% ',
            color: isDark ? 'rgba(255, 255, 255, 0.7)' : '#4E5969',
          },
          itemStyle: {
            borderColor: isDark ? '#000' : '#fff',
            borderWidth: 1,
          },
          data: [
            {
              value: [148564],
              name: '老人',
              itemStyle: {
                color: '#249EFF',
              },
            },
            {
              value: [334271],
              name: '工作人员',
              itemStyle: {
                color: '#846BCE',
              },
            },
            {
              value: [445694],
              name: '义工',
              itemStyle: {
                color: '#21CCFF',
              },
            },
          ],
        },
      ],
    };
  });
  const { loading } = useLoading(false);
</script>

<style scoped lang="less"></style>
