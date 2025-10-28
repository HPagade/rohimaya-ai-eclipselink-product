"""
EclipseLink AI - Multi-Language Translation Demo
Real-time translation of clinical handoffs to 50+ languages
"""

import streamlit as st
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Multi-Language Translation - EclipseLink AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand colors
PEACOCK_TEAL = "#1a9b8e"
PHOENIX_GOLD = "#f4c430"
LUNAR_BLUE = "#2c3e50"
ECLIPSE_NAVY = "#1a2332"

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {PEACOCK_TEAL} 0%, {LUNAR_BLUE} 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }}
    .language-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-top: 4px solid {PEACOCK_TEAL};
        margin-bottom: 1rem;
    }}
    .original-text {{
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {LUNAR_BLUE};
        margin-bottom: 1rem;
    }}
    .translated-text {{
        background: #e8f8f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {PEACOCK_TEAL};
        margin-bottom: 1rem;
    }}
    .flag-icon {{
        font-size: 2rem;
        margin-right: 0.5rem;
    }}
    .language-name {{
        font-size: 1.2rem;
        font-weight: bold;
        color: {PEACOCK_TEAL};
    }}
    .translation-time {{
        background: {PHOENIX_GOLD};
        color: {ECLIPSE_NAVY};
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌐 Multi-Language Translation Demo</h1>
    <p style="font-size: 1.2rem; margin: 0;">Instant translation of clinical handoffs to 50+ languages</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'translated' not in st.session_state:
    st.session_state.translated = False
if 'selected_languages' not in st.session_state:
    st.session_state.selected_languages = ["Spanish", "Mandarin Chinese", "Tagalog"]

# Sidebar
with st.sidebar:
    st.image("https://img.shields.io/badge/EclipseLink-AI-1a9b8e?style=for-the-badge", use_container_width=True)
    st.markdown("---")
    st.markdown("### Translation Settings")

    st.markdown("**Select Languages:**")

    # Language selection
    languages = {
        "Spanish": "🇪🇸",
        "Mandarin Chinese": "🇨🇳",
        "Tagalog": "🇵🇭",
        "French": "🇫🇷",
        "German": "🇩🇪",
        "Arabic": "🇸🇦",
        "Hindi": "🇮🇳",
        "Portuguese": "🇵🇹",
        "Russian": "🇷🇺",
        "Japanese": "🇯🇵",
        "Korean": "🇰🇷",
        "Vietnamese": "🇻🇳",
        "Italian": "🇮🇹",
        "Polish": "🇵🇱",
        "Ukrainian": "🇺🇦"
    }

    selected_langs = st.multiselect(
        "Choose up to 3 languages",
        options=list(languages.keys()),
        default=st.session_state.selected_languages,
        max_selections=3
    )

    st.session_state.selected_languages = selected_langs

    st.markdown("---")
    st.markdown("### Use Cases")
    st.info("""
    **For Healthcare Teams:**
    - 🌍 Diverse nursing staff
    - 🗣️ Multilingual communication
    - 🏥 International facilities
    - 📱 Travel nurses

    **For Families:**
    - 👨‍👩‍👧‍👦 Non-English speaking families
    - 🌐 Family portal translation
    - 📞 Remote family updates
    """)

    st.markdown("---")
    st.markdown("### Supported Languages")
    st.success("""
    ✅ 50+ languages supported
    ✅ Medical terminology accuracy
    ✅ Cultural sensitivity
    ✅ Real-time translation
    """)

    if st.button("Reset Demo", type="secondary"):
        st.session_state.translated = False
        st.rerun()

# Original handoff text
original_sbar = {
    "situation": "This is Sarah Johnson, 68-year-old female, post-operative day 0 following coronary artery bypass graft surgery times four vessels. Patient is currently stable in the ICU requiring close monitoring.",
    "background": "Patient has a history of coronary artery disease, hypertension, and type 2 diabetes mellitus. She was admitted three days ago with unstable angina. Cardiac catheterization showed 90% stenosis in the left anterior descending artery.",
    "assessment": "Patient is currently intubated and sedated on propofol. Vital signs are stable with blood pressure 118 over 72, heart rate 78 and regular. Oxygen saturation is 98% on 40% inspired oxygen. Chest tubes are draining normally with 150 milliliters output in the last hour.",
    "recommendation": "Continue current sedation and monitor chest tube output hourly. Plan to extubate in the morning if patient remains stable overnight. Cardiac enzymes and EKG scheduled for 6 AM."
}

# Translations (simulated for demo)
translations = {
    "Spanish": {
        "situation": "Esta es Sarah Johnson, mujer de 68 años, día postoperatorio 0 después de cirugía de injerto de derivación de arteria coronaria en cuatro vasos. La paciente está actualmente estable en la UCI y requiere monitoreo cercano.",
        "background": "La paciente tiene antecedentes de enfermedad arterial coronaria, hipertensión y diabetes mellitus tipo 2. Fue admitida hace tres días con angina inestable. El cateterismo cardíaco mostró estenosis del 90% en la arteria descendente anterior izquierda.",
        "assessment": "La paciente está actualmente intubada y sedada con propofol. Los signos vitales son estables con presión arterial 118 sobre 72, frecuencia cardíaca 78 y regular. La saturación de oxígeno es 98% con oxígeno inspirado al 40%. Los tubos torácicos están drenando normalmente con 150 mililitros de salida en la última hora.",
        "recommendation": "Continuar la sedación actual y monitorear la salida del tubo torácico cada hora. Se planea extubar en la mañana si la paciente permanece estable durante la noche. Enzimas cardíacas y ECG programados para las 6 AM."
    },
    "Mandarin Chinese": {
        "situation": "这是莎拉·约翰逊，68岁女性，冠状动脉旁路移植手术四支血管术后第0天。患者目前在重症监护室稳定，需要密切监测。",
        "background": "患者有冠状动脉疾病、高血压和2型糖尿病病史。她三天前因不稳定型心绞痛入院。心导管检查显示左前降支动脉狭窄90%。",
        "assessment": "患者目前插管并使用丙泊酚镇静。生命体征稳定，血压118/72，心率78次/分且规律。血氧饱和度98%，吸入氧浓度40%。胸腔引流管引流正常，最近一小时引流量150毫升。",
        "recommendation": "继续目前的镇静治疗，每小时监测胸腔引流量。如果患者整夜保持稳定，计划早上拔管。心肌酶和心电图检查定于早上6点。"
    },
    "Tagalog": {
        "situation": "Ito si Sarah Johnson, 68 taong gulang na babae, post-operative araw 0 pagkatapos ng coronary artery bypass graft surgery sa apat na ugat. Ang pasyente ay kasalukuyang stable sa ICU at nangangailangan ng malapit na pagsubaybay.",
        "background": "Ang pasyente ay may kasaysayan ng coronary artery disease, hypertension, at type 2 diabetes mellitus. Siya ay na-admit tatlong araw na ang nakalipas na may unstable angina. Ang cardiac catheterization ay nagpakita ng 90% stenosis sa left anterior descending artery.",
        "assessment": "Ang pasyente ay kasalukuyang naka-intubate at naka-sedate sa propofol. Ang vital signs ay stable na may blood pressure na 118 over 72, heart rate 78 at regular. Ang oxygen saturation ay 98% sa 40% inspired oxygen. Ang chest tubes ay normal na dumadaloy na may 150 milliliters output sa nakaraang oras.",
        "recommendation": "Ipagpatuloy ang kasalukuyang sedation at subaybayan ang chest tube output kada oras. Plano na mag-extubate sa umaga kung ang pasyente ay mananatiling stable sa buong gabi. Ang cardiac enzymes at EKG ay naka-iskedyul para sa 6 AM."
    },
    "French": {
        "situation": "Voici Sarah Johnson, femme de 68 ans, jour post-opératoire 0 après une chirurgie de pontage coronarien sur quatre vaisseaux. La patiente est actuellement stable en soins intensifs et nécessite une surveillance étroite.",
        "background": "La patiente a des antécédents de maladie coronarienne, d'hypertension et de diabète de type 2. Elle a été admise il y a trois jours avec une angine instable. Le cathétérisme cardiaque a montré une sténose de 90% de l'artère coronaire descendante antérieure gauche.",
        "assessment": "La patiente est actuellement intubée et sédatée au propofol. Les signes vitaux sont stables avec une pression artérielle de 118 sur 72, une fréquence cardiaque de 78 et régulière. La saturation en oxygène est de 98% avec 40% d'oxygène inspiré. Les drains thoraciques drainent normalement avec 150 millilitres de débit dans la dernière heure.",
        "recommendation": "Continuer la sédation actuelle et surveiller le débit des drains thoraciques toutes les heures. Prévoir l'extubation le matin si la patiente reste stable pendant la nuit. Enzymes cardiaques et ECG prévus à 6 heures du matin."
    },
    "German": {
        "situation": "Dies ist Sarah Johnson, 68 Jahre alte Frau, postoperativer Tag 0 nach einer koronaren Bypass-Operation an vier Gefäßen. Die Patientin ist derzeit auf der Intensivstation stabil und benötigt eine engmaschige Überwachung.",
        "background": "Die Patientin hat eine Vorgeschichte von koronarer Herzkrankheit, Bluthochdruck und Typ-2-Diabetes. Sie wurde vor drei Tagen mit instabiler Angina aufgenommen. Die Herzkatheterisierung zeigte eine 90%ige Stenose der linken absteigenden Koronararterie.",
        "assessment": "Die Patientin ist derzeit intubiert und mit Propofol sediert. Die Vitalzeichen sind stabil mit einem Blutdruck von 118 über 72, Herzfrequenz 78 und regelmäßig. Die Sauerstoffsättigung beträgt 98% bei 40% inspiriertem Sauerstoff. Die Thoraxdrainagen fördern normal mit 150 Milliliter Ausstoß in der letzten Stunde.",
        "recommendation": "Aktuelle Sedierung fortsetzen und stündlich die Thoraxdrainage überwachen. Extubation am Morgen geplant, wenn die Patientin über Nacht stabil bleibt. Herzenzyme und EKG für 6 Uhr morgens geplant."
    },
    "Arabic": {
        "situation": "هذه سارة جونسون، امرأة تبلغ من العمر 68 عامًا، اليوم الصفر بعد العملية الجراحية لتطعيم مجازة الشريان التاجي في أربعة أوعية. المريضة مستقرة حاليًا في وحدة العناية المركزة وتحتاج إلى مراقبة دقيقة.",
        "background": "المريضة لديها تاريخ من مرض الشريان التاجي وارتفاع ضغط الدم والسكري من النوع 2. تم إدخالها قبل ثلاثة أيام بسبب الذبحة الصدرية غير المستقرة. أظهر قسطرة القلب تضيقًا بنسبة 90٪ في الشريان التاجي الأمامي النازل الأيسر.",
        "assessment": "المريضة حاليًا مُنبوبة ومُهدئة بالبروبوفول. العلامات الحيوية مستقرة مع ضغط دم 118 على 72، معدل ضربات القلب 78 ومنتظم. تشبع الأكسجين 98٪ على 40٪ أكسجين مُستنشق. أنابيب الصدر تصرف بشكل طبيعي مع 150 مليلتر في الساعة الأخيرة.",
        "recommendation": "الاستمرار في التهدئة الحالية ومراقبة تصريف أنبوب الصدر كل ساعة. من المخطط إزالة الأنبوب في الصباح إذا ظلت المريضة مستقرة طوال الليل. إنزيمات القلب وتخطيط القلب مجدولان الساعة 6 صباحًا."
    },
    "Hindi": {
        "situation": "यह सारा जॉनसन है, 68 वर्षीय महिला, चार वाहिकाओं में कोरोनरी धमनी बाईपास ग्राफ्ट सर्जरी के बाद पोस्ट-ऑपरेटिव दिन 0। रोगी वर्तमान में आईसीयू में स्थिर है और निकट निगरानी की आवश्यकता है।",
        "background": "रोगी को कोरोनरी धमनी रोग, उच्च रक्तचाप और टाइप 2 मधुमेह का इतिहास है। उसे तीन दिन पहले अस्थिर एनजाइना के साथ भर्ती किया गया था। कार्डियक कैथीटेराइजेशन ने बाएं पूर्वकाल अवरोही धमनी में 90% स्टेनोसिस दिखाया।",
        "assessment": "रोगी वर्तमान में इंटुबेटेड है और प्रोपोफोल पर शामक है। महत्वपूर्ण संकेत स्थिर हैं जिसमें रक्तचाप 118/72, हृदय गति 78 और नियमित है। ऑक्सीजन संतृप्ति 40% प्रेरित ऑक्सीजन पर 98% है। छाती की नलियां सामान्य रूप से निकल रही हैं जिसमें पिछले घंटे में 150 मिलीलीटर आउटपुट है।",
        "recommendation": "वर्तमान शामक जारी रखें और छाती ट्यूब आउटपुट की प्रति घंटा निगरानी करें। यदि रोगी रात भर स्थिर रहता है तो सुबह एक्सट्यूबेट करने की योजना है। कार्डियक एंजाइम और ईसीजी सुबह 6 बजे निर्धारित हैं।"
    },
    "Portuguese": {
        "situation": "Esta é Sarah Johnson, mulher de 68 anos, dia pós-operatório 0 após cirurgia de enxerto de bypass de artéria coronária em quatro vasos. A paciente está atualmente estável na UTI e requer monitoramento próximo.",
        "background": "A paciente tem histórico de doença arterial coronariana, hipertensão e diabetes mellitus tipo 2. Foi admitida há três dias com angina instável. O cateterismo cardíaco mostrou estenose de 90% na artéria descendente anterior esquerda.",
        "assessment": "A paciente está atualmente intubada e sedada com propofol. Os sinais vitais estão estáveis com pressão arterial 118 sobre 72, frequência cardíaca 78 e regular. A saturação de oxigênio é de 98% com 40% de oxigênio inspirado. Os drenos torácicos estão drenando normalmente com 150 mililitros de débito na última hora.",
        "recommendation": "Continuar a sedação atual e monitorar o débito dos drenos torácicos a cada hora. Planeja-se extubar pela manhã se a paciente permanecer estável durante a noite. Enzimas cardíacas e ECG agendados para as 6h da manhã."
    },
    "Russian": {
        "situation": "Это Сара Джонсон, 68-летняя женщина, послеоперационный день 0 после операции аортокоронарного шунтирования на четырех сосудах. Пациентка в настоящее время стабильна в отделении интенсивной терапии и требует тщательного наблюдения.",
        "background": "У пациентки в анамнезе ишемическая болезнь сердца, гипертония и сахарный диабет 2 типа. Она была госпитализирована три дня назад с нестабильной стенокардией. Катетеризация сердца показала стеноз 90% в левой передней нисходящей артерии.",
        "assessment": "Пациентка в настоящее время интубирована и седатирована пропофолом. Жизненные показатели стабильны: артериальное давление 118 на 72, частота сердечных сокращений 78 и регулярная. Насыщение кислородом 98% при 40% вдыхаемого кислорода. Плевральные дренажи дренируют нормально с оттоком 150 миллилитров за последний час.",
        "recommendation": "Продолжить текущую седацию и ежечасно контролировать отток из плевральных дренажей. Планируется экстубация утром, если пациентка останется стабильной в течение ночи. Сердечные ферменты и ЭКГ запланированы на 6 утра."
    },
    "Japanese": {
        "situation": "これはサラ・ジョンソンさん、68歳女性、4本の血管に対する冠動脈バイパス移植術後の術後0日目です。患者は現在ICUで安定しており、綿密な監視が必要です。",
        "background": "患者は冠動脈疾患、高血圧、2型糖尿病の既往歴があります。3日前に不安定狭心症で入院しました。心臓カテーテル検査では左前下行枝動脈に90%の狭窄が認められました。",
        "assessment": "患者は現在挿管されており、プロポフォールで鎮静されています。バイタルサインは安定しており、血圧118/72、心拍数78で規則的です。酸素飽和度は40%酸素吸入で98%です。胸腔ドレーンは正常に排液しており、過去1時間で150ミリリットルの排液があります。",
        "recommendation": "現在の鎮静を継続し、胸腔ドレーンの排液量を毎時監視してください。患者が一晩中安定していれば、朝に抜管する予定です。心臓酵素とECGは午前6時に予定されています。"
    },
    "Korean": {
        "situation": "이것은 사라 존슨으로, 68세 여성이며 4개 혈관에 대한 관상동맥 우회술 후 수술 후 0일째입니다. 환자는 현재 중환자실에서 안정적이며 면밀한 모니터링이 필요합니다.",
        "background": "환자는 관상동맥 질환, 고혈압, 제2형 당뇨병의 병력이 있습니다. 3일 전 불안정 협심증으로 입원했습니다. 심장 카테터 검사에서 좌전하행동맥에 90% 협착이 나타났습니다.",
        "assessment": "환자는 현재 삽관되어 있으며 프로포폴로 진정되어 있습니다. 활력 징후는 안정적이며 혈압 118/72, 심박수 78로 규칙적입니다. 산소 포화도는 40% 흡입 산소에서 98%입니다. 흉부 배액관은 정상적으로 배액되고 있으며 지난 1시간 동안 150밀리리터의 배액이 있었습니다.",
        "recommendation": "현재 진정을 계속하고 흉부 배액관 배출량을 매시간 모니터링하십시오. 환자가 밤새 안정적으로 유지되면 아침에 발관할 계획입니다. 심장 효소 및 심전도는 오전 6시에 예정되어 있습니다."
    },
    "Vietnamese": {
        "situation": "Đây là Sarah Johnson, nữ 68 tuổi, ngày 0 sau phẫu thuật bắc cầu động mạch vành trên bốn mạch máu. Bệnh nhân hiện đang ổn định tại ICU và cần theo dõi sát.",
        "background": "Bệnh nhân có tiền sử bệnh động mạch vành, tăng huyết áp và đái tháo đường type 2. Cô ấy được nhập viện ba ngày trước với đau thắt ngực không ổn định. Thông tim cho thấy hẹp 90% ở động mạch xuống trước trái.",
        "assessment": "Bệnh nhân hiện đang được đặt nội khí quản và an thần bằng propofol. Các dấu hiệu sinh tồn ổn định với huyết áp 118/72, nhịp tim 78 và đều. Độ bão hòa oxy là 98% với 40% oxy hít vào. Các ống dẫn lưu ngực đang dẫn lưu bình thường với 150 mililít ra trong giờ qua.",
        "recommendation": "Tiếp tục an thần hiện tại và theo dõi lượng dẫn lưu ống ngực mỗi giờ. Kế hoạch rút nội khí quản vào sáng nếu bệnh nhân vẫn ổn định qua đêm. Enzyme tim và điện tâm đồ được lên lịch lúc 6 giờ sáng."
    },
    "Italian": {
        "situation": "Questa è Sarah Johnson, donna di 68 anni, giorno post-operatorio 0 dopo intervento di bypass coronarico su quattro vasi. La paziente è attualmente stabile in terapia intensiva e richiede un monitoraggio ravvicinato.",
        "background": "La paziente ha una storia di malattia coronarica, ipertensione e diabete mellito di tipo 2. È stata ricoverata tre giorni fa con angina instabile. Il cateterismo cardiaco ha mostrato una stenosi del 90% nell'arteria discendente anteriore sinistra.",
        "assessment": "La paziente è attualmente intubata e sedata con propofol. I segni vitali sono stabili con pressione sanguigna 118 su 72, frequenza cardiaca 78 e regolare. La saturazione di ossigeno è del 98% con ossigeno inspirato al 40%. I drenaggi toracici stanno drenando normalmente con 150 millilitri di output nell'ultima ora.",
        "recommendation": "Continuare la sedazione attuale e monitorare l'output del drenaggio toracico ogni ora. Si prevede di estubare al mattino se la paziente rimane stabile durante la notte. Enzimi cardiaci ed ECG programmati per le 6 del mattino."
    },
    "Polish": {
        "situation": "To jest Sarah Johnson, 68-letnia kobieta, dzień pooperacyjny 0 po operacji pomostowania tętnic wieńcowych na czterech naczyniach. Pacjentka jest obecnie stabilna na OIOM i wymaga ścisłego monitorowania.",
        "background": "Pacjentka ma w wywiadzie chorobę wieńcową, nadciśnienie tętnicze i cukrzycę typu 2. Została przyjęta trzy dni temu z niestabilną dławicą piersiową. Cewnikowanie serca wykazało 90% zwężenie w lewej tętnicy zstępującej przedniej.",
        "assessment": "Pacjentka jest obecnie zaintubowana i sedowana propofolem. Parametry życiowe są stabilne z ciśnieniem krwi 118 na 72, częstością akcji serca 78 i regularną. Saturacja tlenu wynosi 98% przy 40% wdychanego tlenu. Dreny klatki piersiowej drenują prawidłowo z 150 mililitrami w ostatniej godzinie.",
        "recommendation": "Kontynuować obecną sedację i monitorować odpływ z drenów klatki piersiowej co godzinę. Planowana ekstubacja rano, jeśli pacjentka pozostanie stabilna przez noc. Enzymy sercowe i EKG zaplanowane na godzinę 6 rano."
    },
    "Ukrainian": {
        "situation": "Це Сара Джонсон, 68-річна жінка, післяопераційний день 0 після операції аортокоронарного шунтування на чотирьох судинах. Пацієнтка зараз стабільна у відділенні інтенсивної терапії і потребує ретельного спостереження.",
        "background": "Пацієнтка має в анамнезі ішемічну хворобу серця, гіпертонію та цукровий діабет 2 типу. Вона була госпіталізована три дні тому з нестабільною стенокардією. Катетеризація серця показала стеноз 90% у лівій передній низхідній артерії.",
        "assessment": "Пацієнтка зараз інтубована та седована пропофолом. Життєві показники стабільні: артеріальний тиск 118 на 72, частота серцевих скорочень 78 і регулярна. Насичення киснем 98% при 40% вдихуваного кисню. Плевральні дренажі дренують нормально з відтоком 150 мілілітрів за останню годину.",
        "recommendation": "Продовжити поточну седацію та щогодини контролювати відтік з плевральних дренажів. Планується екстубація вранці, якщо пацієнтка залишиться стабільною протягом ночі. Серцеві ферменти та ЕКГ заплановані на 6 ранку."
    }
}

# Main content
st.markdown("### 📝 Original English Handoff (SBAR)")

with st.expander("View Original English SBAR", expanded=False):
    st.markdown(f"""
    <div class="original-text">
        <strong>Situation:</strong><br>
        {original_sbar['situation']}<br><br>
        <strong>Background:</strong><br>
        {original_sbar['background']}<br><br>
        <strong>Assessment:</strong><br>
        {original_sbar['assessment']}<br><br>
        <strong>Recommendation:</strong><br>
        {original_sbar['recommendation']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Translation button
if not st.session_state.translated:
    if len(st.session_state.selected_languages) == 0:
        st.warning("⚠️ Please select at least one language from the sidebar to translate.")
    else:
        col_center = st.columns([1, 2, 1])
        with col_center[1]:
            if st.button("🌐 Translate to Selected Languages", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status = st.empty()

                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status.text(f"🌐 Translating to {len(st.session_state.selected_languages)} languages...")
                    elif i < 60:
                        status.text("🔍 Verifying medical terminology accuracy...")
                    elif i < 90:
                        status.text("✅ Applying cultural sensitivity adjustments...")
                    else:
                        status.text("🎉 Translation complete!")
                    time.sleep(0.02)

                st.session_state.translated = True
                time.sleep(0.5)
                st.rerun()

# Display translations
if st.session_state.translated:
    st.success(f"✅ Successfully translated to {len(st.session_state.selected_languages)} language(s) in 1.8 seconds!")

    st.markdown("---")
    st.markdown("### 🌍 Translated Handoffs")

    for lang in st.session_state.selected_languages:
        if lang in translations:
            flag = languages.get(lang, "🌐")

            with st.expander(f"{flag} {lang} Translation", expanded=True):
                col_header, col_time = st.columns([4, 1])

                with col_header:
                    st.markdown(f'<div class="language-name">{flag} {lang}</div>', unsafe_allow_html=True)

                with col_time:
                    st.markdown('<span class="translation-time">⚡ 0.6s</span>', unsafe_allow_html=True)

                translation = translations[lang]

                st.markdown(f"""
                <div class="translated-text">
                    <strong>Situation:</strong><br>
                    {translation['situation']}<br><br>
                    <strong>Background:</strong><br>
                    {translation['background']}<br><br>
                    <strong>Assessment:</strong><br>
                    {translation['assessment']}<br><br>
                    <strong>Recommendation:</strong><br>
                    {translation['recommendation']}
                </div>
                """, unsafe_allow_html=True)

                # Action buttons
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"📄 Export PDF", key=f"pdf_{lang}"):
                        st.success(f"✅ PDF exported in {lang}!")

                with col2:
                    if st.button(f"📧 Email to Team", key=f"email_{lang}"):
                        st.success(f"✅ Sent to {lang}-speaking team members!")

                with col3:
                    if st.button(f"🔊 Text-to-Speech", key=f"tts_{lang}"):
                        st.success(f"✅ Audio generated in {lang}!")

    st.markdown("---")

    # Comparison view
    st.markdown("### 🔄 Side-by-Side Comparison")

    comparison_lang = st.selectbox(
        "Select language to compare with English",
        options=st.session_state.selected_languages
    )

    if comparison_lang:
        col_english, col_translated = st.columns(2)

        with col_english:
            st.markdown("#### 🇺🇸 English (Original)")
            st.markdown(f"""
            <div class="original-text">
                <strong>Situation:</strong><br>
                {original_sbar['situation']}<br><br>
                <strong>Background:</strong><br>
                {original_sbar['background'][:100]}...
            </div>
            """, unsafe_allow_html=True)

        with col_translated:
            st.markdown(f"#### {languages.get(comparison_lang, '🌐')} {comparison_lang}")
            if comparison_lang in translations:
                translation = translations[comparison_lang]
                st.markdown(f"""
                <div class="translated-text">
                    <strong>Situation:</strong><br>
                    {translation['situation']}<br><br>
                    <strong>Background:</strong><br>
                    {translation['background'][:100]}...
                </div>
                """, unsafe_allow_html=True)

# Statistics
st.markdown("---")
st.markdown("### 📊 Translation Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Languages Supported", "50+")
with col2:
    st.metric("Avg Translation Time", "0.6 sec")
with col3:
    st.metric("Medical Term Accuracy", "99.2%")
with col4:
    st.metric("Character Limit", "Unlimited")

# Use case examples
st.markdown("---")
st.markdown("### 💼 Real-World Use Cases")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🏥 Hospital Scenario: Diverse Nursing Staff

    **Challenge:** Large metropolitan hospital with nurses who speak:
    - 🇺🇸 English (60%)
    - 🇪🇸 Spanish (25%)
    - 🇵🇭 Tagalog (10%)
    - 🇨🇳 Mandarin (5%)

    **Solution:**
    - Handoffs created in any language
    - Auto-translated for all team members
    - Everyone reads in their preferred language
    - Reduces miscommunication errors
    """)

with col2:
    st.markdown("""
    #### 👨‍👩‍👧‍👦 Family Portal Scenario

    **Challenge:** Patient's family in Mexico speaks only Spanish

    **Solution:**
    - Clinician creates handoff in English
    - Family portal auto-translates to Spanish
    - Real-time updates in family's language
    - Reduces anxiety, improves understanding
    - Cultural sensitivity maintained
    """)

st.markdown("---")

# Language coverage
st.markdown("### 🌎 Global Language Coverage")

st.markdown("""
**Most Commonly Used Languages in US Healthcare:**
- 🇪🇸 Spanish (Primary - 13% of US population)
- 🇨🇳 Mandarin Chinese (3.5M speakers)
- 🇵🇭 Tagalog (1.8M speakers, major nursing community)
- 🇻🇳 Vietnamese (1.5M speakers)
- 🇫🇷 French (1.3M speakers)
- 🇰🇷 Korean (1.1M speakers)
- 🇩🇪 German (1M speakers)
- 🇦🇪 Arabic (1.2M speakers)
- 🇮🇳 Hindi (900K speakers)
- 🇷🇺 Russian (900K speakers)

**Plus 40+ additional languages supported**
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>EclipseLink AI™</strong> - Breaking Language Barriers in Healthcare</p>
    <p style="font-size: 0.9rem;">© 2025 Rohimaya Health AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
