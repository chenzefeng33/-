import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import { Message, Modal } from '@arco-design/web-vue';
import { useUserStore } from '@/store';
import { getToken } from '@/utils/auth';

export interface HttpResponse<T = unknown> {
  status: number;
  msg: string;
  code: number;
  data: T;
  token: string;
}

if (import.meta.env.VITE_API_BASE_URL) {
  axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;
}

axios.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // let each request carry token
    // this example using the JWT token
    // Authorization is a custom headers key
    // please modify it according to the actual situation
    const token = getToken();
    console.log(token);
    if (token) {
      if (!config.headers) {
        config.headers = {};
      }
      config.headers.Authorization = `${token}`;
      console.log(config.headers.Authorization);
    }
    return config;
  },
  (error) => {
    // do something
    return Promise.reject(error);
  }
);
// add response interceptors
axios.interceptors.response.use(
  (response: AxiosResponse<HttpResponse>) => {
      console.log("拦截器读取response",response);
    const res = response.data;
    // console.log("拦截器读取token",res.token);
    // console.log("拦截器读取code",res.code);
    // console.log("拦截器读取",res);
    // if the custom code is not 20000, it is judged as an error.
    if (res.code !== 200 ) {
      Message.error({
        content: res.status || 'Error',
        duration: 5 * 1000,
      });
      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (
        [50008, 50012, 50014].includes(res.code) &&
        response.config.url !== 'http://127.0.0.1:8000/user/login'
      ) {
        Modal.error({
          title: 'Confirm logout',
          content:
            'You have been logged out, you can cancel to stay on this page, or log in again',
          okText: 'Re-Login',
          async onOk() {
            const userStore = useUserStore();

            await userStore.logout();
            window.location.reload();
          },
        });
      }
      console.log("reject!!!");
      return Promise.reject(new Error(res.status|| 'Error'));
    }
    return response;
  },
  (error) => {
    Message.error({
      content: error.msg || 'Request Error',
      duration: 5 * 1000,
    });
    return Promise.reject(error);
  }
);
