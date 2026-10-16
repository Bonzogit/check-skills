# 网站成品验收

通用的网站质量验收 Skill。对照当前需求与设计，检查真实内容、画面、操作和业务结果，输出可修复问题并定向复验。当前版本 **0.2.0**。

## 具体做什么

- 判断网站是否清楚表达业务，并提供访客作判断所需的信息。
- 实际查看主次、字体、密度、对齐、图片、响应布局和设计符合度。
- 走完关键路径，检查上下文、操作反馈、保存结果、错误恢复与相关状态。
- 按影响区分阻断、主要缺陷、一般缺陷与改进建议，提供位置、复现、预期、实际与修复条件。
- 把产品逻辑问题退回策划，素材问题退回素材准备，布局和业务问题退回建站；修复后只复验受影响范围。

入口：[SKILL.md](website-quality-review/SKILL.md)。方法：[内容与视觉](website-quality-review/references/quality.md)、[检查选择](website-quality-review/references/checks.md)、[问题与复验](website-quality-review/references/remediation.md)。

可配合[策划与设计](https://github.com/Bonzogit/site-design)及现有建站 Skill，也可单独验收已有网站。不绑定示例网站、行业、框架和部署平台；没有原方案时注明推导的检查依据，不要求先重做策划。没有源码目录仍可检查公开页面，报告实际可见范围。

将 website-quality-review 文件夹放入宿主的用户 skills 目录即可使用。仅需保存机器可检查记录时，使用包内报告模板与检查器；记录结构通过不等于网站品质通过。相同执行者自检不称独立评审，未测项目保持未验证。

验证与限制见[VALIDATION.md](VALIDATION.md)。公开包不含具体网站工程、客户数据或凭据。[当前 v0.2.0](https://github.com/Bonzogit/check-skills/tree/versions/v0.2.0) · [上一版 v0.1.0](https://github.com/Bonzogit/check-skills/tree/versions/v0.1.0)，历史分支固定保留。
