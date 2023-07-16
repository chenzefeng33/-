import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const DASHBOARD: AppRouteRecordRaw = {
  path: '/dashboard',
  name: 'dashboard',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.dashboard',
    requiresAuth: true,
    icon: 'icon-dashboard',
    order: 0,
  },
  children: [
    {
      path: 'workplace',
      name: 'Workplace',
      component: () => import('@/views/dashboard/workplace/index.vue'),
      meta: {
        locale: 'menu.dashboard.workplace',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'workplace-fall',
      name: 'Workplace-fall',
      component: () => import('@/views/dashboard/workplace-fall/index.vue'),
      meta: {
        locale: 'menu.dashboard.workplace-fall',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default DASHBOARD;
