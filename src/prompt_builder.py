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