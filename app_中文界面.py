import os
from textwrap import dedent

import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI 营销策略助手",
    page_icon="✨",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem;}
    .hero {padding: 1.4rem 1.6rem; border: 1px solid rgba(128,128,128,.22); border-radius: 18px; margin-bottom: 1.2rem;}
    .eyebrow {font-size: .8rem; text-transform: uppercase; letter-spacing: .12em; opacity: .65;}
    .muted {opacity: .72;}
    .output-card {padding: 1rem 1.1rem; border: 1px solid rgba(128,128,128,.18); border-radius: 14px; margin-bottom: .8rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI × 营销工作流</div>
      <h1 style="margin: .35rem 0 .4rem 0;">AI 营销策略助手</h1>
      <div class="muted">把营销 Brief 快速转成可执行的消费者洞察、核心创意（Big Idea）、渠道策略、执行计划、预算与 KPI。</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ 设置")
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        help="仅在当前会话中使用。部署时也可以通过 Streamlit Secrets 设置 OPENAI_API_KEY。",
    )
    model = st.text_input("模型", value=os.getenv("OPENAI_MODEL", "gpt-5.6"))
    st.caption("没有 API Key 也可以点击下方的 Demo，查看完整产品效果。")

    st.divider()
    st.subheader("产品逻辑")
    st.caption("需求简报 → 洞察 → 策略 → 执行 → 预算 → KPI")

TAB1, TAB2 = st.tabs(["营销方案生成", "竞品传播分析"])


def get_api_key():
    return api_key_input.strip() or os.getenv("OPENAI_API_KEY", "")


def call_openai(system_prompt: str, user_prompt: str) -> str:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("NO_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_prompt,
    )
    return response.output_text


CAMPAIGN_SYSTEM = dedent(
    """
    You are a senior brand strategist and integrated marketing planner.
    Your job is to turn a raw marketing brief into a practical, evidence-aware campaign plan.
    Avoid generic buzzwords. Make assumptions explicit. Do not fabricate market data or statistics.
    When the brief does not contain enough evidence, write '待验证' rather than inventing facts.
    Output in Simplified Chinese unless the brief clearly asks for another language.

    Structure the answer with these exact sections:
    1. 一句话策略判断
    2. 目标人群与消费者洞察
    3. 核心传播命题 / 核心创意（Big Idea）
    4. 信息架构（核心卖点 + 支撑信息）
    5. 渠道与内容策略
    6. 执行节奏（预热 / 爆发 / 长尾）
    7. 预算建议（金额或比例，解释为什么）
    8. KPI 与衡量方式
    9. 风险与待验证假设
    10. 一页式营销方案摘要

    For channel strategy, distinguish platform roles rather than simply listing platforms.
    For budget, respect the user's total budget if provided.
    For KPI, separate awareness, engagement, conversion and learning metrics when relevant.
    """
)

COMPETITOR_SYSTEM = dedent(
    """
    You are a competitive intelligence analyst specializing in brand communication.
    Analyze only the evidence the user provides. Never invent campaign details.
    Output in Simplified Chinese.

    Structure the answer with these exact sections:
    1. 竞品传播地图
    2. 各竞品核心传播命题
    3. 目标人群与场景差异
    4. 渠道与内容打法对比
    5. 共同套路与同质化点
    6. 可占领的传播空位
    7. 对我方品牌的三条行动建议
    8. 需要进一步补充的数据
    """
)

with TAB1:
    st.subheader("把需求简报变成营销方案")
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("品牌 / 产品", placeholder="例如：Logitech Zone Vibe Pro")
        objective = st.text_input("营销目标", placeholder="例如：新品种草 + 电商转化")
        audience = st.text_area("目标人群", placeholder="例如：22–30 岁一二线城市知识型职场人")
        platforms = st.multiselect(
            "重点平台",
            ["小红书", "抖音", "B站", "微信", "微博", "知乎", "LinkedIn", "线下活动", "电商平台"],
            default=["小红书", "B站"],
        )
    with col2:
        budget = st.text_input("预算", placeholder="例如：15 万元")
        duration = st.text_input("营销周期", placeholder="例如：6 周")
        tone = st.text_input("品牌调性 / 限制条件", placeholder="例如：专业、克制，不夸大 AI 能力")
        context = st.text_area(
            "已知资料 / 需求简报",
            height=170,
            placeholder="粘贴产品卖点、背景资料、已有洞察、必须包含的信息等。",
        )

    user_prompt = dedent(
        f"""
        请基于以下 Brief 生成营销方案：
        - 品牌/产品：{brand or '未填写'}
        - 营销目标：{objective or '未填写'}
        - 目标人群：{audience or '未填写'}
        - 重点平台：{', '.join(platforms) if platforms else '未指定'}
        - 预算：{budget or '未填写'}
        - 周期：{duration or '未填写'}
        - 品牌调性/限制：{tone or '未填写'}
        - 已知资料：{context or '未填写'}

        请优先使用 Brief 中已有信息。信息不足时明确标注“待验证”，不要编造市场规模、用户比例或竞品事实。
        """
    )

    c1, c2 = st.columns([1, 1])
    generate = c1.button("✨ 生成营销方案", type="primary", use_container_width=True)
    demo = c2.button("▶ 查看示例", use_container_width=True)

    if generate:
        if not brand and not context:
            st.warning("至少填写品牌/产品或粘贴一段 Brief。")
        else:
            try:
                with st.spinner("正在生成策略…"):
                    result = call_openai(CAMPAIGN_SYSTEM, user_prompt)
                st.session_state["campaign_result"] = result
            except ValueError:
                st.info("当前没有 API Key。你可以先点击“查看示例”，或在左侧填入 OpenAI API Key。")
            except Exception as exc:
                st.error(f"生成失败：{exc}")

    if demo:
        st.session_state["campaign_result"] = dedent(
            """
            ## 1. 一句话策略判断
            把“AI 办公耳机”从参数型外设，转化为年轻知识工作者在混合办公场景中的“专注效率搭子”。

            ## 2. 目标人群与消费者洞察
            **核心人群：** 22–30 岁、频繁在办公室 / 居家 / 咖啡店切换的年轻职场人。\n\n
            **洞察假设：** 他们购买办公耳机并不只追求音质，而是在寻找一种能降低环境干扰、减少会议疲劳、保持专业状态的工具。该洞察需通过用户访谈或搜索趋势进一步验证。

            ## 3. 核心传播命题 / 核心创意（Big Idea）
            **“把注意力留给真正重要的事。”**\n\n
            产品角色：不是又一个耳机，而是帮助用户从嘈杂环境切回专注状态的工作入口。

            ## 4. 信息架构（核心卖点 + 支撑信息）
            - 核心卖点：跨场景保持清晰沟通与专注体验
            - 支撑 1：通勤 / 咖啡店 / 开放办公区等真实场景演示
            - 支撑 2：会议沟通、长时佩戴、设备切换等效率体验
            - 支撑 3：AI 相关能力只陈述已确认功能，避免“AI 万能化”表述

            ## 5. 渠道与内容策略
            - **小红书：** 场景种草与真实体验，负责“我为什么需要它”
            - **B站：** 深度测评与工作流演示，负责“它到底好不好用”
            - **电商页面：** 承接参数验证、优惠与购买转化
            - **线下体验：** 在共享办公 / 企业会议场景验证真实使用反馈

            ## 6. 执行节奏（预热 / 爆发 / 长尾）
            **预热 1–2 周：** KOC 真实办公痛点内容 + 悬念式场景短片。\n
            **爆发 2 周：** KOL 深度体验 + 多场景挑战 + 商品页优惠码。\n
            **长尾 2 周：** 用户 UGC、FAQ、企业试用案例与再营销。

            ## 7. 预算建议
            以 15 万元为例：内容/KOL 45%，线下体验 25%，媒体与电商承接 20%，监测与机动 10%。优先保证“可被体验和验证”的内容，而非把预算过度集中于单次曝光。

            ## 8. KPI 与衡量方式
            - Awareness：有效曝光、品牌/产品搜索增量
            - Engagement：完播率、收藏率、评论中的购买意向信号
            - Conversion：商品页点击、优惠码使用、购买转化
            - Learning：高频痛点、拒绝理由、企业客户留资质量

            ## 9. 风险与待验证假设
            - “AI”是否真的是用户购买主因：待验证
            - 不同办公场景下最强卖点排序：待验证
            - 避免夸大降噪、会议或 AI 能力

            ## 10. 一页式营销方案摘要
            **目标：** 新品种草 + 转化\n
            **人群：** 混合办公年轻职场人\n
            **核心创意（Big Idea）：** 把注意力留给真正重要的事\n
            **核心打法：** 场景种草 → 深度测评 → 电商承接 → 线下验证\n
            **关键指标：** 搜索增量、收藏率、点击率、优惠码转化、用户反馈质量
            """
        )

    if st.session_state.get("campaign_result"):
        st.divider()
        st.markdown(st.session_state["campaign_result"])
        st.download_button(
            "下载方案 Markdown",
            st.session_state["campaign_result"],
            file_name="营销方案.md",
            mime="text/markdown",
        )

with TAB2:
    st.subheader("把竞品资料变成传播空位")
    st.caption("把竞品新闻稿、Social 文案、Campaign 案例摘要等粘贴进来。工具只分析你提供的证据，不会凭空编造。")
    own_brand = st.text_input("我方品牌 / 产品（可选）", key="own_brand")
    competitor_text = st.text_area(
        "竞品资料",
        key="competitor_text",
        height=320,
        placeholder="示例：\n【品牌 A】……\n【品牌 B】……\n【品牌 C】……",
    )
    analyze = st.button("🔎 分析竞品", type="primary", use_container_width=True)

    if analyze:
        if not competitor_text.strip():
            st.warning("请先粘贴竞品资料。")
        else:
            prompt = f"我方品牌：{own_brand or '未指定'}\n\n竞品资料如下：\n{competitor_text}"
            try:
                with st.spinner("正在提炼竞品传播打法…"):
                    result = call_openai(COMPETITOR_SYSTEM, prompt)
                st.session_state["competitor_result"] = result
            except ValueError:
                st.info("当前没有 API Key。请在左侧填入 OpenAI API Key 后再分析。")
            except Exception as exc:
                st.error(f"分析失败：{exc}")

    if st.session_state.get("competitor_result"):
        st.divider()
        st.markdown(st.session_state["competitor_result"])
        st.download_button(
            "下载竞品分析 Markdown",
            st.session_state["competitor_result"],
            file_name="竞品传播分析.md",
            mime="text/markdown",
        )

st.divider()
st.caption("本工具为 AI 营销工作流原型。AI 生成内容在对外使用前，请由人工复核。")
