# -*- coding: utf-8 -*-
"""홈페이지 번역표 — 한국어 원문 → en / ja / zh.

키는 index.html 의 **텍스트 노드 전체** 또는 **속성값 전체**와 정확히 일치해야 한다.
부분 문자열로 치환하면 '개' 같은 짧은 말이 '개인정보처리방침' 안에서도 바뀐다.
빌드 때 남은 한글이 있으면 gen_blog.py 가 멈춘다.
"""

LANGS = ["en", "ja", "zh"]

LANG_META = {
    "ko": {"label": "한국어", "short": "KO", "html": "ko", "dir": "", "hreflang": "ko"},
    "en": {"label": "English", "short": "EN", "html": "en", "dir": "en/", "hreflang": "en"},
    "ja": {"label": "日本語", "short": "JA", "html": "ja", "dir": "ja/", "hreflang": "ja"},
    "zh": {"label": "中文", "short": "ZH", "html": "zh-Hans", "dir": "zh/", "hreflang": "zh-Hans"},
}

# 인라인 태그가 섞여 조각으로 쪼개지는 문단은 요소째 바꾼다.
# 조각 단위로 옮기면 어순이 다른 언어에서 문장이 깨진다.
BLOCKS = {
    'CODE V <code>.seq</code>와 Zemax OpticStudio <code>.zmx</code>를 그대로 열어 광선추적·스팟·MTF·수차를 봅니다. <b>파일은 브라우저 안에서만 계산되고 서버로 보내지 않습니다.</b> 설계 데이터를 남의 서버에 올릴 수 없는 일이라 그렇게 만들었습니다.': {
        "en": 'Open CODE V <code>.seq</code> and Zemax OpticStudio <code>.zmx</code> files as they are and read ray traces, spot diagrams, MTF and aberrations. <b>The file is computed inside your browser and never sent to a server.</b> A lens prescription is the design, so it could not work any other way.',
        "ja": 'CODE V の <code>.seq</code> と Zemax OpticStudio の <code>.zmx</code> をそのまま開き、光線追跡・スポット・MTF・収差を見ます。<b>ファイルはブラウザの中だけで計算され、サーバーには送りません。</b>設計データを他人のサーバーに預けられない仕事なので、そう作りました。',
        "zh": '直接打开 CODE V 的 <code>.seq</code> 与 Zemax OpticStudio 的 <code>.zmx</code>，查看光线追迹、点列图、MTF 与像差。<b>文件只在浏览器内计算，不会上传到服务器。</b>镜头处方本身就是设计，无法交给别人的服务器，所以做成了这样。',
    },
}

# 텍스트 노드·속성값 전체 일치
T = {
    "LightOn Plus Lab — AI 앱 스튜디오": ("LightOn Plus Lab — AI App Studio", "LightOn Plus Lab — AI アプリスタジオ", "LightOn Plus Lab — AI 应用工作室"),
    "라이트온 플러스 랩 · 경기 안양": ("LightOn Plus Lab · Anyang, Korea", "ライトオン・プラス・ラボ · 韓国 安養", "LightOn Plus Lab · 韩国 安养"),
    "앱을 만들어": ("We build apps,", "アプリを作り、", "我们做应用，"),
    "스토어에 올리고": ("ship them to the stores,", "ストアに出し、", "上架到商店，"),
    "직접 운영합니다.": ("and run them ourselves.", "自分たちで運営します。", "并亲自运营。"),
    "기획·개발·배포·운영을 혼자 끝내는 AI 앱 스튜디오입니다. 스토어에 올린 뒤에도 사용자 피드백으로 계속 고칩니다.": (
        "A one-person AI app studio that takes a product from idea to store listing to daily operation. Shipping is the start — we keep fixing from user feedback.",
        "企画・開発・公開・運営を一人で完結させる AI アプリスタジオです。ストアに出した後も、ユーザーの声で直し続けます。",
        "从策划、开发、上架到运营由一人完成的 AI 应用工作室。上架之后仍根据用户反馈持续打磨。"),
    "출시된 앱 보기": ("See the apps", "アプリを見る", "查看应用"),
    "제작 의뢰하기": ("Start a project", "制作を相談する", "发起项目"),
    "개": ("", "", ""),
    "스토어에 출시한 앱": ("Apps on the stores", "ストア公開アプリ", "已上架应用"),
    "분+": ("min+", "分+", "分+"),
    "송빗이 만드는 곡 길이": ("Song length Songbit writes", "Songbit が作る曲の長さ", "Songbit 生成的歌曲时长"),
    "AI 노트가 인식하는 언어": ("Languages AI Note hears", "AI ノートが聞き分ける言語", "AI 笔记可识别语言"),
    "곳": ("", "", ""),
    "모모아이": ("Momoi", "モモアイ", "Momoi"),
    "통화 녹음 → AI 요약·할 일·일정": ("Call recording → AI summary, tasks, events", "通話録音 → AI 要約・タスク・予定", "通话录音 → AI 摘要・待办・日程"),
    "받기": ("Get", "入手", "获取"),
    "송빗": ("Songbit", "Songbit", "Songbit"),
    "키워드만 고르면 완곡 한 편": ("Pick a few keywords, get a full song", "キーワードを選ぶだけで一曲まるごと", "只需选关键词，生成整首歌"),
    "라이트온 AI 노트": ("LightOn AI Note", "LightOn AI ノート", "LightOn AI 笔记"),
    "강의 전사 + 간격반복 복습": ("Lecture transcripts + spaced review", "講義の文字起こし＋間隔反復", "课堂转写 + 间隔重复复习"),
    "게임 두 편은 설치 없이 브라우저에서 바로 플레이": ("Two games play straight in the browser, nothing to install", "ゲーム2本はインストール不要、ブラウザですぐ遊べます", "两款游戏无需安装，浏览器直接玩"),
    "해보기": ("Play", "遊ぶ", "试玩"),
    "두 스토어에 출시한 앱": ("Apps on both stores", "両ストアで公開中のアプリ", "两大商店上架的应用"),
    "직접 기획하고 만들어 스토어에 올리고, 사용자 피드백으로 계속 고칩니다. Google Play 8개, App Store 7개 — 다섯은 두 곳에 모두 올라가 있습니다.": (
        "Planned, built and shipped here, then kept in repair from user feedback. Eight on Google Play, seven on the App Store — five are on both.",
        "自分たちで企画し、作り、ストアに出し、ユーザーの声で直し続けています。Google Play に8本、App Store に7本 — うち5本は両方にあります。",
        "自行策划、开发、上架，并依据用户反馈持续修正。Google Play 8 款，App Store 7 款 — 其中 5 款两边都有。"),
    "모모아이 Momoi": ("Momoi", "モモアイ Momoi", "Momoi"),
    "생산성": ("Productivity", "仕事効率化", "效率"),
    "인앱 구매": ("In-app purchases", "アプリ内課金", "应用内购买"),
    "회의 녹음 추가": ("Meeting recording added", "会議録音を追加", "新增会议录音"),
    "통화 녹음을 올리면 AI가 요약·할 일·일정을 자동으로. AI가 정리하고, 당신은 실행만.": (
        "Upload a call recording and AI writes the summary, the tasks and the calendar entries. It files; you act.",
        "通話録音を上げれば、AI が要約・タスク・予定まで自動で。整理は AI、あなたは実行だけ。",
        "上传通话录音，AI 自动生成摘要、待办与日程。整理交给 AI，你只管执行。"),
    "녹음을 올리면 전사 → 요약 → 액션 아이템까지 자동 생성": ("Upload once: transcript → summary → action items", "録音を上げるだけで 文字起こし → 要約 → アクション項目まで", "上传录音即可：转写 → 摘要 → 行动项"),
    "화자별 전사로 누가 무슨 말을 했는지 구분": ("Speaker-separated transcripts show who said what", "話者分離で誰が何を言ったかが分かる", "按说话人分离，清楚谁说了什么"),
    "통화 속 일정은 캘린더에 자동 등록 + 리마인더": ("Dates mentioned in the call land in your calendar, with reminders", "通話に出た予定はカレンダーへ自動登録＋リマインド", "通话中提到的日程自动进日历并提醒"),
    "스크린샷·붙여넣은 텍스트도 AI가 프로젝트·마감일로 분류": ("Screenshots and pasted text get sorted into projects and deadlines too", "スクリーンショットや貼り付けたテキストもプロジェクト・期限に仕分け", "截图与粘贴文本也会归入项目与截止日"),
    "웹에서 쓰기": ("Use on the web", "ウェブで使う", "网页版"),
    "자세히": ("Details", "詳しく", "详情"),
    "광고 · 1:00": ("Ad · 1:00", "広告 · 1:00", "广告 · 1:00"),
    "송빗 Songbit": ("Songbit", "Songbit", "Songbit"),
    "음악·오디오": ("Music & Audio", "音楽・オーディオ", "音乐与音频"),
    "무료 크레딧 제공": ("Free credits to start", "無料クレジットあり", "赠送免费额度"),
    "키워드만 고르면 AI가 가사부터 멜로디까지 나만의 노래를 완성해드려요.": (
        "Choose a few keywords and AI writes the lyrics, the melody and the vocal — a song that is yours.",
        "キーワードを選ぶだけで、AI が歌詞からメロディ、ボーカルまで一曲に仕上げます。",
        "只需选几个关键词，AI 便从歌词到旋律、人声完成一首属于你的歌。"),
    "장르·분위기·키워드 선택 → AI 작사 → 보컬 완곡까지": ("Genre, mood, keywords → AI lyrics → finished vocal track", "ジャンル・雰囲気・キーワード → AI 作詞 → ボーカル完成まで", "选择曲风、氛围、关键词 → AI 作词 → 完成人声成品"),
    "음색 선택: 부드러운 · 파워풀 · 허스키 · 랩": ("Pick a voice: soft, powerful, husky or rap", "声質を選択：やわらか・パワフル・ハスキー・ラップ", "音色可选：柔和 · 有力 · 沙哑 · 说唱"),
    "곡 언어 선택: 한국어 · 한+영 믹스 · 영어": ("Pick a language: Korean, Korean-English mix, or English", "曲の言語：韓国語・韓英ミックス・英語", "歌曲语言：韩语 · 韩英混合 · 英语"),
    "만든 곡 보관·재생·공유, 첫 가입 시 무료 크레딧 제공": ("Keep, play and share what you make. Free credits when you sign up.", "作った曲の保存・再生・共有。初回登録で無料クレジット。", "作品可保存、播放与分享，注册即赠免费额度。"),
    "교육": ("Education", "教育", "教育"),
    "강의·회의를 정확히 받아적고, AI 요약과 간격반복 복습으로 진짜 외우게 하는 노트.": (
        "Takes down lectures and meetings accurately, then makes them stick with AI summaries and spaced repetition.",
        "講義や会議を正確に書き取り、AI 要約と間隔反復で本当に覚えさせるノート。",
        "准确记录课堂与会议，再用 AI 摘要和间隔重复真正记住。"),
    "실시간 전사 + 정밀 모드 화자 분리 (한·영·중·일 자동 인식)": ("Live transcription, plus speaker separation in precision mode (Korean, English, Chinese, Japanese detected automatically)", "リアルタイム文字起こし＋精密モードの話者分離（韓・英・中・日を自動判別）", "实时转写，精确模式支持说话人分离（自动识别韩、英、中、日）"),
    "핵심 요약, AI 튜터, 플래시카드·퀴즈 자동 생성": ("Key summaries, an AI tutor, flashcards and quizzes generated for you", "要点要約、AI チューター、フラッシュカード・クイズを自動生成", "要点摘要、AI 导师、自动生成闪卡与测验"),
    "과학적 간격 반복(SRS)으로 복습 타이밍 자동 관리": ("Spaced repetition (SRS) decides when you review", "科学的な間隔反復（SRS）で復習タイミングを自動管理", "以科学的间隔重复（SRS）自动安排复习时机"),
    "노트는 기기에 암호화 저장 — 클라우드 동기화·광고·추적 없음": ("Notes are encrypted on the device — no cloud sync, no ads, no tracking", "ノートは端末に暗号化保存 — クラウド同期・広告・追跡なし", "笔记加密存于本机 — 无云同步、无广告、无追踪"),
    "중요한 대화일수록 먼저 말해 보는 AI 음성 대화 연습 코치.": (
        "A voice coach for the conversations that matter — rehearse them before you have them.",
        "大事な話ほど先に言ってみる、AI 音声会話の練習コーチ。",
        "越重要的对话越要先练一遍 — AI 语音对话陪练。"),
    "쿠폰북": ("Coupon Book", "クーポンブック", "优惠券本"),
    "종이 쿠폰·도장판·이용권을 한곳에. 회원가입 없이 내 폰에만 저장됩니다.": (
        "Paper coupons, stamp cards and passes in one place. No sign-up — it stays on your phone.",
        "紙のクーポン・スタンプカード・回数券を一か所に。登録不要、端末の中だけに保存。",
        "纸质优惠券、集章卡与次卡集中管理。无需注册，只存在手机里。"),
    "주말 안에 한글 읽기. 마흔 글자를 획순으로 익히는 무료 학습 앱.": (
        "Read Hangul in a weekend. Forty letters, stroke by stroke, free.",
        "週末でハングルが読める。40文字を筆順で覚える無料アプリ。",
        "一个周末学会读韩文。四十个字母，按笔顺学，免费。"),
    "가나다 놀이": ("Ganada Play", "ガナダ遊び", "Ganada 识字"),
    "아기 호랑이 호야와 자음·모음부터 낱말·문장까지. 소리와 획순으로 배우는 유아 한글.": (
        "From consonants and vowels to words and sentences, with Hoya the tiger cub. Hangul for small children, by sound and stroke order.",
        "子トラのホヤと一緒に、子音・母音から単語・文章まで。音と筆順で学ぶ幼児ハングル。",
        "和小老虎 Hoya 一起，从辅音元音到词语句子。用声音和笔顺学的幼儿韩文。"),
    "돌맹이 아레나": ("Stone Arena", "ストーンアリーナ", "石子竞技场"),
    "오목·알까기·바둑·장기·체스 다섯 종을 한 앱에. 컴퓨터 10단계와 2인 대국.": (
        "Gomoku, Alkkagi, Go, Janggi and Chess in one app. Ten computer levels and two-player games.",
        "五目並べ・アルカギ・囲碁・チャンギ・チェスの5種を1つに。CPU10段階と2人対局。",
        "五子棋、弹石棋、围棋、韩国象棋、国际象棋五合一。电脑十级与双人对弈。"),
    "타워 디펜스": ("Tower Defense", "タワーディフェンス", "塔防"),
    "정통 타워 디펜스. 광고 없이 한 번 구매로 끝나고 오프라인에서도 돌아갑니다.": (
        "Classic tower defense. One purchase, no ads, works offline.",
        "正統派タワーディフェンス。広告なし、買い切り、オフラインでも動きます。",
        "正统塔防。无广告，一次买断，离线可玩。"),
    "사방에서 몰려오는 군체로부터 코어를 지키는 웨이브 디펜스.": (
        "Wave defense — hold the core against a swarm closing in from every side.",
        "四方から迫る群体からコアを守るウェーブディフェンス。",
        "波次防守 — 抵挡四面八方涌来的虫群，守住核心。"),
    "브라우저에서 바로": ("Play in browser", "ブラウザですぐ", "浏览器直接玩"),
    "광학 설계": ("Optical design", "光学設計", "光学设计"),
    "렌즈 설계 파일을 브라우저에서 엽니다": ("Open lens design files in the browser", "レンズ設計ファイルをブラウザで開きます", "在浏览器里打开镜头设计文件"),
    "렌즈 데이터": ("Lens data", "レンズデータ", "镜头数据"),
    "면·반경·두께·유리·굴절률을 처방 시트처럼 읽습니다.": (
        "Surfaces, radii, thickness, glass and index — read like a prescription sheet.",
        "面・曲率半径・厚み・硝材・屈折率を処方シートのように読みます。",
        "面、半径、厚度、玻璃与折射率，像处方单一样读。"),
    "수차와 왜곡": ("Aberration and distortion", "収差と歪曲", "像差与畸变"),
    "비점수차 필드 곡선(T·S)과 f·tanθ / f·θ 기준 왜곡을 함께 봅니다.": (
        "Astigmatic field curves (T and S) next to distortion against f·tanθ and f·θ.",
        "非点収差のフィールドカーブ（T・S）と、f·tanθ / f·θ 基準の歪曲を並べて見ます。",
        "像散场曲（T·S）与以 f·tanθ / f·θ 为基准的畸变并排查看。"),
    "스루포커스 MTF": ("Through-focus MTF", "スルーフォーカス MTF", "离焦 MTF"),
    "초점 이동 ±5~50 µm 구간에서 주파수별 응답을 확인합니다.": (
        "Response by frequency across a focus shift of ±5 to 50 µm.",
        "フォーカス移動 ±5〜50 µm の範囲で周波数ごとの応答を確認します。",
        "在 ±5~50 µm 的离焦范围内查看各频率响应。"),
    "줌 위치": ("Zoom positions", "ズーム位置", "变焦位置"),
    "줌 구간을 바꿔 가며 보고, 바로 열어 볼 예제 렌즈가 들어 있습니다.": (
        "Switch between zoom positions. A sample lens is included to open right away.",
        "ズーム位置を切り替えながら確認。すぐ開けるサンプルレンズ入り。",
        "可切换变焦位置查看，并内置可直接打开的示例镜头。"),
    "한국어 · English · 日本語 · 中文": ("English · 한국어 · 日本語 · 中文", "日本語 · English · 한국어 · 中文", "中文 · English · 한국어 · 日本語"),
    "Lens 열기": ("Open Lens", "Lens を開く", "打开 Lens"),
    "운영 원칙": ("How we operate", "運営の原則", "运营原则"),
    "Google Play 데이터 보안 항목에 선언한 내용 그대로입니다.": (
        "Exactly what we declare in the Google Play Data Safety section.",
        "Google Play のデータセーフティに申告した内容そのままです。",
        "与我们在 Google Play 数据安全中声明的内容一致。"),
    "전송 중 암호화": ("Encrypted in transit", "通信の暗号化", "传输加密"),
    "모모아이·송빗·AI 노트가 데이터를 암호화해 전송합니다.": (
        "Momoi, Songbit and AI Note encrypt data in transit.",
        "モモアイ・Songbit・AI ノートはデータを暗号化して送信します。",
        "Momoi、Songbit 与 AI 笔记均加密传输数据。"),
    "데이터 삭제 요청": ("Deletion on request", "データ削除の請求", "可申请删除数据"),
    "언제든 계정과 데이터의 삭제를 요청할 수 있습니다.": (
        "You can ask us to delete your account and data at any time.",
        "アカウントとデータの削除はいつでも請求できます。",
        "你可以随时要求删除账号与数据。"),
    "AI 노트는 기기 저장": ("AI Note stays on device", "AI ノートは端末保存", "AI 笔记存于本机"),
    "노트를 기기에 암호화 저장하고, 광고·행동 추적을 하지 않습니다.": (
        "Notes are encrypted on the device. No ads, no behavioural tracking.",
        "ノートは端末に暗号化保存し、広告も行動追跡も行いません。",
        "笔记加密保存在设备上，不投放广告、不进行行为追踪。"),
    "서울 리전 운영": ("Run in the Seoul region", "ソウルリージョンで運用", "运行于首尔区域"),
    "백엔드는 Google Cloud Run 서울 리전(asia-northeast3)에서 동작합니다.": (
        "The backend runs on Google Cloud Run in the Seoul region (asia-northeast3).",
        "バックエンドは Google Cloud Run のソウルリージョン（asia-northeast3）で動きます。",
        "后端运行在 Google Cloud Run 首尔区域（asia-northeast3）。"),
    "기술 구성": ("What it runs on", "技術構成", "技术构成"),
    "실제로 이 앱들이 돌아가는 구성입니다. 쓰지 않는 기술은 적지 않습니다.": (
        "What these apps actually run on. Nothing listed that we do not use.",
        "実際にこれらのアプリが動いている構成です。使っていない技術は書きません。",
        "这些应用真实运行所依赖的构成。没用到的技术不会写上去。"),
    "Cloud Run (서울 리전)": ("Cloud Run (Seoul region)", "Cloud Run（ソウルリージョン）", "Cloud Run（首尔区域）"),
    "Soniox 전사 · 화자 분리": ("Soniox transcription & diarization", "Soniox 文字起こし・話者分離", "Soniox 转写与说话人分离"),
    "AI 음악 생성 엔진": ("AI music generation engine", "AI 音楽生成エンジン", "AI 音乐生成引擎"),
    "앱": ("App", "アプリ", "应用"),
    "Google Play 인앱결제": ("Google Play Billing", "Google Play アプリ内課金", "Google Play 应用内结算"),
    "웹": ("Web", "ウェブ", "网页"),
    "토스페이먼츠": ("Toss Payments", "Toss Payments", "Toss Payments"),
    "그 밖에 운영 중인 서비스": ("Other things we run", "そのほかに運営中のサービス", "其他在运营的服务"),
    "스토어 앱 외에도 웹에서 바로 쓸 수 있는 앱과 게임을 만들어 운영합니다. 게임은 설치 없이 눌러서 해볼 수 있습니다.": (
        "Besides the store apps we build and run web apps and games. The games open and play with nothing to install.",
        "ストアアプリのほかに、ウェブですぐ使えるアプリやゲームも作って運営しています。ゲームはインストール不要で遊べます。",
        "除了商店应用，我们还做并运营网页应用和游戏。游戏无需安装，点开即玩。"),
    "말씀찾기": ("Bible Search", "みことば検索", "经文检索"),
    "음성·텍스트로 성경 구절을 검색하고 감정별 탐색과 읽기 계획까지 제공하는 AI 동반자.": (
        "Search scripture by voice or text, browse by feeling, and follow a reading plan.",
        "音声やテキストで聖句を検索し、感情別に探し、通読プランまで。",
        "用语音或文字检索经文，按心情浏览，还有读经计划。"),
    "영수증 AI": ("Receipt AI", "レシート AI", "票据 AI"),
    "사진 한 장으로 경비를 자동 관리하는 AI OCR — 9개 카테고리 분류와 월별 리포트 제공.": (
        "AI OCR that files expenses from one photo — nine categories and a monthly report.",
        "写真1枚で経費を自動管理する AI OCR — 9カテゴリ分類と月次レポート。",
        "一张照片自动管理开支的 AI OCR — 九类归档与月度报表。"),
    "도시를 삼키며 커지는 구멍. 무한 모드와 2분 러시 — 설치 없이 브라우저에서 바로 플레이.": (
        "A hole that swallows the city and grows. Endless mode and a two-minute rush — plays in the browser.",
        "街を飲み込みながら大きくなる穴。無限モードと2分ラッシュ — ブラウザですぐ。",
        "吞噬城市不断变大的洞。无尽模式与两分钟冲刺 — 浏览器直接玩。"),
    "노딱": ("Noddak", "ノッタク", "Noddak"),
    "딱지 사진 한 장으로 위반 내용·항소 가능성·법적 근거를 분석하고 이의신청서까지 작성합니다.": (
        "Photograph the ticket and it reads the offence, weighs the appeal and drafts the objection.",
        "違反切符の写真1枚から内容・不服申立ての見込み・法的根拠を分析し、異議申立書まで作成。",
        "拍一张罚单照片，即可分析违规内容、申诉可能性与法律依据，并代写异议书。"),
    "멍냥로그": ("Pet Log", "わんにゃんログ", "宠物日志"),
    "사진을 올리면 AI가 우리 아이 시점으로 일기를 씁니다. 기분 태그와 건강 신호까지 잡아냅니다.": (
        "Upload a photo and AI keeps the diary in your pet's voice, tagging mood and health signals.",
        "写真を上げると AI がうちの子の視点で日記を書きます。気分タグや健康サインも拾います。",
        "上传照片，AI 以毛孩子的视角写日记，还会标出情绪与健康信号。"),
    "우리집 식탁": ("Our Family Table", "わが家の食卓", "我家餐桌"),
    "가족 인원과 한 달 식비를 정하면 주간 식단과 장보기 목록을 만들고, 담은 재료가 싸지면 알려줍니다.": (
        "Set the family size and the monthly food budget; it plans the week, builds the shopping list and tells you when something in the basket gets cheaper.",
        "家族の人数と月の食費を決めれば、週の献立と買い物リストを作り、カゴの材料が安くなったら知らせます。",
        "设定家庭人数与月度food预算，它会安排一周菜单、生成购物清单，并在篮中食材降价时通知你。"),
    "수학친구": ("Math Friend", "数学フレンド", "数学伙伴"),
    "초등부터 수능까지 단계별 풀이. 문제를 사진으로 찍으면 AI가 해설해 줍니다.": (
        "Step-by-step solutions from primary school to the college entrance exam. Photograph a problem and AI explains it.",
        "小学から大学入試まで段階別の解法。問題を撮れば AI が解説します。",
        "从小学到高考的分步解法。拍下题目，AI 为你讲解。"),
    "전체 작업 보기": ("See all our work", "すべての制作を見る", "查看全部作品"),
    "만들면서 쓴 글": ("Notes from building", "作りながら書いたもの", "开发手记"),
    "앱을 만들고 스토어에 올리면서 실제로 부딪힌 것들을 기록합니다.": (
        "What we actually ran into while building apps and getting them onto the stores.",
        "アプリを作ってストアに出す中で実際にぶつかったことを記録しています。",
        "记录做应用、上架过程中真正遇到的问题。"),
    "강의를 녹음하고 요약해도 왜 안 외워질까": ("Why recording and summarising a lecture still does not make it stick", "講義を録音して要約しても、なぜ覚えられないのか", "录音加摘要，为什么还是记不住"),
    "전사와 요약은 이제 흔한 기능이 됐습니다. 그런데 노트가 깔끔할수록 다시 안 보게 되는 역설이 있습니다. 망각 곡선과 간격 반복이 그 빈틈을 어떻게 메우는지 정리했습니다.": (
        "Transcription and summaries are everywhere now. The paradox is that the tidier the note, the less you go back to it. On the forgetting curve and what spaced repetition fills in.",
        "文字起こしと要約はもう当たり前の機能です。ところがノートが整うほど見返さなくなるという逆説があります。忘却曲線と間隔反復がその隙間をどう埋めるか。",
        "转写和摘要早已普及。悖论在于：笔记越整洁，越不会再看。关于遗忘曲线，以及间隔重复如何补上这段空缺。"),
    "가사 싱크가 최대 16초 밀린 이유 — 세지 말고 대조하라": ("Why the lyrics drifted up to 16 seconds — match, do not count", "歌詞同期が最大16秒ずれた理由 — 数えるな、照合しろ", "歌词最多偏移 16 秒的原因 — 别数，去比对"),
    "가라오케 가사가 곡 후반으로 갈수록 밀렸고, 한국어 곡에서 유독 심했습니다. 원인은 타임스탬프가 아니라 단어를 세는 방식이었습니다. 비례식 추정을 문자 오프셋 대조로 바꾼 기록.": (
        "Karaoke lyrics drifted further the longer the song ran, and worst in Korean. The culprit was not the timestamps but how we counted words. Replacing proportional estimation with character-offset matching.",
        "カラオケ歌詞が曲の後半ほどずれ、韓国語曲で特にひどい。原因はタイムスタンプではなく単語の数え方でした。比例推定を文字オフセット照合に変えた記録。",
        "卡拉OK歌词越到后半越偏，韩语歌尤其严重。问题不在时间戳，而在数词的方式。把比例估算改为字符偏移比对的记录。"),
    "웹앱을 구글 플레이에 올리기 — TWA 출시 실전 기록": ("Putting a web app on Google Play — a TWA release, in practice", "ウェブアプリを Google Play に出す — TWA 公開の実録", "把网页应用上架 Google Play — TWA 发布实录"),
    "PWA를 TWA로 감싸 Google Play에 출시하며 실제로 겪은 절차와 함정들 — assetlinks, AAB 서명, target API, 비공개 테스트 요건까지.": (
        "Wrapping a PWA as a TWA and shipping it: the steps and the traps — assetlinks, AAB signing, target API, closed-testing requirements.",
        "PWA を TWA で包んで Google Play に出すまでの手順と落とし穴 — assetlinks、AAB 署名、target API、クローズドテスト要件まで。",
        "把 PWA 包成 TWA 上架 Google Play 的实际流程与坑 — assetlinks、AAB 签名、target API、封闭测试要求。"),
    "전체 글 보기": ("Read all posts", "すべての記事を見る", "查看全部文章"),
    "직접 만들어 본 사람에게 맡기세요": ("Hand it to someone who has shipped one", "自分で作って出した人に任せてください", "交给真正做过并上架的人"),
    "같은 방식으로 여러분의 제품도 만듭니다. 기획부터 스토어 등록·인앱결제 연동·운영까지 한 사람이 이어서 담당합니다.": (
        "We build your product the same way. One person carries it from planning through store listing, in-app billing and operation.",
        "同じやり方であなたの製品も作ります。企画からストア登録・アプリ内課金・運営まで、一人が最後まで担当します。",
        "我们用同样的方式做你的产品。从策划到上架、内购接入与运营，由一人全程负责。"),
    "문제와 사용자 흐름 정리": ("Frame the problem and the user flow", "課題とユーザーフローの整理", "梳理问题与用户流程"),
    "핵심 AI 기능 검증": ("Prove the core AI feature", "中核となる AI 機能の検証", "验证核心 AI 功能"),
    "웹·앱 배포와 연동": ("Ship web and app, wired up", "ウェブ・アプリの公開と連携", "网页与应用的发布与打通"),
    "데이터 기반 개선": ("Improve from the data", "データに基づく改善", "基于数据的改进"),
    "2~6주 안에 실제로 동작하는 MVP를 만들어 가설을 빠르게 검증합니다.": (
        "A working MVP in two to six weeks, so the hypothesis gets tested early.",
        "2〜6週間で実際に動く MVP を作り、仮説を早く検証します。",
        "2~6 周内做出真正可用的 MVP，尽早验证假设。"),
    "LLM·전사·화자 분리·생성형 미디어를 직접 붙여 본 경험으로 설계합니다.": (
        "Designed by someone who has wired up LLMs, transcription, diarization and generative media firsthand.",
        "LLM・文字起こし・話者分離・生成メディアを実際に組み込んだ経験で設計します。",
        "以亲手接入 LLM、转写、说话人分离与生成式媒体的经验来设计。"),
    "웹·앱 배포부터 스토어 등록과 인앱결제 연동까지 실제로 출시해 드립니다.": (
        "From deployment to store listing and in-app billing — we actually ship it.",
        "ウェブ・アプリの公開からストア登録、アプリ内課金の連携まで、実際に出します。",
        "从发布到上架、内购接入 — 我们真的把它推上线。"),
    "출시 후 30일 무상 수정. 소스코드는 100% 인계하고 락인은 없습니다.": (
        "Thirty days of free fixes after launch. You get all the source. No lock-in.",
        "公開後30日間は無償修正。ソースコードは100%引き渡し、ロックインはありません。",
        "上线后 30 天免费修正。源码 100% 交付，不做绑定。"),
    "프로젝트가 있으신가요?": ("Have a project?", "プロジェクトがありますか？", "有项目吗？"),
    "아이디어 단계든, 이미 돌아가는 서비스에 AI를 붙이고 싶은 단계든 괜찮습니다. 24시간 안에 회신드립니다.": (
        "An idea, or an AI feature for something already running — either is fine. We reply within 24 hours.",
        "アイデア段階でも、すでに動いているサービスに AI を足したい段階でも構いません。24時間以内に返信します。",
        "无论是想法阶段，还是想给已在运行的服务加上 AI，都可以。我们 24 小时内回复。"),
    "상담 요청": ("Get in touch", "相談する", "联系我们"),
    "AI를 실제 제품으로 만드는 1인 스튜디오. 경기도 안양.": (
        "A one-person studio that turns AI into shipped products. Anyang, Korea.",
        "AI を実際の製品にする一人スタジオ。韓国・安養。",
        "把 AI 做成真实产品的一人工作室。韩国安养。"),
    "전체 앱": ("All apps", "すべてのアプリ", "全部应用"),
    "Lens 렌즈 해석": ("Lens — optical analysis", "Lens レンズ解析", "Lens 镜头解析"),
    "카카오톡 1:1 문의": ("KakaoTalk chat", "KakaoTalk で問い合わせ", "KakaoTalk 咨询"),
    "개인정보처리방침": ("Privacy Policy", "プライバシーポリシー", "隐私政策"),
    "이용약관": ("Terms of Service", "利用規約", "服务条款"),
    "상호: 라이트온 플러스 랩 · 대표: 박승혁 · 사업자등록번호 229-15-70907 · 통신판매업신고: 제 2026-안양동안-0514 호 · 경기도 안양시 동안구 관평로 333, 6동 504호(관양동)": (
        "LightOn Plus Lab · Representative: Seunghyuk Park · Business reg. 229-15-70907 · E-commerce reg. 2026-Anyang Dongan-0514 · 333 Gwanpyeong-ro, Dongan-gu, Anyang, Gyeonggi, Korea (Bldg 6, #504)",
        "商号: ライトオン・プラス・ラボ · 代表: パク・スンヒョク · 事業者登録番号 229-15-70907 · 通信販売業申告 第2026-安養東安-0514号 · 韓国 京畿道安養市東安区冠坪路333、6棟504号",
        "商号：LightOn Plus Lab · 代表：朴丞赫 · 营业执照号 229-15-70907 · 电子商务备案 第2026-安养东安-0514号 · 韩国京畿道安养市东安区冠坪路 333 号 6 栋 504 室"),
    "모모아이·송빗·라이트온 AI 노트를 만드는 1인 AI 앱 스튜디오. Google Play 출시·운영.": (
        "The one-person AI app studio behind Momoi, Songbit and LightOn AI Note. Shipped and run on Google Play.",
        "モモアイ・Songbit・LightOn AI ノートを作る一人 AI アプリスタジオ。Google Play で公開・運営。",
        "打造 Momoi、Songbit 与 LightOn AI 笔记的一人 AI 应用工作室。在 Google Play 上架并运营。"),
    "모모아이 · 송빗 · 라이트온 AI 노트 — Google Play에서 서비스 중인 AI 앱을 직접 만들고 운영합니다.": (
        "Momoi · Songbit · LightOn AI Note — AI apps we build and run ourselves, live on Google Play.",
        "モモアイ · Songbit · LightOn AI ノート — Google Play で提供中の AI アプリを自分たちで作り運営しています。",
        "Momoi · Songbit · LightOn AI 笔记 — 我们自行开发并运营、已在 Google Play 上线的 AI 应用。"),
    "LightOn Plus Lab 홈": ("LightOn Plus Lab home", "LightOn Plus Lab ホーム", "LightOn Plus Lab 首页"),
    "메뉴": ("Menu", "メニュー", "菜单"),
    "모바일 메뉴": ("Mobile menu", "モバイルメニュー", "移动端菜单"),
    "모모아이 광고 영상 재생 — 1분, 소리 있음": ("Play the Momoi ad — one minute, with sound", "モモアイの広告を再生 — 1分、音あり", "播放 Momoi 广告 — 1 分钟，有声"),
    "송빗 광고 영상 재생 — 1분, 소리 있음": ("Play the Songbit ad — one minute, with sound", "Songbit の広告を再生 — 1分、音あり", "播放 Songbit 广告 — 1 分钟，有声"),
    "라이트온 AI 노트의 AI 요약 화면 — 핵심 요약, 키포인트, 챕터별 정리로 나뉜 강의 요약": (
        "LightOn AI Note's summary screen — a lecture broken into key summary, key points and chapters",
        "LightOn AI ノートの AI 要約画面 — 要点要約・キーポイント・章立てに分かれた講義要約",
        "LightOn AI 笔记的摘要界面 — 分为要点摘要、关键点与章节的课堂整理"),
}


# JSON-LD 안의 한글 — 영문 페이지에 한국어 구조화 데이터가 남으면
# 검색 결과 스니펫이 한국어로 나온다. 앱 이름은 실제 App Store 영문 등록명을 쓴다.
LD = {
    "라이트온 플러스 랩": ("LightOn Plus Lab", "ライトオン・プラス・ラボ", "LightOn Plus Lab"),
    "경기도": ("Gyeonggi-do", "京畿道", "京畿道"),
    "안양시": ("Anyang-si", "安養市", "安养市"),
    "AI를 실제 제품으로 만드는 1인 스튜디오. 기획부터 배포·운영까지 AI 앱을 직접 만들어 운영합니다.": (
        "A one-person studio that turns AI into shipped products — planned, released and operated in-house.",
        "AI を実際の製品にする一人スタジオ。企画から公開・運営まで自分たちで手がけます。",
        "把 AI 做成真实产品的一人工作室。从策划到发布与运营，全部自行完成。"),
    "모모아이 Momoi - AI 통화 요약, 회의록": ("Momoi — AI Call Summary & Meeting Notes", "モモアイ Momoi — AI 通話要約・議事録", "Momoi — AI 通话摘要与会议记录"),
    "통화 녹음을 올리면 AI가 요약·할 일·일정을 자동으로 만들어 주는 AI 인박스와 캘린더.": (
        "An AI inbox and calendar: upload a call recording and it writes the summary, tasks and events.",
        "通話録音を上げれば要約・タスク・予定を自動で作る AI インボックスとカレンダー。",
        "上传通话录音即自动生成摘要、待办与日程的 AI 收件箱与日历。"),
    "송빗 Songbit - AI 노래 만들기": ("Songbit - AI Song Maker", "Songbit - AI 作曲", "Songbit - AI 歌曲创作"),
    "장르·분위기·키워드만 고르면 AI가 가사부터 보컬 완곡까지 만들어 주는 AI 음악 스튜디오.": (
        "An AI music studio: pick genre, mood and keywords, and it writes the lyrics through to a finished vocal track.",
        "ジャンル・雰囲気・キーワードを選ぶだけで、歌詞からボーカル完成曲まで作る AI 音楽スタジオ。",
        "只需选择曲风、氛围与关键词，便从歌词到完整人声成品的 AI 音乐工作室。"),
    "라이트온 AI 노트: 강의 녹음 암기": ("LightOn AI Note", "LightOn AI ノート", "LightOn AI 笔记"),
    "강의·회의를 화자 분리로 전사하고, AI 요약과 간격반복(SRS) 복습으로 외우게 하는 노트 앱.": (
        "A note app that transcribes lectures and meetings with speaker separation, then makes them stick with AI summaries and spaced repetition.",
        "講義や会議を話者分離で文字起こしし、AI 要約と間隔反復（SRS）で覚えさせるノートアプリ。",
        "以说话人分离转写课堂与会议，再用 AI 摘要与间隔重复（SRS）帮助记忆的笔记应用。"),
    "중요한 대화를 먼저 말해 보고 점검하는 AI 음성 대화 연습 코치.": (
        "A voice coach for rehearsing and reviewing the conversations that matter.",
        "大事な会話を先に話してみて点検する、AI 音声会話の練習コーチ。",
        "先把重要对话说一遍再检视的 AI 语音对话陪练。"),
    "쿠폰북 — 내 쿠폰·도장·이용권 지갑": ("Coupon Book: Stamps & Passes", "クーポンブック — クーポン・スタンプ・回数券の財布", "优惠券本 — 券、印章与次卡钱包"),
    "종이 쿠폰·도장판·이용권을 회원가입 없이 기기에만 저장해 관리하는 쿠폰 지갑.": (
        "A coupon wallet that keeps paper coupons, stamp cards and passes on the device, with no sign-up.",
        "紙のクーポン・スタンプカード・回数券を登録不要で端末だけに保存して管理する財布。",
        "无需注册、仅存于本机的优惠券、集章卡与次卡钱包。"),
    "한글 마흔 글자를 획순으로 익히는 무료 한국어 읽기 학습 앱.": (
        "A free app for learning to read Korean — forty Hangul letters, stroke by stroke.",
        "ハングル40文字を筆順で覚える無料の韓国語リーディング学習アプリ。",
        "按笔顺学会四十个韩文字母的免费韩语阅读学习应用。"),
    "가나다 놀이 - 유아 한글 첫걸음": ("Ganada Play — first steps in Hangul", "ガナダ遊び — 幼児のハングル入門", "Ganada 识字 — 幼儿韩文启蒙"),
    "자음·모음부터 낱말·문장까지 소리와 획순으로 배우는 만 3~7세 한글 학습 앱.": (
        "Hangul for ages three to seven — consonants and vowels through to words and sentences, by sound and stroke order.",
        "子音・母音から単語・文章まで、音と筆順で学ぶ3〜7歳向けハングル学習アプリ。",
        "面向 3~7 岁，从辅音元音到词句、以声音与笔顺学习的韩文应用。"),
    "돌맹이 아레나": ("Stone Arena", "ストーンアリーナ", "石子竞技场"),
    "오목·알까기·바둑·장기·체스 다섯 종을 담은 보드게임 모음. 컴퓨터 10단계와 2인 대국.": (
        "Five board games in one — Gomoku, Alkkagi, Go, Janggi and Chess. Ten computer levels and two-player play.",
        "五目並べ・アルカギ・囲碁・チャンギ・チェスの5種を収めたボードゲーム集。CPU10段階と2人対局。",
        "五子棋、弹石棋、围棋、韩国象棋、国际象棋五合一的棋类合集。电脑十级与双人对弈。"),
    "타워 디펜스: 왕국 방어전": ("Tower Defense: Kingdom Siege", "タワーディフェンス：王国防衛戦", "塔防：王国保卫战"),
    "타워 10종으로 왕국을 지키는 정통 타워 디펜스. 광고 없이 오프라인으로 즐깁니다.": (
        "Classic tower defense with ten towers. No ads, plays offline.",
        "10種のタワーで王国を守る正統派タワーディフェンス。広告なし、オフラインで遊べます。",
        "用十种塔守卫王国的正统塔防。无广告，可离线游玩。"),
    "CORE SIEGE: 바스티온-7": ("CORE SIEGE: Bastion-7", "CORE SIEGE：バスティオン-7", "CORE SIEGE：堡垒-7"),
    "사방에서 몰려오는 군체로부터 코어를 지키는 SF 웨이브 디펜스.": (
        "Science-fiction wave defense — hold the core against a swarm closing in from every side.",
        "四方から迫る群体からコアを守る SF ウェーブディフェンス。",
        "抵挡四面涌来的虫群、守住核心的科幻波次防守。"),
    "CODE V .seq와 Zemax OpticStudio .zmx 렌즈 파일을 브라우저에서 열어 광선추적·스팟·MTF·수차를 해석하는 도구. 파일은 브라우저 안에서만 계산된다.": (
        "A tool that opens CODE V .seq and Zemax OpticStudio .zmx lens files in the browser for ray tracing, spot diagrams, MTF and aberrations. The file is computed inside the browser only.",
        "CODE V の .seq と Zemax OpticStudio の .zmx をブラウザで開き、光線追跡・スポット・MTF・収差を解析するツール。ファイルはブラウザ内だけで計算されます。",
        "在浏览器中打开 CODE V .seq 与 Zemax OpticStudio .zmx 镜头文件，进行光线追迹、点列图、MTF 与像差分析的工具。文件仅在浏览器内计算。"),
}
