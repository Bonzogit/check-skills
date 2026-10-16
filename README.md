# 网站成品验收 / 0.1.0

检查当前网站样板、修改或上线结果的实际画面与用户路径，报告可复现问题并按影响范围复验。

入口：[website-quality-review/SKILL.md](website-quality-review/SKILL.md)。安装时将整个 website-quality-review 文件夹放入宿主用户 skills 目录；本机交付已另行安装。使用示例：`使用 $website-quality-review 检查当前网站样板，按实际设计和用户路径列出问题并复验。`

## 工作方式

读取当前任务、版本、设计与已有有效检查 → 实际观察/操作 → 区分设计、素材、实现与业务问题 → 定向修复 → 只复验受影响路径。可以单独验收已有站点，也可承接 [策划与设计](https://github.com/Bonzogit/site-design) 和现有建站 Skill。

检查按范围选择，见 [检查表](website-quality-review/references/checks.md)。报告模板和检查器只约束版本、证据与问题状态；检查器不会操作浏览器、评判图片含义或认证网站品质。示例：

```text
python website-quality-review/scripts/review_check.py <project> --version <version>
```

加 `--require-pass` 会拒绝声明未完成或有未解决问题的记录；结构检查通过不能冒充实际视觉/功能验收。相同执行者自检不称独立评审。完整验证与限制见 [VALIDATION.md](VALIDATION.md)。

本包不包含私人项目、截图、客户数据或自动后台调度。原建站 Skill 继续负责业务开发测试、原项目部署及数据保留。

当前固定版本：[versions/v0.1.0](https://github.com/Bonzogit/check-skills/tree/versions/v0.1.0)。首版暂无旧版本；后续保留历史快照。
