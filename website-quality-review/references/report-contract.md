# 验收记录1.1

记录根目录仍为当前网站工程，默认docs/review-report.json；只读网站诊断也可用等价文字报告，不强制造工程。脚本只检查本地记录，不访问网址或读取图片含义。

1.0历史记录继续支持，返回coverageRecorded=false，不能称计划覆盖已校验。新记录用1.1，不修改旧版本报告来冒充本次检查。

| 字段 | 约定 |
|---|---|
| schemaVersion/projectVersion | 1.1及当前网站版本，不能用Skill版本代替网站版本 |
| scope/executor | mode为sample/full/change/deployment，affected为本次范围的非空字符串列表；executor是真实执行者 |
| coverage | 非空对象数组，每项有唯一id、basis（需求/方案依据）、expected（可观察预期）、page、environment；不同语言/设备/状态须分别判断时拆ID |
| checks | 每个coverage ID都应有对应项，未执行填unverified而非省略。新增发现需扩展本次覆盖，不能只挑通过项 |
| check状态 | pass/fail/unverified/not-applicable；result说明实际结果或限制，not-applicable需reason |
| pass证据 | 当前version、method、page、viewport、带时区observedAt、environment与非空evidence数组。page/environment与对应coverage一致 |
| evidence | 相对工程根的非空本地文件，使用正斜杠，禁止绝对路径、盘符、反斜杠、父级跳转或越界链接；截图与日志各自证明相关结果 |
| findings | 唯一id、ownerStage、expected、actual、reproduce、state，另有severity与impact；affectedChecks指向相关coverage ID |
| 问题状态 | open/fixed-awaiting-recheck/verified/accepted；verifiedByCheck必须为相关通过项，所有affectedChecks均通过才可标verified |

severity为blocker/major/minor/suggestion。accepted仅记录延期或接受，不计通过；保留理由。修完代码但尚未观察原问题，仍为fixed-awaiting-recheck。

返回recordStructurePassed表示记录合法；declaredChecksPassed要求已列检查完成且无未解决问题或记录错误；websiteQualityCertified始终false。覆盖列表本身是否完整、证据是否真实证明结果、画面是否合理，仍由实际执行者判断。保存一张空白截图也可能满足文件存在检查，必须实际查看，不得借此宣称通过。
