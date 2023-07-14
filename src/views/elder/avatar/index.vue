<template>
  <div class="container">
    <Breadcrumb :items="['menu.elder', 'menu.elder.avatar']" />
    <a-card class="general-card">
      <div :style="{ display: 'flex' }">
        <a-row :gutter="24">
          <!-- <a-col :span="24">
            <div style="margin-top: 15px; margin-left: 95%;">
          <a-input-search
                :placeholder="$t('搜索')"
                style="width: 240px;"
          />
        </div>
          </a-col> -->
          <a-col :span="6" style="margin-top: 25px;">
            <a-card @click="handleAdd" style="height: 220px; width: 223px;">
              <icon-plus style="font-size: 190px " />
              <a-modal v-model:visible="visible" @ok="handleOk" @cancel="handleCancel">
                <template #title>
                  新增头像
                </template>
                <a-form :model="form" :style="{ width: '400px' }" @submit="handleSubmit">
                  <a-form-item field="ID" label="ID">
                    <a-input
                        v-model="input_id"
                        placeholder="请输入ID"
                    />
                  </a-form-item>
                  <a-form-item field="avatar" label="头像">
                    <div style="margin-left: auto; margin-right: auto;">
                      <video ref="videoElement" autoplay></video>
                    </div>
                  </a-form-item>
                  <a-form-item>
                    <a-button @click="takePhoto">拍照</a-button>
                  </a-form-item>
                </a-form>
              </a-modal>
            </a-card>
          </a-col>
          <a-col :span="6" style="margin-top: 25px;" v-for="image in images">
            <a-card title="姓名" hoverable style="height: 220px;">
              <template #extra>
                <a-link>修改</a-link>
              </template>
              <!-- <img
                  :style="{ width: '100%', transform: 'translateY(+2px)' } "
                  alt="dessert"
                  src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a20012a2d4d5b9db43dfc6a01fe508c0.png~tplv-uwbnlip3yd-webp.webp"
                /> -->
              <img :src="image" alt="照片" :style="{ width: '100%', transform: 'translateY(+2px)' } ">
            </a-card>
          </a-col>
        </a-row>
      </div>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, reactive, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';

const videoElement = ref<HTMLVideoElement | null>(null);
let mediaStream: MediaStream | null = null;
const photoDataUrl = ref('');

const visible = ref(false);
const input_id = ref();
const images = reactive([]);
const form = reactive({
  name: '',
  post: '',
  isRead: false,
});
const handleSubmit = () => {
  console.log();
};
const handleAdd = () => {
  visible.value = true;
  startCamera();
};
const handleOk = () => {
  visible.value = false;
  stopCamera();
};
const handleCancel = () => {
  visible.value = false;
  stopCamera();
}


async function startCamera() {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream;
    }
  } catch (error) {
    console.error('启动摄像头失败:', error);
  }
}

function stopCamera() {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
  }
}

function takePhoto() {
  if (videoElement.value) {
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.value.videoWidth;
    canvas.height = videoElement.value.videoHeight;
    canvas.getContext('2d')?.drawImage(videoElement.value, 0, 0);

    // 将画布中的图像转换为数据URL
    const photoDataUrl = canvas.toDataURL('image/jpeg');
    images.push(photoDataUrl);
    console.log(111,photoDataUrl);
    console.log(images);
    // 将photoDataUrl发送给后端接口
    // 你可以使用axios或其他HTTP库发送POST请求
    // 例如：axios.post('/api/upload-photo', { photoUrl: photoDataUrl })
  }
}
</script>

<script lang="ts">
export default {
  name: 'Card',
};

</script>

<style scoped lang="less">
video {
  width: 100%; /* 设置视频宽度为父容器的100% */
  height: auto; /* 让高度自适应宽度的比例 */
}
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
