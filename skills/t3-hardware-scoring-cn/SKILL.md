---
name: t3-hardware-scoring-cn
description: MantaBase T3硬件审计系统（中文版）。通过Brand Blinding、三Auditor（Tool/Toy/Trash）专项评分和Peer Review，基于设计理论对硬件产品客观分类。触发：产品链接、T3审计、Tool/Toy/Trash分类、硬件评估、VC投资建议
compatibility: 需要 Python（beautifulsoup4>=4.12.3, requests>=2.31.0）、网络访问（用于产品页面爬取）
metadata:
  version: "1.0"
---

# MantaBase T3硬件审计系统

## 任务目标
- 本Skill用于：通过硬件产品链接自动爬取信息，经过Brand Blinding去品牌化处理后，由三个独立Auditor基于权威参考书进行专项评分，通过Peer Review互相审查并优化，最终实现Tool/Toy/Trash客观分类
- 能力包含：网页信息爬取、Brand Blinding信息过滤、三Auditor专项评分、Peer Review互相审查、Final Judge综合判断
- 触发条件：用户提供硬件产品链接，要求进行T3审计或分类评分
- 核心理念：透明第一、客观评估、并行审计、专家评审、持续优化

## 前置准备
- 无需额外准备，系统会自动处理网页内容提取

## 操作步骤

### 标准流程

#### 1. 获取用户输入
- 引导用户提供硬件产品链接（支持电商平台、官网、评测网站等）
- 可选：获取用户关注的特定维度或审计重点

#### 2. 获取产品信息（推荐Agent方式）

**必读** [references/mandatory-page-list.md](references/mandatory-page-list.md)，按站点类型（Shopify / Kickstarter）执行固定爬取清单，确保数据输入一致。

**方式A：Agent直接抓取（推荐）**
- 阅读 [references/web-fetch-guide.md](references/web-fetch-guide.md) 掌握完整提取策略
- 识别站点类型后，按 mandatory-page-list 依次 fetch，写入 `01-level0-source-urls.md`、`02-level0-extracts.md`
- 使用web_fetch工具直接访问产品页面
- 优势：
  - ✅ 数据完整性高（智能提取关键信息）
  - ✅ 适应不同网站结构
  - ✅ 可处理复杂页面（动态加载、多标签页）
  - ✅ 可同时访问多个相关页面（产品页、评测页、规格页）
  - ✅ Agent能主动识别缺失信息并补充
- 执行要点：
  ```
  ⚠️ 重要：单一页面可能信息不完整，Agent应：
  
  1. 多页面访问：
     - 产品详情页 → 基本信息、价格
     - 产品规格页 → 技术参数
     - 用户评价页 → 用户反馈
     - 评测页面 → 专业评价
  
  2. 价格信息提取：
     - 查找schema.org结构化数据
     - 尝试购物车页面
     - 搜索"产品名称 + price"
     - 若缺失：在报告中明确标注
  
  3. 动态内容处理：
     - 使用分页抓取（offset参数）
     - 尝试不同URL变体
     - 查找移动版页面
  
  4. 数据完整性验证：
     - 基本信息：必须完整
     - 技术规格：至少50%
     - 用户反馈：至少一项
  ```

**方式B：Python脚本抓取（辅助/批量场景）**
- 适用场景：批量处理多个产品、离线分析
- 调用脚本提取产品页面内容：
  ```bash
  python scripts/crawl_product_info.py --url <product_url> --pretty
  ```
- 参数说明：
  - `--url`：产品页面URL（必需）
  - `--pretty`：美化JSON输出（可选）
  - `--output`：输出文件路径（可选）
- 注意：脚本方式可能数据不完整，建议优先使用Agent方式

- 脚本返回：产品名称、描述、特性、价格、目标用户、完整客观数据等结构化信息

#### 3. Brand Blinding信息过滤（智能体执行）
- 阅读 [references/defluff-guide.md](references/defluff-guide.md) 掌握Brand Blinding原则
- 智能体对产品信息进行去品牌化处理：
  - 去除品牌名称和商标引用
  - 去除营销话术和夸大描述
  - 识别并移除情感化形容词
  - 提取纯功能性信息和客观参数
  - 保持事实的完整性和准确性
- 输出：Brand-Blinded后的客观产品信息

#### 4. 三Auditor专项评分（智能体并行执行）
- 每个Auditor**同时**独立评估，各司其职
- 每个Auditor读取自己的独立指南，不查看其他Auditor的指南或报告

**🟢 Tool Auditor（工具审计员）**
- 阅读 [references/tool-auditor.md](references/tool-auditor.md) 获取完整指南
- **必遵** [references/auditor-templates.md](references/auditor-templates.md) 严格评分表格模板
- 评估角度：解决实际痛点、实用性、可靠性
- 权威参考：Tony Fadell《Build》专项检查清单
- 专项检查：
  - 痛点识别与解决（30分）
  - 注重细节与一致性（25分）
  - 简洁高效（25分）
  - 工程可靠性（20分）
- 输出：专项评分报告（总分100分），包含每个检查项的得分、理由、证据
- Litmus Test：如果明天它坏了，用户的工作流会停滞吗？

**🟡 Toy Auditor（玩具审计员）**
- 阅读 [references/toy-auditor.md](references/toy-auditor.md) 获取完整指南
- **必遵** [references/auditor-templates.md](references/auditor-templates.md) 严格评分表格模板
- 评估角度：情感价值、愉悦体验、美学设计
- 权威参考：Don Norman《设计心理学》专项检查清单
- 专项检查：
  - 感官愉悦（30分）
  - 惊喜与发现（25分）
  - 情感联结（25分）
  - 可探索性（20分）
- 输出：专项评分报告（总分100分），包含每个检查项的得分、理由、证据
- Litmus Test：用户是否会把它放在显眼的位置"炫耀"或收藏？

**🔴 Trash Auditor（垃圾审计员）**
- 阅读 [references/trash-auditor.md](references/trash-auditor.md) 获取完整指南
- **必遵** [references/auditor-templates.md](references/auditor-templates.md) 严格评分表格模板
- **必读** [references/trash-red-flags.md](references/trash-red-flags.md) 应用「火眼金睛」高敏感触发清单
- 评估角度：逻辑缺陷、营销欺诈、设计违背
- 权威参考：Dieter Rams十大设计原则违背程度检查清单
- 专项检查：
  - 原则违背（30分）
  - 问题制造（25分）
  - 价值缺失（25分）
  - 可替代性（20分）
- 输出：专项评分报告（总分0-100分，正向评分），包含每个检查项的得分、理由、证据
- Litmus Test：如果这个产品明天消失，世界会变得更好还是更糟？

**关键原则**：
- **信息隔离**：每个Auditor只能访问Brand-Blinded后的客观产品信息，严禁查看原始产品信息
- **专项评分**：必须基于权威参考书的专项检查清单进行评分
- **证据驱动**：每个评分必须基于具体证据，避免主观判断
- **独立评估**：三个Auditor同时评估，互不干扰，互不交流
- **客观报告**：每个Auditor只报告客观发现，不"辩护"自己的分类
- **诚实记录**：即使证据支持其他分类，也要如实记录

#### 5. Peer Review互相审查（智能体并行执行）
- 阅读 [references/peer-review-guide.md](references/peer-review-guide.md) 掌握Peer Review流程
- 三个Auditor互相审查其他两个Auditor的报告：

**交叉审查**：
- Tool Auditor审查：Toy报告 + Trash报告
- Toy Auditor审查：Tool报告 + Trash报告
- Trash Auditor审查：Tool报告 + Toy报告

**审查内容**：
- 评分是否合理？
- 证据是否充分？
- 是否有被忽视的跨分类证据？
- 是否存在偏见或遗漏？

**审查输出**：
- 审查意见（包含具体建议和理由）
- 评分调整建议
- 跨分类证据补充

**关键原则**：
- 基于事实和证据，不针对个人
- 提供具体的改进建议
- 审查者和被审查者保持开放心态
- 记录所有审查意见和回应

#### 6. Auditor优化报告（智能体执行）
- 每个Auditor基于收到的审查意见，优化自己的报告：
  - 分析审查意见的合理性
  - 接受合理的建议并修改报告
  - 对于不合理的意见，提供反驳理由
  - 记录所有的修改和理由

**优化输出**：
- 原始报告
- 优化后的报告
- 修改记录（接受/拒绝的审查意见及理由）

#### 7. Final Judge综合判断（智能体执行）
- 阅读 [references/t3-classification.md](references/t3-classification.md) 获取分类判断指南
- 阅读三个Auditor优化后的最终报告
- 综合分析三个报告的结论和证据
- 应用T3分类规则：
  - 计算综合评分：Composite = max(Tool评分, Toy评分) - Trash评分
  - 确定主导分类（满足2个以上条件）
  - 确定次要分类（如有）
  - 应用Litmus Test一致性分析
- 输出：最终分类、置信度、判断理由、改进建议

#### 8. 生成审计报告

**输出文件**：统一命名为 `99-audit-report.md`（禁止使用 `99-report-summary.md` 等别名）。报告目录：`tmp/reports/t3-{YYYY-MM-DD}-{case-id}/`。

**报告结构**（见 [references/report-schema.md](references/report-schema.md)）：
1. **YAML 元数据块**（`---` 包裹）：供网站 leaderboard 解析，含 `case_id`、`source_url`、`scores`、`chart_data`、`litmus_tests`、`classification` 等
2. **文字分析内容**：从三 Auditor 的 `extract_for_report` 聚合，章节固定为：产品概述、Tool 要点、Toy 要点、Trash 要点、Final Judge 判断理由、改进建议

**必须包含**：
- 产品基本信息（原始信息和Brand-Blinded信息对比）
- 三Auditor专项评分表格（[auditor-templates.md](references/auditor-templates.md) 规定格式）
- Peer Review 汇总
- Final Judge 判断结果

### 可选分支

- **当产品信息不足**：提示用户补充描述或提供更多参考资料
- **当评分接近边界**：分析主导因素，说明分类判断依据
- **当Auditor意见分歧**：Final Judge需详细说明权衡逻辑
- **当存在争议**：提供多视角分析，列出不同分类的理由和证据

## 资源索引

- **辅助脚本**（批量处理/离线分析场景）：
  - [scripts/crawl_product_info.py](scripts/crawl_product_info.py)（用途：网页内容爬取和产品信息提取，参数：`--url <product_url> [--pretty] [--output <file>]`）
  - [scripts/synthesize_results.py](scripts/synthesize_results.py)（用途：格式化三Auditor结果并计算最终分类，参数：`--input <auditor_reports.json> [--pretty] [--output <file>]`）

- **领域参考**：
  - [references/mandatory-page-list.md](references/mandatory-page-list.md)（何时读取：步骤2 获取产品信息时，必读；固定爬取清单）
  - [references/report-schema.md](references/report-schema.md)（何时读取：步骤8 生成 99-audit-report.md 时，必遵；YAML 结构定义）
  - [references/file-naming-convention.md](references/file-naming-convention.md)（何时读取：创建报告目录时，必遵；文件命名规范）
  - [references/isolation-manifest-template.md](references/isolation-manifest-template.md)（何时读取：创建 00-isolation-manifest.md 时参考）
  - [references/web-fetch-guide.md](references/web-fetch-guide.md)（何时读取：Agent使用web_fetch工具提取产品信息时，必读）
  - [references/tool-auditor.md](references/tool-auditor.md)（何时读取：Tool Auditor执行专项评分时）
  - [references/toy-auditor.md](references/toy-auditor.md)（何时读取：Toy Auditor执行专项评分时）
  - [references/trash-auditor.md](references/trash-auditor.md)（何时读取：Trash Auditor执行专项评分时）
  - [references/trash-red-flags.md](references/trash-red-flags.md)（何时读取：Trash Auditor应用火眼金睛触发清单时，必读）
  - [references/auditor-templates.md](references/auditor-templates.md)（何时读取：三Auditor执行专项评分时，必遵；保证表格输出可复现）
  - [references/t3-classification.md](references/t3-classification.md)（何时读取：Final Judge进行综合判断时）
  - [references/scoring-checklists.md](references/scoring-checklists.md)（何时读取：快速查阅检查清单索引时）
  - [references/defluff-guide.md](references/defluff-guide.md)（何时读取：进行Brand Blinding处理时）
  - [references/peer-review-guide.md](references/peer-review-guide.md)（何时读取：进行Peer Review时）
  - [references/objective-data-standard.md](references/objective-data-standard.md)（何时读取：所有阶段，确保客观数据完整性）
  - [references/design-theories.md](references/design-theories.md)（何时读取：进行设计理论分析时）

## 注意事项

- **🚨 信息隔离（最重要）**：
  - 必须确保三Auditor只能访问Brand-Blinded后的客观产品信息
  - 严禁Auditor查看原始产品信息、品牌名称、营销话术
  - 智能体在执行Auditor任务时，必须明确说明仅基于Brand-Blinded信息评估
  - 审计报告中必须包含"信息来源说明"字段

- **📊 客观数据完整性（核心）**：
  - 必须收集完整的客观数据（技术规格、性能、可靠性、市场、可持续性、成本）
  - 所有客观数据在Brand Blinding阶段**必须保留**，不得移除或修改
  - 每个Auditor的评分必须基于可验证的客观数据，避免主观臆断
  - 参考 [references/objective-data-standard.md](references/objective-data-standard.md) 了解客观数据标准
  - 审计报告中必须包含客观数据汇总和数据完整性评分
  - 如果客观数据不足，必须标注数据缺失对评估的影响

- **Brand Blinding的重要性**：
  - 必须先进行Brand Blinding，确保评估基于客观信息，而非品牌影响
  - Brand Blinding必须保留所有客观数据，仅移除品牌信息和营销话术
  - 区分"客观数据"和"营销话术"是Brand Blinding的核心任务

- **专项评分的必要性**：
  - 必须基于权威参考书的专项检查清单进行评分
  - 每个评分必须追溯到具体的检查项和证据
  - 确保评分的一致性和可重复性

- **三Auditor独立性**：
  - 三个Auditor必须同时独立评估，互不干扰，互不交流
  - 每个Auditor只能看到自己的评估任务和Brand-Blinded信息
  - 禁止Auditor之间交换信息或参考其他Auditor的结论

- **Peer Review的客观性**：
  - 审查基于事实和证据，不针对个人
  - 提供具体的改进建议
  - 审查者和被审查者保持开放心态
  - 记录所有审查意见和回应

- **客观性原则**：Auditors报告客观发现，即使证据支持其他分类也要如实报告

- **透明性**：所有评估过程、理由、证据都要在报告中清晰呈现

- **智能体主导**：Brand Blinding、三Auditor专项评分、Peer Review、Final Judge都由智能体执行，脚本仅负责爬取和格式化

## 使用示例

### 示例1：完整T3审计流程
- **功能说明**：完整的Brand Blinding + 专项评分 + Peer Review + Final Judge流程
- **执行方式**：
  1. 智能体爬取产品信息
  2. 智能体执行Brand Blinding
  3. 智能体同时启动三Auditor专项评分
  4. 智能体执行Peer Review互相审查
  5. 智能体优化报告
  6. 智能体执行Final Judge判断
  7. 生成完整审计报告
- **关键参数**：产品URL
- **输出示例**：
  ```
  产品：智能手表X
  Brand-Blinded：可穿戴健康监测设备，具备心率、血氧、睡眠追踪功能
  
  🟢 Tool Auditor专项评分：82/100
    - 痛点识别与解决：28/30 ✓
      * 识别出明确痛点（9/10）
      * 解决方案直击痛点（9/10）
      * 优于现有方案（10/10）
    - 注重细节与一致性：20/25 ✓
      * 交互精心设计（8/10）
      * 设计语言一致（7/10）
      * 隐藏复杂性（5/5）
    - 简洁高效：20/25 ✓
      * 遵循少即是多（8/10）
      * 操作高效（7/10）
      * 不引人注意（5/5）
    - 工程可靠性：14/20 ✓
      * 稳定可靠（7/10）
      * 质量控制（7/10）
  
  🟡 Toy Auditor专项评分：65/100
    - 可视性：12/15 ✓
      * 状态清晰可见（8/10）
      * 操作显而易见（4/5）
    - 反馈：11/15 ✓
      * 即时反馈（7/10）
      * 反馈信息准确（4/5）
    - 限制因素：12/15 ✓
      * 限制机制完善（7/10）
      * 限制自然合理（5/5）
    - 映射：11/15 ✓
      * 自然映射（7/10）
      * 符合心理模型（4/5）
    - 一致性：7/10 ✓
      * 内部一致（4/5）
      * 符合标准（3/5）
    - 情感设计：12/30 ✓
      * 本能层（6/10）
      * 行为层（3/10）
      * 反思层（3/10）
  
  🔴 Trash Auditor专项评分：25/100
    - 原则1（创新）：2/10 - 小幅创新
    - 原则2（有用）：8/10 - 功能实用
    - 原则3（美观）：6/10 - 外观一般
    - 原则4（易于理解）：7/10 - 基本易懂
    - 原则5（不引人注目）：8/10 - 基本不引人注意
    - 原则6（诚实）：3/10 - 略有夸大
    - 原则7（持久）：5/10 - 可能过时
    - 原则8（细节）：6/10 - 细节一般
    - 原则9（环境友好）：4/10 - 环保一般
    - 原则10（尽可能少）：7/10 - 较为简洁
  
  Peer Review结果：
    - Tool Auditor建议降低Toy评分（-15分）✓ 已接受
    - Toy Auditor建议提高Tool评分（+5分）✗ 已拒绝
    - Trash Auditor建议降低Toy评分（-10分）✓ 已接受
  
  Final Judge: Tool (置信度: 78%)
  理由：Tool专项评分（82）显著高于Toy专项评分（65），Trash评分（25）低，产品主要价值在于解决健康监测痛点
  ```

### 示例2：快速T3分类
- **功能说明**：简化流程，重点进行Brand Blinding和关键专项评分
- **执行方式**：智能体简化评估，聚焦核心检查项
- **关键参数**：产品URL，评估重点（可选）
- **指导要点**：快速识别产品的核心价值主张，应用Litmus Test和专项检查清单

### 示例3：竞品对比审计
- **功能说明**：对多个同类产品进行并行T3审计对比
- **执行方式**：批量爬取 + 并行三Auditor专项评分 + Peer Review + 对比分析
- **输出格式**：对比表格 + 每个产品的详细审计报告

## 审计流程可视化

```
用户输入URL
    ↓
爬取产品信息（原始信息）
    ↓
Brand Blinding (智能体去除品牌影响)
    ├─ 原始信息 🔒 (密封，不对Auditor公开)
    └─ Brand-Blinded信息 ✅ (唯一公开给Auditor的信息源)
    ↓
┌─────────────────────────────────────────┐
│ 三Auditor专项评分 (智能体并行执行)       │
│ 🔒 信息隔离：每个Auditor仅能访问        │
│    Brand-Blinded后的客观产品信息           │
│ 📚 权威参考：专项评分检查清单            │
├───────────────┬─────────────┬────────────┤
│ 🟢 Tool       │ 🟡 Toy      │ 🔴 Trash   │
│ Auditor       │ Auditor     │ Auditor    │
│ 🔒 信息隔离   │ 🔒 信息隔离 │ 🔒 信息隔离│
│ 📚 Build清单  │ 📚 设计心理 │ 📚 Rams原则│
└───────┬───────┴─────┬───────┴──────┬────┘
        │             │              │
   专项评分      专项评分       专项评分
   (初始版本)   (初始版本)     (初始版本)
        │             │              │
   独立报告      独立报告       独立报告
        │             │              │
        └─────────────┼──────────────┘
                      ↓
┌─────────────────────────────────────┐
│  Peer Review互相审查 (智能体并行)    │
│  🔒 信息隔离：仅能看到对方De-        │
│     Branded报告，不能看原始信息      │
├─────────────────────────────────────┤
│ Tool审查Toy+Trash │ Toy审查Tool+Trash│
│  │审查意见         │ 审查意见        │
│  └─────────────────┴──────────────┐ │
│  Trash审查Tool+Toy │ 审查意见      │ │
└───────┬─────────────┴──────────────┘
        │
   审查意见汇总
        ↓
┌─────────────────────────────────────┐
│  Auditor优化报告 (智能体)           │
├─────────────────────────────────────┤
│ Tool优化 │ Toy优化 │ Trash优化      │
└───────┬────┴────┬───┴─────┬─────────┘
        │          │          │
   优化报告   优化报告   优化报告
        │          │          │
        └──────────┼──────────┘
                   ↓
         Final Judge综合判断
                   ↓
               生成审计报告
               (包含完整审计链)
```

## 🔒 信息隔离保证

为确保三Auditor的客观性，系统必须严格遵守以下信息隔离规则：

### 信息层级
1. **原始信息（Level 0）**：包含品牌名称、营销话术、情感化描述
   - 状态：🔒 密封
   - 访问权限：仅Brand Blinding模块和Final Judge（用于对比）
   - 禁止：三Auditor严禁访问

2. **Brand-Blinded信息（Level 1）**：纯功能性和客观参数
   - 状态：✅ 公开
   - 访问权限：三Auditor和Final Judge
   - 内容：技术规格、功能列表、使用场景（去品牌化）

### 智能体执行检查清单
智能体在执行Auditor任务时，必须确认：
- [ ] 已明确说明仅使用Brand-Blinded信息
- [ ] 已基于权威参考书的专项检查清单进行评分
- [ ] 未引用任何品牌名称
- [ ] 未参考任何营销话术
- [ ] 评估报告中包含"信息来源：Brand-Blinded产品信息"声明
- [ ] 评估报告中包含"专项评分依据：XXX检查清单"声明

### 审计报告验证
每个Auditor的报告必须包含：
```json
{
  "auditor": "Tool",
  "total_score": 82,
  "checklist_score": 82,
  "information_source": "Brand-Blinded产品信息（已隔离原始品牌信息）",
  "scoring_basis": "Tony Fadell《Build》专项检查清单",
  "information_isolation_confirmed": true,
  "checklist_compliance_confirmed": true
}
```
