# LR-SOC-Copilot

<!-- LR-LAB-CHROME:START -->
<p align="center">
  <a href="https://github.com/LLR6"><img alt="LR Lab" src="https://img.shields.io/badge/LR_LAB-0x4C52-0D1117?style=for-the-badge&logo=github&logoColor=white"></a>
  <img alt="SOC / IR" src="https://img.shields.io/badge/SOC_%2F_IR-6366F1?style=for-the-badge">
</p>
<p align="center"><strong>Every conclusion needs evidence.</strong><br><sub>Alert correlation and local runbook retrieval</sub></p>
<p align="center"><a href="https://github.com/LLR6/LR-SOC-Copilot/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/LLR6/LR-SOC-Copilot?style=flat-square&logo=github&label=stars"></a>
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/LLR6/LR-SOC-Copilot?style=flat-square"> <img alt="Maintained" src="https://img.shields.io/badge/status-active-success?style=flat-square"></p>
<p align="center"><a href="https://github.com/LLR6">Profile</a> · <a href="https://github.com/LLR6?tab=repositories">All projects</a> · <a href="https://github.com/LLR6/LR-SOC-Copilot/issues">Issues</a></p>
<!-- LR-LAB-CHROME:END -->

<!-- LR-PROJECT-DOCS:START -->
### Project docs
[Architecture](./docs/ARCHITECTURE.md) · [Benchmarks](./docs/BENCHMARKS.md) · [Evidence model](./docs/EVIDENCE_MODEL.md) · [Threat model](./docs/THREAT_MODEL.md) · [Roadmap](./docs/ROADMAP.md) · [Releasing](./docs/RELEASING.md)
<!-- LR-PROJECT-DOCS:END -->
<p align="center">[Threat model](docs/THREAT_MODEL.md)</p>

<!-- LR-SECOND-PASS:START -->
<p align="center"><a href="#5-分钟-demo">5-minute demo</a> · <a href="./runbooks">Runbooks</a> · <a href="./docs/EVIDENCE_MODEL.md">Evidence model</a> · <a href="./src">Source</a> · <a href="./tests">Tests</a></p>
<!-- LR-SECOND-PASS:END -->



<p align="center"><img src="./docs/media/social-preview.svg" alt="LR-SOC-Copilot" width="100%"></p>
<p align="center"><img src="./docs/media/demo.gif" alt="LR-SOC-Copilot reproducible demo" width="100%"></p>
<p align="center"><strong>Every conclusion needs evidence.</strong></p>
<p align="center">Alert correlation and local runbook retrieval for investigation.</p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/LR-SOC-Copilot/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-8b5cf6"></p>

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

<!-- LR-ENGINEERING-REF:START -->
## Engineering Reference

[Architecture](docs/ARCHITECTURE.md) · [Evidence model](docs/EVIDENCE_MODEL.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Release checklist](docs/RELEASE_CHECKLIST.md) · [Case schema](schemas/case-report.schema.json)

These files document the project's architecture, safety boundaries, reproducibility assumptions and release process.
<!-- LR-ENGINEERING-REF:END -->

<!-- LR-LAB-FOOTER:START -->
---
<p align="center"><sub>Part of <a href="https://github.com/LLR6">LR Lab</a> · Security × AI × Android × Automation</sub><br><sub>Build things that are useful, inspectable, and reproducible.</sub></p>
<!-- LR-LAB-FOOTER:END -->

