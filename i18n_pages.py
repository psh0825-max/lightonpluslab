# -*- coding: utf-8 -*-
"""products.html · lens.html 번역표.

홈(i18n_home)과 같은 규칙 — 텍스트 노드 전체 일치. 인라인 태그로 쪼개지는
제목·문단은 BLOCKS2 에서 요소째 바꾼다.
"""

# 인라인 태그가 섞여 어순이 흔들리는 자리
BLOCKS2 = {
    '<h1 class="reveal reveal-d1">AI 앱을 <em>카테고리</em>별로</h1>': {
        "en": '<h1 class="reveal reveal-d1">AI apps <em>by category</em></h1>',
        "ja": '<h1 class="reveal reveal-d1">AI アプリを<em>カテゴリ</em>別に</h1>',
        "zh": '<h1 class="reveal reveal-d1">按<em>类别</em>看 AI 应用</h1>',
    },
    '<h1 class="reveal reveal-d1">렌즈 파일을 <em>브라우저에서</em> 엽니다</h1>': {
        "en": '<h1 class="reveal reveal-d1">Open lens files <em>in the browser</em></h1>',
        "ja": '<h1 class="reveal reveal-d1">レンズファイルを<em>ブラウザで</em>開きます</h1>',
        "zh": '<h1 class="reveal reveal-d1"><em>在浏览器里</em>打开镜头文件</h1>',
    },
    '<p class="reveal reveal-d2">CODE V <code>.seq</code>와 Zemax OpticStudio <code>.zmx</code>를 그대로 열어 단면과 1차 특성, 스팟 다이어그램, MTF, 광선 수차, 필드 곡률을 봅니다. 설치할 것도, 계정을 만들 것도 없습니다.</p>': {
        "en": '<p class="reveal reveal-d2">Open CODE V <code>.seq</code> and Zemax OpticStudio <code>.zmx</code> files as they are and read the layout and first-order properties, spot diagrams, MTF, ray aberrations and field curvature. Nothing to install, no account to make.</p>',
        "ja": '<p class="reveal reveal-d2">CODE V の <code>.seq</code> と Zemax OpticStudio の <code>.zmx</code> をそのまま開き、断面と一次特性、スポットダイアグラム、MTF、光線収差、像面湾曲を見ます。インストールもアカウント登録も不要です。</p>',
        "zh": '<p class="reveal reveal-d2">直接打开 CODE V 的 <code>.seq</code> 与 Zemax OpticStudio 的 <code>.zmx</code>，查看剖面与一阶特性、点列图、MTF、光线像差与场曲。无需安装，也不用注册。</p>',
    },
    '<span><code>.seq</code> 또는 <code>.zmx</code> 파일을 화면에 놓으면 바로 열립니다. 붙여넣기도 됩니다.</span>': {
        "en": '<span>Drop a <code>.seq</code> or <code>.zmx</code> file on the page and it opens. Pasting works too.</span>',
        "ja": '<span><code>.seq</code> または <code>.zmx</code> のファイルを画面に置けばすぐ開きます。貼り付けでも構いません。</span>',
        "zh": '<span>把 <code>.seq</code> 或 <code>.zmx</code> 文件拖到页面上即可打开，粘贴也行。</span>',
    },
}

T2 = {
    # ---------------------------------------------------------------- products
    "앱 목록 — LightOn Plus Lab | 스토어 앱 & 웹 앱": ("Apps — LightOn Plus Lab | Store apps & web apps", "アプリ一覧 — LightOn Plus Lab | ストアアプリ＆ウェブアプリ", "应用一览 — LightOn Plus Lab | 商店应用与网页应用"),
    "앱 목록 — LightOn Plus Lab": ("Apps — LightOn Plus Lab", "アプリ一覧 — LightOn Plus Lab", "应用一览 — LightOn Plus Lab"),
    "스토어에 출시한 앱 10종과, 웹에서 바로 쓸 수 있는 앱들입니다. 카드를 누르면 바로 이동합니다.": (
        "Ten apps on the stores, plus the ones that run straight in a browser. Tap a card to go there.",
        "ストアに出した10本と、ブラウザですぐ使えるアプリです。カードを押すとそのまま移動します。",
        "已上架商店的 10 款，以及可在浏览器直接使用的应用。点击卡片即可前往。"),
    "LightOn Plus Lab이 만든 앱 전체 목록. Google Play·App Store 출시 앱과 웹에서 바로 쓰는 AI 앱들을 카테고리별로 살펴보세요.": (
        "Every app LightOn Plus Lab has built — on Google Play and the App Store, and AI apps that run in a browser, sorted by category.",
        "LightOn Plus Lab が作ったアプリの全一覧。Google Play・App Store のアプリと、ブラウザですぐ使える AI アプリをカテゴリ別に。",
        "LightOn Plus Lab 制作的全部应用。Google Play 与 App Store 上架应用，以及可在浏览器直接使用的 AI 应用，按类别浏览。"),
    "스토어 출시 앱": ("On the stores", "ストア公開アプリ", "商店上架应用"),
    "생산성 · 인앱 구매": ("Productivity · In-app purchases", "仕事効率化 · アプリ内課金", "效率 · 应用内购买"),
    "음악·오디오 · 인앱 구매": ("Music & Audio · In-app purchases", "音楽・オーディオ · アプリ内課金", "音乐与音频 · 应用内购买"),
    "교육 · 인앱 구매": ("Education · In-app purchases", "教育 · アプリ内課金", "教育 · 应用内购买"),
    "통화·회의 녹음을 올리면 AI가 전사·요약·액션 아이템을 만들고, 통화 속 일정은 캘린더에 자동 등록합니다. 화자별 전사와 스크린샷 분석까지.": (
        "Upload a call or meeting recording and AI writes the transcript, the summary and the action items; dates mentioned go straight to the calendar. Speaker-separated transcripts and screenshot analysis too.",
        "通話・会議の録音を上げれば、AI が文字起こし・要約・アクション項目を作り、通話に出た予定はカレンダーへ自動登録。話者分離とスクリーンショット解析まで。",
        "上传通话或会议录音，AI 生成转写、摘要与行动项，通话中提到的日程自动进日历。还支持说话人分离与截图分析。"),
    "장르·분위기·키워드만 고르면 AI가 가사부터 보컬 완곡까지 만들어 줍니다. 음색과 곡 언어(한국어·한+영·영어)를 고를 수 있고, 첫 가입 시 무료 크레딧을 제공합니다.": (
        "Pick genre, mood and keywords and AI takes it from lyrics to a finished vocal track. Choose the voice and the language (Korean, Korean-English, English). Free credits when you sign up.",
        "ジャンル・雰囲気・キーワードを選ぶだけで、AI が歌詞からボーカル完成曲まで。声質と曲の言語（韓国語・韓英・英語）を選べ、初回登録で無料クレジット。",
        "只需选择曲风、氛围与关键词，AI 便从歌词做到完整人声成品。可选音色与歌曲语言（韩语、韩英、英语），注册即赠免费额度。"),
    "강의를 녹음하면 정밀 모드가 화자를 구분해 전사하고, AI가 요약·플래시카드·퀴즈를 만들어 간격반복(SRS)으로 복습시켜 줍니다. 노트는 기기에 암호화 저장됩니다.": (
        "Record a lecture and precision mode transcribes it by speaker; AI builds the summary, flashcards and quizzes and schedules review by spaced repetition. Notes are encrypted on the device.",
        "講義を録音すれば精密モードが話者を分けて文字起こしし、AI が要約・フラッシュカード・クイズを作って間隔反復（SRS）で復習させます。ノートは端末に暗号化保存。",
        "录下课堂，精确模式按说话人转写；AI 生成摘要、闪卡与测验，并以间隔重复（SRS）安排复习。笔记加密存于设备。"),
    "강의를 녹음하면 정밀 모드가 화자를 구분해 전사하고, AI가 요약·플래시카드·퀴즈를 만들어 간격반복(SRS)으로 복습시켜 줍니다.": (
        "Record a lecture and precision mode transcribes it by speaker; AI builds the summary, flashcards and quizzes and schedules review by spaced repetition.",
        "講義を録音すれば精密モードが話者を分けて文字起こしし、AI が要約・フラッシュカード・クイズを作って間隔反復（SRS）で復習させます。",
        "录下课堂，精确模式按说话人转写；AI 生成摘要、闪卡与测验，并以间隔重复（SRS）安排复习。"),
    "업무 관리": ("Work management", "業務管理", "工作管理"),
    "모모아이 Momoi — 웹": ("Momoi — web", "モモアイ Momoi — ウェブ", "Momoi — 网页版"),
    "통화 녹음 → AI가 요약·할 일·일정 자동 추출. AI 인박스 + 캘린더 + PWA.": (
        "Call recording → AI pulls out the summary, tasks and events. An AI inbox, a calendar, a PWA.",
        "通話録音 → AI が要約・タスク・予定を自動抽出。AI インボックス＋カレンダー＋PWA。",
        "通话录音 → AI 自动提取摘要、待办与日程。AI 收件箱 + 日历 + PWA。"),
    "Google Play 앱은 위 출시 앱 섹션에서 받을 수 있습니다.": (
        "The Google Play build is in the store section above.",
        "Google Play 版は上のストアアプリの欄から入手できます。",
        "Google Play 版可在上方商店应用一节获取。"),
    "AI 생산성": ("AI productivity", "AI 生産性", "AI 效率"),
    "AI 계약분석": ("AI Contract Review", "AI 契約書分析", "AI 合同分析"),
    "계약서 업로드 → AI 법률 전문가가 독소조항·위험요소·수정사항을 분석합니다.": (
        "Upload a contract and an AI counsel reads it for poison clauses, risks and the edits to ask for.",
        "契約書をアップロード → AI の法務が毒素条項・リスク・修正点を分析します。",
        "上传合同 → AI 法务分析其中的霸王条款、风险点与修改建议。"),
    "무료 3회 · 베이직 ₩4,900 · 프로 ₩9,900": ("3 free · Basic ₩4,900 · Pro ₩9,900", "無料3回 · ベーシック ₩4,900 · プロ ₩9,900", "免费 3 次 · 基础版 ₩4,900 · 专业版 ₩9,900"),
    "사진 한 장으로 경비 자동 관리. AI OCR + 9개 카테고리 분류 + 월별 리포트.": (
        "Expenses filed from one photo. AI OCR, nine categories, a monthly report.",
        "写真1枚で経費を自動管理。AI OCR＋9カテゴリ分類＋月次レポート。",
        "一张照片自动管理开支。AI OCR + 九类归档 + 月度报表。"),
    "무료 월 10회 · 월간 ₩2,900 · 연간 ₩23,900": ("10 free a month · ₩2,900/mo · ₩23,900/yr", "無料 月10回 · 月額 ₩2,900 · 年額 ₩23,900", "每月免费 10 次 · 月付 ₩2,900 · 年付 ₩23,900"),
    "녹취록AI — 법원 제출용 녹취록": ("Transcript AI — court-ready transcripts", "録取録 AI — 裁判所提出用の書き起こし", "笔录 AI — 可提交法院的笔录"),
    "통화 녹음 업로드 → AI가 화자 분리·타임스탬프·법원 제출 서식까지 자동 정리.": (
        "Upload a call recording and AI separates the speakers, stamps the times and lays it out in court format.",
        "通話録音をアップロード → AI が話者分離・タイムスタンプ・裁判所提出書式まで自動で整えます。",
        "上传通话录音 → AI 自动完成说话人分离、时间戳，直至法院提交格式。"),
    "크레딧 충전식 · ₩4,900부터": ("Prepaid credits · from ₩4,900", "クレジットチャージ式 · ₩4,900から", "充值点数 · ₩4,900 起"),
    "교육 &amp; 성장": ("Learning &amp; growth", "学習＆成長", "学习与成长"),
    "AI 수학 과외 선생님. 초등~수능까지 단계별 문제풀이 + 사진 촬영 해설.": (
        "An AI maths tutor. Step-by-step solutions from primary school to the entrance exam, and explanations from a photo.",
        "AI の数学家庭教師。小学から大学入試まで段階別の解法＋写真を撮れば解説。",
        "AI 数学家教。从小学到高考的分步解法，拍照即可讲解。"),
    "마음을 말하면 AI가 성경 구절을 찾아줍니다. 음성 검색 + 31,088절 전문.": (
        "Say what is on your mind and AI finds the verse. Voice search across all 31,088 verses.",
        "心のうちを話せば AI が聖句を探します。音声検索＋全31,088節。",
        "说出心事，AI 为你找到经文。语音检索，全文 31,088 节。"),
    "무료 설치 · 인앱 구매 · Google Play 출시": ("Free to install · In-app purchases · On Google Play", "無料インストール · アプリ内課金 · Google Play 公開", "免费安装 · 应用内购买 · Google Play 上架"),
    "게임": ("Games", "ゲーム", "游戏"),
    "바스티온-7의 코어를 지키는 타워 디펜스. 터렛 5종, 보스 웨이브, 아레나 5종.": (
        "Tower defense holding the core of Bastion-7. Five turrets, boss waves, five arenas.",
        "バスティオン-7のコアを守るタワーディフェンス。タレット5種、ボスウェーブ、アリーナ5種。",
        "守卫堡垒-7核心的塔防。五种炮塔、Boss 波次、五个竞技场。"),
    "브라우저에서 바로 플레이 · 설치 불필요": ("Plays in the browser · nothing to install", "ブラウザですぐプレイ · インストール不要", "浏览器直接玩 · 无需安装"),
    "도시를 삼키며 커지는 구멍. 무한 모드와 120초 러시, 도시 이벤트와 마일스톤.": (
        "A hole that swallows the city and grows. Endless mode, a 120-second rush, city events and milestones.",
        "街を飲み込みながら大きくなる穴。無限モードと120秒ラッシュ、街のイベントとマイルストーン。",
        "吞噬城市不断变大的洞。无尽模式与 120 秒冲刺，城市事件与里程碑。"),
    "키즈 &amp; 가족": ("Kids &amp; family", "キッズ＆ファミリー", "儿童与家庭"),
    "한글이랑 놀자": ("Play with Hangul", "ハングルとあそぼう", "和韩文一起玩"),
    "어린이 한글 학습 앱. 공룡·로봇 테마, 음성+터치, GPT 대화 지원.": (
        "Hangul for children — dinosaur and robot themes, voice and touch, with GPT conversation.",
        "子ども向けハングル学習。恐竜・ロボットのテーマ、音声＋タッチ、GPT 会話つき。",
        "儿童韩文学习。恐龙与机器人主题，语音加触控，支持 GPT 对话。"),
    "멀티미디어 &amp; 크리에이티브": ("Multimedia &amp; creative", "マルチメディア＆クリエイティブ", "多媒体与创作"),
    "SongBit — AI 뮤직 스튜디오": ("SongBit — AI music studio", "SongBit — AI ミュージックスタジオ", "SongBit — AI 音乐工作室"),
    "장르·분위기만 고르면 AI가 작사부터 보컬 곡까지 2~3분 만에 완성. 악보·뮤직비디오 생성, MP3 다운로드·공유 지원.": (
        "Choose genre and mood and AI goes from lyrics to a vocal track in two or three minutes. Sheet music, music video, MP3 download and sharing.",
        "ジャンルと雰囲気を選ぶだけで、AI が作詞からボーカル曲まで2〜3分で完成。楽譜・ミュージックビデオ生成、MP3 ダウンロードと共有。",
        "只需选曲风与氛围，AI 在 2~3 分钟内从作词完成到人声成品。生成乐谱与音乐视频，支持 MP3 下载与分享。"),
    "충전식 · ₩5,000 (11곡) · ₩10,000 (23곡) · ₩30,000 (70곡) · 앱은 Google Play": (
        "Prepaid · ₩5,000 (11 songs) · ₩10,000 (23) · ₩30,000 (70) · app on Google Play",
        "チャージ式 · ₩5,000（11曲）· ₩10,000（23曲）· ₩30,000（70曲）· アプリは Google Play",
        "充值制 · ₩5,000（11 首）· ₩10,000（23 首）· ₩30,000（70 首）· 应用在 Google Play"),
    "생활 &amp; 반려동물": ("Everyday &amp; pets", "暮らし＆ペット", "生活与宠物"),
    "쿠폰북 — 내 쿠폰 지갑": ("Coupon Book — my coupon wallet", "クーポンブック — わたしのクーポン財布", "优惠券本 — 我的券包"),
    "카페 도장판(횟수)·금액권(잔액)을 등록해 남은 횟수와 잔액 관리. 만료 D-7·3·1 알림 + 매장 근처 도착 알림 + 지도. 데이터는 전부 내 기기에만 저장.": (
        "Register stamp cards and stored-value passes and track what is left. Expiry alerts at 7, 3 and 1 days, an alert when you reach the shop, and a map. All of it stays on your device.",
        "カフェのスタンプカード（回数）・金額券（残高）を登録して残りを管理。期限 D-7・3・1 の通知＋店舗接近の通知＋地図。データはすべて端末内だけ。",
        "登记咖啡店集章卡（次数）与储值券（余额），管理剩余量。到期前 7、3、1 天提醒，靠近门店提醒，附地图。数据全部只存于本机。"),
    "무료 · Google Play · App Store · 웹": ("Free · Google Play · App Store · web", "無料 · Google Play · App Store · ウェブ", "免费 · Google Play · App Store · 网页"),
    "멍냥로그 — 반려동물 일기": ("Pet Log — a diary for your pet", "わんにゃんログ — ペットの日記", "宠物日志 — 毛孩子的日记"),
    "사진을 올리면 AI가 우리 아이 시점의 일기를 대신 써주는 앱. 성격별 말투, 기분 태그 자동 추출, 일기 속 건강 신호 감지.": (
        "Upload a photo and AI writes the diary in your pet's voice — a tone per personality, mood tags pulled out automatically, and health signals spotted in the entries.",
        "写真を上げると AI がうちの子の視点で日記を書くアプリ。性格ごとの口調、気分タグの自動抽出、日記からの健康サイン検知。",
        "上传照片，AI 以毛孩子的视角代写日记。按性格的语气、自动提取情绪标签、从日记中察觉健康信号。"),
    "무료": ("Free", "無料", "免费"),
    "스마트 시티 &amp; 생활정보": ("Smart city &amp; everyday info", "スマートシティ＆生活情報", "智慧城市与生活信息"),
    "노딱 — 주정차 위반 AI": ("Noddak — parking ticket AI", "ノッタク — 駐停車違反 AI", "Noddak — 违停罚单 AI"),
    "딱지 사진 한 장이면 10초 안에 위반 내용·항소 가능성·법적 근거를 분석하고 이의신청서까지 자동 작성. 로그인 없이 사용, 사진은 저장하지 않음.": (
        "One photo of the ticket and in ten seconds it reads the offence, weighs the appeal, cites the law and drafts the objection. No login, and the photo is not kept.",
        "違反切符の写真1枚で10秒以内に内容・不服申立ての見込み・法的根拠を分析し、異議申立書まで自動作成。ログイン不要、写真は保存しません。",
        "一张罚单照片，10 秒内分析违规内容、申诉可能性与法律依据，并自动起草异议书。无需登录，照片不保存。"),
    "크레딧 ₩500/회 · 5회 ₩2,000 · 10회 ₩3,500 · Pro 월 ₩3,900 무제한": (
        "₩500 per use · 5 for ₩2,000 · 10 for ₩3,500 · Pro ₩3,900/mo unlimited",
        "1回 ₩500 · 5回 ₩2,000 · 10回 ₩3,500 · Pro 月額 ₩3,900 無制限",
        "每次 ₩500 · 5 次 ₩2,000 · 10 次 ₩3,500 · Pro 月付 ₩3,900 不限次"),
    "비슷한 앱을 만들고 싶으신가요?": ("Want something like these built?", "こうしたアプリを作りたいですか？", "想做类似的应用吗？"),
    "아이디어가 있으신 분들은 24시간 내 회신드립니다. 첫 상담은 무료.": (
        "Bring the idea and we reply within 24 hours. The first consultation is free.",
        "アイデアがあればお送りください。24時間以内に返信します。初回相談は無料。",
        "有想法就告诉我们，24 小时内回复。首次咨询免费。"),

    # ---------------------------------------------------------------- lens
    "Lens — 렌즈 설계 파일 브라우저 해석 — LightOn Plus Lab": ("Lens — read lens design files in the browser — LightOn Plus Lab", "Lens — レンズ設計ファイルをブラウザで解析 — LightOn Plus Lab", "Lens — 在浏览器解析镜头设计文件 — LightOn Plus Lab"),
    "Lens — 렌즈 해석 — LightOn Plus Lab": ("Lens — optical analysis — LightOn Plus Lab", "Lens — レンズ解析 — LightOn Plus Lab", "Lens — 镜头解析 — LightOn Plus Lab"),
    "광학 설계 · 무료": ("Optical design · free", "光学設計 · 無料", "光学设计 · 免费"),
    "설계 문의": ("Design enquiry", "設計のご相談", "设计咨询"),
    "예제로 들어 있는 트리플렛 f50 F4. 왼쪽이 처방 시트, 오른쪽이 해석 화면입니다.": (
        "The triplet f50 F4 that ships as the sample. Prescription sheet on the left, analysis on the right.",
        "サンプルとして入っているトリプレット f50 F4。左が処方シート、右が解析画面です。",
        "内置示例三片式 f50 F4。左为处方单，右为解析界面。"),
    "파일은 브라우저 안에서만 계산되고 서버로 올라가지 않습니다.": (
        "The file is computed inside your browser and never uploaded.",
        "ファイルはブラウザの中だけで計算され、アップロードされません。",
        "文件只在浏览器内计算，不会上传。"),
    "렌즈 처방은 그 자체가 설계입니다. 남의 서버에 올려 두고 해석할 수 있는 물건이 아니라서, 계산을 전부 브라우저 안에서 하도록 만들었습니다. 파일을 놓는 순간부터 그 데이터는 이 컴퓨터를 떠나지 않습니다.": (
        "A lens prescription is the design. It is not something you can park on somebody else's server to analyse, so the whole computation happens in the browser. From the moment you drop the file, the data does not leave this computer.",
        "レンズ処方はそれ自体が設計です。他人のサーバーに預けて解析できるものではないので、計算をすべてブラウザ内で行うようにしました。ファイルを置いた瞬間から、そのデータはこのコンピュータを離れません。",
        "镜头处方本身就是设计，不是可以放到别人服务器上去分析的东西，所以把全部计算都放在浏览器里。从你放下文件的那一刻起，数据就不会离开这台电脑。"),
    "무엇을 보여주나": ("What it shows", "何を見せるか", "能看到什么"),
    "해석 탭 여섯 개. 열면 바로 계산해서 그립니다.": (
        "Six analysis tabs. Open one and it computes and draws.",
        "解析タブは6つ。開けばその場で計算して描きます。",
        "六个解析标签页。打开即计算并绘制。"),
    "단면 · 1차 특성": ("Layout · first-order", "断面 · 一次特性", "剖面 · 一阶特性"),
    "렌즈 단면과 광선 경로. 초점거리·F수 같은 1차량을 함께 읽습니다.": (
        "The lens cross-section and the ray paths, with first-order quantities like focal length and F-number alongside.",
        "レンズ断面と光線経路。焦点距離・F値といった一次量も併せて読みます。",
        "镜头剖面与光线路径，并同时读取焦距、F 数等一阶量。"),
    "스팟 다이어그램": ("Spot diagram", "スポットダイアグラム", "点列图"),
    "기준 파장 주광선을 기준으로, RMS는 중심(centroid) 기준 직경으로 냅니다.": (
        "Referenced to the chief ray at the reference wavelength; RMS is given as a centroid-based diameter.",
        "基準波長の主光線を基準とし、RMS は重心（centroid）基準の直径で出します。",
        "以基准波长主光线为参考，RMS 以质心（centroid）为基准的直径给出。"),
    "회절 한계를 같이 그려 어디까지가 설계 여유인지 보입니다. 스루포커스는 초점 이동 ±5~50 µm.": (
        "The diffraction limit is drawn alongside, so you can see how much design margin is left. Through-focus runs ±5 to 50 µm.",
        "回折限界も一緒に描き、どこまでが設計余裕かが見えます。スルーフォーカスは焦点移動 ±5〜50 µm。",
        "同时绘出衍射极限，看得出还剩多少设计余量。离焦范围 ±5~50 µm。"),
    "광선 수차": ("Ray aberration", "光線収差", "光线像差"),
    "왼쪽은 접선(Y) εy vs 동공 Py, 오른쪽은 시상(X) εx vs Px. 단위 µm.": (
        "Tangential (Y) εy against pupil Py on the left, sagittal (X) εx against Px on the right. Units are µm.",
        "左はタンジェンシャル（Y）εy vs 瞳 Py、右はサジタル（X）εx vs Px。単位は µm。",
        "左为子午（Y）εy 对瞳孔 Py，右为弧矢（X）εx 对 Px。单位 µm。"),
    "필드 곡률 · 왜곡": ("Field curvature · distortion", "像面湾曲 · 歪曲", "场曲 · 畸变"),
    "비점수차 필드 곡선을 T 실선·S 점선으로, 왜곡은 f·tanθ와 f·θ 기준을 함께.": (
        "Astigmatic field curves as a solid T and a dashed S, with distortion against both f·tanθ and f·θ.",
        "非点収差のフィールドカーブを T 実線・S 点線で、歪曲は f·tanθ と f·θ の両基準で。",
        "像散场曲以 T 实线、S 虚线表示，畸变同时给出 f·tanθ 与 f·θ 两种基准。"),
    "유리": ("Glass", "硝材", "玻璃"),
    "SCHOTT·HOYA·OHARA·CDGM·SUMITA·HIKARI 6개사 1,598종. refractiveindex.info 공개 데이터.": (
        "1,598 glasses from six makers — SCHOTT, HOYA, OHARA, CDGM, SUMITA and HIKARI. Open data from refractiveindex.info.",
        "SCHOTT・HOYA・OHARA・CDGM・SUMITA・HIKARI の6社1,598種。refractiveindex.info の公開データ。",
        "SCHOTT、HOYA、OHARA、CDGM、SUMITA、HIKARI 六家共 1,598 种。来自 refractiveindex.info 的公开数据。"),
    "스팟 다이어그램 — 필드별 스팟과 RMS 직경을 한 화면에.": (
        "Spot diagram — every field's spot and RMS diameter on one screen.",
        "スポットダイアグラム — フィールドごとのスポットと RMS 直径を一画面に。",
        "点列图 — 各视场的点列与 RMS 直径同屏呈现。"),
    "MTF — 회절 한계를 점선으로 겹쳐 그리고, 주파수별 값을 표로 같이 냅니다.": (
        "MTF — the diffraction limit overlaid as a dashed line, with the values by frequency in a table below.",
        "MTF — 回折限界を点線で重ね、周波数ごとの値も表で出します。",
        "MTF — 以虚线叠加衍射极限，并以表格给出各频率数值。"),
    "필드 곡률 · 왜곡 — T·S 곡선과 f·tanθ / f·θ 기준 왜곡.": (
        "Field curvature and distortion — T and S curves, distortion against f·tanθ and f·θ.",
        "像面湾曲・歪曲 — T・S 曲線と f·tanθ / f·θ 基準の歪曲。",
        "场曲与畸变 — T·S 曲线，以及 f·tanθ / f·θ 基准的畸变。"),
    "고쳐 가며 봅니다": ("Edit as you look", "直しながら見ます", "边改边看"),
    "읽기만 하는 뷰어가 아닙니다. 표의 값을 고치면 그 자리에서 다시 계산합니다.": (
        "Not a read-only viewer. Change a value in the table and it recomputes on the spot.",
        "読むだけのビューアではありません。表の値を直せばその場で再計算します。",
        "不是只读查看器。改动表中数值，立刻重新计算。"),
    "면 데이터": ("Surface data", "面データ", "面数据"),
    "반경·두께·유리·반구경을 바로 고칩니다. 반구경은 CIR(사용자 개구) 또는 CODE V 방식의 기본 개구를 씁니다.": (
        "Edit radius, thickness, glass and semi-diameter directly. Semi-diameter comes from CIR (a user aperture) or CODE V's default aperture.",
        "曲率半径・厚み・硝材・半径を直接編集。半径は CIR（ユーザー開口）または CODE V 方式の既定開口を使います。",
        "可直接修改半径、厚度、玻璃与半口径。半口径取自 CIR（用户光阑）或 CODE V 的默认光阑。"),
    "시스템 · 필드 · 파장": ("System · fields · wavelengths", "システム · フィールド · 波長", "系统 · 视场 · 波长"),
    "필드 각과 파장(nm)·가중치를 바꿔 가며 같은 렌즈를 다른 조건에서 봅니다.": (
        "Change field angles and wavelengths with their weights to see the same lens under other conditions.",
        "フィールド角と波長（nm）・重みを変えながら、同じレンズを別の条件で見ます。",
        "改变视场角与波长（nm）及权重，在不同条件下查看同一镜头。"),
    "줌 렌즈는 구간을 전환해 가며 각 위치의 성능을 확인합니다.": (
        "For a zoom, switch between positions and check the performance at each.",
        "ズームレンズは区間を切り替えながら各位置の性能を確認します。",
        "变焦镜头可切换各档位，查看每个位置的性能。"),
    "시작하는 법": ("How to start", "始め方", "如何开始"),
    "파일을 끌어다 놓기": ("Drop a file", "ファイルをドロップ", "拖入文件"),
    "가진 파일이 없다면": ("No file to hand?", "ファイルがなければ", "手头没有文件？"),
    "예제 렌즈가 들어 있습니다. 눌러서 전체 흐름을 먼저 보셔도 됩니다.": (
        "A sample lens is included — open it and walk the whole flow first.",
        "サンプルレンズが入っています。押して一連の流れを先に見ても構いません。",
        "内置示例镜头。可以先打开，把整个流程走一遍。"),
    "네 개 언어": ("Four languages", "4つの言語", "四种语言"),
    "한국어 · English · 日本語 · 中文. 어두운 화면으로 바꿔 쓸 수 있습니다.": (
        "English, 한국어, 日本語 and 中文. There is a dark theme too.",
        "日本語・English・한국어・中文。ダークテーマにも切り替えられます。",
        "中文、English、한국어、日本語。也可切换为深色界面。"),
    "열어 보시면 됩니다": ("Just open it", "開いてみてください", "打开看看就好"),
    "가입도, 설치도, 업로드도 없습니다.": ("No sign-up, no install, no upload.", "登録もインストールもアップロードもありません。", "无需注册、安装或上传。"),
    "다른 제품 보기": ("See other products", "ほかの製品を見る", "查看其他产品"),
    "CODE V .seq와 Zemax OpticStudio .zmx 렌즈 파일을 브라우저에서 열어 단면과 1차 특성, 스팟 다이어그램, MTF, 광선 수차, 필드 곡률을 해석합니다. 파일은 브라우저 안에서만 계산되고 서버로 올라가지 않습니다. 무료.": (
        "Open CODE V .seq and Zemax OpticStudio .zmx lens files in the browser to read layout and first-order properties, spot diagrams, MTF, ray aberrations and field curvature. The file is computed inside the browser and never uploaded. Free.",
        "CODE V の .seq と Zemax OpticStudio の .zmx をブラウザで開き、断面と一次特性、スポットダイアグラム、MTF、光線収差、像面湾曲を解析します。ファイルはブラウザ内だけで計算され、アップロードされません。無料。",
        "在浏览器中打开 CODE V .seq 与 Zemax OpticStudio .zmx 镜头文件，解析剖面与一阶特性、点列图、MTF、光线像差与场曲。文件只在浏览器内计算，不会上传。免费。"),
    "Lens 화면 — 왼쪽은 시스템·파장·필드와 면 데이터 표, 오른쪽은 단면도와 EFL·F수·TTL 같은 1차 특성": (
        "The Lens screen — system, wavelengths, fields and the surface table on the left; the layout and first-order values such as EFL, F-number and TTL on the right",
        "Lens の画面 — 左はシステム・波長・フィールドと面データ表、右は断面図と EFL・F値・TTL などの一次特性",
        "Lens 界面 — 左侧为系统、波长、视场与面数据表，右侧为剖面图及 EFL、F 数、TTL 等一阶特性"),
    "스팟 다이어그램 — 네 개 필드의 스팟과 RMS 직경": (
        "Spot diagram — spots and RMS diameters for four fields",
        "スポットダイアグラム — 4フィールドのスポットと RMS 直径",
        "点列图 — 四个视场的点列与 RMS 直径"),
    "MTF 곡선 — 접선·시상과 회절 한계, 아래에 주파수별 수치 표": (
        "MTF curves — tangential and sagittal with the diffraction limit, and a table of values by frequency below",
        "MTF 曲線 — タンジェンシャル・サジタルと回折限界、下に周波数ごとの数値表",
        "MTF 曲线 — 子午与弧矢及衍射极限，下方为各频率数值表"),
    "비점수차 필드 곡선과 왜곡 그래프, 아래에 상고별 수치 표": (
        "Astigmatic field curves and a distortion plot, with a table of values by image height below",
        "非点収差のフィールドカーブと歪曲グラフ、下に像高ごとの数値表",
        "像散场曲与畸变曲线，下方为各像高数值表"),
}
