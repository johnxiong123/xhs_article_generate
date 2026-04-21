"""
本地文件写入器
将稿件写入本地Markdown文件
"""

import os
import re
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class LocalWriter:
    """写入本地文件"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_articles(self, articles: List[Dict], filename: str = None) -> str:
        """
        将文章写入Markdown文件

        Args:
            articles: 文章列表
            filename: 文件名

        Returns:
            输出文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 从第一篇文章获取标题，清理特殊字符
            title = ""
            if articles:
                raw_title = articles[0].get("title", "")
                # 清理标题：移除特殊字符，限制长度
                title = re.sub(r'[\\/:*?"<>|]', '', raw_title)[:30]
            if title:
                filename = f"rewritten_{timestamp}_{title}.md"
            else:
                filename = f"rewritten_{timestamp}.md"

        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 小红书稿件改写结果\n\n")
            f.write(f"改写时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"共 {len(articles)} 篇稿件\n\n")
            f.write("---\n\n")

            for i, article in enumerate(articles, 1):
                f.write(f"## 【稿件 {i}】\n\n")
                f.write(f"**标题**：{article.get('title', '无标题')}\n\n")

                content = article.get('content', '')
                if isinstance(content, list):
                    content = '\n\n'.join(content)

                f.write(f"**正文**：\n\n{content}\n\n")

                tags = article.get('tags', '')
                if tags:
                    if isinstance(tags, list):
                        tags = ' '.join([f'#{t}' for t in tags])
                    f.write(f"**标签**：{tags}\n\n")

                f.write("---\n\n")

        return str(output_path)