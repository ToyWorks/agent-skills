# 评分检查清单索引

## 概览
本文件汇总了T3硬件评分系统中所有Auditor的检查清单索引。每个Auditor都有独立的完整指南文档。

## 检查清单索引

### Tool Auditor检查清单
- **文件路径**：[tool-auditor.md](tool-auditor.md)
- **检查清单名称**：Tony Fadell《Build》专项检查清单
- **评分逻辑**：正向评分（0-100分）
- **评估维度**：
  1. 痛点识别与解决（30分）
  2. 注重细节与一致性（25分）
  3. 简洁高效（25分）
  4. 工程可靠性（20分）
- **Litmus Test**：如果明天它坏了，用户的工作流会停滞吗？

### Toy Auditor检查清单
- **文件路径**：[toy-auditor.md](toy-auditor.md)
- **检查清单名称**：Don Norman《设计心理学》专项检查清单
- **评分逻辑**：正向评分（0-100分）
- **评估维度**：
  1. 感官愉悦（30分）
  2. 惊喜与发现（25分）
  3. 情感联结（25分）
  4. 可探索性（20分）
- **Litmus Test**：用户是否会把它放在显眼的位置"炫耀"或收藏？

### Trash Auditor检查清单
- **文件路径**：[trash-auditor.md](trash-auditor.md)
- **检查清单名称**：Dieter Rams十大设计原则违背程度检查清单
- **评分逻辑**：正向评分（0-100分，分数越高越符合Trash特征）
- **评估维度**：
  1. 原则违背（30分）
  2. 问题制造（25分）
  3. 价值缺失（25分）
  4. 可替代性（20分）
- **Litmus Test**：如果这个产品明天消失，世界会变得更好还是更糟？

## 检查清单使用流程

### 1. 信息准备
- 准备Brand-Blinded后的产品信息
- 确保客观数据完整
- 参考 [objective-data-standard.md](objective-data-standard.md)

### 2. 选择Auditor
- 根据评估目标选择对应的Auditor
- Tool Auditor：评估Tool特征
- Toy Auditor：评估Toy特征
- Trash Auditor：评估Trash特征

### 3. 读取检查清单
- 打开对应的Auditor指南文件
- 阅读完整的检查清单
- 理解评分逻辑和标准

### 4. 执行评估
- 逐项评估每个检查项
- 基于客观数据打分
- 记录评分理由和证据

### 5. 生成报告
- 汇总评分结果
- 生成标准格式的报告
- 执行Litmus Test

## 严格输出模板

**必遵** [auditor-templates.md](auditor-templates.md)：每个 Auditor 必须输出**完整填写的评分表格**（列：检查项ID | 检查项名称 | 满分 | 得分 | 简短理由≤50字），表格行数固定，不得省略，保证结果可复现。

## 报告格式要求

所有Auditor报告必须遵循统一的JSON格式，且**先输出表格再输出JSON**，包含：
- 基本信息（时间戳、Auditor类型）
- 信息来源声明（Brand-Blinded信息）
- 评分依据声明（检查清单名称）
- 总分和分项得分
- 检查项详细评分
- 客观数据摘要
- 优势和劣势
- 跨分类证据
- Litmus Test结果

## T3分类指南

- **文件路径**：[t3-classification.md](t3-classification.md)
- **内容**：T3分类定义、Litmus Test、Final Judge指南、分类判断逻辑
- **用途**：Final Judge综合三个Auditor报告，做出最终分类决策

## 相关参考文档

- [objective-data-standard.md](objective-data-standard.md)：客观数据标准
- [t3-taxonomy.md](t3-taxonomy.md)：T3分类详细说明（保留为历史参考）
- [peer-review-guide.md](peer-review-guide.md)：Peer Review流程指南

## 注意事项

1. **独立评估**：每个Auditor独立工作，不参考其他Auditor的报告
2. **信息隔离**：只能使用Brand-Blinded信息，严禁访问原始品牌信息
3. **客观数据**：所有评分必须基于客观数据，避免主观判断
4. **完整记录**：详细记录评分理由和证据
5. **诚实评估**：即使证据支持其他分类，也要如实记录

## 快速参考

### 评分逻辑对比

| Auditor | 评分逻辑 | 分数范围 | 分数含义 |
|---------|---------|---------|---------|
| Tool Auditor | 正向 | 0-100 | 分数越高，越符合Tool特征 |
| Toy Auditor | 正向 | 0-100 | 分数越高，越符合Toy特征 |
| Trash Auditor | 正向 | 0-100 | 分数越高，越符合Trash特征 |

### Litmus Test对比

| Auditor | Litmus Test问题 | 是 → | 否 → |
|---------|----------------|------|------|
| Tool Auditor | 明天坏了，工作流会停滞吗？ | Tool | 不是纯粹的Tool |
| Toy Auditor | 会放在显眼位置炫耀或收藏吗？ | Toy | 不是纯粹的Toy |
| Trash Auditor | 明天消失，世界会更好吗？ | Trash | 不是Trash |

### 综合评分计算

```
综合评分 = (Tool评分 + Toy评分 - Trash评分) / 3
```

- 所有Auditor：正向评分
- Tool和Toy：分数越高，越符合Tool/Toy特征
- Trash：分数越高，越符合Trash特征
- 综合评分范围：-100到100
  - 正值：偏向Tool/Toy
  - 负值：偏向Trash
  - 0附近：混合分类
