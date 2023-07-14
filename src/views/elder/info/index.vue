<template>
  <div class="container">
    <Breadcrumb :items="['menu.elder', 'menu.elder.info']" />
    <a-card class="general-card" :title="$t('查询表格')">
      <a-row>
        <a-col :flex="1">
          <a-form
            :model="formModel"
            :label-col-props="{ span: 6 }"
            :wrapper-col-props="{ span: 18 }"
            label-align="left"
          >
            <a-row :gutter="12">
              <a-col :span="10">
                <a-form-item
                  field="id"
                  :label="$t('身份证号')"
                >
                  <a-input
                    v-model="formModel  .id_card"
                    :placeholder="$t('请输入身份证号')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item field="name" :label="$t('姓名')">
                  <a-input
                    v-model="formModel.username"
                    :placeholder="$t('请输入姓名')"
                  />
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-col>
        <a-divider style="height: 40px" direction="vertical" />
        <a-col :flex="'60px'" style="text-align: right">
          <a-space direction="horizontal" :size="20">
            <a-button type="primary" @click="search">
              <template #icon>
                <icon-search />
              </template>
              {{ $t('搜索') }}
            </a-button>
            <a-button @click="reset">
              <template #icon>
                <icon-refresh />
              </template>
              {{ $t('重置') }}
            </a-button>
          </a-space>
        </a-col>
      </a-row>
      <a-divider style="margin-top: 0" />
      <a-row style="margin-bottom: 16px">
        <a-col :span="12">
          <a-space>
            <a-button type="primary" @click="newMember">
              <template #icon>
                <icon-plus />
              </template>
              {{ $t('新建') }}
            </a-button>
            <a-modal v-model:visible="visible" @ok="handleOk" @cancel="handleCancel">
              <template #title>
                添加
              </template>
              <a-form :model="form" :style="{width:'420px'}">
                <a-form-item field="id" label="身份证号">
                  <a-input v-model="form.id_card" />
                </a-form-item>
                <a-form-item field="name" label="姓名">
                  <a-input v-model="form.username" />
                </a-form-item>
                <a-form-item field="sex" label="性别">
                  <a-select v-model="form.gender">
                    <a-option value="男">男</a-option>
                    <a-option value="女">女</a-option>
                  </a-select>
                </a-form-item>
                <a-form-item field="age" label="电话号码">
                  <a-input v-model="form.phone" />
                </a-form-item>
                <a-form-item field="checkin" label="入院时间">
                  <a-input v-model="form.checkin_date" />
                </a-form-item>
              </a-form>
            </a-modal>
          </a-space>
        </a-col>
        <a-col
          :span="12"
          style="display: flex; align-items: center; justify-content: end"
        >

          <a-tooltip :content="$t('刷新')">
            <div class="action-icon" @click="search"
              ><icon-refresh size="18"
            /></div>
          </a-tooltip>
          <a-dropdown @select="handleSelectDensity">
            <a-tooltip :content="$t('密度')">
              <div class="action-icon"><icon-line-height size="18" /></div>
            </a-tooltip>
            <template #content>
              <a-doption
                v-for="item in densityList"
                :key="item.value"
                :value="item.value"
                :class="{ active: item.value === size }"
              >
                <span>{{ item.name }}</span>
              </a-doption>
            </template>
          </a-dropdown>
          <a-tooltip :content="$t('列设置')">
            <a-popover
              trigger="click"
              position="bl"
              @popup-visible-change="popupVisibleChange"
            >
              <div class="action-icon"><icon-settings size="18" /></div>
              <template #content>
                <div id="tableSetting">
                  <div
                    v-for="(item, index) in showColumns"
                    :key="item.dataIndex"
                    class="setting"
                  >
                    <div style="margin-right: 4px; cursor: move">
                      <icon-drag-arrow />
                    </div>
                    <div>
                      <a-checkbox
                        v-model="item.checked"
                        @change="
                          handleChange($event, item as TableColumnData, index)
                        "
                      >
                      </a-checkbox>
                    </div>
                    <div class="title">
                      {{ item.title === '#' ? '序列号' : item.title }}
                    </div>
                  </div>
                </div>
              </template>
            </a-popover>
          </a-tooltip>
        </a-col>
      </a-row>
      <a-table
        row-key="ID"
        :loading="loading"
        :pagination="pagination"
        :columns="(cloneColumns as TableColumnData[])"
        :data="renderData"
        :bordered="false"
        :size="size"
        @page-change="onPageChange"
      >
      <template #check="{ record }">
          <a-button @click="d_handleClick">查看</a-button>
          <a-drawer :width="600" :visible="d_visible" @ok="d_handleOk" @cancel="d_handleCancel" unmountOnClose>
            <div>
              <Chart/>
              <Line/>
            </div>
          </a-drawer>
        </template>
        <template #index="{ rowIndex }">
          {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
        </template>


      </a-table>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
  import { computed, ref, reactive, watch, nextTick } from 'vue';
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import {queryPolicyList, PolicyRecord, PolicyParams, } from '@/api/list';
  import { Pagination } from '@/types/global';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import cloneDeep from 'lodash/cloneDeep';
  import Sortable from 'sortablejs';
  import axios from "axios";
  import Chart from './components/chart_emotion.vue';
  import Line from './components/chart_action.vue';
  import {getToken} from "@/utils/auth";

  type SizeProps = 'mini' | 'small' | 'medium' | 'large';
  type Column = TableColumnData & { checked?: true };

  const d_visible = ref(false);

  const d_handleClick = () => {
    d_visible.value = true;
  };
  const d_handleOk = () => {
      d_visible.value = false;
    };
    const d_handleCancel = () => {
      d_visible.value = false;
    }

  const newMember = () => {
    visible.value = true;
  };
  const visible = ref(false);
  const form = reactive({
        ID: '',
        id_card: '',
        username: '',
        gender: '',
        phone:'',
        checkin_date: '',

    });
  const handleOk = () => {
    visible.value = false;
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/oldman/add`,
      data: {
        username:form.username,
        id_card:form.id_card,
        gender:form.gender,
        phone:form.phone,
      }
    })
        .then(function (value){
          searchData();
          console.log(value);
          if (value.status === 200){
            console.log("succuss");
          }else{
            console.log("error");
          }
        })
        .catch();
  };
  const handleCancel = () => {
    visible.value = false;
  }

  const generateFormModel = () => {
    return {
      ID: '',
      id_card: '',
      username: '',
      gender: '',
      phone:'',
      checkin_date: '',
    };
  };
  const { loading, setLoading } = useLoading(true);
  const { t } = useI18n();
  // const renderData = ref<PolicyRecord[]>([]);
  const renderData = ref<any[]>([]);
  const formModel = ref(generateFormModel());
  const cloneColumns = ref<Column[]>([]);
  const showColumns = ref<Column[]>([]);

  const size = ref<SizeProps>('medium');

  const basePagination: Pagination = {
    current: 1,
    pageSize: 20,
  };
  const pagination = reactive({
    ...basePagination,
  });
  const densityList = computed(() => [
    {
      name: t('迷你'),
      value: 'mini',
    },
    {
      name: t('偏小'),
      value: 'small',
    },
    {
      name: t('中等'),
      value: 'medium',
    },
    {
      name: t('偏大'),
      value: 'large',
    },
  ]);

  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('序号'),
      dataIndex: 'pk',
      slotName: 'pk',
    },
    {
      title: t('身份证号'),
      dataIndex: 'fields.id_card',
      render: ({ record }) => record.fields.id_card,
    },
    {
      title: t('姓名'),
      dataIndex: 'fields.username',
      render: ({ record }) => record.fields.username,
    },
    {
      title: t('性别'),
      dataIndex: 'fields.gender',
      render: ({ record }) => record.fields.gender,
    },
    {
      title: t('手机号'),
      dataIndex: 'fields.phone',
      render: ({ record }) => record.fields.phone,
    },
    {
      title: t('入院时间'),
      dataIndex: 'fields.checkin_date',
      render: ({ record }) => record.fields.checkin_date,
    },
    {
      title: '具体操作',
      slotName: 'check'
    }
  ]);

  const fetchData = async (
    params: PolicyParams = { current: 1, pageSize: 20 }
  ) => {
    setLoading(true);
    try {
      const { data } = await queryPolicyList(params);
      console.log("181818",data);
      console.log("555",data.list);
      renderData.value = data.list;
      pagination.current = params.current;
      pagination.total = data.total;
    } catch (err) {
      console.log("出错了！");
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };

  const searchData = () => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/oldman/getbyname?page=${  pagination.current  }&pageSize=${  pagination.pageSize}`,
      data: {
        username:formModel.value.username
       }
    })
        .then(function (value){
          console.log(value);
          if (value.status === 200){
            renderData.value = value.data.list;
            pagination.total = value.data.total;
            console.log("succuss");
            console.log("111",renderData.value);
            console.log("555",value.data)
          }else{
            console.log("error");
          }
        })
        .catch();
  }
  const searchDataById = () => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/oldman/getbyidcard?page=${  pagination.current  }&pageSize=${  pagination.pageSize}`,
      data: {
        id_card:formModel.value.id_card
      }
    })
        .then(function (value){
          console.log(value);
          if (value.status === 200){
            renderData.value = value.data.list;
            pagination.total = value.data.total;
            console.log("succuss");
            console.log("111",renderData.value);
            console.log("555",value.data)
          }else{
            console.log("error");
          }
        })
        .catch();
  }
  const search = () => {
    if(formModel.value.username){
      searchData();
    }
    else if(formModel.value.id_card)
      searchDataById()
    else fetchData()
  };
  const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
  };

  fetchData();
  const reset = () => {
    formModel.value = generateFormModel();
  };

  const handleSelectDensity = (
    val: string | number | Record<string, any> | undefined,
    e: Event
  ) => {
    size.value = val as SizeProps;
  };

  const handleChange = (
    checked: boolean | (string | boolean | number)[],
    column: Column,
    index: number
  ) => {
    if (!checked) {
      cloneColumns.value = showColumns.value.filter(
        (item) => item.dataIndex !== column.dataIndex
      );
    } else {
      cloneColumns.value.splice(index, 0, column);
    }
  };

  const exchangeArray = <T extends Array<any>>(
    array: T,
    beforeIdx: number,
    newIdx: number,
    isDeep = false
  ): T => {
    const newArray = isDeep ? cloneDeep(array) : array;
    if (beforeIdx > -1 && newIdx > -1) {
      // 先替换后面的，然后拿到替换的结果替换前面的
      newArray.splice(
        beforeIdx,
        1,
        newArray.splice(newIdx, 1, newArray[beforeIdx]).pop()
      );
    }
    return newArray;
  };

  const popupVisibleChange = (val: boolean) => {
    if (val) {
      nextTick(() => {
        const el = document.getElementById('tableSetting') as HTMLElement;
        const sortable = new Sortable(el, {
          onEnd(e: any) {
            const { oldIndex, newIndex } = e;
            exchangeArray(cloneColumns.value, oldIndex, newIndex);
            exchangeArray(showColumns.value, oldIndex, newIndex);
          },
        });
      });
    }
  };
  watch(
    () => columns.value,
    (val) => {
      cloneColumns.value = cloneDeep(val);
      cloneColumns.value.forEach((item, index) => {
        item.checked = true;
      });
      showColumns.value = cloneDeep(cloneColumns.value);
    },
    { deep: true, immediate: true }
  );
</script>

<script lang="ts">
  export default {
    name: 'SearchTable',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
  .action-icon {
    margin-left: 12px;
    cursor: pointer;
  }
  .active {
    color: #0960bd;
    background-color: #e3f4fc;
  }
  .setting {
    display: flex;
    align-items: center;
    width: 200px;
    .title {
      margin-left: 12px;
      cursor: pointer;
    }
  }
</style>
