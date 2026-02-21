# Brand Blinding信息过滤指南

## 目录
- [Brand Blinding的目的](#brand-blinding的目的)
- [核心原则](#核心原则)
- [过滤规则](#过滤规则)
- [处理流程](#处理流程)
- [示例对比](#示例对比)
- [常见陷阱](#常见陷阱)

## Brand Blinding的目的

### 为什么需要Brand Blinding？

在评估智能硬件产品时，品牌影响力会干扰客观判断：
- **品牌光环效应**：知名品牌的产品容易被高估
- **营销话术干扰**：夸大宣传和情感化描述影响理性分析
- **社交偏见**：流行产品容易被过度美化

### Brand Blinding的目标

- **客观性**：去除品牌相关的所有主观影响
- **一致性**：所有产品基于相同标准评估
- **公平性**：不因品牌知名度而产生偏见
- **第一性原理**：回归产品本身的物理功能和逻辑

## 核心原则

### 1. 事实保留原则
- 保留所有客观的技术规格和参数
- 保留真实的功能描述
- 保留实际的使用场景

### 2. 主观移除原则
- 移除品牌名称和商标引用
- 移除营销话术和夸大描述
- 移除情感化形容词和主观评价

### 3. 中性重述原则
- 将主观描述重述为中性事实
- 将品牌相关内容重述为通用描述
- 保持信息的完整性和准确性

## 过滤规则

### 规则1：品牌名称移除

**需要移除**：
- 品牌名称（如"Apple"、"Dyson"、"Tesla"）
- 产品线名称（如"iPhone"、"AirPods"）
- 商标引用（如"AirTag"、"Kindle"）

**处理方式**：
- 替换为通用类别（如"智能手表"、"无线耳机"、"追踪器"）
- 如果品牌即产品类别，使用通用描述

**示例**：
```
原始：Apple Watch Series 9
Brand-Blinded：智能手表（第9代）
```

### 规则2：营销话术移除

**需要移除的营销词汇**：
- 夸大形容词："revolutionary"、"groundbreaking"、"ultimate"、"best-in-class"
- 模糊承诺："game-changing"、"life-changing"、"unprecedented"
- 营销口号："Designed by Apple in California"、"Think Different"

**处理方式**：
- 直接移除营销词汇
- 保留实际的功能描述
- 如果信息缺失，标注"未提供具体信息"

**示例**：
```
原始：revolutionary new sensor technology
Brand-Blinded：新型传感器技术
```

### 规则3：情感化描述移除

**需要移除的情感词汇**：
- 正面情感："amazing"、"stunning"、"beautiful"、"elegant"
- 负面情感："terrible"、"awful"、"poor"
- 主观评价："premium quality"、"high-end"、"luxury"

**处理方式**：
- 移除情感形容词
- 保留可验证的属性描述
- 将"premium"替换为具体材质或规格

**示例**：
```
原始：premium aluminum alloy body
Brand-Blinded：铝合金机身
```

### 规则4：功能性信息保留（必须完整保留）

**🔴 重要**：所有客观数据必须完整保留，不得移除或修改！

**必须保留的客观数据**（详见 [objective-data-standard.md](objective-data-standard.md)）：

#### 技术规格（Technical Specs）
- 处理器型号、核心数、主频
- 存储容量、存储类型
- 内存容量、内存类型
- 屏幕尺寸、分辨率、刷新率
- 电池容量、续航时间、充电功率
- WiFi版本、蓝牙版本
- 传感器列表
- 防护等级（IPXX）
- 重量、尺寸

#### 性能数据（Performance Data）
- 响应时间、处理能力
- 功耗数据
- 发热情况
- 噪音水平

#### 可靠性数据（Reliability Data）
- 故障率/MTBF
- 质保期
- 返修率
- 用户投诉率

#### 市场数据（Market Data）
- 上市时间
- 销量数据
- 用户评价数量、平均评分
- 第三方评分

#### 可持续性数据（Sustainability Data）
- 材料成分
- 可回收性
- 能耗等级
- 维修性

#### 成本数据（Cost Data）
- 标价、折扣后价格
- 维护成本
- 配件成本
- 订阅费用

**处理方式**：
- 完整保留所有客观数据
- 保持数据原始格式
- 保留数据来源标注
- 不得修改或省略任何客观数据

**示例**：
```
原始：Apple M2 chip with 8-core CPU, 256GB SSD storage
Brand-Blinded：processor: "M2", cpu_cores: 8, storage: "256GB SSD"
客观数据：完整保留
```

### 规则5：功能性信息保留

**必须保留**：
- 技术规格：尺寸、重量、电池容量、处理器型号
- 功能列表：支持的功能和特性
- 参数数据：续航时间、充电速度、精度等
- 使用场景：实际使用场景描述

**示例**：
```
原始：up to 18 hours of battery life
Brand-Blinded：续航时间：最长18小时
```

### 规则5：第三方评价处理

**需要移除**：
- 品牌相关评价："best in class"、"industry leader"
- 未验证的赞誉："highly rated"、"critically acclaimed"

**处理方式**：
- 移除未验证的评价
- 保留可验证的第三方认证或奖项（注明来源）
- 如果提到具体测试结果，保留数据

**示例**：
```
原始：rated 5 stars by 1000+ users
Brand-Blinded：用户评价：1000+用户评分（具体评分未提供）
```

## 处理流程

### 步骤1：识别品牌信息
扫描产品信息，识别：
- 品牌名称和商标
- 营销话术和宣传用语
- 情感化描述和主观评价

### 步骤2：分类处理
将识别到的信息分类：
- **品牌相关**：品牌名称、商标、品牌引用
- **营销相关**：营销话术、夸大描述
- **情感相关**：情感化形容词、主观评价
- **功能相关**：技术规格、功能列表、参数数据

### 步骤3：移除和替换
- **品牌相关**：替换为通用类别
- **营销相关**：直接移除
- **情感相关**：移除情感词汇，保留事实
- **功能相关**：完整保留

### 步骤4：验证和优化
- 检查信息完整性
- 确保无品牌残留
- 验证信息准确性
- 优化表述清晰度

## 示例对比

### 示例1：智能手表

**原始描述**：
```
Apple Watch Series 9 features Apple's revolutionary S9 chip, 
delivering stunning performance with the most advanced display 
ever. The beautiful aluminum case is crafted with premium materials, 
offering up to 18 hours of battery life. Rated 4.8 stars by users.
```

**Brand-Blinded描述**：
```
智能手表（第9代）配备S9芯片，显示屏具有高性能。铝合金机身，
续航时间最长18小时。用户评价：评分4.8/5。
```

### 示例2：无线耳机

**原始描述**：
```
Dyson Zone is the groundbreaking noise-canceling headphones with 
purifying visor, featuring amazing electrostatic technology. The 
elegant design provides ultimate comfort for all-day wear.
```

**Brand-Blinded描述**：
```
降噪耳机配备空气净化面罩，使用静电技术。设计舒适，适合全天候佩戴。
```

### 示例3：智能家居设备

**原始描述**：
```
Nest Learning Thermostat learns your schedule and programs itself, 
saving energy automatically. The beautiful design complements any home.
Energy Star certified.
```

**Brand-Blinded描述**：
```
智能恒温器学习用户使用习惯，自动调节温度以节省能源。设计简约。
Energy Star认证。
```

## 常见陷阱

### 陷阱1：过度删除
**问题**：删除过多信息，导致产品功能描述不完整

**解决**：
- 区分品牌信息和功能信息
- 保留所有技术规格和参数
- 确保功能描述完整

### 陷阱2：信息丢失
**问题**：移除营销话术后，关键功能信息缺失

**解决**：
- 如果营销话术中包含实际功能，提取功能部分
- 使用中性语言重新描述
- 标注信息来源

### 陷阱3：品牌残留
**问题**：品牌名称或引用未完全移除

**解决**：
- 检查所有品牌名称和商标
- 检查品牌相关的形容词（如"Apple-like"）
- 检查第三方评价中的品牌引用

### 陷阱4：上下文断裂
**问题**：移除品牌信息后，描述变得不连贯

**解决**：
- 使用通用词汇保持连贯性
- 适当补充上下文信息
- 确保描述逻辑清晰

## Brand Blinding检查清单

在完成Brand Blinding后，检查：
- [ ] 所有品牌名称已移除或替换
- [ ] 所有营销话术已移除
- [ ] 所有情感化形容词已移除
- [ ] 所有技术规格已保留
- [ ] 所有功能描述已保留
- [ ] 描述逻辑清晰连贯
- [ ] 无品牌残留
- [ ] 信息完整准确

## 智能体执行要点

### 作为智能体执行Brand Blinding时：

1. **系统性扫描**：逐段检查产品信息
2. **上下文理解**：理解品牌词汇在上下文中的作用
3. **智能替换**：选择最合适的通用词汇
4. **验证检查**：完成后自我检查是否有遗漏
5. **标注说明**：在报告中说明Brand Blinding的处理范围

### 输出格式

Brand-Blinded产品信息应包含：
```
原始信息：[原始描述]
Brand-Blinded信息：[处理后的描述]
处理说明：
  - 移除的品牌信息：[列表]
  - 移除的营销话术：[列表]
  - 保留的功能信息：[列表]
  - 替换的词汇：[原词] → [替换词]
```
