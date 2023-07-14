
import localeLogin from '@/views/login/locale/zh-CN';

import localeWorkplace from '@/views/dashboard/workplace/locale/zh-CN';

import localeSettings from './zh-CN/settings';

export default {
  'menu.dashboard': '监控中心',
  'menu.server.dashboard': '仪表盘-服务端',
  'menu.server.workplace': '工作台-服务端',
  'menu.server.monitor': '实时监控-服务端',

  'menu.elder': '老年人中心',
  'menu.elder.info':'信息管理',
  'menu.elder.avatar':'头像管理',
  'menu.elder.form':'报表统计',
  'menu.elder.analysis' : '数据分析',

  'menu.admin': '系统管理员中心',
  'menu.admin.info':'信息管理',
  'menu.admin.avatar':'头像管理',
  'menu.admin.form':'报表统计',

  'menu.worker': '工作人员管理',
  'menu.worker.info':'信息管理',
  'menu.worker.avatar':'头像管理',
  'menu.worker.form':'报表统计',

  'menu.volunteer': '义工管理',
  'menu.volunteer.info':'信息管理',
  'menu.volunteer.avatar':'头像管理',
  'menu.volunteer.form':'报表统计',

  'menu.data':'实时数据管理',

  'menu.list': '列表页',
  'menu.result': '结果页',
  'menu.exception': '异常页',
  'menu.form': '表单页',
  'menu.profile': '详情页',
  'menu.visualization': '数据可视化',
  'menu.user': '个人中心',
  'navbar.docs': '文档中心',
  'navbar.action.locale': '切换为中文',
  ...localeSettings,
  ...localeLogin,
  ...localeWorkplace,
};
