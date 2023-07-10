<template>
  <a-form
    ref="formRef"
    :model="formData"
    class="form"
    :label-col-props="{ span: 8 }"
    :wrapper-col-props="{ span: 16 }"
  >
    <a-form-item
      field="email"
      :label="$t('邮箱')"
      :rules="[
        {
          required: true,
          message: $t('请输入邮箱'),
        },
      ]"
    >
      <a-input
        v-model="formData.email"
        :placeholder="$t('请输入邮箱')"
      />
    </a-form-item>
    <a-form-item
      field="nickname"
      :label="$t('昵称')"
      :rules="[
        {
          required: true,
          message: $t('请输入昵称'),
        },
      ]"
    >
      <a-input
        v-model="formData.nickname"
        :placeholder="$t('请输入昵称')"
      />
    </a-form-item>
    <a-form-item
      field="countryRegion"
      :label="$t('国家/地区')"
      :rules="[
        {
          required: true,
          message: $t('请选择国家/地区'),
        },
      ]"
    >
      <a-select
        v-model="formData.countryRegion"
        :placeholder="$t('请选择国家/地区')"
      >
        <a-option value="China">中国</a-option>
      </a-select>
    </a-form-item>
    <a-form-item
      field="area"
      :label="$t('所在区域')"
      :rules="[
        {
          required: true,
          message: $t('请选择所在区域'),
        },
      ]"
    >
      <a-cascader
        v-model="formData.area"
        :placeholder="$t('请选择所在区域')"
        :options="[
          {
            label: '北京',
            value: 'beijing',
            children: [
              {
                label: '北京',
                value: 'beijing',
                children: [
                  {
                    label: '朝阳',
                    value: 'chaoyang',
                  },
                ],
              },
            ],
          },
        ]"
        allow-clear
      />
    </a-form-item>
    <a-form-item
      field="address"
      :label="$t('具体地址')"
    >
      <a-input
        v-model="formData.address"
        :placeholder="$t('请输入具体地址')"
      />
    </a-form-item>
    <a-form-item
      field="profile"
      :label="$t('个人简介')"
      :rules="[
        {
          maxLength: 200,
          message: $t('个人简介超过最大长度限制'),
        },
      ]"
      row-class="keep-margin"
    >
      <a-textarea
        v-model="formData.profile"
        :placeholder="$t('请输入个人简介')"
      />
    </a-form-item>
    <a-form-item>
      <a-space>
        <a-button type="primary" @click="validate">
          {{ $t('保存') }}
        </a-button>
        <a-button type="secondary" @click="reset">
          {{ $t('重置') }}
        </a-button>
      </a-space>
    </a-form-item>
  </a-form>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import { FormInstance } from '@arco-design/web-vue/es/form';
  import { BasicInfoModel } from '@/api/user-center';

  const formRef = ref<FormInstance>();
  const formData = ref<BasicInfoModel>({
    email: '',
    nickname: '',
    countryRegion: '',
    area: '',
    address: '',
    profile: '',
  });
  const validate = async () => {
    const res = await formRef.value?.validate();
    if (!res) {
      // do some thing
      // you also can use html-type to submit
    }
  };
  const reset = async () => {
    await formRef.value?.resetFields();
  };
</script>

<style scoped lang="less">
  .form {
    width: 540px;
    margin: 0 auto;
  }
</style>
