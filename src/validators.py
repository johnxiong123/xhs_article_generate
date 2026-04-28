"""
关键词验证器和雷同度检测器
"""

import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class KeywordValidator:
    """关键词验证器"""

    def __init__(self, keywords: List[str]):
        """
        初始化验证器

        Args:
            keywords: 必须包含的关键词列表
        """
        self.keywords = keywords

    def validate(self, article: str) -> Tuple[bool, List[str]]:
        """
        验证文章是否包含所有关键词

        Args:
            article: 文章内容

        Returns:
            (是否通过, 缺失的关键词列表)
        """
        if not article or not article.strip():
            return False, ["__EMPTY_CONTENT__"]

        missing = []
        for keyword in self.keywords:
            if keyword not in article:
                missing.append(keyword)

        return len(missing) == 0, missing

    def validate_articles(self, articles: List[Dict]) -> Dict[str, any]:
        """
        验证多篇文章

        Args:
            articles: 稿件列表

        Returns:
            验证结果报告
        """
        if not articles:
            return {
                "all_passed": False,
                "results": [],
                "error": "未生成任何文章",
            }

        results = []
        all_passed = True

        for i, article in enumerate(articles):
            passed, missing = self.validate(article.get("content", ""))
            result = {
                "index": article.get("index", i + 1),
                "title": article.get("title", ""),
                "passed": passed,
                "missing_keywords": missing,
            }
            results.append(result)
            if not passed:
                all_passed = False

        return {
            "all_passed": all_passed,
            "results": results,
        }


class SimilarityChecker:
    """雷同度检测器"""

    def __init__(self, threshold: float = 0.7, high_threshold: float = 0.85):
        """
        初始化检测器

        Args:
            threshold: 中等相似度阈值，超过标记需确认
            high_threshold: 高相似度阈值，超过需重写
        """
        self.threshold = threshold
        self.high_threshold = high_threshold
        self.vectorizer = TfidfVectorizer()

    def check_similarity(self, articles: List[Dict]) -> Dict[str, any]:
        """
        检测文章之间的相似度

        Args:
            articles: 稿件列表

        Returns:
            相似度检测报告
        """
        if len(articles) < 2:
            return {
                "has_issues": False,
                "pairs": [],
                "message": "文章数量不足，无法进行相似度检测",
            }

        # 提取文本内容
        texts = [a.get("content", "") for a in articles]
        titles = [a.get("title", f"稿件{i+1}") for i, a in enumerate(articles)]

        # 计算TF-IDF向量
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
        except ValueError:
            # 文本太短无法向量化
            return {
                "has_issues": False,
                "pairs": [],
                "message": "文章内容太短，无法进行相似度检测",
            }

        # 计算两两相似度
        similarities = cosine_similarity(tfidf_matrix)
        np.fill_diagonal(similarities, 0)  # 排除自身比较

        # 收集高相似度对
        issues = []
        for i in range(len(articles)):
            for j in range(i + 1, len(articles)):
                sim = similarities[i][j]
                if sim > self.threshold:
                    issue = {
                        "article_1": titles[i],
                        "article_2": titles[j],
                        "similarity": round(sim, 3),
                        "level": "high" if sim > self.high_threshold else "medium",
                    }
                    issues.append(issue)

        return {
            "has_issues": len(issues) > 0,
            "pairs": issues,
            "message": f"检测到 {len(issues)} 对可能雷同的文章",
        }
