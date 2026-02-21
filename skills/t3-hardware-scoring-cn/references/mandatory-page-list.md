# 固定爬取页面清单（Mandatory Page List）

## 目的

确保每次 T3 审计的**数据输入一致**，减少因爬取页面不同导致的评估结果波动。Agent 必须按站点类型执行本清单，不得自行增减页面类型。

---

## 站点类型识别

| 站点类型 | 识别规则 | 使用的清单 |
|----------|----------|------------|
| **Shopify 独立站** | URL 含 `myshopify.com`、或访问到 `*.com/pages/`、`*.com/policies/` 等 Shopify 典型路径 | Shopify 清单 |
| **Kickstarter** | URL 含 `kickstarter.com/projects/` | Kickstarter 清单 |
| **未识别** | 以上均不匹配 | 默认按 Shopify 尝试 S1、S2，其余可选 |

---

## Shopify 独立站清单

从用户输入 URL 解析 `{domain}`（如 `nunatechnology.com`），构造以下 URL。

| 序号 | 页面类型 | URL 派生规则 | 必需 | 用途 |
|------|----------|--------------|------|------|
| S1 | Homepage | `https://{domain}/` | **是** | 产品概览、营销信息、主推产品链接 |
| S2 | Product | 用户输入的 product URL；或从 S1 提取主推产品链接 | **是** | 价格、规格、评价、in-the-box |
| S3 | How it works | `https://{domain}/pages/how-it-works` | 否 | 技术说明、工作原理 |
| S4 | FAQ | `https://{domain}/pages/faq` | 否 | 功能 Q&A、订阅、连接问题 |
| S5 | Refund/Warranty | `https://{domain}/policies/refund-policy` | 否 | 退货、质保条款 |
| S6 | Shipping | `https://{domain}/policies/shipping-policy` | 否 | 配送、DOA |
| S7 | Privacy | `https://{domain}/policies/privacy-policy` | 否 | 数据、云端、隐私 |
| S8 | User guide / Support | `https://{domain}/pages/user-guide` 或 `https://{domain}/pages/support` | 否 | App 链接、故障排查 |

### Shopify 执行规则

- **S1、S2** 为必需；若无法获取，必须标注原因
- **S3–S8** 按顺序尝试；若 404 或无法访问，在 `01-level0-source-urls.md` 中标注 `status: unavailable`
- `02-level0-extracts.md` 中，未获取的区块写 `## S{n} — [类型]\n(未获取)`
- S8 先尝试 `/pages/user-guide`，若 404 再尝试 `/pages/support`

---

## Kickstarter 清单

用户输入的项目 URL 格式：`https://www.kickstarter.com/projects/{creator}/{slug}`

| 序号 | 页面类型 | URL 派生规则 | 必需 | 用途 |
|------|----------|--------------|------|------|
| S1 | Project main | 用户输入的项目 URL | **是** | 描述、目标、筹款、回报档位、风险、故事 |
| S2 | Updates | `{project_url}/posts` 或主页面内 updates 区块 | 否 | 进度更新 |
| S3 | Comments | 主页面内 comments 区块 或 `{project_url}/comments`（若存在） | 否 | 支持者反馈 |

### Kickstarter 执行规则

- **S1** 为必需；主页面通常含大部分信息
- **S2、S3** 为补充；Kickstarter 多为单页应用，updates 和 comments 可能嵌入主页面，可尝试独立 URL 或解析主页面区块
- 若 S2/S3 无独立 URL 或无法分离，标注 `(主页面已包含或未分离)`

---

## 输出格式要求

### 01-level0-source-urls.md 固定格式

```markdown
# Level 0 (Sealed) — Source URLs

Collected on: YYYY-MM-DD
Site type: Shopify | Kickstarter

| ID | Type | URL | Status |
|----|------|-----|--------|
| S1 | Homepage | https://... | ok |
| S2 | Product | https://... | ok |
| S3 | How it works | https://... | unavailable |
...
```

- `Status`: `ok` | `unavailable`
- 按 S1、S2、… 顺序，不得跳过序号

### 02-level0-extracts.md 固定格式

```markdown
# Level 0 (Sealed) — Raw Extracts

## S1 — Homepage
(抓取内容)

## S2 — Product
(抓取内容)

## S3 — How it works
(未获取)
...
```

- 每个 S{n} 对应一个 `## S{n} — [类型]` 区块
- 未获取的写 `(未获取)`，不得省略区块

---

## 与 SKILL 流程的集成

执行步骤 2「获取产品信息」时：

1. **必读**本文件 `mandatory-page-list.md`
2. 根据用户输入 URL 识别站点类型
3. 按对应清单依次 `web_fetch`，记录结果
4. 写入 `01-level0-source-urls.md` 和 `02-level0-extracts.md`，格式严格遵循上述要求
