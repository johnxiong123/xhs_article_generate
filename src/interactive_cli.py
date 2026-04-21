"""
小红书素人稿件写作 Skill - 交互式CLI
引导用户输入参数，简化使用流程
"""

import os
import sys
import readline  # 启用完整的终端行编辑功能（退格、方向键）
import argparse
from dotenv import load_dotenv

sys.path.insert(0, '.')
load_dotenv()

# 检查API Key
if not os.getenv("DEEPSEEK_API_KEY"):
    print("❌ 错误：请先配置 DeepSeek API Key")
    print("   编辑 .env 文件，添加：DEEPSEEK_API_KEY=你的API Key")
    sys.exit(1)

from skill import XiaohongshuArticleSkill


def input_scenes():
    """输入场景"""
    print("\n" + "=" * 50)
    print("📝 场景设置")
    print("=" * 50)
    print("请输入产品/场景（多个用逗号分隔）")
    print("示例：避孕场景, 推迟月经场景, 调节月经场景")
    scenes_input = input("> ").strip()
    if not scenes_input:
        print("⚠️  未输入场景，使用默认值：通用场景")
        return ["通用场景"]
    return [s.strip() for s in scenes_input.split(",")]


def input_persona():
    """输入人设"""
    print("\n" + "=" * 50)
    print("👤 人设设定")
    print("=" * 50)
    print("请输入人设要求（描述写稿人的身份和风格）")
    print("示例：素人口吻，25岁女生，分享真实使用体验")
    persona = input("> ").strip()
    if not persona:
        print("⚠️  未输入人设，使用默认值：素人口吻")
        return "素人口吻，真实分享"
    return persona


def input_keywords():
    """输入关键词"""
    print("\n" + "=" * 50)
    print("🔑 关键词设置")
    print("=" * 50)
    print("请输入必须包含的关键词（多个用逗号分隔）")
    print("示例：内射, 避孕")
    keywords_input = input("> ").strip()
    if not keywords_input:
        print("⚠️  未输入关键词，将跳过关键词验证")
        return []
    return [k.strip() for k in keywords_input.split(",")]


def input_requirements():
    """输入额外要求"""
    print("\n" + "=" * 50)
    print("📋 额外要求（可选）")
    print("=" * 50)
    print("请输入额外写作要求，直接回车跳过")
    print("示例：语气自然，不要太广告腔，800字以内")
    requirements = input("> ").strip()
    return requirements


def input_article_count():
    """输入文章数量"""
    print("\n" + "=" * 50)
    print("📄 文章数量")
    print("=" * 50)
    print("请输入需要生成的稿件数量（默认5篇）")
    count_input = input("> ").strip()
    if not count_input:
        return 5
    try:
        count = int(count_input)
        if count < 1 or count > 20:
            print("⚠️  数量超出范围，使用默认值5")
            return 5
        return count
    except ValueError:
        print("⚠️  无效输入，使用默认值5")
        return 5


def input_word_count():
    """输入字数要求"""
    print("\n" + "=" * 50)
    print("📏 字数要求")
    print("=" * 50)
    print("请输入每篇文章的字数要求")
    print("示例：800-1000字, 1000字左右")
    word_count = input("> ").strip()
    if not word_count:
        return "800-1000字"
    return word_count


def input_style():
    """输入风格"""
    print("\n" + "=" * 50)
    print("✨ 写作风格")
    print("=" * 50)
    print("请输入文章风格要求")
    print("示例：素人口吻，轻松自然，第一人称")
    style = input("> ").strip()
    if not style:
        return "素人口吻，轻松自然，第一人称"
    return style


def confirm_and_run(scenes, persona, keywords, requirements, article_count, word_count, style):
    """确认并运行"""
    print("\n" + "=" * 50)
    print("📋 确认信息")
    print("=" * 50)
    print(f"场景：{', '.join(scenes)}")
    print(f"人设：{persona}")
    print(f"关键词：{', '.join(keywords) if keywords else '无'}")
    print(f"写作要求：{requirements if requirements else '无'}")
    print(f"文章数量：{article_count} 篇")
    print(f"字数要求：{word_count}")
    print(f"风格：{style}")
    print("\n" + "=" * 50)

    confirm = input("确认开始生成？(y/n) > ").strip().lower()
    return confirm in ["y", "yes", "是", ""]


def display_results(result):
    """显示结果"""
    print("\n" + "=" * 50)
    print("📤 生成结果")
    print("=" * 50)

    if result["success"]:
        print("✅ 生成成功！")
        print(f"\n共生成 {len(result['articles'])} 篇稿件：\n")

        for i, article in enumerate(result["articles"], 1):
            print("-" * 40)
            print(f"【稿件 {i}】")
            print(f"标题：{article.get('title', '无标题')}")
            print(f"正文预览：{article.get('content', '')[:150]}...")
            print(f"标签：{article.get('tags', '无')}")
            print()
    else:
        print("❌ 生成失败！")
        for error in result.get("errors", []):
            print(f"  - {error}")

    # 显示验证结果
    if result.get("keyword_validation"):
        print("-" * 40)
        kv = result["keyword_validation"]
        if kv["all_passed"]:
            print("✅ 关键词验证：通过")
        else:
            print("❌ 关键词验证：未通过")
            for r in kv["results"]:
                if not r["passed"]:
                    print(f"  - {r['title']}: 缺少 {', '.join(r['missing_keywords'])}")

    if result.get("similarity_check"):
        print("-" * 40)
        sc = result["similarity_check"]
        print(f"🔍 雷同度检测：{sc['message']}")
        if sc.get("pairs"):
            for pair in sc["pairs"]:
                level = "🔴" if pair["level"] == "high" else "🟡"
                print(f"  {level} {pair['article_1']} ≈ {pair['article_2']} ({pair['similarity']})")


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
