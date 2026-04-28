"""
飞书文档读取器
从飞书文档读取参考稿件库
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class FeishuReader:
    """读取飞书文档中的参考稿件"""

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

    def get_document_content(self, document_id: str) -> Dict:
        """获取文档内容"""
        access_token = self._get_access_token()
        url = f"{self.base_url}/docx/v1/documents/{document_id}"

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def read_reference_articles(self, document_id: str, scenes: List[str]) -> List[Dict]:
        """
        读取参考稿件库，按场景筛选

        Args:
            document_id: 飞书文档ID
            scenes: 场景列表，如 ["避孕场景", "推迟月经场景"]

        Returns:
            匹配到的参考文章列表
        """
        content = self.get_document_content(document_id)

        articles = []
        # 文档内容在 content["data"]["document"]["content"] 中
        # 这里需要根据实际飞书文档结构解析
        # 简化实现：返回空列表，待根据实际文档结构调整

        return articles

    def parse_articles_from_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """
        从飞书文档block结构解析文章

        Args:
            blocks: 飞书文档的block列表

        Returns:
            解析后的文章列表
        """
        articles = []
        current_article = None

        for block in blocks:
            block_type = block.get("block_type")
            content = block.get("content", [])

            if block_type == 2:  # 标题块
                if current_article:
                    articles.append(current_article)
                current_article = {"title": "", "content": [], "tags": []}

            if current_article is not None:
                if block_type == 2:  # 标题
                    current_article["title"] = self._extract_text_from_content(content)
                elif block_type == 3:  # 正文
                    current_article["content"].append(self._extract_text_from_content(content))
                elif block_type == 4:  # 代码块
                    pass
                elif block_type == 7:  # 有序列表
                    pass
                elif block_type == 8:  # 无序列表
                    pass
                elif block_type == 13:  # 引用
                    pass

        if current_article:
            articles.append(current_article)

        return articles

    def _extract_text_from_content(self, content: List) -> str:
        """从飞书内容块中提取文本"""
        if not content:
            return ""
        return "".join(
            element.get("text", "") for element in content if isinstance(element, dict)
        )


# 模拟实现，用于测试
class MockFeishuReader(FeishuReader):
    """测试用模拟飞书读取器"""

    def __init__(self):
        super().__init__()

    def read_reference_articles(self, document_id: str, scenes: List[str]) -> List[Dict]:
        """返回模拟数据"""
        mock_articles = [
            {
                "title": "[避孕场景] 第一次用避孕药，我的真实感受",
                "content": [
                    "和男朋友在一起一年多，一直用TT，但是最近感觉不太方便...",
                    "后来在闺蜜推荐下尝试了短期避孕药...",
                    "说说我的使用感受：",
                    "1. 每天定时吃，有点麻烦但可以接受",
                    "2. 情绪有点波动，但很快就适应了",
                    "3. 效果还是很可靠的",
                ],
                "tags": ["避孕", "避孕药", "真实体验", "素人"],
                "scene": "避孕场景",
            },
            {
                "title": "[推迟月经场景] 高考前我用避孕药推迟了月经",
                "content": [
                    "高考那段时间正好赶上姨妈期...",
                    "妈妈带我去看了医生，医生建议可以服用避孕药推迟...",
                    "吃了大概10天，确实成功推迟了...",
                    "不过大家一定要听医嘱，不要自己乱吃！",
                ],
                "tags": ["推迟月经", "高考", "避孕药", "真实体验"],
                "scene": "推迟月经场景",
            },
            {
                "title": "[避孕场景] 长期吃短效避孕药，皮肤变好了？",
                "content": [
                    "吃了半年短效避孕药，发现皮肤比以前好了...",
                    "查了一下资料，原来是因为激素稳定了...",
                    "不过这个效果因人而异啦",
                    "姐妹们如果要吃，一定要定期检查身体！",
                ],
                "tags": ["避孕", "短效避孕药", "护肤", "素人"],
                "scene": "避孕场景",
            },
        ]

        # 按场景筛选
        if not scenes:
            return mock_articles

        filtered = [a for a in mock_articles if a.get("scene") in scenes]
        return filtered if filtered else mock_articles
