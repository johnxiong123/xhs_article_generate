# Article Skill 本地化改写设计方案

**Date:** 2026-04-21
**Status:** Approved

## 背景

article-skill 当前使用飞书文档作为输入输出，需要添加本地文件支持，同时增加风格分析能力。

## 目标

- 支持本地 docx 文件作为输入（原始稿件 + 参考范文）
- 支持本地 markdown 文件作为输出
- 增加 style_analyzer 模块学习参考稿件风格
- 改进 prompt 结构，提升生成质量

## 架构

### 保留模块

| 文件 | 功能 |
|------|------|
| `feishu_reader.py` | 飞书文档读取 |
| `feishu_writer.py` | 飞书文档写入 |
| `article_generator.py` | DeepSeek API 稿件生成 |
| `validators.py` | 关键词验证 |

### 新增模块

| 文件 | 功能 | 来源 |
|------|------|------|
| `word_reader.py` | 读取本地 docx 文件 | 复用 rewrite-skill |
| `local_writer.py` | 写入本地 markdown 文件 | 复用 rewrite-skill |
| `style_analyzer.py` | 分析参考稿件风格 | 复用 rewrite-skill |

### 重构模块

| 文件 | 改动 |
|------|------|
| `prompt_builder.py` | 改进 prompt 结构，参考 rewrite prompt 重构 |
| `skill.py` | 支持 `mode="local"` / `mode="feishu"` 切换 |

## 目录结构

```
xiaohongshu-article-skill/
├── data/
│   ├── original/          # 原始稿件（docx）
│   └── references/        # 参考范文（docx）
├── output/                # 生成稿件输出
├── src/
│   ├── skill.py           # 主入口（支持双模式）
│   ├── feishu_reader.py   # 保留
│   ├── feishu_writer.py   # 保留
│   ├── word_reader.py     # 新增
│   ├── local_writer.py    # 新增
│   ├── style_analyzer.py  # 新增
│   ├── prompt_builder.py  # 重构
│   ├── article_generator.py
│   └── validators.py
└── prompts/
    └── write_article.md   # 重构 prompt 模板
```

## Prompt 重构方案

### 新结构（按优先级排列）

```
1. 角色定义
2. 范文原文（完整展示，作为写作范例）
3. 风格特征提炼（语气、句式、结构、标签使用方式）
4. 写作要求（场景+关键词+人设）
5. 输出格式
```

### 各部分具体设计

#### 1. 角色定义
不变，沿用现有描述。

#### 2. 范文原文
将参考范文中最典型的一篇完整内容作为"写作范例"展示给模型。

#### 3. 风格特征提炼
- 语气风格（口语化程度、情感强度）
- 开头方式（故事型/疑问型/陈述型）
- 段落结构（长短句比例、段落数量）
- 句式特征（常用句型、修辞手法）
- 标签使用（数量、位置、风格）

#### 4. 写作要求
- 场景列表
- 必须包含的关键词
- 人设要求
- 额外写作要求
- 字数要求

#### 5. 输出格式
标题 + 正文 + 标签

## skill.py 双模式设计

```python
class XiaohongshuArticleSkill:
    def __init__(self, mode: str = "local"):
        """
        mode: "local" | "feishu"
        """
        self.mode = mode

        if mode == "local":
            self.reader = WordReader()
            self.writer = LocalWriter()
        else:
            self.reader = FeishuReader()
            self.writer = FeishuWriter()

        self.style_analyzer = StyleAnalyzer()
        self.prompt_builder = PromptBuilder()
        self.article_generator = ArticleGenerator()
```

## 文件修改清单

1. **新增** `src/word_reader.py` — 复用 rewrite-skill 代码
2. **新增** `src/local_writer.py` — 复用 rewrite-skill 代码
3. **新增** `src/style_analyzer.py` — 复用 rewrite-skill 代码
4. **重构** `src/prompt_builder.py` — 改进 prompt 结构
5. **重构** `src/skill.py` — 支持双模式
6. **重构** `prompts/write_article.md` — 新 prompt 模板
7. **新增** `data/original/` 目录
8. **新增** `data/references/` 目录
9. **新增** `output/` 目录

## 验证方式

1. 本地模式测试：
   - 在 `data/references/` 放置参考范文
   - 运行 `python3 src/interactive_cli.py --mode local`
   - 确认稿件生成到 `output/` 目录

2. 飞书模式测试：
   - 保持原有流程不变
   - 确认双模式切换正常