# Article Skill 本地化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 article-skill 改写为支持本地文件输入输出，同时保留飞书模式

**Architecture:** 参照 rewrite-skill 架构，新增 WordReader/LocalWriter/StyleAnalyzer 模块，修改 skill.py 支持双模式切换，重构 prompt 结构。

**Tech Stack:** Python 3, python-docx, 复用 rewrite-skill 代码

---

## 文件结构

```
xiaohongshu-article-skill/
├── data/
│   ├── original/          # 原始稿件（新增）
│   └── references/        # 参考范文（新增）
├── output/                # 生成稿件输出（新增）
├── src/
│   ├── skill.py           # 修改：支持 mode 参数
│   ├── word_reader.py     # 新增：复制自 rewrite-skill
│   ├── local_writer.py    # 新增：复制自 rewrite-skill
│   ├── style_analyzer.py  # 新增：复制自 rewrite-skill
│   └── interactive_cli.py # 修改：支持 --mode 参数
└── prompts/
    └── write_article.md   # 重构 prompt 模板
```

---

## Task 1: 创建目录结构

**Files:**
- Create: `data/original/` (directory)
- Create: `data/references/` (directory)
- Create: `output/` (directory)

- [ ] **Step 1: 创建目录**

Run: `mkdir -p /Users/admin/claude_ref/xiaohongshu-article-skill/data/original /Users/admin/claude_ref/xiaohongshu-article-skill/data/references /Users/admin/claude_ref/xiaohongshu-article-skill/output`

- [ ] **Step 2: 创建 .gitkeep 文件保持目录**

Run: `touch /Users/admin/claude_ref/xiaohongshu-article-skill/data/original/.gitkeep /Users/admin/claude_ref/xiaohongshu-article-skill/data/references/.gitkeep /Users/admin/claude_ref/xiaohongshu-article-skill/output/.gitkeep`

- [ ] **Step 3: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add data/original/ data/references/ output/
git commit -m "$(cat <<'EOF'
feat: add data directories for local file input/output

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 新增 word_reader.py

**Files:**
- Create: `src/word_reader.py` (复制自 rewrite-skill)

- [ ] **Step 1: 复制 word_reader.py**

Run: `cp /Users/admin/claude_ref/xiaohongshu-rewrite-skill/src/word_reader.py /Users/admin/claude_ref/xiaohongshu-article-skill/src/word_reader.py`

- [ ] **Step 2: 验证文件内容**

Run: `head -20 /Users/admin/claude_ref/xiaohongshu-article-skill/src/word_reader.py`
Expected: 包含 "Word文档读取器" 和 `class WordReader`

- [ ] **Step 3: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add src/word_reader.py
git commit -m "$(cat <<'EOF'
feat: add WordReader for reading local docx files

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: 新增 local_writer.py

**Files:**
- Create: `src/local_writer.py` (复制自 rewrite-skill)

- [ ] **Step 1: 复制 local_writer.py**

Run: `cp /Users/admin/claude_ref/xiaohongshu-rewrite-skill/src/local_writer.py /Users/admin/claude_ref/xiaohongshu-article-skill/src/local_writer.py`

- [ ] **Step 2: 验证文件内容**

Run: `head -20 /Users/admin/claude_ref/xiaohongshu-article-skill/src/local_writer.py`
Expected: 包含 "本地文件写入器" 和 `class LocalWriter`

- [ ] **Step 3: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add src/local_writer.py
git commit -m "$(cat <<'EOF'
feat: add LocalWriter for writing markdown output

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 新增 style_analyzer.py

**Files:**
- Create: `src/style_analyzer.py` (复制自 rewrite-skill)

- [ ] **Step 1: 复制 style_analyzer.py**

Run: `cp /Users/admin/claude_ref/xiaohongshu-rewrite-skill/src/style_analyzer.py /Users/admin/claude_ref/xiaohongshu-article-skill/src/style_analyzer.py`

- [ ] **Step 2: 验证文件内容**

Run: `head -20 /Users/admin/claude_ref/xiaohongshu-article-skill/src/style_analyzer.py`
Expected: 包含 "风格分析器" 和 `class StyleAnalyzer`

- [ ] **Step 3: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add src/style_analyzer.py
git commit -m "$(cat <<'EOF'
feat: add StyleAnalyzer for learning reference article style

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: 重构 prompts/write_article.md

**Files:**
- Modify: `prompts/write_article.md` (完全重写)

- [ ] **Step 1: 备份原文件**

Run: `cp /Users/admin/claude_ref/xiaohongshu-article-skill/prompts/write_article.md /Users/admin/claude_ref/xiaohongshu-article-skill/prompts/write_article.md.bak`

- [ ] **Step 2: 写入新的 prompt 模板**

Write to `prompts/write_article.md`:

```markdown
# 小红书素人稿件写作 Prompt

## 角色定义
你是一个专业的小红书素人稿件写作者，擅长根据参考范文生成符合特定风格的内容。

## 范文原文
以下是一篇典型的素人稿件，作为你写作的参考范例：

{reference_article}

## 风格特征提炼
根据范文分析得出的风格特点：
- 语气风格：{tone}
- 开头方式：{opening_style}
- 段落结构：{paragraph_structure}
- 句式特征：{sentence_features}
- 标签使用：{tag_usage}

## 写作要求

**场景：** {scenes}

**人设：** {persona}

**必须包含的关键词：** {keywords}

**字数要求：** {word_count}

**风格要求：** {style}

**额外要求：** {requirements}

## 输出格式
每篇文章包含：
- 标题：简洁有吸引力
- 正文：符合上述风格特征
- 标签：3-5个相关标签

---
【稿件1】
标题：
正文：
标签：
---
【稿件2】
标题：
正文：
标签：
---
（以此类推）
```

- [ ] **Step 3: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add prompts/write_article.md
git commit -m "$(cat <<'EOF'
refactor: restructure write_article prompt template

新的 prompt 结构：
1. 角色定义
2. 范文原文（完整展示）
3. 风格特征提炼
4. 写作要求
5. 输出格式

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: 重构 prompt_builder.py

**Files:**
- Modify: `src/prompt_builder.py`

**Changes:** 修改 `build_prompt()` 方法以适配新模板，添加风格分析调用，提取范文中最典型的一篇

- [ ] **Step 1: 读取当前文件**

Read: `src/prompt_builder.py`

- [ ] **Step 2: 重写 prompt_builder.py**

Write to `src/prompt_builder.py`:

```python
"""
Prompt组装器
将场景+人设+参考+关键词组装成写作Prompt
"""

import os
from typing import List, Dict
from pathlib import Path


class PromptBuilder:
    """组装写作Prompt"""

    def __init__(self, template_path: str = None):
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__), "..", "prompts", "write_article.md"
            )
        with open(template_path, "r", encoding="utf-8") as f:
            self.template = f.read()

    def build_prompt(
        self,
        scenes: List[str],
        persona: str,
        reference_articles: List[Dict],
        keywords: List[str],
        requirements: str = "",
        article_count: int = 5,
        word_count: str = "800-1000字",
        style: str = "素人口吻，轻松自然，第一人称",
        style_features: Dict = None,
    ) -> str:
        """
        组装完整的写作Prompt

        Args:
            scenes: 场景列表
            persona: 人设要求
            reference_articles: 参考文章列表
            keywords: 必须包含的关键词
            requirements: 额外写作要求
            article_count: 生成文章数量
            word_count: 字数要求
            style: 风格要求
            style_features: 风格特征字典（来自 StyleAnalyzer）

        Returns:
            组装后的完整Prompt
        """
        # 格式化场景
        scenes_text = "、".join(scenes) if scenes else "通用场景"

        # 格式化参考稿件 - 提取最典型的一篇作为范文
        reference_article = self._extract_main_reference(reference_articles)

        # 格式化关键词
        keywords_text = "、".join(keywords) if keywords else "无"

        # 从 style_features 提取风格特征（或使用默认值）
        if style_features:
            tone = style_features.get("tone", "自然亲切")
            opening_style = style_features.get("opening_style", "故事型开头")
            paragraph_structure = style_features.get("paragraph_structure", "短段落为主")
            sentence_features = style_features.get("sentence_features", "短句、口语化")
            tag_usage = style_features.get("tag_usage", "")
        else:
            tone, opening_style, paragraph_structure, sentence_features, tag_usage = self._infer_style_features(
                reference_articles
            )

        # 填充模板
        prompt = self.template.format(
            scenes=scenes_text,
            persona=persona,
            reference_article=reference_article,
            keywords=keywords_text,
            requirements=requirements or "无特殊要求",
            count=article_count,
            word_count=word_count,
            style=style,
            tone=tone,
            opening_style=opening_style,
            paragraph_structure=paragraph_structure,
            sentence_features=sentence_features,
            tag_usage=tag_usage,
        )

        return prompt

    def _extract_main_reference(self, articles: List[Dict]) -> str:
        """从参考文章中提取最典型的一篇作为范文"""
        if not articles:
            return "无参考稿件，请使用通用素人风格写作"

        # 选择第一篇作为主范文
        article = articles[0]
        title = article.get("title", "无标题")
        content = article.get("content", [])
        tags = article.get("tags", [])

        if isinstance(content, list):
            content_text = "\n".join(content)
        else:
            content_text = str(content)

        tags_text = " ".join([f"#{t}" for t in tags]) if tags else ""

        result = f"标题：{title}\n\n内容：\n{content_text}"
        if tags_text:
            result += f"\n\n标签：{tags_text}"

        return result

    def _infer_style_features(self, articles: List[Dict]) -> tuple:
        """从参考文章推断风格特征（简单版本）"""
        if not articles:
            return ("自然亲切", "故事型开头", "短段落为主", "短句、口语化", "")

        # 合并所有内容进行统计
        all_content = ""
        all_tags = []
        for a in articles:
            c = a.get("content", "")
            if isinstance(c, list):
                all_content += " ".join(c)
            else:
                all_content += str(c)
            tags = a.get("tags", [])
            if isinstance(tags, list):
                all_tags.extend(tags)
            elif tags:
                all_tags.append(tags)

        # 简单推断
        first_person = "我" in all_content
        tone = "第一人称" if first_person else "第三人称"
        tone = "自然亲切，" + tone

        # 检查开头方式
        opening_starts = []
        for a in articles:
            c = a.get("content", "")
            if isinstance(c, list) and c:
                first_line = c[0][:20] if c else ""
            else:
                first_line = str(c)[:20] if c else ""
            opening_starts.append(first_line)

        opening_style = "故事型开头"

        # 段落结构（基于总字数/段落数估算）
        total_paras = sum(len(a.get("content", [])) for a in articles)
        avg_paras = total_paras / len(articles) if articles else 0
        if avg_paras > 10:
            paragraph_structure = "长段落为主"
        else:
            paragraph_structure = "短段落为主"

        # 句式特征
        sentence_features = "短句、口语化"

        # 标签使用
        tag_usage = " ".join([f"#{t}" for t in all_tags[:5]]) if all_tags else ""

        return (tone, opening_style, paragraph_structure, sentence_features, tag_usage)

    def _format_reference_articles(self, articles: List[Dict]) -> str:
        """格式化参考文章（兼容旧方法）"""
        if not articles:
            return "无参考稿件，请使用通用素人风格写作"

        formatted = []
        for i, article in enumerate(articles, 1):
            title = article.get("title", "")
            content = article.get("content", [])
            tags = article.get("tags", [])

            content_text = "\n".join(content) if isinstance(content, list) else str(content)
            tags_text = " ".join([f"#{t}" for t in tags]) if tags else ""

            formatted.append(f"--- 示例{i} ---\n标题：{title}\n内容：\n{content_text}\n标签：{tags_text}")

        return "\n\n".join(formatted)
```

- [ ] **Step 3: 验证语法**

Run: `cd /Users/admin/claude_ref/xiaohongshu-article-skill/src && python3 -c "from prompt_builder import PromptBuilder; print('OK')"`
Expected: `OK`

- [ ] **Step 4: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add src/prompt_builder.py
git commit -m "$(cat <<'EOF'
refactor: restructure PromptBuilder to support new prompt template

- 支持 style_features 参数
- 提取主范文作为参考示例
- 推断风格特征（语气、开头、段落、句式、标签）

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: 重构 skill.py 支持双模式

**Files:**
- Modify: `src/skill.py`

**Changes:** 添加 `mode` 参数，支持 local/feishu 切换

- [ ] **Step 1: 读取当前文件**

Read: `src/skill.py`

- [ ] **Step 2: 重写 skill.py**

Write to `src/skill.py`:

```python
"""
小红书素人稿件写作 Skill 主入口
整合所有模块，提供统一的写作流程
使用 DeepSeek API 生成稿件
支持本地模式和飞书模式
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

from feishu_reader import FeishuReader, MockFeishuReader
from feishu_writer import FeishuWriter, MockFeishuWriter
from word_reader import WordReader
from local_writer import LocalWriter
from style_analyzer import StyleAnalyzer
from prompt_builder import PromptBuilder
from article_generator import ArticleGenerator
from validators import KeywordValidator, SimilarityChecker

load_dotenv()


class XiaohongshuArticleSkill:
    """小红书素人稿件写作Skill（支持本地/飞书双模式）"""

    def __init__(
        self,
        mode: str = "local",
        use_mock_feishu: bool = True,
        feishu_document_id: str = None,
        data_dir: str = None,
        output_dir: str = None,
    ):
        """
        初始化Skill

        Args:
            mode: 运行模式，"local" 或 "feishu"
            use_mock_feishu: 是否使用模拟飞书（仅飞书模式有效）
            feishu_document_id: 飞书文档ID（飞书模式使用）
            data_dir: 数据目录路径（本地模式：original/ 和 references/ 的父目录）
            output_dir: 输出目录路径（本地模式使用）
        """
        self.mode = mode

        if mode == "local":
            self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "..", "data")
            self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "..", "output")
            self.reader = WordReader()
            self.writer = LocalWriter(output_dir=self.output_dir)
        elif mode == "feishu":
            self.use_mock_feishu = use_mock_feishu
            if use_mock_feishu:
                self.reader = MockFeishuReader()
                self.writer = MockFeishuWriter()
            else:
                self.reader = FeishuReader()
                self.writer = FeishuWriter()
                self.feishu_document_id = feishu_document_id
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'local' or 'feishu'.")

        self.style_analyzer = StyleAnalyzer()
        self.prompt_builder = PromptBuilder()
        self.article_generator = ArticleGenerator()

    def run(
        self,
        scenes: List[str],
        persona: str,
        keywords: List[str],
        requirements: str = "",
        article_count: int = 5,
        word_count: str = "800-1000字",
        style: str = "素人口吻，轻松自然，第一人称",
    ) -> Dict:
        """
        执行完整的写作流程

        Args:
            scenes: 场景列表，如 ["避孕场景", "推迟月经场景"]
            persona: 人设要求
            keywords: 必须包含的关键词
            requirements: 额外写作要求
            article_count: 生成文章数量
            word_count: 字数要求
            style: 风格要求

        Returns:
            执行结果报告
        """
        result = {
            "success": False,
            "articles": [],
            "keyword_validation": None,
            "similarity_check": None,
            "errors": [],
        }

        # 1. 读取参考稿件
        print("1. 读取参考稿件...")
        try:
            if self.mode == "local":
                reference_articles = self._read_local_references(scenes)
            else:
                reference_articles = self.reader.read_reference_articles(
                    self.feishu_document_id if not self.use_mock_feishu else "mock",
                    scenes,
                )
            print(f"   找到 {len(reference_articles)} 篇参考稿件")
        except Exception as e:
            result["errors"].append(f"读取参考稿件失败: {str(e)}")
            return result

        # 2. 分析风格特征
        print("2. 分析范文风格...")
        style_features = self.style_analyzer.analyze(reference_articles)
        print(f"   人称：{style_features.get('perspective')}")

        # 3. 组装Prompt
        print("3. 组装写作Prompt...")
        prompt = self.prompt_builder.build_prompt(
            scenes=scenes,
            persona=persona,
            reference_articles=reference_articles,
            keywords=keywords,
            requirements=requirements,
            article_count=article_count,
            word_count=word_count,
            style=style,
            style_features=style_features,
        )

        # 4. 生成稿件
        print("4. 生成稿件...")
        try:
            articles = self.article_generator.generate_articles(prompt, article_count)
            print(f"   生成 {len(articles)} 篇稿件")
            result["articles"] = articles
        except Exception as e:
            result["errors"].append(f"生成稿件失败: {str(e)}")
            return result

        # 5. 关键词验证
        print("5. 验证关键词...")
        validator = KeywordValidator(keywords)
        keyword_result = validator.validate_articles(articles)
        result["keyword_validation"] = keyword_result
        print(f"   关键词验证: {'通过' if keyword_result['all_passed'] else '未通过'}")

        # 6. 雷同度检测
        print("6. 检测雷同度...")
        similarity_checker = SimilarityChecker()
        similarity_result = similarity_checker.check_similarity(articles)
        result["similarity_check"] = similarity_result
        print(f"   雷同度检测: {similarity_result['message']}")

        # 7. 写入输出
        if keyword_result["all_passed"]:
            print("7. 写入输出文件...")
            try:
                if self.mode == "local":
                    output_path = self.writer.write_articles(articles)
                    print(f"   写入成功: {output_path}")
                else:
                    if self.use_mock_feishu:
                        self.writer.write_articles("mock-doc-id", articles)
                        print("   (模拟) 写入成功")
                    else:
                        doc_title = f"小红书稿件_{'_'.join(scenes)}_{len(articles)}篇"
                        document_id = self.writer.create_document(doc_title)
                        self.writer.write_articles(document_id, articles)
                        print(f"   写入成功: {document_id}")
                result["success"] = True
            except Exception as e:
                result["errors"].append(f"写入失败: {str(e)}")
        else:
            result["errors"].append("关键词验证未通过，请重新生成")

        return result

    def _read_local_references(self, scenes: List[str]) -> List[Dict]:
        """从本地文件读取参考稿件"""
        references_dir = os.path.join(self.data_dir, "references")

        if not os.path.exists(references_dir):
            print(f"   警告：参考目录不存在: {references_dir}")
            return []

        articles = []
        for filename in os.listdir(references_dir):
            if filename.endswith(".docx"):
                file_path = os.path.join(references_dir, filename)
                try:
                    file_articles = self.reader.read_reference_articles(file_path)
                    # 按场景筛选
                    if scenes:
                        filtered = [a for a in file_articles if any(s in a.get("title", "") for s in scenes)]
                        articles.extend(filtered if filtered else file_articles)
                    else:
                        articles.extend(file_articles)
                except Exception as e:
                    print(f"   读取失败 {filename}: {e}")
                    continue

        return articles


# 便捷函数
def write_articles(
    scenes: List[str],
    persona: str,
    keywords: List[str],
    requirements: str = "",
    article_count: int = 5,
    mode: str = "local",
) -> Dict:
    """
    便捷的稿件写作函数

    Args:
        scenes: 场景列表
        persona: 人设要求
        keywords: 必须包含的关键词
        requirements: 额外写作要求
        article_count: 生成数量
        mode: 运行模式，"local" 或 "feishu"

    Returns:
        执行结果报告
    """
    skill = XiaohongshuArticleSkill(mode=mode)
    return skill.run(
        scenes=scenes,
        persona=persona,
        keywords=keywords,
        requirements=requirements,
        article_count=article_count,
    )


if __name__ == "__main__":
    # 示例调用（本地模式）
    result = write_articles(
        scenes=["避孕场景", "推迟月经场景"],
        persona="素人口吻，25岁女生，分享真实使用体验",
        keywords=["内射", "避孕"],
        requirements="语气自然，不要太广告腔",
        article_count=3,
        mode="local",
    )

    print("\n=== 最终结果 ===")
    print(f"成功: {result['success']}")
    print(f"文章数: {len(result['articles'])}")
    if result["errors"]:
        print(f"错误: {result['errors']}")
```

- [ ] **Step 3: 验证语法**

Run: `cd /Users/admin/claude_ref/xiaohongshu-article-skill/src && python3 -c "from skill import XiaohongshuArticleSkill; print('OK')"`
Expected: `OK`

- [ ] **Step 4: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add src/skill.py
git commit -m "$(cat <<'EOF'
feat: support dual mode (local/feishu) in skill.py

- Add mode parameter: "local" or "feishu"
- Local mode uses WordReader + LocalWriter
- Add style_analyzer integration
- Add _read_local_references() helper

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: 修改 interactive_cli.py 支持 --mode 参数

**Files:**
- Modify: `src/interactive_cli.py`

**Changes:** 添加命令行参数解析，支持 `--mode local` 和 `--mode feishu`

- [ ] **Step 1: 读取当前文件**

Read: `src/interactive_cli.py`

- [ ] **Step 2: 修改 interactive_cli.py**

在文件顶部添加 argparse import，并在 `run_interactive()` 前添加参数解析逻辑：

在 `import readline` 后添加：
```python
import argparse
```

在 `def run_interactive()` 前添加：
```python
def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="小红书素人稿件写作 Skill")
    parser.add_argument(
        "--mode",
        choices=["local", "feishu"],
        default="local",
        help="运行模式：local 或 feishu（默认：local）"
    )
    parser.add_argument(
        "--use-mock",
        action="store_true",
        default=True,
        help="使用模拟飞书模式（仅 feishu 模式有效）"
    )
    return parser.parse_args()
```

修改 `if __name__ == "__main__":` 块：
```python
if __name__ == "__main__":
    args = parse_args()
    mode = args.mode
    use_mock = args.use_mock if mode == "feishu" else True

    print(f"\n运行模式：{mode.upper()}")
    if mode == "feishu":
        print(f"飞书模式：{'模拟' if use_mock else '真实'}")
```

在 `run_interactive()` 函数开头修改 skill 初始化：
```python
    skill = XiaohongshuArticleSkill(mode="local")  # 默认 local
    # 如果需要飞书模式，从 args 传递（需要改函数签名或使用全局）
```

完整重写 `if __name__ == "__main__":` 块：
```python
if __name__ == "__main__":
    args = parse_args()

    print(f"\n运行模式：{args.mode.upper()}")
    if args.mode == "feishu":
        print(f"飞书模式：{'模拟' if args.use_mock else '真实'}")

    # 简单方式：将 mode 传递给 run_interactive
    run_interactive(args.mode, args.use_mock if args.mode == "feishu" else True)
```

然后修改 `def run_interactive()` 为 `def run_interactive(mode="local", use_mock=True)`，并在函数内修改 skill 初始化：
```python
    skill = XiaohongshuArticleSkill(mode=mode, use_mock_feishu=use_mock)
```

完整替换 `if __name__ == "__main__":` 块和 `run_interactive` 函数：

```python
def run_interactive(mode="local", use_mock=True):
    """运行交互式CLI"""
    print("\n" + "=" * 50)
    print("小红书素人稿件写作 Skill")
    print(f"模式：{mode.upper()}")
    print("=" * 50)

    # 交互式输入
    scenes = input_scenes()
    persona = input_persona()
    keywords = input_keywords()
    requirements = input_requirements()
    article_count = input_article_count()
    word_count = input_word_count()
    style = input_style()

    # 确认
    if not confirm_and_run(scenes, persona, keywords, requirements, article_count, word_count, style):
        print("\n已取消。")
        return

    # 执行
    print("\n🚀 开始生成，请稍候...")

    skill = XiaohongshuArticleSkill(mode=mode, use_mock_feishu=use_mock)
    result = skill.run(
        scenes=scenes,
        persona=persona,
        keywords=keywords,
        requirements=requirements,
        article_count=article_count,
        word_count=word_count,
        style=style,
    )

    # 显示结果
    display_results(result)


if __name__ == "__main__":
    args = parse_args()

    print(f"\n运行模式：{args.mode.upper()}")
    if args.mode == "feishu":
        print(f"飞书模式：{'模拟' if args.use_mock else '真实'}")

    run_interactive(mode=args.mode, use_mock=args.use_mock if args.mode == "feishu" else True)
```

- [ ] **Step 3: 验证语法**

Run: `cd /Users/admin/claude_ref/xiaohongshu-article-skill/src && python3 -c "import interactive_cli; print('OK')"`
Expected: `OK`

- [ ] **Step 4: 测试 --help**

Run: `cd /Users/admin/claude_ref/xiaohongshu-article-skill/src && python3 interactive_cli.py --help`
Expected: 显示帮助信息，包含 --mode 选项

- [ ] **Step 5: 提交**

Run:
```bash
cd /Users/admin/claude_ref/xiaohongshu-article-skill
git add src/interactive_cli.py
git commit -m "$(cat <<'EOF'
feat: add --mode parameter to interactive_cli

支持 --mode local 和 --mode feishu 切换运行模式

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: 整体验证

**Files:**
- Test: `src/interactive_cli.py`

- [ ] **Step 1: 本地模式测试**

Run: `cd /Users/admin/claude_ref/xiaohongshu-article-skill/src && python3 interactive_cli.py --mode local`
（按提示输入测试数据，观察是否正常读取 data/references/ 目录）

- [ ] **Step 2: 检查输出目录**

Run: `ls -la /Users/admin/claude_ref/xiaohongshu-article-skill/output/`
Expected: 生成的 markdown 文件

- [ ] **Step 3: 飞书模式测试**

Run: `cd /Users/admin/claude_ref/xiaohongshu-article-skill/src && python3 interactive_cli.py --mode feishu --use-mock`
Expected: 使用模拟飞书模式运行

---

## 验证清单

1. [ ] `python3 -c "from skill import XiaohongshuArticleSkill; s = XiaohongshuArticleSkill(mode='local'); print('local mode OK')"`
2. [ ] `python3 -c "from skill import XiaohongshuArticleSkill; s = XiaohongshuArticleSkill(mode='feishu', use_mock_feishu=True); print('feishu mode OK')"`
3. [ ] `python3 -c "from word_reader import WordReader; print('word_reader OK')"`
4. [ ] `python3 -c "from local_writer import LocalWriter; print('local_writer OK')"`
5. [ ] `python3 -c "from style_analyzer import StyleAnalyzer; print('style_analyzer OK')"`
6. [ ] `python3 -c "from prompt_builder import PromptBuilder; print('prompt_builder OK')"`

---

## 任务顺序

Task 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9（线性执行，完成一项验证一项）

---

## 备注

- 所有文件复制自 rewrite-skill，确保代码一致
- 本地模式默认读取 `data/references/*.docx` 作为参考范文
- 输出默认写入 `output/*.md`
- 飞书模式保持原有行为不变