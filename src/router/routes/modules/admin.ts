import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const ADMIN: AppRouteRecordRaw = {
  path: '/admin',
  name: 'admin',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.admin',
    icon: 'icon-idcard',
    requiresAuth: true,
    order: 1,
  },
  children: [
    {
        path: 'form',
        name: 'Form-admin',
        component: () => import('@/views/admin/form/index.vue'),
        meta: {
          locale: 'menu.admin.form',
          requiresAuth: true,
          roles: ['*'],
        },
      },
  ],
};

export default ADMIN;
