# LR-SOC-Copilot：可复现使用案例

作者：LLR6

## 要解决的场景

按实体和时间关联 JSONL 告警，检索本地 Runbook，生成可回到源行核对的调查摘要。适合离线分诊、关联逻辑实验和调查材料整理；当前检索使用词频余弦相似度。

## 复现

先克隆仓库并进入根目录，Python 3.10+。

```bash
python -m pip install -e .
soc-copilot examples/alerts.jsonl --runbooks runbooks --format json --output demo.json
```

这份[公开输出](../examples/showcase/output.json)由仓库源码实际运行产生，未手工修改。对应源码提交：`8fb495b4c8de5cbd042068c64b34e09a358fc1ae`。输入为仓库自带示例文本，没有使用用户真实日志。

## 结果怎么看

本次 **4 条示例告警生成 2 个案件**：前三条进入 CASE-001，L1↔L2 共享账号/IP（161 秒），L2↔L3 共享主机（144 秒）；L4 的 DNS 告警独立。CASE-001 的证据完整性为 3/3；这不表示入侵概率为 100%。

| 你的场景 | 可以先试什么 |
| --- | --- |
| 登录失败、成功登录和进程告警分散 | 查看共享实体、时间差与案件关联边 |
| 想知道摘要有没有原始依据 | 核对文件行号和 evidence_coverage |
| 有本地处置文档，查找不方便 | 返回相关 Runbook 片段与相似度 |

## 换成自己的输入

将示例路径替换为自己的 JSONL 告警，先对照 examples/alerts.jsonl 检查实体与时间字段；将 --runbooks 指向自己的 Markdown 文档目录。

## 有用的反馈

提交最小可复现输入、实际输出与预期行为。日志请先去敏；明确误报或遗漏发生在哪一行。详细能力边界和输入要求见 [README](../README.md)。
