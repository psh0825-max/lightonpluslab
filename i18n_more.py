# -*- coding: utf-8 -*-
"""about.html · services.html · contact.html 번역표.

홈·제품 페이지와 같은 규칙 — 텍스트 노드 전체 일치. 인라인 태그로 쪼개지는 제목과
문의 메일 양식(href 안의 제목·본문)은 BLOCKS3 에서 통째로 바꾼다.
"""

BLOCKS3 = {
    '<h1 class="reveal reveal-d1">빠른 실행력과 <em>제품 감각</em></h1>': {
        'en': '<h1 class="reveal reveal-d1">Fast execution, <em>product sense</em></h1>',
        'ja': '<h1 class="reveal reveal-d1">速い実行力と<em>プロダクト感覚</em></h1>',
        'zh': '<h1 class="reveal reveal-d1">快速执行力与<em>产品感</em></h1>',
    },
    '<h1 class="reveal reveal-d1">AI를 중심으로 <em>제품</em>을 만듭니다</h1>': {
        'en': '<h1 class="reveal reveal-d1">We build <em>products</em> around AI</h1>',
        'ja': '<h1 class="reveal reveal-d1">AI を中心に<em>製品</em>を作ります</h1>',
        'zh': '<h1 class="reveal reveal-d1">以 AI 为核心打造<em>产品</em></h1>',
    },
    '<h1 class="reveal reveal-d1">프로젝트가 <em>있으신가요</em>?</h1>': {
        'en': '<h1 class="reveal reveal-d1">Have a <em>project</em> in mind?</h1>',
        'ja': '<h1 class="reveal reveal-d1">プロジェクトが<em>ありますか</em>？</h1>',
        'zh': '<h1 class="reveal reveal-d1">有<em>项目</em>想做吗？</h1>',
    },
    'href="mailto:support@lightonpluslab.com?subject=프로젝트%20문의%20%E2%80%94%20LightOn%20Plus%20Lab&body=%EC%95%84%EB%9E%98%20%ED%95%AD%EB%AA%A9%EC%9D%84%20%EC%95%84%EC%8B%9C%EB%8A%94%20%EB%A7%8C%ED%81%BC%EB%A7%8C%20%EC%B1%84%EC%9B%8C%20%EB%B3%B4%EB%82%B4%EC%A3%BC%EC%84%B8%EC%9A%94.%0A%0A1.%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EC%8B%B6%EC%9C%BC%EC%8B%A0%EA%B0%80%EC%9A%94%3F%0A%0A2.%20%EB%88%84%EA%B0%80%20%EC%93%B0%EB%82%98%EC%9A%94%3F%0A%0A3.%20%EC%9B%90%ED%95%98%EC%8B%9C%EB%8A%94%20%EC%9D%BC%EC%A0%95%0A%0A4.%20%EC%98%88%EC%82%B0%20%EB%B2%94%EC%9C%84%0A%0A5.%20%EC%B0%B8%EA%B3%A0%20%EC%9E%90%EB%A3%8C%C2%B7%EB%A7%81%ED%81%AC%0A"': {
        'en': 'href="mailto:support@lightonpluslab.com?subject=Project%20inquiry%20%E2%80%94%20LightOn%20Plus%20Lab&body=Fill%20in%20only%20what%20you%20know.%0A%0A1.%20What%20do%20you%20want%20to%20build%3F%0A%0A2.%20Who%20will%20use%20it%3F%0A%0A3.%20Timeline%0A%0A4.%20Budget%20range%0A%0A5.%20References%20%2F%20links%0A"',
        'ja': 'href="mailto:support@lightonpluslab.com?subject=%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AE%E3%81%94%E7%9B%B8%E8%AB%87%20%E2%80%94%20LightOn%20Plus%20Lab&body=%E3%82%8F%E3%81%8B%E3%82%8B%E7%AF%84%E5%9B%B2%E3%81%A7%E3%81%94%E8%A8%98%E5%85%A5%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82%0A%0A1.%20%E4%BD%95%E3%82%92%E4%BD%9C%E3%82%8A%E3%81%9F%E3%81%84%E3%81%A7%E3%81%99%E3%81%8B%EF%BC%9F%0A%0A2.%20%E8%AA%B0%E3%81%8C%E4%BD%BF%E3%81%84%E3%81%BE%E3%81%99%E3%81%8B%EF%BC%9F%0A%0A3.%20%E3%81%94%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%97%A5%E7%A8%8B%0A%0A4.%20%E4%BA%88%E7%AE%97%E3%81%AE%E7%9B%AE%E5%AE%89%0A%0A5.%20%E5%8F%82%E8%80%83%E8%B3%87%E6%96%99%E3%83%BB%E3%83%AA%E3%83%B3%E3%82%AF%0A"',
        'zh': 'href="mailto:support@lightonpluslab.com?subject=%E9%A1%B9%E7%9B%AE%E5%92%A8%E8%AF%A2%20%E2%80%94%20LightOn%20Plus%20Lab&body=%E8%AF%B7%E6%8C%89%E6%89%80%E7%9F%A5%E5%A1%AB%E5%86%99%E5%8D%B3%E5%8F%AF%E3%80%82%0A%0A1.%20%E6%83%B3%E5%81%9A%E4%BB%80%E4%B9%88%EF%BC%9F%0A%0A2.%20%E8%B0%81%E4%BC%9A%E4%BD%BF%E7%94%A8%EF%BC%9F%0A%0A3.%20%E6%9C%9F%E6%9C%9B%E8%BF%9B%E5%BA%A6%0A%0A4.%20%E9%A2%84%E7%AE%97%E8%8C%83%E5%9B%B4%0A%0A5.%20%E5%8F%82%E8%80%83%E8%B5%84%E6%96%99%E4%B8%8E%E9%93%BE%E6%8E%A5%0A"',
    },
}

T3 = {
    '소개 — LightOn Plus Lab': (
        'About — LightOn Plus Lab',
        '紹介 — LightOn Plus Lab',
        '关于 — LightOn Plus Lab'),
    'LightOn Plus Lab — AI 앱을 직접 만들어 Google Play에 출시하고 운영하는 1인 개발 스튜디오.': (
        'LightOn Plus Lab — a one-person studio that builds AI apps, ships them on Google Play and runs them.',
        'LightOn Plus Lab — AI アプリを自ら作り、Google Play で公開して運営する一人開発スタジオ。',
        'LightOn Plus Lab — 亲手打造 AI 应用、在 Google Play 上架并运营的一人开发工作室。'),
    '"기능 추가"가 아니라 "사용자가 계속 쓰는 흐름"을 만듭니다. AI 앱을 직접 만들어 Google Play에 출시하고 운영하는 1인 스튜디오.': (
        'Not "more features" — a flow people keep using. A one-person studio that builds AI apps, ships them on Google Play and runs them.',
        '「機能の追加」ではなく「使い続けてもらえる流れ」を作ります。AI アプリを自ら作り、Google Play で公開して運営する一人スタジオ。',
        '我们打造的不是“新增功能”，而是“让人持续使用的流程”。亲手做 AI 应用、在 Google Play 上架并运营的一人工作室。'),
    '원칙': (
        'Principles',
        '原則',
        '原则'),
    '빠르게 만들기 → 사용자 반응으로 개선 → 운영 가능한 구조로 정리.': (
        'Build fast → improve from how people respond → settle it into something that can be run.',
        '素早く作る → ユーザーの反応で改善 → 運営できる形に整える。',
        '快速做出来 → 根据用户反馈改进 → 整理成可长期运营的结构。'),
    '강점': (
        'Strengths',
        '強み',
        '优势'),
    'AI를 제품에 붙일 때 필요한 UX·비용·성능·운영을 한 사람이 함께 고려합니다.': (
        'When AI goes into a product, one person weighs the UX, cost, performance and operations together.',
        'AI を製品に組み込むときの UX・コスト・性能・運営を、一人がまとめて考えます。',
        '把 AI 放进产品时所需的 UX、成本、性能与运维，由同一个人一并考虑。'),
    '협업': (
        'Working together',
        '協業',
        '协作'),
    '짧은 주기로 공유·피드백 → 빠른 반복. 문서·일정·우선순위를 투명하게.': (
        'Short cycles of sharing and feedback → fast iteration. Docs, schedule and priorities stay in the open.',
        '短いサイクルで共有・フィードバック → 素早い反復。ドキュメント・日程・優先順位は透明に。',
        '短周期共享与反馈 → 快速迭代。文档、进度与优先级保持透明。'),
    '숫자로 보는 LightOn': (
        'By the numbers: LightOn',
        '数字で見る LightOn',
        '用数字看 LightOn'),
    '주': (
        'weeks',
        '週',
        '周'),
    '일': (
        'days',
        '日',
        '天'),
    'Google Play 출시 앱': (
        'Apps on Google Play',
        'Google Play 公開アプリ',
        'Google Play 上架应用'),
    'MVP 시작까지': (
        'To a working MVP',
        'MVP 着手まで',
        '到 MVP 启动'),
    '첫 회신 시간': (
        'To the first reply',
        '最初の返信まで',
        '首次回复'),
    '무료 수정 기간': (
        'Of free revisions',
        '無償修正期間',
        '免费修改期'),
    '박승혁 — 1인 개발 스튜디오': (
        'Seunghyuk Park — a one-person studio',
        'パク・スンヒョク — 一人開発スタジオ',
        '朴丞赫 — 一人开发工作室'),
    'LightOn Plus Lab은 박승혁이 혼자 운영하는 스튜디오입니다. 기획·디자인·개발·배포·운영을 모두 한 사람이 담당하며, 결정이 빠르고 맥락이 끊기지 않습니다.': (
        'LightOn Plus Lab is a studio run by Seunghyuk Park alone. Planning, design, development, release and operation all sit with one person, so decisions are quick and no context gets lost.',
        'LightOn Plus Lab はパク・スンヒョクが一人で運営するスタジオです。企画・デザイン・開発・公開・運営をすべて一人が担うので、決定が速く、文脈が途切れません。',
        'LightOn Plus Lab 是朴丞赫一人运营的工作室。策划、设计、开发、发布与运营都由一人负责，决策快，脉络不会中断。'),
    '기술 스택': (
        'Tech stack',
        '技術スタック',
        '技术栈'),
    'AI 경험': (
        'AI experience',
        'AI の経験',
        'AI 经验'),
    'GPT-4o mini · Gemini 2.5 Flash · Claude · Soniox 전사·화자 분리 · Vision · TTS · RAG · 임베딩': (
        'GPT-4o mini · Gemini 2.5 Flash · Claude · Soniox transcription & speaker diarization · Vision · TTS · RAG · embeddings',
        'GPT-4o mini · Gemini 2.5 Flash · Claude · Soniox 文字起こし・話者分離 · Vision · TTS · RAG · 埋め込み',
        'GPT-4o mini · Gemini 2.5 Flash · Claude · Soniox 转写与说话人分离 · Vision · TTS · RAG · 嵌入'),
    '출시 이력': (
        'Track record',
        'リリース実績',
        '上线记录'),
    'Google Play: 모모아이 · 송빗 · 라이트온 AI 노트. 웹: 영수증 AI · 말씀찾기 · 노딱 · 쿠폰북 · 멍냥로그 · 수학친구 등 운영 중.': (
        'Google Play: Momoi · Songbit · LightOn AI Note. Web: Receipt AI · Bible Search · Noddak · Coupon Book · Pet Log · Math Friend and more, all in service.',
        'Google Play: モモアイ · Songbit · LightOn AI ノート。ウェブ: レシート AI · みことば検索 · ノッタク · クーポンブック · わんにゃんログ · 数学フレンドなどを運営中。',
        'Google Play：Momoi · Songbit · LightOn AI 笔记。网页：票据 AI · 经文检索 · Noddak · 优惠券本 · 宠物日志 · 数学伙伴等，均在运营。'),
    '함께 만들고 싶은 프로젝트가 있으신가요?': (
        "Have a project you'd like to build together?",
        '一緒に作りたいプロジェクトはありますか？',
        '有想一起做的项目吗？'),
    '아이디어 단계든, 이미 돌아가는 서비스에 AI를 붙이고 싶으신 단계든 좋습니다. 24시간 내 회신드립니다.': (
        'An idea, or an AI feature for something already running — either is fine. We reply within 24 hours.',
        'アイデア段階でも、すでに動いているサービスに AI を足したい段階でも構いません。24時間以内に返信します。',
        '无论是想法阶段，还是想给已在运行的服务加上 AI，都可以。我们 24 小时内回复。'),
    '서비스 — LightOn Plus Lab': (
        'Services — LightOn Plus Lab',
        'サービス — LightOn Plus Lab',
        '服务 — LightOn Plus Lab'),
    'LightOn Plus Lab의 AI 앱 개발 서비스 — AI 기능 탑재, API & 배포, MVP 제작, 자동화': (
        'AI app development by LightOn Plus Lab — AI features, APIs & deployment, MVPs, automation',
        'LightOn Plus Lab の AI アプリ開発サービス — AI 機能の搭載、API と公開、MVP 制作、自動化',
        'LightOn Plus Lab 的 AI 应用开发服务 — AI 功能集成、API 与部署、MVP 制作、自动化'),
    '"AI 기능"을 중심으로 앱·웹 제품을 만듭니다. Google Play에 직접 앱을 출시하고 운영하면서 쌓은 방식 그대로 진행합니다.': (
        'We build app and web products around an AI feature, the same way we ship and run our own apps on Google Play.',
        '「AI 機能」を中心にアプリ・ウェブ製品を作ります。Google Play で自らアプリを公開・運営してきたやり方そのままで進めます。',
        '以“AI 功能”为核心打造应用与网页产品，沿用我们在 Google Play 亲自上架、运营应用时积累的方法。'),
    'AI 기능 탑재': (
        'AI features',
        'AI 機能の搭載',
        'AI 功能集成'),
    '챗봇·요약·검색(RAG)·추천·자동화를 제품에 자연스럽게 녹여냅니다. LLM·비전·음성 중 필요한 AI 기술을 선별해 연동합니다.': (
        'Chatbots, summaries, search (RAG), recommendations and automation, woven into the product. We pick the AI that fits — language models, vision or speech — and wire it in.',
        'チャットボット・要約・検索（RAG）・レコメンド・自動化を製品に自然に溶け込ませます。LLM・ビジョン・音声から必要な AI 技術を選んで連携します。',
        '把聊天机器人、摘要、检索（RAG）、推荐与自动化自然地融入产品。从 LLM、视觉、语音中挑选所需的 AI 技术并接入。'),
    'API &amp; 배포': (
        'APIs &amp; deployment',
        'API と公開',
        'API 与部署'),
    '서버·API 설계부터 클라우드 배포, 모니터링, 비용 최적화까지. Cloud Run · Firebase · Vercel · Cloudflare 등 실제로 운영해 본 구성으로 정리합니다.': (
        'From server and API design to cloud deployment, monitoring and cost tuning — on setups we run ourselves: Cloud Run, Firebase, Vercel, Cloudflare.',
        'サーバー・API 設計からクラウドへの公開、モニタリング、コスト最適化まで。Cloud Run · Firebase · Vercel · Cloudflare など、実際に運用してきた構成でまとめます。',
        '从服务器与 API 设计，到云端部署、监控与成本优化。采用我们实际运营过的组合：Cloud Run · Firebase · Vercel · Cloudflare 等。'),
    'MVP 제작': (
        'MVPs',
        'MVP 制作',
        'MVP 制作'),
    '빠르게 실험 가능한 MVP를 만들고, 검증 후 기능을 확장합니다. 최소 2주부터 실제 동작하는 결과물을 확인할 수 있습니다.': (
        'An MVP you can test quickly, extended once it proves out. You can see something working in as little as two weeks.',
        'すぐに試せる MVP を作り、検証してから機能を広げます。最短2週間で実際に動く成果物を確認できます。',
        '先做出能快速试验的 MVP，验证后再扩展功能。最快 2 周就能看到真正可用的成果。'),
    '이렇게 진행됩니다': (
        'How it goes',
        '進め方',
        '合作流程'),
    '짧은 주기로 공유·피드백 → 빠른 반복. 2주차부터 실물 프로토타입을 확인할 수 있습니다.': (
        'Short cycles of sharing and feedback → fast iteration. A real prototype from week two.',
        '短いサイクルで共有・フィードバック → 素早い反復。2週目から実物のプロトタイプを確認できます。',
        '短周期共享与反馈 → 快速迭代。第 2 周起即可看到实物原型。'),
    '상담 &amp; 기획': (
        'Consulting &amp; planning',
        '相談と企画',
        '咨询与规划'),
    '목표·핵심 기능·일정·예산을 정리합니다. 필요하면 간단한 PoC로 가능성을 먼저 확인합니다.': (
        'We pin down the goal, core features, schedule and budget. If needed, a quick proof of concept checks feasibility first.',
        '目標・核心機能・日程・予算を整理します。必要なら簡単な PoC で先に可能性を確かめます。',
        '梳理目标、核心功能、进度与预算。必要时先用简单的 PoC 验证可行性。'),
    '개발 &amp; 피드백': (
        'Development &amp; feedback',
        '開発とフィードバック',
        '开发与反馈'),
    '1~2주 단위로 빌드를 공유하고 피드백을 반영합니다. 빠른 반복이 핵심입니다.': (
        'A build every one to two weeks, with your feedback folded in. Fast iteration is the point.',
        '1〜2週間ごとにビルドを共有し、フィードバックを反映します。素早い反復が肝心です。',
        '每 1~2 周共享一次构建并吸收反馈。快速迭代是关键。'),
    '배포 &amp; 운영': (
        'Launch &amp; operation',
        '公開と運営',
        '上线与运营'),
    '스토어 등록·인앱결제 연동·도메인·모니터링까지 세팅하고 안정적으로 인계드립니다. Google Play 출시 경험이 있습니다.': (
        'Store listing, in-app billing, domains and monitoring are set up and handed over cleanly. We have shipped on Google Play ourselves.',
        'ストア登録・アプリ内課金・ドメイン・モニタリングまで整え、安定した状態でお引き渡しします。Google Play での公開経験があります。',
        '从商店上架、内购接入、域名到监控全部配置好，稳妥交接。我们有 Google Play 上架经验。'),
    '이런 것도 만듭니다': (
        'We also build',
        'こんなものも作ります',
        '我们也做这些'),
    '목표·예산·일정에 맞게 조합합니다.': (
        'Combined to fit your goal, budget and schedule.',
        '目標・予算・日程に合わせて組み合わせます。',
        '按目标、预算与进度灵活组合。'),
    '문서 검색(RAG) 기반 Q&amp;A': (
        'Document Q&amp;A with retrieval (RAG)',
        '文書検索（RAG）ベースの Q&amp;A',
        '基于文档检索（RAG）的问答'),
    '사내·개인 문서를 업로드하고 질문하면 근거 기반 답변을 제공합니다.': (
        'Upload company or personal documents and ask; answers come with their sources.',
        '社内・個人の文書をアップロードして質問すると、根拠つきで回答します。',
        '上传公司或个人文档后提问，回答附带依据。'),
    '이미지·카메라 기반 AI': (
        'Image and camera AI',
        '画像・カメラベースの AI',
        '基于图像与相机的 AI'),
    '카메라 입력을 분석해 분류·검출·가이드를 제공합니다. (스캔·측정·인식)': (
        'Camera input analysed to classify, detect and guide (scanning, measuring, recognition).',
        'カメラ入力を解析し、分類・検出・ガイドを行います。（スキャン・計測・認識）',
        '分析相机输入，实现分类、检测与引导。（扫描、测量、识别）'),
    '고객 지원 자동화': (
        'Customer support automation',
        'カスタマーサポートの自動化',
        '客服自动化'),
    'FAQ + 티켓 요약 + 답변 초안 생성으로 CS 속도와 품질을 개선합니다.': (
        'FAQs, ticket summaries and draft replies make support faster and better.',
        'FAQ ＋ チケット要約 ＋ 返信下書きの生成で、サポートの速さと質を上げます。',
        'FAQ + 工单摘要 + 回复草稿生成，提升客服速度与质量。'),
    '업무 자동화 봇': (
        'Workflow bots',
        '業務自動化ボット',
        '业务自动化机器人'),
    '반복 업무를 자동화하는 챗봇·워크플로우. 텔레그램·슬랙·이메일 연동.': (
        'Chatbots and workflows that take over repetitive work, connected to Telegram, Slack or email.',
        '繰り返し業務を自動化するチャットボット・ワークフロー。Telegram・Slack・メール連携。',
        '把重复工作自动化的聊天机器人与工作流，可接入 Telegram、Slack、邮件。'),
    '프로젝트 문의': (
        'Project inquiry',
        'プロジェクトのご相談',
        '项目咨询'),
    '24시간 내 회신드립니다. 첫 상담은 무료입니다.': (
        'We reply within 24 hours. The first consultation is free.',
        '24時間以内に返信します。初回相談は無料です。',
        '我们 24 小时内回复。首次咨询免费。'),
    '연락처 — LightOn Plus Lab': (
        'Contact — LightOn Plus Lab',
        'お問い合わせ — LightOn Plus Lab',
        '联系我们 — LightOn Plus Lab'),
    'LightOn Plus Lab에 프로젝트를 문의하세요. 24시간 내 회신드립니다.': (
        'Ask LightOn Plus Lab about your project. We reply within 24 hours.',
        'LightOn Plus Lab にプロジェクトをご相談ください。24時間以内に返信します。',
        '欢迎向 LightOn Plus Lab 咨询项目。我们 24 小时内回复。'),
    '아이디어 단계든, 돌아가는 서비스에 AI를 붙이고 싶으신 단계든 괜찮습니다. 24시간 안에 친절하게 회신드립니다.': (
        "An idea, or an AI feature for something already running — either is fine. You'll hear back within 24 hours.",
        'アイデア段階でも、動いているサービスに AI を足したい段階でも構いません。24時間以内に丁寧に返信します。',
        '无论是想法阶段，还是想给运行中的服务加上 AI，都可以。我们 24 小时内认真回复。'),
    '가장 빠릅니다. 프로젝트 요청서·견적 문의도 이메일로 받습니다.': (
        'The fastest way. Project briefs and quote requests come by email too.',
        'いちばん早い方法です。プロジェクト依頼書や見積もりのご相談もメールで受け付けます。',
        '最快的方式。项目需求书与报价咨询也通过邮件接收。'),
    '요청서 양식으로 보내기': (
        'Send with the brief template',
        '依頼書フォームで送る',
        '用需求模板发送'),
    '무엇을·누가·일정·예산 항목이 미리 채워진 메일이 열립니다.': (
        'Opens an email with what, who, timeline and budget already laid out.',
        '「何を・誰が・日程・予算」の項目が入ったメールが開きます。',
        '打开一封已列好“做什么、谁用、进度、预算”等项目的邮件。'),
    '카카오톡 1:1': (
        'KakaoTalk chat',
        'KakaoTalk 1:1',
        'KakaoTalk 一对一'),
    '채팅으로 물어보기': (
        'Ask in chat',
        'チャットで聞く',
        '在聊天里提问'),
    '평일 10:00~18:00 실시간 응대. 그 외 시간은 메시지를 남겨주세요.': (
        'Live on weekdays, 10:00–18:00 KST. Outside those hours, leave a message.',
        '平日 10:00〜18:00（韓国時間）はリアルタイムで対応。それ以外の時間はメッセージを残してください。',
        '工作日 10:00–18:00（韩国时间）实时回复，其他时间请留言。'),
    '평일 10:00~18:00. 부재 시 메시지 남겨주시면 회신.': (
        "Weekdays, 10:00–18:00 KST. If we miss you, leave a message and we'll get back to you.",
        '平日 10:00〜18:00（韓国時間）。不在の際はメッセージを残していただければ折り返します。',
        '工作日 10:00–18:00（韩国时间）。未接通请留言，我们会回复。'),
    '경기도 안양시': (
        'Anyang, Gyeonggi-do, Korea',
        '韓国 京畿道 安養市',
        '韩国 京畿道 安养市'),
    '동안구 관평로 333, 6동 504호 · 원격 미팅 기본.': (
        '504, Bldg 6, 333 Gwanpyeong-ro, Dongan-gu · Meetings are remote by default.',
        '東安区 冠坪路 333、6棟 504号 · 打ち合わせは基本オンライン。',
        '东安区 冠坪路 333，6 栋 504 号 · 默认远程会议。'),
    '평일 10:00–18:00 기준 24시간 내 회신 · 주말·공휴일은 다음 근무일에 회신': (
        'Replies within 24 hours, counting weekdays 10:00–18:00 KST · weekends and holidays: the next working day',
        '平日 10:00〜18:00（韓国時間）基準で24時間以内に返信 · 土日祝日は翌営業日に返信',
        '以工作日 10:00–18:00（韩国时间）计，24 小时内回复 · 周末与节假日顺延至下一个工作日'),
}
