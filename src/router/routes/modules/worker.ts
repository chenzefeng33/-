import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const WORKER: AppRouteRecordRaw = {
  path: '/worker',
  name: 'worker',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.worker',
    icon: 'icon-user-group',
    requiresAuth: true,
    order: 3,
  },
  children: [
    {
      path: 'info',
      name: 'Info-worker',
      component: () => import('@/views/worker/info/index.vue'),
      meta: {
        locale: 'menu.worker.info',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'avatar',
      name: 'Avatar-worker',
      component: () => import('@/views/worker/avatar/index.vue'),
      meta: {
        locale: 'menu.worker.avatar',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
        path: 'form',
        name: 'Form-worker',
        component: () => import('@/views/worker/form/index.vue'),
        meta: {
          locale: 'menu.worker.form',
          requiresAuth: true,
          roles: ['*'],
        },
      },
  ],
};

export default WORKER;
