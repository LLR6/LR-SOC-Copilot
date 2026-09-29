# Evidence Model

LR-SOC-Copilot 的核心约束是：**摘要不能比证据走得更远。**

## Source references

每条输入 alert 在读取 JSONL 时都会记录：

`filename:L<number>`

Case 中的 Evidence ID（E1、E2…）引用这些源行，而不是把摘要当作新的事实来源。

## Evidence coverage

v0.2 增加 `evidence_coverage`：

- `complete`：同时具有 source、timestamp、rule、entities 的证据条数；
- `total`：Case 证据总数；
- `ratio`：complete / total。

Coverage 不是“事件真实性概率”。它只衡量调查摘要的基本字段是否可回查。

## Runbook retrieval

Runbook 只来自本地 Markdown 文件。当前检索是透明的词频余弦相似度，不调用远程模型。

CLI 支持：

- `--top-runbooks N`：限制每个 Case 返回的 Runbook chunk 数；
- `--min-score N`：只输出达到最低分诊分数的 Case。

分数仍是 triage heuristic，不是入侵结论。

## Investigation discipline

建议分析人员按下面顺序使用输出：

1. 从最早 Evidence 回到源系统；
2. 验证共享实体是否真的属于同一活动；
3. 检查时间关系；
4. 阅读本地 Runbook；
5. 主动寻找 benign explanation；
6. 记录反证；
7. 最后才写调查结论。

## Future work

- 时间衰减；
- ATT&CK Technique 映射；
- 引用完整性校验；
- Case split / merge 人工反馈；
- 本地 LLM 摘要，但必须保持 Evidence ID 引用；
- investigation outcome 反馈学习。
