"""
稿件生成器
调用MiniMax API进行稿件生成，失败时Fallback到GLM
"""

import os
import re
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ArticleGenerator:
    """使用MiniMax API生成稿件，失败时Fallback到GLM"""

    def __init__(self, model: str = "MiniMax-M2.7", timeout: int = 300):
        # MiniMax 客户端
        minimax_key = os.getenv("MINIMAX_API_KEY")
        self.minimax_client = OpenAI(
            api_key=minimax_key,
            base_url="https://api.minimaxi.com/v1",
        ) if minimax_key else None

        # GLM 客户端
        glm_key = os.getenv("GLM_API_KEY")
        self.glm_client = OpenAI(
            api_key=glm_key,
            base_url="https://open.bigmodel.cn/api/paas/v4",
        ) if glm_key else None

        self.minimax_model = model
        self.glm_model = "glm-4.5-air"
        self.timeout = timeout

    def generate_articles(
        self,
        prompt: str,
        article_count: int = 2,
        max_tokens: int = 16000,
    ) -> List[Dict]:
        """
        生成多篇稿件

        Args:
            prompt: 组装好的写作Prompt
            article_count: 需要生成的篇数
            max_tokens: 最大token数

        Returns:
            生成的稿件列表
        """
        # 优先使用 MiniMax，超时则 fallback 到 GLM
        last_error = None

        if self.minimax_client:
            try:
                response = self.minimax_client.chat.completions.create(
                    model=self.minimax_model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=self.timeout,
                )
                if hasattr(response, "choices"):
                    content = response.choices[0].message.content
                    return self._parse_articles(content, article_count)
            except Exception as e:
                last_error = str(e)
                print(f"   MiniMax 调用失败，尝试 GLM: {last_error[:50]}")

        # Fallback 到 GLM
        if self.glm_client:
            try:
                response = self.glm_client.chat.completions.create(
                    model=self.glm_model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=self.timeout,
                )
                if hasattr(response, "choices"):
                    content = response.choices[0].message.content
                    return self._parse_articles(content, article_count)
            except Exception as e:
                last_error = str(e)
                print(f"   GLM 调用也失败: {last_error[:50]}")

        raise Exception(f"所有 API 都调用失败: {last_error}")

    def _parse_articles(self, content: str, expected_count: int) -> List[Dict]:
        """
        解析模型输出为结构化稿件

        Args:
            content: 模型返回的原始文本
            expected_count: 期望的稿件数量

        Returns:
            解析后的稿件列表
        """
        articles = []

        # 按分隔符分割稿件（处理 ---  后有换行和空格的情况）
        pattern = r"---\s*【稿件(\d+)】"
        parts = re.split(pattern, content)

        for i in range(1, len(parts), 2):
            try:
                idx = parts[i]
                article_text = parts[i + 1] if i + 1 < len(parts) else ""

                article = self._parse_single_article(article_text, idx)
                if article:
                    articles.append(article)
            except (ValueError, IndexError):
                continue

        # 如果解析失败，尝试其他方式
        if not articles:
            articles = self._fallback_parse(content, expected_count)

        return articles

    def _parse_single_article(self, text: str, idx: str) -> Optional[Dict]:
        """解析单篇稿件"""
        article = {"index": int(idx), "title": "", "content": "", "tags": ""}

        # 提取标题（兼容带**格式和普通格式）
        title_match = re.search(r"\*\*标题\*\*：(.+?)(?:\n|$)", text) or re.search(r"标题：(.+?)(?:\n|$)", text)
        if title_match:
            article["title"] = title_match.group(1).strip()

        # 提取正文（兼容"正文：内容"和"正文：\n内容"两种格式，以及**格式）
        content_match = re.search(r"\*\*正文\*\*：\n?(.+?)(?:标签：|$)", text, re.DOTALL) or re.search(r"正文：\n?(.+?)(?:标签：|$)", text, re.DOTALL)
        if content_match:
            extracted_content = content_match.group(1).strip()
            # 过滤掉误匹配到标签的情况
            if "标签：" not in extracted_content and "正文：" not in extracted_content:
                article["content"] = extracted_content

        # 提取标签（兼容带**格式和普通格式）
        tags_match = re.search(r"\*\*标签\*\*：(.+?)$", text) or re.search(r"标签：(.+?)$", text)
        if tags_match:
            article["tags"] = tags_match.group(1).strip()

        return article if article["title"] or article["content"] else None

    def _fallback_parse(self, content: str, expected_count: int) -> List[Dict]:
        """备用解析方法 - 简单按段落分割"""
        lines = content.split("\n")
        articles = []
        current_article = None

        for line in lines:
            if "【稿件" in line:
                if current_article:
                    articles.append(current_article)
                match = re.search(r"【稿件(\d+)】", line)
                current_article = {
                    "index": int(match.group(1)) if match else len(articles) + 1,
                    "title": "",
                    "content": "",
                    "tags": "",
                }
            elif current_article:
                if not current_article["title"]:
                    current_article["title"] = line.strip()
                else:
                    current_article["content"] += line + "\n"

        if current_article:
            articles.append(current_article)

        return articles[:expected_count]