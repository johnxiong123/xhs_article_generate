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
        writing_notes: str = "",
        article_count: int = 2,
        word_count: str = "800-1000字",
    ) -> Dict:
        """
        执行完整的写作流程

        Args:
            scenes: 场景列表
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
            writing_notes=writing_notes,
            article_count=article_count,
            word_count=word_count,
            style_features=style_features,
        )

        # 4. 生成稿件
        print("4. 生成稿件...")
        try:
            articles = self.article_generator.generate_articles(prompt, article_count)
            print(f"   生成 {len(articles)} 篇稿件")
            result["articles"] = articles
            if len(articles) < article_count:
                msg = f"⚠️ 期望生成 {article_count} 篇，实际 {len(articles)} 篇"
                print(f"   {msg}")
                result["errors"].append(msg)
        except Exception as e:
            result["errors"].append(f"生成稿件失败: {str(e)}")
            return result

        # 守门：若未产出任何文章，直接终止流程
        if not articles:
            result["errors"].append("未生成任何文章，跳过验证与写入")
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

        # 7. 写入输出：通过的写入正常文件；未通过但正文非空的写入 _failed.md 供人工修改
        non_empty = [a for a in articles if a.get("content", "").strip()]
        if not non_empty:
            result["errors"].append("所有文章正文为空，跳过写入")
            return result

        per_results = keyword_result.get("results", [])
        passed_titles = {r["title"] for r in per_results if r.get("passed")}
        passed_articles = [a for a in non_empty if a.get("title") in passed_titles]
        failed_articles = [a for a in non_empty if a.get("title") not in passed_titles]

        result["written"] = None
        result["written_failed"] = None

        print("7. 写入输出文件...")
        try:
            if self.mode == "local":
                if passed_articles:
                    p = self.writer.write_articles(passed_articles)
                    result["written"] = p
                    print(f"   ✅ 通过 {len(passed_articles)} 篇 → {p}")
                if failed_articles:
                    fp = self.writer.write_failed(failed_articles, per_results)
                    result["written_failed"] = fp
                    print(f"   ⚠️ 未通过 {len(failed_articles)} 篇 → {fp}（请人工补关键词）")
                result["success"] = bool(passed_articles)
                if not passed_articles:
                    result["errors"].append("无稿件通过关键词验证，已写入 _failed.md 供人工修改")
            else:
                if self.use_mock_feishu:
                    self.writer.write_articles("mock-doc-id", non_empty)
                    print("   (模拟) 写入成功")
                else:
                    doc_title = f"小红书稿件_{'_'.join(scenes)}_{len(non_empty)}篇"
                    document_id = self.writer.create_document(doc_title)
                    self.writer.write_articles(document_id, non_empty)
                    print(f"   写入成功: {document_id}")
                result["success"] = keyword_result["all_passed"]
                if not keyword_result["all_passed"]:
                    result["errors"].append("部分稿件未通过关键词验证")
        except Exception as e:
            result["errors"].append(f"写入失败: {str(e)}")

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
    writing_notes: str = "",
    article_count: int = 2,
    mode: str = "local",
) -> Dict:
    """便捷的稿件写作函数"""
    skill = XiaohongshuArticleSkill(mode=mode)
    return skill.run(
        scenes=scenes,
        persona=persona,
        keywords=keywords,
        writing_notes=writing_notes,
        article_count=article_count,
    )


if __name__ == "__main__":
    result = write_articles(
        scenes=["避孕场景", "推迟月经场景"],
        persona="素人口吻，25岁女生，分享真实使用体验",
        keywords=["内射", "避孕"],
        writing_notes="语气自然，不要太广告腔；素人口吻，第一人称",
        article_count=2,
        mode="local",
    )

    print("\n=== 最终结果 ===")
    print(f"成功: {result['success']}")
    print(f"文章数: {len(result['articles'])}")
    if result["errors"]:
        print(f"错误: {result['errors']}")