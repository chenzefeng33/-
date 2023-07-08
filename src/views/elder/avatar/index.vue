<template>
  <div class="container">
    <Breadcrumb :items="['menu.elder', 'menu.elder.avatar']" />
    <a-card class="general-card">
        <div :style="{ display: 'flex' }">
          <a-row :gutter="24">
            <a-col :span="24">
              <div style="margin-top: 15px; margin-left: 75%;">
            <a-input-search
                  :placeholder="$t('搜索')"
                  style="width: 240px;"
            />
          </div>
            </a-col>
            <a-col :span="6" style="margin-top: 15px;">
              <a-card>
                <a-result :status="null" :title="$t('新增头像')">
                  <template #icon>
                    <icon-plus style="font-size: 81px" />
                  </template>
                </a-result>
              </a-card>
            </a-col>
            <a-col :span="6" style="margin-top: 15px;">
              <a-card title="姓名" hoverable>
                <template #extra>
                  <a-link>修改</a-link>
                </template>
                <img
                    :style="{ width: '100%', transform: 'translateY(+2px)' } "
                    alt="dessert"
                    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
                  />
              </a-card>
            </a-col>
            <a-col :span="6" style="margin-top: 15px;">
              <a-card title="姓名" hoverable>
                <template #extra>
                  <a-link>修改</a-link>
                </template>
                <img
                    :style="{ width: '100%', transform: 'translateY(+2px)' }"
                    alt="dessert"
                    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
                  />
              </a-card>
            </a-col>
            <a-col :span="6" style="margin-top: 15px;">
              <a-card title="姓名" hoverable>
                <template #extra>
                  <a-link>修改</a-link>
                </template>
                <img
                    :style="{ width: '100%', transform: 'translateY(+2px)' }"
                    alt="dessert"
                    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
                  />
              </a-card>
            </a-col>
            <a-col :span="6" style="margin-top: 15px;">
              <a-card title="姓名" hoverable>
                <template #extra>
                  <a-link>修改</a-link>
                </template>
                <img
                    :style="{ width: '100%', transform: 'translateY(+2px)' } "
                    alt="dessert"
                    src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
                  />
              </a-card>
            </a-col>
          </a-row>
      </div>
    </a-card>
  </div>
</template>

<script lang="ts">
  export default {
    name: 'Card',
  };
</script>

<style scoped lang="less">
  .card-demo {
    margin-left: 24px;
    transition-property: all;
  }
  .card-demo:hover {
    transform: translateY(-4px);
  }
  .container {
    padding: 0 20px 20px 20px;
    :deep(.arco-list-content) {
      overflow-x: hidden;
    }

    :deep(.arco-card-meta-title) {
      font-size: 14px;
    }
  }
</style>
