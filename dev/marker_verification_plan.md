# 标记验证计划 (Marker Verification Plan)

## 第一部分：理论验证 (无需数据)

### 1. 预期的标记结构

根据EEG_Segmentation.xlsx分析：

#### **完整标记列表** (38个标记/会话)

```
会话结构：
├─ eye_closed (1个)          ← 基线：眼睛闭合
│
├─ 问题1-6循环 (6×6=36个)
│  对于每个问题 {N = 1-6}:
│  ├─ {N}_problem    (1个)   ← 问题呈现
│  ├─ {N}_type       (1个)   ← 用户输入/打字
│  ├─ {N}_rate       (1个)   ← 评分 (解答前)
│  ├─ {N}_solution   (1个)   ← 答案显示
│  ├─ {N}_eval       (1个)   ← 评价/反馈
│  └─ {N}_rate       (1个)   ← 评分 (解答后)
│
└─ eye_closed_2 (1个)        ← 基线：眼睛闭合 (结束)

总计: 1 + 36 + 1 = 38 个标记
```

### 2. 每个标记的定义

| # | 标记名称 | 代码 | 类型 | 描述 | 预期出现次数 |
|---|---------|------|------|------|------------|
| 1 | eye_closed | EC | 基线 | 眼睛闭合, 无刺激 | 1 |
| 2-7 | 1_problem | PROB | 刺激 | 问题1呈现 | 1 |
| 8 | 1_type | TYPE | 响应 | 用户输入答案1 | 1 |
| 9 | 1_rate | RATE | 评分 | 用户评分自信度(前) | 1 |
| 10 | 1_solution | SOL | 反馈 | 显示正确答案1 | 1 |
| 11 | 1_eval | EVAL | 反馈 | 显示评价/分数 | 1 |
| 12 | 1_rate | RATE | 评分 | 用户评分自信度(后) | 1 |
| ... | ... | ... | ... | ... | ... |
| 37 | 6_rate | RATE | 评分 | 用户评分自信度(后) | 1 |
| 38 | eye_closed_2 | EC | 基线 | 眼睛闭合, 结束 | 1 |

### 3. 标记序列验证规则

```
规则1：顺序必须正确
✓ 必须以 eye_closed 开始
✓ 必须以 eye_closed_2 结束
✓ 问题必须按顺序 (1-6)

规则2：完整性检查
✓ 每个问题必须有 6 个标记
✓ 缺少任何标记 = 不完整

规则3：计数验证
✓ eye_closed: 1个
✓ eye_closed_2: 1个
✓ {N}_problem: 6个 (每个问题1个)
✓ {N}_type: 6个 (每个问题1个)
✓ {N}_rate: 12个 (每个问题2个)
✓ {N}_solution: 6个 (每个问题1个)
✓ {N}_eval: 6个 (每个问题1个)

总计: 1 + 6 + 6 + 12 + 6 + 6 + 1 = 38个

规则4：时间间隔验证
✓ eye_closed 应该持续 ~30-60 秒
✓ 每个问题周期应该 ~20-40 秒
✓ 标记应该有逻辑的时间顺序
```

### 4. 可能的标记代码映射

BrainVision 格式可能使用数字代码：

```
推测的标记代码 (需要从PDF/documentation确认):

刺激码示例:
S  1  ← Problem
S  2  ← Solution  
S  3  ← Rating
S  4  ← Evaluation
S  5  ← Typing
S  6  ← Eye Closed

或者使用问题编号:
S 10  ← Problem 1
S 20  ← Problem 2
S 30  ← Problem 3
...
S 60  ← Problem 6

实际映射需要从PDF或原始代码确认！
```

### 5. 可能的不匹配情况 (Record Mismatches)

```
预期的不匹配类型：

不匹配1：标记名称不同
- 预期: "problem"
- 实际: "S 10" 或 "PROB" 或 "Stimulus"
→ 需要映射表

不匹配2：标记缺失
- 预期: 38个标记
- 实际: 36个标记
→ 某些事件未被记录

不匹配3：额外标记
- 预期: 38个标记
- 实际: 42个标记
→ 额外的标记或重复

不匹配4：顺序错误
- 预期: problem → type → rate → solution → eval → rate
- 实际: problem → rate → type → solution → eval → rate
→ 实验流程不同

不匹配5：计数错误
- 预期: 每个问题出现1次
- 实际: 某个问题出现0次或2次
→ 试验中断或重复
```

---

## 第二部分：实际验证 (需要数据)

### 使用 load_data.py 进行验证

```python
import mne
from pathlib import Path

# 当有数据时运行
file_path = "path/to/eeg_file.vhdr"
raw = mne.io.read_raw_brainvision(file_path, preload=True)

# 提取事件
events, event_id = mne.events_from_annotations(raw)

# 验证步骤
print("已提取的事件代码:")
for name, code in event_id.items():
    count = sum(1 for e in events if e[2] == code)
    print(f"  {name}: {count}个")

# 比较与预期
expected_counts = {
    'eye_closed': 1,
    '1_problem': 1,
    # ... 等等
}

for marker, expected in expected_counts.items():
    actual = sum(1 for e in events if event_id.get(marker) == e[2])
    match = "✓" if actual == expected else "✗"
    print(f"{match} {marker}: 预期={expected}, 实际={actual}")
```

---

## 第三部分：文档验证

### 从PDF提取标记信息

```
需要从 "Cognitive studies of design_experiment notebook.pdf" 确认:

1. 实验设计
   - 有多少个问题? (应该是6)
   - 每个问题的流程是什么?
   - 有哪些事件?

2. 标记定义
   - 每个事件用什么代码表示?
   - 时间点是什么?
   - 持续时间是多少?

3. 特殊情况
   - 是否有测试/练习试验?
   - 是否有中断/重新开始?
   - 是否有多个会话?

4. 基线条件
   - eye_closed 应该持续多长?
   - 在开始和结束都有吗?
   - 是否还有其他基线?
```

---

## 验证检查清单

### ✓ 理论验证 (现在能做)
- [ ] 创建标记定义表
- [ ] 定义预期的标记序列
- [ ] 列出所有可能的不匹配情况
- [ ] 创建标记代码映射表(推测)
- [ ] 定义验证规则
- [ ] 准备验证脚本

### ✓ 文档验证 (现在能做)
- [ ] 阅读PDF文档
- [ ] 提取标记定义信息
- [ ] 确认实验设计
- [ ] 记录所有发现

### ⏳ 实际验证 (需要数据)
- [ ] 运行 load_data.py 读取EEG文件
- [ ] 提取实际标记
- [ ] 与预期标记比较
- [ ] 记录所有不匹配
- [ ] 创建标记映射表

---

## 输出文件

```
验证完成后应该有:

1. marker_definitions.csv
   - 标记名称
   - 标记代码
   - 描述
   - 预期计数

2. marker_mismatches.txt
   - 记录所有发现的差异
   - 标记代码的实际映射
   - 可能的解释

3. verification_report.md
   - 详细的验证报告
   - 通过/失败状态
   - 建议的解决方案
```

---

## 现在就能做的任务清单

- [ ] 1. 分析PDF文档
- [ ] 2. 创建标记定义表
- [ ] 3. 定义验证规则
- [ ] 4. 准备验证脚本
- [ ] 5. 创建不匹配记录表
- [ ] 6. 准备标记映射框架

**一旦获得September数据，直接运行验证！**
