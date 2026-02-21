# T3分类与Final Judge指南

## 目录
- [T3分类定义](#t3分类定义)
- [Litmus Test](#litmus-test)
- [Final Judge角色](#final-judge角色)
- [分类判断逻辑](#分类判断逻辑)
- [综合评分计算](#综合评分计算)
- [分类决策流程](#分类决策流程)

## T3分类定义

### Tool（工具）
**核心特征**：解决实际、明确的问题

**关键指标**：
- 实用性：解决真实痛点
- 可靠性：高稳定性，不引人注目
- 效率：成为用户工作流的一部分
- 依赖性：用户需要定期使用

**示例**：
- 🟢 高端工具：Apple AirPods、Dyson吸尘器
- 🟡 兼具Toy属性：高端咖啡机（好用+美观）

### Toy（玩具）
**核心特征**：带来感官愉悦、惊喜和情感满足

**关键指标**：
- 乐趣：带来直接的情感满足
- 惊喜：超出预期的正面体验
- 情感联结：建立情感联系和记忆
- 可探索性：提供探索和发现的空间

**示例**：
- 🟡 兼具Tool属性：游戏主机（娱乐+功能）
- 🔴 接近Trash：无实用价值的网红产品

### Trash（垃圾）
**核心特征**：违背设计原则，缺乏清晰价值，制造问题而非解决问题

**关键指标**：
- 设计违背：违背基本设计原则
- 问题制造：制造新问题
- 价值缺失：缺乏清晰价值主张
- 可替代性：容易被替代或淘汰

**示例**：
- 🔴 纯粹Trash：山寨产品、伪创新产品
- 🟡 接近Trash：过度营销的平庸产品

### 混合分类
现实中的产品往往兼具多个分类特征：

**Tool + Toy**（最多见）
- 示例：Apple AirPods、高端咖啡机、智能手表
- 特征：既实用又美观，既解决问题又带来愉悦

**Toy + Trash**
- 示例：网红小家电（好看但无实用价值）
- 特征：外观吸引人，但缺乏实际功能

**Tool + Trash**
- 示例：必需但设计糟糕的产品
- 特征：功能必需，但用户体验差

## Litmus Test

### Tool Litmus Test
**问题**："如果明天它坏了，用户的工作流会停滞吗？"
- **是** → Tool
- **否** → 不是纯粹的Tool

### Toy Litmus Test
**问题**："用户是否会把它放在显眼的位置'炫耀'或收藏？"
- **是** → Toy
- **否** → 不是纯粹的Toy

### Trash Litmus Test
**问题**："如果这个产品明天消失，世界会变得更好还是更糟？"
- **更好** → Trash
- **更糟** → 不是Trash
- **无影响** → 可能是Trash（无存在价值）

## Final Judge角色

### 核心职责
Final Judge（最终裁决者）基于三个独立Auditor的报告，综合评估并做出最终分类决策。

### 工作原则
1. **客观公正**：基于客观数据和事实，避免主观偏见
2. **信息隔离**：不访问原始品牌信息，仅基于Brand-Blinded信息
3. **综合权衡**：综合考虑三个Auditor的评分和证据
4. **透明决策**：分类决策必须有明确的理由和依据

### 输入信息
- Tool Auditor报告（总分0-100）
- Toy Auditor报告（总分0-100）
- Trash Auditor报告（总分0-100，反向评分）

### 输出信息
- 最终分类结果
- 分类理由
- 主导分类
- 次要分类（如有）
- 综合评分

## 分类判断逻辑

### Step 1: 计算综合评分

```python
def calculate_composite_score(tool_score, toy_score, trash_score):
    """
    计算综合评分

    Args:
        tool_score: Tool Auditor评分（0-100，正向）
        toy_score: Toy Auditor评分（0-100，正向）
        trash_score: Trash Auditor评分（0-100，正向）

    Returns:
        composite_score: 综合评分（-100到100）
    """
    # 综合评分 = (Tool + Toy - Trash) / 3
    # 所有Auditor都是正向评分，Trash分数越高越Trash
    composite = (tool_score + toy_score - trash_score) / 3
    return composite
```

**评分解释**：
- **综合评分 > 30**：强烈偏向Tool/Toy
- **综合评分 0-30**：偏向Tool/Toy
- **综合评分 -30-0**：偏向Trash
- **综合评分 < -30**：强烈偏向Trash

### Step 2: 确定主导分类

#### 判断Tool是否为主导
**条件**（满足2个以上）：
- Tool评分 ≥ 70
- Tool评分 > Toy评分 + 15
- Tool评分 > Trash评分 + 15
- Litmus Test结果为"是"

#### 判断Toy是否为主导
**条件**（满足2个以上）：
- Toy评分 ≥ 70
- Toy评分 > Tool评分 + 15
- Toy评分 > Trash评分 + 15
- Litmus Test结果为"是"

#### 判断Trash是否为主导
**条件**（满足2个以上）：
- Trash评分 ≥ 70（正向评分，越高越Trash）
- Trash评分 > Tool评分 + 15
- Trash评分 > Toy评分 + 15
- Litmus Test结果为"更好"

### Step 3: 确定次要分类

**Tool主导时，次要分类判断**：
- Toy评分 ≥ 60 且 Toy评分 > Trash评分 + 15 → 次要分类：Toy
- Trash评分 ≥ 60 且 Trash评分 > Toy评分 + 15 → 次要分类：Trash

**Toy主导时，次要分类判断**：
- Tool评分 ≥ 60 且 Tool评分 > Trash评分 + 15 → 次要分类：Tool
- Trash评分 ≥ 60 且 Trash评分 > Tool评分 + 15 → 次要分类：Trash

**Trash主导时，次要分类判断**：
- Tool评分 ≥ 50 → 次要分类：Tool
- Toy评分 ≥ 50 → 次要分类：Toy
- Tool和Toy都 ≥ 50 → 次要分类：Tool + Toy

### Step 4: 特殊情况处理

**无明确主导**：
- 三个评分都接近（差异<15）→ 混合分类
- 综合评分在-15到15之间 → 混合分类

**矛盾评分**：
- Tool评分高但Trash Litmus Test为"更好" → 深入审查
- Toy评分高但Trash评分低 → 深入审查
- 需要重新审视客观数据

## 综合评分计算

### 评分权重
- **Tool Auditor**：1.0（正向）
- **Toy Auditor**：1.0（正向）
- **Trash Auditor**：-1.0（反向）

### 计算公式
```
综合评分 = (Tool评分 + Toy评分 - Trash评分) / 3
```

### 评分范围
- **最小值**：-100（Tool=0, Toy=0, Trash=100）
- **最大值**：100（Tool=100, Toy=100, Trash=0）
- **中值**：0（Tool=33.3, Toy=33.3, Trash=33.3）

### 评分解释

| 综合评分区间 | 分类倾向 | 说明 |
|------------|---------|------|
| 70-100 | 强烈Tool/Toy | 明确的Tool或Toy特征 |
| 40-69 | 明显Tool/Toy | Tool/Toy特征明显 |
| 15-39 | 偏向Tool/Toy | Tool/Toy特征占优 |
| -14-14 | 混合 | 各特征均衡，无明显倾向 |
| -39--15 | 偏向Trash | Trash特征占优 |
| -69--40 | 明显Trash | Trash特征明显 |
| -100--70 | 强烈Trash | 明确的Trash特征 |

## 分类决策流程

### 完整流程图

```
┌─────────────────────────────────────┐
│ 1. 接收三个Auditor报告              │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 2. 计算综合评分                     │
│    Composite = (Tool + Toy - Trash)/3 │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 3. 确定主导分类                     │
│    - 检查每个分类的判断条件         │
│    - 确定1个主导分类                │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 4. 确定次要分类（如有）             │
│    - 检查其他分类的评分             │
│    - 确定是否满足次要分类条件       │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 5. 生成最终分类决策                 │
│    - 记录分类理由                   │
│    - 生成分类报告                   │
└─────────────────────────────────────┘
```

### 决策模板

```json
{
  "final_judge": {
    "timestamp": "2024-01-01T00:00:00Z",
    "auditor_reports": {
      "tool": {
        "total_score": 82,
        "litmus_test": {"answer": "是", "confidence": "高"}
      },
      "toy": {
        "total_score": 75,
        "litmus_test": {"answer": "是", "confidence": "中等"}
      },
      "trash": {
        "total_score": 25,
        "litmus_test": {"answer": "无影响", "confidence": "中等"}
      }
    },
    "composite_score": 44.0,
    "classification": {
      "primary": "Tool",
      "secondary": ["Toy"],
      "final_label": "Tool + Toy"
    },
    "decision_reasoning": {
      "primary_reason": "Tool评分最高（82），且显著高于Trash评分（差异57），明确符合Tool特征",
      "secondary_reason": "Toy评分较高（75），仅次于Tool评分，产品兼具Toy属性",
      "composite_interpretation": "综合评分44，偏向Tool/Toy",
      "litmus_test_consistency": "Tool和Toy的Litmus Test结果均为'是'，与分类一致"
    },
    "confidence": "高",
    "information_source": "Brand-Blinded产品信息（三个独立Auditor报告）"
  }
}
```

## 分类报告格式

### 必须包含的信息

1. **基本信息**
   - 时间戳
   - 产品标识（Brand-Blinded）
   - 信息来源声明

2. **Auditor报告汇总**
   - 三个Auditor的总分
   - 三个Litmus Test结果

3. **综合评分**
   - 综合评分计算结果
   - 评分解释

4. **分类决策**
   - 主导分类
   - 次要分类（如有）
   - 最终分类标签

5. **决策理由**
   - 主导分类理由
   - 次要分类理由（如有）
   - 综合评分解释
   - Litmus Test一致性分析

6. **置信度**
   - 决策置信度（高/中/低）
   - 不确定因素（如有）

## 注意事项

1. **信息隔离**：Final Judge也只能访问Brand-Blinded信息
2. **客观数据**：分类决策必须基于客观数据
3. **透明决策**：分类理由必须清晰明确
4. **处理矛盾**：遇到矛盾评分时，需要深入审查
5. **记录完整**：所有决策过程必须完整记录
