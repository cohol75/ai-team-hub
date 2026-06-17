# AI Team Hub — Skill 双段式格式规范

每个 Skill 由两段组成：**人读说明**（Markdown）和 **Agent 执行指令**（YAML）。

## 第一段：人读说明（Human Section）

自由格式的 Markdown 文档。建议包含：
- 功能描述
- 使用场景
- 使用方式/示例
- 注意事项

## 第二段：Agent 执行指令（Agent Section）

严格 YAML 格式，Pydantic 校验。必须符合以下 Schema：

```yaml
# ---- 必填字段 ----
name: "skill-name-slug"        # 小写字母、数字、连字符，3-80 字符
version: "1.0.0"               # SemVer 格式
description: "..."              # 10-500 字符
category: "code-review"        # 固定枚举值（见下方列表）
steps:                          # 1-20 个步骤
  - step: 1                    # 整数，从 1 开始连续
    action: "analyze"          # 固定枚举值
    instruction: "..."         # 10-5000 字符，Markdown
    expected_output: "..."     # 10-1000 字符

# ---- 可选字段 ----
model: "claude-opus-4"
model_provider: "anthropic"
tags: ["python", "fastapi"]
input_description: "..."
output_description: "..."
dependencies: ["pytest >= 7.0"]
```

### Category 枚举

`code-review` | `debugging` | `deployment` | `testing` | `architecture` | `documentation` | `refactoring` | `performance` | `security` | `data-processing` | `frontend` | `devops` | `other`

### Action 枚举

`analyze` | `execute` | `generate` | `review` | `test` | `deploy`

- `execute` 类型的步骤 **必须** 提供 `command` 字段

### 完整示例

```yaml
name: python-code-review
version: "1.0.0"
description: "Automated Python code review: check style, bugs, and suggest improvements"
category: code-review
model: claude-opus-4
model_provider: anthropic
tags:
  - python
  - flake8
  - linting
input_description: "Python source code to review"
output_description: "Markdown report with issues and fix suggestions"
steps:
  - step: 1
    action: analyze
    instruction: "Read the provided Python code and identify potential issues in: style (PEP 8), type safety, exception handling, and performance"
    expected_output: "A list of issues found, each with severity level (error/warning/info)"
  - step: 2
    action: generate
    instruction: "For each issue found in step 1, generate a specific fix suggestion with code example"
    expected_output: "A markdown report with: summary stats, per-file issues list, fix suggestions with code diffs"
```

## 校验规则

提交时平台自动校验：
1. YAML 可解析
2. 所有必填字段存在且类型正确
3. `name` 符合 slug 正则：`^[a-z0-9]+(-[a-z0-9]+)*$`
4. `category` 在枚举列表中
5. `action` 在枚举列表中
6. `execute` action 必须有 `command`
7. 步骤编号连续从 1 开始
8. 字段长度限制
