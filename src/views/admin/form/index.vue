<template>
    <div class="container">
      <Breadcrumb
        :items="[
          'menu.admin',
          'menu.admin.form',
        ]"
      />
      <a-space direction="vertical" :size="16" fill>
        <ContentPublishingSource />
      </a-space>
    </div>
  </template>
  
  <script lang="ts" setup>
    import ContentPublishingSource from './components/content-publishing-source.vue';
  </script>
  
  <script lang="ts">
    export default {
      name: 'Form-admin',
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
  