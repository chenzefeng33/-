import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const ELDER: AppRouteRecordRaw = {
  path: '/elder',
  name: 'elder',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.elder',
    icon: 'icon-user',
    requiresAuth: true,
    order: 2,
  },
  children: [
    {
      path: 'info',
      name: 'Info-elder',
      component: () => import('@/views/elder/info/index.vue'),
      meta: {
        locale: 'menu.elder.info',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'avatar',
      name: 'Avatar-elder',
      component: () => import('@/views/elder/avatar/index.vue'),
      meta: {
        locale: 'menu.elder.avatar',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
        path: 'form',
        name: 'Form-elder',
        component: () => import('@/views/elder/form/index.vue'),
        meta: {
          locale: 'menu.elder.form',
          requiresAuth: true,
          roles: ['*'],
        },
      },
  ],
};

export default ELDER;
