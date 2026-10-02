# LR-SOC-Copilot

### 四条告警，哪些是一件事？把关联理由展开看。

按实体和时间关联 JSONL 告警，检索本地 Runbook，生成可回到源行核对的调查摘要。适合离线分诊、关联逻辑实验和调查材料整理；当前检索使用词频余弦相似度。

[快速体验](#5-分钟-demo) · [实跑案例](docs/DEMO.md) · [完整输出](examples/showcase/output.json) · [反馈问题](https://github.com/LLR6/LR-SOC-Copilot/issues)

| 你的场景 | 可以先试什么 |
| --- | --- |
| 登录失败、成功登录和进程告警分散 | 查看共享实体、时间差与案件关联边 |
| 想知道摘要有没有原始依据 | 核对文件行号和 evidence_coverage |
| 有本地处置文档，查找不方便 | 返回相关 Runbook 片段与相似度 |

<p align="center"><img src="./docs/media/social-preview.svg" alt="LR-SOC-Copilot" width="100%"></p>
<p align="center"><img src="./docs/media/demo.gif" alt="LR-SOC-Copilot reproducible demo" width="100%"></p>
<p align="center"><strong>Every conclusion needs evidence.</strong></p>
<p align="center">Alert correlation and local runbook retrieval for investigation.</p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/LR-SOC-Copilot/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> </p>

## 30 秒看懂

把 JSONL 告警按时间窗口和共享实体组成案件图，再用本地词频向量检索 Runbook。每条结论保留 `文件:L行` 证据引用，调查员可以回到原始告警核对。

```text
Alerts → Entity/time graph → Cases → Runbook retrieval → Evidence brief
```

## 5 分钟 Demo

```bash
python -m pip install -e .
soc-copilot examples/alerts.jsonl --runbooks runbooks --output brief.md
soc-copilot examples/alerts.jsonl --runbooks runbooks --format json --output cases.json
```

样例把登录失败、随后成功登录和同主机异常子进程关联为一个案件；另一条 DNS 告警保持独立。案件分数是透明的分诊启发式。

## 三个核心设计

- **证据优先**：告警引用保留源文件行号，摘要不会脱离证据。
- **实体关联**：共享账号、IP、主机或进程且落在时间窗口内的告警进入同一连通分量。
- **本地知识检索**：Runbook 留在本机；当前版本使用可解释的词频余弦相似度。

## 边界

它不自动定性入侵，不替代分析员确认，也不会根据分数直接执行封禁。关联规则可能把同一共享实体上的无关活动连在一起，因此报告明确要求检查反证。


## 实跑结果与使用案例

本次 **4 条示例告警生成 2 个案件**：前三条进入 CASE-001，L1↔L2 共享账号/IP（161 秒），L2↔L3 共享主机（144 秒）；L4 的 DNS 告警独立。CASE-001 的证据完整性为 3/3；这不表示入侵概率为 100%。

[查看运行过程与读结果的方法](docs/DEMO.md) · [查看未经改写的 JSON 输出](examples/showcase/output.json)

## 研究路线

加入 ATT&CK 映射、时间衰减、图特征、可选本地 LLM 摘要、引用完整性校验和调查反馈学习。

作者：LLR6 · MIT License

<!-- LR-CONTENT-UPGRADE:START -->
## v0.2：让“有证据”也可以被检查

Case 现在会输出 `evidence_coverage`，统计证据是否同时具备：

- source line
- timestamp
- rule
- entities

Coverage 只衡量**可回查完整性**，不等于事件真实性概率。

CLI 同时新增：

```bash
soc-copilot examples/alerts.jsonl \
  --runbooks runbooks \
  --top-runbooks 2 \
  --min-score 40 \
  --output brief.md
```

`--top-runbooks` 控制每个 Case 最多返回多少本地知识片段；`--min-score` 用于缩小分诊列表，但不会把分数包装成“是否入侵”的结论。

证据模型见 [docs/EVIDENCE_MODEL.md](docs/EVIDENCE_MODEL.md)。

<!-- LR-CONTENT-UPGRADE:END -->

<!-- LR-DEEP-CONTENT:START -->
### Explainable correlation + retrieval benchmark

Case 现在会保留 `correlation_edges`，每条边记录：

- 左右两条源证据；
- 共享实体；
- 时间差（秒）。

因此“为什么这三条告警被归到一个 Case”可以直接从产物回查，而不是只能相信聚合器。

仓库还新增 `benchmarks/retrieval.json`，用固定查询检查 5 类本地 Runbook 的 Top-1 检索结果。CI 会运行检索 benchmark 并保存 JSON artifact，避免新增文档后把已有检索行为悄悄冲乱。
<!-- LR-DEEP-CONTENT:END -->

<details>
<summary>工程文档与兼容性</summary>

[Architecture](./docs/ARCHITECTURE.md) · [Benchmarks](./docs/BENCHMARKS.md) · [Evidence model](./docs/EVIDENCE_MODEL.md) · [Threat model](./docs/THREAT_MODEL.md) · [Roadmap](./docs/ROADMAP.md) · [Compatibility](./docs/COMPATIBILITY.md) · [Releasing](./docs/RELEASING.md) · [Support](./SUPPORT.md)
 · [Change risk](./docs/CHANGE_RISK.md) · [Failure modes](./docs/FAILURE_MODES.md) · [Performance](./docs/PERFORMANCE.md)

[贡献说明](CONTRIBUTING.md) · [版本记录](CHANGELOG.md) · [输出格式](schemas)

</details>
