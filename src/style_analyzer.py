"""
风格分析器
分析范文的风格特征（语气、句式、标签使用方式）
"""

from typing import List, Dict


class StyleAnalyzer:
    """分析范文风格特征"""

    def __init__(self):
        pass

    def analyze(self, articles: List[Dict]) -> Dict:
        """
        分析范文风格特征（极简版本）

        直接收集整理，不做 hardcode 判断。

        Args:
            articles: 范文列表

        Returns:
            风格特征字典
        """
        if not articles:
            return self._default_style()

        # 收集所有内容
        def get_content(a):
            c = a.get("content", "")
            if isinstance(c, list):
                return " ".join(c)
            return c

        all_content = " ".join([get_content(a) for a in articles])
        all_tags = []
        for a in articles:
            tags = a.get("tags", [])
            if isinstance(tags, list):
                all_tags.extend(tags)
            elif tags:
                all_tags.append(tags)

        # 简单检测人称
        first_person = "我" in all_content
        perspective = "第一人称" if first_person else "第三人称"

        # 标签使用
        tag_usage = " ".join([f"#{t}" for t in all_tags[:10]]) if all_tags else ""

        return {
            "perspective": perspective,
            "tag_usage": tag_usage,
            "_source_articles": articles,
        }

    def _default_style(self) -> Dict:
        """默认风格（当无范文时）"""
        return {
            "perspective": "第一人称",
            "tag_usage": "",
            "_source_articles": [],
        }
