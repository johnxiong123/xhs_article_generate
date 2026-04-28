"""
飞书文档写入器
将稿件写入飞书文档
"""

import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class FeishuWriter:
    """写入飞书文档"""

    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_access_token(self) -> str:
        """获取飞书访问令牌"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["tenant_access_token"]

    def create_document(self, title: str) -> str:
        """
        创建新文档

        Args:
            title: 文档标题

        Returns:
            文档ID
        """
        access_token = self._get_access_token()
        url = f"{self.base_url}/docx/v1/documents"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        data = {"title": title}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["data"]["document"]["document_id"]

    def write_articles(self, document_id: str, articles: List[Dict]) -> bool:
        """
        将文章写入文档

        Args:
            document_id: 文档ID
            articles: 文章列表

        Returns:
            是否成功
        """
        access_token = self._get_access_token()

        # 构建文档内容
        children = []
        for article in articles:
            # 标题
            children.append(
                {
                    "block_type": 2,
                    "heading1": {"elements": [{"type": "text_run", "text_run": {"content": article.get("title", "")}}]}
                }
            )
            # 正文段落
            content = article.get("content", "")
            for para in content.split("\n\n"):
                if para.strip():
                    children.append(
                        {
                            "block_type": 3,
                            "text": {
                                "elements": [{"type": "text_run", "text_run": {"content": para.strip()}}]
                            },
                        }
                    )
            # 标签
            tags = article.get("tags", "")
            if tags:
                children.append(
                    {
                        "block_type": 3,
                        "text": {
                            "elements": [{"type": "text_run", "text_run": {"content": f"标签：{tags}"}}]
                        },
                    }
                )
            # 分隔线
            children.append({"block_type": 22})  # divider block

        # 批量插入block
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{document_id}/children"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        data = {"children": children, "index": -1}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True


# 模拟实现，用于测试
class MockFeishuWriter(FeishuWriter):
    """测试用模拟飞书写入器"""

    def __init__(self):
        super().__init__()

    def write_articles(self, document_id: str, articles: List[Dict]) -> bool:
        """打印输出而非真正写入"""
        print(f"\n=== 模拟写入文档 {document_id} ===")
        for article in articles:
            print(f"\n--- 稿件 {article.get('index')} ---")
            print(f"标题：{article.get('title')}")
            print(f"正文：{article.get('content')[:100]}...")
            print(f"标签：{article.get('tags')}")
        return True
