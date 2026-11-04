# -*- coding: utf-8 -*-
"""lens.html 이 2026-10-22 이후 늘어난 만큼의 번역표.

PR #47~#49 에서 Lens 페이지에 해석 탭 설명·가이드 카드 10장·상표 고지가 붙고
공용 푸터에 「Lens 문서」가 들어왔다. 10-22 번역표에는 그 문구가 없어 영어판에
한글이 남는다 — build_i18n 의 한글 검사기가 빌드를 세운다.

광학 용어는 업계에서 쓰는 표현으로 옮긴다(상대 조도 → relative illumination,
에너지 집중도 → enclosed energy, 상면 만곡 → field curvature, 주광선 → chief
ray, 처짐 → sag, CRA → chief ray angle). 직역하면 검색도 안 되고 읽는 사람이
무슨 지표인지 못 알아본다.
"""

_LENS_DESC = ("CODE V .seq와 Zemax OpticStudio .zmx, CSV 렌즈 표를 브라우저에서 열어 단면과 1차 특성, "
              "스팟 다이어그램, MTF, 광선 수차, 필드 곡률·왜곡·색수차, PSF·에너지 집중도, 상대 조도, "
              "Seidel 3차 수차와 풋프린트를 해석합니다. 파일은 브라우저 안에서만 계산되고 서버로 올라가지 않습니다. 무료.")

# 인라인 태그가 섞여 조각으로 쪼개지는 문단은 요소째 바꾼다.
BLOCKS4 = {
    'CODE V <code>.seq</code>와 Zemax OpticStudio <code>.zmx</code>, CSV 렌즈 표를 그대로 열어 단면과 1차 특성, 스팟 다이어그램, MTF, 광선 수차, 필드 곡률·왜곡, PSF, 상대 조도, Seidel 수차를 봅니다. 설치할 것도, 계정을 만들 것도 없습니다.': {
        "en": 'Open CODE V <code>.seq</code>, Zemax OpticStudio <code>.zmx</code> and CSV lens tables as they are and read the cross-section and first-order data, spot diagrams, MTF, ray aberrations, field curvature and distortion, PSF, relative illumination and Seidel aberrations. Nothing to install, no account to create.',
        "ja": 'CODE V の <code>.seq</code>、Zemax OpticStudio の <code>.zmx</code>、CSV のレンズ表をそのまま開き、断面と一次特性、スポットダイアグラム、MTF、光線収差、像面湾曲・歪曲、PSF、相対照度、ザイデル収差を見ます。インストールも、アカウント作成も要りません。',
        "zh": '直接打开 CODE V 的 <code>.seq</code>、Zemax OpticStudio 的 <code>.zmx</code> 与 CSV 镜头表格，查看剖面与一阶特性、点列图、MTF、光线像差、场曲·畸变、PSF、相对照度、赛德尔像差。无需安装，也不必注册账号。',
    },
    '해석 탭 여덟 개와 유리 탭. 열면 바로 계산해서 그립니다. 축과 단위, 계산 방식은 <a href="lens-docs.html">문서</a>에 전부 적어 뒀습니다.': {
        "en": 'Eight analysis tabs and a glass tab. Open a file and it computes and plots straight away. The axes, the units and the method behind each number are all written out in the <a href="lens-docs.html">docs</a>.',
        "ja": '解析タブ八つとガラスタブ。開けばすぐ計算して描きます。軸と単位、計算方法は<a href="lens-docs.html">ドキュメント</a>にすべて書いてあります。',
        "zh": '八个解析标签页与一个玻璃标签页。打开文件即刻计算并绘图。坐标轴、单位与计算方式都写在<a href="lens-docs.html">文档</a>里。',
    },
}

T4 = {
    # 공용 푸터 — 여섯 페이지 전부에 들어간다
    'Lens 문서': (
        'Lens docs',
        'Lens ドキュメント',
        'Lens 文档'),
    '지원 범위 · 해석 규약 문서': (
        'Supported scope · analysis conventions',
        '対応範囲・解析規約のドキュメント',
        '支持范围 · 解析约定文档'),
    'CODE V는 Synopsys, Inc.의, Zemax OpticStudio는 Ansys, Inc.의 상표입니다. 그 밖의 상표는 각 소유자의 재산입니다. Lens는 이 회사들과 제휴 관계가 없으며 보증이나 후원을 받지 않습니다.': (
        'CODE V is a trademark of Synopsys, Inc.; Zemax OpticStudio is a trademark of Ansys, Inc. '
        'All other trademarks are the property of their respective owners. Lens is not affiliated with, '
        'endorsed by, or sponsored by these companies.',
        'CODE V は Synopsys, Inc. の、Zemax OpticStudio は Ansys, Inc. の商標です。'
        'その他の商標は各所有者に帰属します。Lens はこれらの企業と提携しておらず、推奨・後援も受けていません。',
        'CODE V 为 Synopsys, Inc. 的商标，Zemax OpticStudio 为 Ansys, Inc. 的商标。'
        '其他商标归各自所有者所有。Lens 与上述公司无隶属关系，也未获其认可或赞助。'),

    # 메타 설명 — meta·og·JSON-LD 세 곳이 같은 문장을 쓴다
    _LENS_DESC: (
        'Open CODE V .seq, Zemax OpticStudio .zmx and CSV lens tables in your browser and read the cross-section '
        'and first-order data, spot diagrams, MTF, ray aberrations, field curvature, distortion and chromatic '
        'aberration, PSF and enclosed energy, relative illumination, and Seidel third-order aberrations and '
        'footprints. The file is computed inside your browser and never uploaded to a server. Free.',
        'CODE V の .seq、Zemax OpticStudio の .zmx、CSV のレンズ表をブラウザで開き、断面と一次特性、スポットダイアグラム、'
        'MTF、光線収差、像面湾曲・歪曲・色収差、PSF・集光エネルギー、相対照度、ザイデル 3 次収差とフットプリントを解析します。'
        'ファイルはブラウザの中だけで計算され、サーバーには送りません。無料。',
        '在浏览器中打开 CODE V .seq、Zemax OpticStudio .zmx 与 CSV 镜头表格，解析剖面与一阶特性、点列图、MTF、'
        '光线像差、场曲·畸变·色差、PSF·包围能量、相对照度、赛德尔三阶像差与光束足迹。文件只在浏览器内计算，不会上传到服务器。免费。'),

    # 해석 탭
    '곡률 · 왜곡 · 색수차': (
        'Field curvature · Distortion · Chromatic',
        '像面湾曲・歪曲・色収差',
        '场曲 · 畸变 · 色差'),
    'PSF · 에너지 집중도': (
        'PSF · Enclosed energy',
        'PSF・集光エネルギー',
        'PSF · 包围能量'),
    '상대 조도': (
        'Relative illumination',
        '相対照度',
        '相对照度'),
    '기준 파장 주광선을 기준으로, RMS는 중심(centroid) 기준 직경으로 냅니다. 상높이별 RMS 직경 곡선도 함께.': (
        'Referenced to the chief ray at the primary wavelength; RMS is reported as a centroid-referenced '
        'diameter. With an RMS diameter curve across field heights.',
        '基準波長の主光線を基準に、RMS は重心（centroid）基準の直径で出します。像高ごとの RMS 直径曲線も併せて。',
        '以基准波长的主光线为基准，RMS 以质心（centroid）为参考的直径给出。并附各像高的 RMS 直径曲线。'),
    '회절 한계를 같이 그려 어디까지가 설계 여유인지 보입니다. 상높이별 MTF와 스루포커스(범위 직접 입력, 기본 ±50 µm).': (
        'The diffraction limit is drawn alongside, so you can see how much design margin is left. MTF across '
        'field heights plus through-focus (enter your own range, ±50 µm by default).',
        '回折限界を重ねて描くので、どこまでが設計余裕かが見えます。像高ごとの MTF とスルーフォーカス'
        '（範囲は直接入力、既定 ±50 µm）。',
        '同时绘出衍射极限，便于看出还剩多少设计余量。各像高的 MTF 与通焦（范围可自行输入，默认 ±50 µm）。'),
    '비점수차 필드 곡선(T 실선·S 점선), f·tanθ와 f·θ 기준 왜곡, 왜곡 격자, 배율 색수차와 축상 색수차.': (
        'Astigmatic field curves (T solid, S dashed), distortion against both f·tanθ and f·θ, '
        'a distortion grid, and lateral and axial chromatic aberration.',
        '非点収差のフィールド曲線（T 実線・S 点線）、f·tanθ と f·θ 基準の歪曲、歪曲格子、'
        '倍率色収差と軸上色収差。',
        '非点像差场曲线（T 实线·S 虚线）、以 f·tanθ 与 f·θ 为基准的畸变、畸变网格、'
        '倍率色差与轴向色差。'),
    '다색 회절 PSF와 Strehl 비, 원 지름별 에너지 집중도, 상높이별 RMS 파면 오차.': (
        'Polychromatic diffraction PSF and Strehl ratio, enclosed energy by circle diameter, and RMS '
        'wavefront error across field heights.',
        '多色回折 PSF と Strehl 比、円直径ごとの集光エネルギー、像高ごとの RMS 波面誤差。',
        '多色衍射 PSF 与 Strehl 比、按圆直径的包围能量、各像高的 RMS 波前误差。'),
    '모든 개구를 통과하는 실제 광속으로 화면 가장자리가 얼마나 어두워지는지 계산합니다.': (
        'Computes how far the edge of the frame falls off, from the real flux that makes it through every aperture.',
        'すべての開口を通る実際の光束から、画面周辺がどれだけ暗くなるかを計算します。',
        '用实际通过所有光阑的光通量，计算画面边缘会暗多少。'),
    'Seidel · 풋프린트': (
        'Seidel · Footprint',
        'ザイデル・フットプリント',
        '赛德尔 · 光束足迹'),
    '면별 Seidel 3차 수차와 그 합을 횡수차와 파면 수차로 읽고, 각 면을 지나는 광속의 모양과 개구 사용률을 봅니다.': (
        'Seidel third-order aberrations by surface and in total, read as ray errors and wave aberration, plus '
        'the beam shape on each surface and how much of its aperture it fills.',
        '面ごとのザイデル 3 次収差とその和を横収差と波面収差で読み、各面を通る光束の形と開口の使用率を見ます。',
        '各面的赛德尔三阶像差及其总和，以横向像差与波像差给出，并可查看各面上的光束形状与孔径使用率。'),

    # 가이드 절
    '가이드': (
        'Guides',
        'ガイド',
        '指南'),
    '문서': (
        'docs',
        'ドキュメント',
        '文档'),
    '렌즈 성능 지표를 처음 보는 분을 위해 그림과 계산 예로 풀어 쓴 글입니다. 영어·일본어·중국어로도 읽을 수 있습니다.': (
        'Written for anyone meeting these lens metrics for the first time, with diagrams and worked examples. '
        'Also available in Korean, Japanese and Chinese.',
        'レンズの性能指標を初めて見る方のために、図と計算例で解きほぐした記事です。韓国語・英語・中国語でも読めます。',
        '为第一次接触镜头性能指标的人写的，配有图解与计算实例。也可用韩语、英语、日语阅读。'),

    # 가이드 카드 열 장
    '렌즈 파일 여는 법': (
        'Opening a lens file',
        'レンズファイルの開き方',
        '如何打开镜头文件'),
    'CODE V .seq와 Zemax .zmx를 브라우저에서 여는 방법, 읽는 항목과 유리 데이터.': (
        'How to open CODE V .seq and Zemax .zmx in the browser, what gets read, and the glass data.',
        'CODE V .seq と Zemax .zmx をブラウザで開く方法、読み取る項目とガラスデータ。',
        '在浏览器中打开 CODE V .seq 与 Zemax .zmx 的方法、读取的项目与玻璃数据。'),
    '렌즈 사양서 읽는 법': (
        'Reading a lens spec sheet',
        'レンズ仕様書の読み方',
        '如何读镜头规格书'),
    '초점 거리, F/#, 화각, 이미지 서클, 왜곡, 상대 조도, CRA가 서로 어떻게 묶이는지.': (
        'How focal length, F/#, field of view, image circle, distortion, relative illumination and chief ray '
        'angle tie together.',
        '焦点距離、F/#、画角、イメージサークル、歪曲、相対照度、CRA が互いにどう結びつくか。',
        '焦距、F/#、视场角、像圈、畸变、相对照度、CRA 之间如何互相关联。'),
    'MTF · PSF · Strehl 비 읽는 법': (
        'Reading MTF, PSF and Strehl ratio',
        'MTF・PSF・Strehl 比の読み方',
        '如何读 MTF · PSF · Strehl 比'),
    'MTF, PSF, 에너지 집중도, 파면 오차의 뜻과 센서 나이퀴스트 주파수 계산.': (
        'What MTF, PSF, enclosed energy and wavefront error mean, and how to work out a sensor’s Nyquist frequency.',
        'MTF、PSF、集光エネルギー、波面誤差の意味と、センサーのナイキスト周波数の計算。',
        'MTF、PSF、包围能量、波前误差的含义，以及传感器奈奎斯特频率的计算。'),
    '상대 조도와 cos⁴ 법칙': (
        'Relative illumination and the cos⁴ law',
        '相対照度と cos⁴ 法則',
        '相对照度与 cos⁴ 定律'),
    '화면 가장자리가 어두워지는 이유와 실제 렌즈가 cos⁴에서 벗어나는 까닭.': (
        'Why the edge of the frame goes dark, and why a real lens departs from cos⁴.',
        '画面周辺が暗くなる理由と、実際のレンズが cos⁴ から外れる理由。',
        '画面边缘变暗的原因，以及真实镜头为何偏离 cos⁴。'),
    '센서 CRA 맞추기': (
        'Matching sensor CRA',
        'センサー CRA を合わせる',
        '匹配传感器 CRA'),
    '센서 CRA 사양의 뜻, 렌즈와 맞지 않을 때 생기는 일, CRA 곡선 비교법.': (
        'What a sensor’s CRA spec means, what goes wrong when the lens does not match it, and how to '
        'compare CRA curves.',
        'センサーの CRA 仕様の意味、レンズと合わないときに起きること、CRA 曲線の比べ方。',
        '传感器 CRA 规格的含义、与镜头不匹配时会发生什么、如何比较 CRA 曲线。'),
    '왜곡과 상면 만곡': (
        'Distortion and field curvature',
        '歪曲と像面湾曲',
        '畸变与场曲'),
    '배럴·핀쿠션 왜곡과 f·θ 렌즈, 페츠발 면과 비점수차, 초점 심도와의 비교.': (
        'Barrel and pincushion distortion and f·θ lenses, the Petzval surface and astigmatism, and '
        'how these compare with depth of focus.',
        '樽型・糸巻き型の歪曲と f·θ レンズ、ペッツバール面と非点収差、焦点深度との比較。',
        '桶形与枕形畸变及 f·θ 镜头、珀兹伐面与非点像差、与焦深的比较。'),
    '비구면 계수 읽는 법': (
        'Reading aspheric coefficients',
        '非球面係数の読み方',
        '如何读非球面系数'),
    '처짐 공식과 코닉 상수, 짝수 비구면 계수의 크기, Q형 비구면, XY 다항식과 Zernike 면.': (
        'The sag equation and the conic constant, the magnitude of the even aspheric coefficients, Q-type '
        'aspheres, and XY-polynomial and Zernike surfaces.',
        'サグの式とコーニック定数、偶数次非球面係数の大きさ、Q 型非球面、XY 多項式と Zernike 面。',
        '矢高公式与二次曲面常数、偶次非球面系数的量级、Q 型非球面、XY 多项式与 Zernike 面。'),
    'F/#와 피사계 심도': (
        'F/# and depth of field',
        'F/# と被写界深度',
        'F/# 与景深'),
    '과초점 거리와 피사계 심도 공식, 50 mm 렌즈와 4 mm 카메라 모듈의 계산 예.': (
        'The hyperfocal distance and depth-of-field formulas, worked through for a 50 mm lens and a 4 mm '
        'camera module.',
        '過焦点距離と被写界深度の式、50 mm レンズと 4 mm カメラモジュールの計算例。',
        '超焦距与景深公式，并以 50 mm 镜头和 4 mm 摄像模组为计算实例。'),
    '코팅과 반사 손실': (
        'Coatings and reflection loss',
        'コーティングと反射損失',
        '镀膜与反射损耗'),
    '면 한 면의 반사율, λ/4 MgF₂ 코팅의 원리, 입사각·파장·접합면·유리 흡수에 따른 투과율.': (
        'The reflectance of a single surface, how a λ/4 MgF₂ coating works, and how transmittance '
        'varies with incidence angle, wavelength, cemented surfaces and glass absorption.',
        '一面あたりの反射率、λ/4 MgF₂ コーティングの原理、入射角・波長・接合面・ガラス吸収による透過率。',
        '单面反射率、λ/4 MgF₂ 镀膜的原理、随入射角·波长·胶合面·玻璃吸收变化的透过率。'),
    '줌 렌즈 파일 읽기': (
        'Reading zoom lens files',
        'ズームレンズのファイルを読む',
        '读取变焦镜头文件'),
    '줌 렌즈가 초점 거리를 바꾸는 원리, .seq의 ZOO와 .zmx 멀티 컨피그레이션, 줌 위치별 확인 항목.': (
        'How a zoom changes focal length, ZOO in .seq and multi-configuration in .zmx, and what to check at '
        'each zoom position.',
        'ズームレンズが焦点距離を変える原理、.seq の ZOO と .zmx のマルチコンフィギュレーション、'
        'ズーム位置ごとの確認項目。',
        '变焦镜头改变焦距的原理、.seq 的 ZOO 与 .zmx 的多重结构、各变焦位置的检查项。'),

    # JSON-LD featureList — 스크립트 안이라 한글 검사기가 못 본다. 손으로 챙긴다.
    'CODE V .seq 읽기': (
        'Reads CODE V .seq',
        'CODE V .seq を読む',
        '读取 CODE V .seq'),
    'Zemax OpticStudio .zmx 읽기': (
        'Reads Zemax OpticStudio .zmx',
        'Zemax OpticStudio .zmx を読む',
        '读取 Zemax OpticStudio .zmx'),
    'XY 다항식 · Zernike 자유곡면': (
        'XY polynomial · Zernike freeform',
        'XY 多項式・Zernike 自由曲面',
        'XY 多项式 · Zernike 自由曲面'),
    'Q-con · 홀수차 비구면': (
        'Q-con · Odd aspheres',
        'Q-con・奇数次非球面',
        'Q-con · 奇次非球面'),
    '회절면(DOE · HOE)': (
        'Diffractive surfaces (DOE · HOE)',
        '回折面（DOE・HOE）',
        '衍射面（DOE · HOE）'),
    'CSV 렌즈 표': (
        'CSV lens tables',
        'CSV レンズ表',
        'CSV 镜头表格'),
    'Seidel 3차 수차 · 풋프린트': (
        'Seidel third-order aberrations · Footprint',
        'ザイデル 3 次収差・フットプリント',
        '赛德尔三阶像差 · 光束足迹'),
    '단면 · 1차 특성': (
        'Cross-section · First-order data',
        '断面・一次特性',
        '剖面 · 一阶特性'),
    '스팟 다이어그램': (
        'Spot diagram',
        'スポットダイアグラム',
        '点列图'),
    '광선 수차': (
        'Ray aberrations',
        '光線収差',
        '光线像差'),
    '필드 곡률 · 왜곡 · 색수차': (
        'Field curvature · Distortion · Chromatic aberration',
        '像面湾曲・歪曲・色収差',
        '场曲 · 畸变 · 色差'),
    '유리 선도': (
        'Glass map',
        'ガラス線図',
        '玻璃图'),
}
