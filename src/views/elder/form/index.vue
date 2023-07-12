<template>
  <div class="container">
    <Breadcrumb
      :items="[
        'menu.elder',
        'menu.elder.form',
      ]"
    />
    <a-space direction="vertical" :size="16" fill>
      <Chart />
    </a-space>
  </div>
</template>

<script lang="ts" setup>
  import Chart from './components/chart_elder.vue';
</script>

<script lang="ts">
  export default {
    name: 'Form-elder',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }

  :deep(.section-title) {
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 16px;
  }

  :deep(.chart-wrap) {
    height: 264px;
  }
</style>
