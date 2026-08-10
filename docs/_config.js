window.$docsify = {
  // 品牌
  name: 'Project.Villy',
  nameLink: '/',
  repo: 'https://github.com/PlutoKeating/Project.Villy',

  // 首页
  homepage: 'README.md',

  // 侧边栏
  loadSidebar: '_sidebar.md',
  subMaxLevel: 3,

  // 杂项
  auto2top: true,
  maxLevel: 4,

  // 搜索
  search: {
    placeholder: '搜索文档...',
    noData: '无结果',
    depth: 4,
    maxAge: 86400000  // 1天缓存
  },

  // 代码复制
  copyCode: {
    buttonText: '复制',
    successText: '已复制',
    errorText: '复制失败'
  }
};
