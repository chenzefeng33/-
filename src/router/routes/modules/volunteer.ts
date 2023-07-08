import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const VOLUNTEER: AppRouteRecordRaw = {
  path: '/volunteer',
  name: 'volunteer',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.volunteer',
    icon: 'icon-sun-fill',
    requiresAuth: true,
    order: 4,
  },
  children: [
    {
      path: 'info',
      name: 'Info-volunteer',
      component: () => import('@/views/volunteer/info/index.vue'),
      meta: {
        locale: 'menu.volunteer.info',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'avatar',
      name: 'Avatar-volunteer',
      component: () => import('@/views/volunteer/avatar/index.vue'),
      meta: {
        locale: 'menu.volunteer.avatar',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
        path: 'form',
        name: 'Form-volunteer',
        component: () => import('@/views/volunteer/form/index.vue'),
        meta: {
          locale: 'menu.volunteer.form',
          requiresAuth: true,
          roles: ['*'],
        },
      },
  ],
};

export default VOLUNTEER;
