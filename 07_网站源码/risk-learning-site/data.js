/* 商业风险处置学习站 - 数据索引调度器 */
/* v3 多文件架构：data.js 仅负责站点元信息 + 栏目注册表 */
/* 各栏目数据由 data-*.js 分文件挂载到 SITE_DATA 上 */

const SITE_DATA = {
  site: {
    title: '商业风险处置 · 实战学习站',
    subtitle: '知识沉淀 · 知识库 · 知识学习 三位一体',
    version: '3.0',
    lastUpdated: '2026-09-17'
  },
  /* 栏目注册表 —— 各分文件挂载数据后，此处引用 */
  sections: [
    { id: 'path',   title: '01 学习路径',   icon: '\u{1F5FA}\uFE0F', dataRef: 'path' },
    { id: 'theory', title: '02 理论课堂',   icon: '\u{1F4D6}', dataRef: 'theory' },
    { id: 'tools',  title: '03 实操工具箱', icon: '\u{1F9F0}', dataRef: 'tools' },
    { id: 'lab',    title: '04 沙盘训练',   icon: '\u{1F3AF}', dataRef: 'lab' },
    { id: 'cases',  title: '05 案例库',     icon: '\u{1F4CB}', dataRef: 'cases' },
    { id: 'law',    title: '06 法规参考',   icon: '\u2696\uFE0F', dataRef: 'law' }
  ]
};
