import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';

export interface PolicyRecord {
  ID: Int16Array;
  id_card: string;
  username: string;
  gender : string;
  phone: string;
  checkin_date: string;
}

export interface PolicyRecord2{
  model: string;
  pk: Int16Array;
  fields: PolicyRecord[];
}
export interface PolicyParams extends Partial<PolicyRecord> {
  current: number;
  pageSize: number;
}

export interface PolicyParamsSearch {
  current: number;
  pageSize: number;
}

export interface PolicyListRes {
  list: PolicyRecord[];
  total: number;
}

export function queryPolicyList(params: PolicyParams) {
  return axios.get<PolicyListRes>('http://127.0.0.1:8000/oldman/getall', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function searchPolicyList(params: PolicyParams,username:string) {
  const data = {
    username
  };

  return axios.post<PolicyListRes>(`http://127.0.0.1:8000/oldman/getbyname?page=1&pageSize=10`, data);
}
export interface ServiceRecord {
  id: number;
  title: string;
  description: string;
  name?: string;
  actionType?: string;
  icon?: string;
  data?: DescData[];
  enable?: boolean;
  expires?: boolean;
}
export function queryInspectionList() {
  // return axios.get('/api/list/quality-inspection');
}

export function queryTheServiceList() {
  // return axios.get('/api/list/the-service');
}

export function queryRulesPresetList() {
  // return axios.get('/api/list/rules-preset');
}
