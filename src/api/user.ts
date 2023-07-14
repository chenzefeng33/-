import axios, {AxiosResponse} from 'axios';
import type { RouteRecordNormalized } from 'vue-router';
import { UserState } from '@/store/modules/user/types';
import {HttpResponse} from "@/api/interceptor";
import {reject} from "lodash";
import {clearToken, setToken} from "@/utils/auth";
import {throwError} from "echarts/types/src/util/log";

export interface LoginData {
  username: string;
  Password: string;
}

export interface LoginRes {
  code: number;
  status: string;
  token: string;

}
export function login(data: LoginData) {
  console.log("success");
  window.localStorage.setItem('userRole','admin');
  // const result = axios.post<LoginRes>('http://127.0.0.1:8000/user/login', data)
  // console.log(result);
  axios.post('http://127.0.0.1:8000/user/login', data)// : AxiosResponse<HttpResponse>
      .then(function (response: AxiosResponse<LoginRes>){

            console.log("post1111",response)
            console.log("post2222",response.data.token)
          if(response.data.token)
            setToken(response.data.token)
          else clearToken()
         return response;
      })
      .catch(error=>{
          console.log("找错")
          reject(error)
      })

  // return result;

}

export function logout() {
  return axios.post<LoginRes>('/api/user/logout');
}

export function getUserInfo() {
  return axios.post<UserState>('/api/user/info');
}

export function getMenuList() {
  return axios.post<RouteRecordNormalized[]>('/api/user/menu');
}
