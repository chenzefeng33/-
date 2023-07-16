import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
import {getToken} from "@/utils/auth";

export interface PolicyRecord {
    ID: Int16Array;
    id_card: string;
    username: string;
    gender : string;
    phone: string;
    hire_date: string;
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
    return axios.get<PolicyListRes>('http://127.0.0.1:8000/employee/getall', {
        params,
        paramsSerializer: (obj) => {
            return qs.stringify(obj);
        }
    });
}

