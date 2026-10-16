# 网站成品验收

通用的网站验收Skill，当前版本 **0.3.0**。承接策划与设计的预期，检查实际内容、画面、动效、关键路径和必要业务结果，形成可以直接修复的问题。适用于完整交付、样板、局部变更与公网检查；不绑定具体项目、行业、框架或部署平台。

## 本版具体能力

- 将策划中的页面职责、主方向、媒体、组件和操作预期映射为本次检查范围，遗漏项保持未验证。
- 区分实现偏差、合理适配、设计问题和偏好；不凭截图存在或参数一致宣称设计质量通过。
- 检查所选动效的起中止、正反向、中断恢复、减少动态、手机、生命周期与加载失败；保留用户确认的表现。
- 问题按定位/内容、素材、呈现、交互、业务和运行环节返回，只复验受影响路径。
- 1.1记录校验覆盖ID、当前版本/页面/环境/本地证据、问题与相关复验关系，避免只列通过项或用无关通过项关闭问题。兼容1.0历史记录，明确其覆盖未校验。

入口：[SKILL.md](website-quality-review/SKILL.md)。方法：[检查覆盖](website-quality-review/references/coverage.md)、[画面对照](website-quality-review/references/visual-comparison.md)、[动效验收](website-quality-review/references/motion-review.md)、[问题与复验](website-quality-review/references/remediation.md)。

与[策划设计](https://github.com/Bonzogit/site-design)及现有建站Skill使用同一份方案，无原方案也可按需求推导检查依据并注明来源，不强迫重做策划或新建网站。业务开发由建站负责，验收读取有效结果并核对必要用户可见链路。相同执行者自检不称独立评审。

## 使用与迁移

将整个website-quality-review目录放入宿主用户skills目录；核心方法、模板和Python标准库检查器自带，不依赖旧电脑路径。已有报告需要机器检查时执行：

```text
python website-quality-review/scripts/review_check.py <工程目录> --version <网站版本> --require-pass
```

字段见[记录协议](website-quality-review/references/report-contract.md)。记录结构/声明检查通过不是网站品质认证；检查器不会操作浏览器或判断图片含义。浏览器、实体设备与业务服务另行准备，策划的完整资料包可选复用，见[工具与迁移](website-quality-review/references/tools-portability.md)。

验证边界见[VALIDATION.md](VALIDATION.md)。本版没有建站、部署、实际新网站视觉检查或独立评审。公开包不含客户截图、网站数据或凭据。

[当前v0.3.0](https://github.com/Bonzogit/check-skills/tree/versions/v0.3.0) · [上一版v0.2.0](https://github.com/Bonzogit/check-skills/tree/versions/v0.2.0)，旧分支固定保留。
