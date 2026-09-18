import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import time

nltk.download('punkt_tab')
nltk.download('stopwords')

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
    text=y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text=y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


#UX / UI
st.set_page_config(
    page_title="AI SMS Guard",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.15), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(168,85,247,.13), transparent 30%),
        #050816;
    color: #f8fafc;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* HERO */

.hero {
    text-align: center;
    padding: 45px 20px 25px;
}

.badge {
    display: inline-block;
    padding: 7px 16px;
    border-radius: 30px;
    border: 1px solid rgba(129,140,248,.35);
    background: rgba(99,102,241,.10);
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    box-shadow: 0 0 20px rgba(99,102,241,.15);
}

.hero h1 {
    font-size: clamp(45px, 6vw, 72px);
    font-weight: 800;
    letter-spacing: -3px;
    margin: 18px 0 10px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #a5b4fc,
        #c084fc,
        #67e8f9
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 680px;
    margin: auto;
    color: #94a3b8;
    font-size: 18px;
    line-height: 1.6;
}


/* MAIN CARD */

.main-card {
    max-width: 900px;
    margin: 25px auto;

    padding: 28px;

    border-radius: 24px;

    background: linear-gradient(
        145deg,
        rgba(255,255,255,.07),
        rgba(255,255,255,.025)
    );

    border: 1px solid rgba(255,255,255,.09);

    box-shadow:
        0 20px 60px rgba(0,0,0,.35),
        inset 0 1px rgba(255,255,255,.06);

    backdrop-filter: blur(18px);
}


/* TEXT AREA */

textarea {
    background: rgba(15,23,42,.8) !important;
    color: #f8fafc !important;

    border: 1px solid rgba(129,140,248,.2) !important;

    border-radius: 16px !important;

    font-size: 16px !important;
}

textarea:focus {
    border-color: #818cf8 !important;

    box-shadow:
        0 0 0 1px #818cf8,
        0 0 25px rgba(129,140,248,.2) !important;
}


/* BUTTON */

.stButton > button {

    width: 100%;

    border: none;

    border-radius: 14px;

    padding: 14px 20px;

    font-size: 16px;

    font-weight: 700;

    color: white;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6,
        #06b6d4
    );

    box-shadow:
        0 0 25px rgba(99,102,241,.25);

    transition: all .25s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 35px rgba(99,102,241,.45);
}


/* ANALYSIS */

.analysis {

    text-align: center;

    padding: 20px;

    color: #a5b4fc;

    font-weight: 600;
}

.scanner {

    width: 100%;

    height: 3px;

    margin-top: 14px;

    background: #1e293b;

    overflow: hidden;

    border-radius: 10px;
}

.scanner-line {

    width: 35%;

    height: 100%;

    background: linear-gradient(
        90deg,
        transparent,
        #818cf8,
        #22d3ee,
        transparent
    );

    animation: scan 1.2s infinite ease-in-out;
}

@keyframes scan {

    0% {
        transform: translateX(-120%);
    }

    100% {
        transform: translateX(350%);
    }
}


/* RESULT */

.result {

    max-width: 900px;

    margin: 25px auto;

    padding: 30px;

    text-align: center;

    border-radius: 22px;

    background: rgba(15,23,42,.8);

    border: 1px solid rgba(255,255,255,.08);

    box-shadow:
        0 20px 50px rgba(0,0,0,.35);
}

.result-icon {
    font-size: 48px;
}

.result-title {

    font-size: 30px;

    font-weight: 800;

    margin-top: 8px;
}

.result-subtitle {

    color: #94a3b8;

    margin-top: 8px;
}


/* EXAMPLES */

.examples-title {

    max-width: 900px;

    margin: 40px auto 15px;

    color: #e2e8f0;

    font-size: 18px;

    font-weight: 700;
}

.example {

    padding: 18px;

    border-radius: 16px;

    height: 100%;

    background: rgba(15,23,42,.65);

    border: 1px solid rgba(255,255,255,.07);

    transition: .25s ease;
}

.example:hover {

    transform: translateY(-4px);

    border-color: rgba(129,140,248,.4);

    box-shadow:
        0 10px 30px rgba(99,102,241,.12);
}

.example-icon {

    font-size: 25px;
}

.example-name {

    margin-top: 7px;

    font-weight: 700;

    color: #e2e8f0;
}

.example-text {

    margin-top: 5px;

    font-size: 13px;

    color: #94a3b8;

    line-height: 1.5;
}


/* FOOTER */

.footer {

    text-align: center;

    padding: 45px 0 20px;

    color: #64748b;

    font-size: 13px;
}

.footer span {
    color: #818cf8;
}

</style>
""", unsafe_allow_html=True)


#========================================================

st.markdown("""
<div class="hero">

    <div class="badge">
        ✦ MACHINE LEARNING POWERED
    </div>

    <h1>AI SMS Guard</h1>

    <p>
        Detect suspicious messages instantly with
        machine learning powered spam detection.
    </p>

</div>
""", unsafe_allow_html=True)


#========================================================
st.markdown("""
<div class="main-card">

<h3>🔍 Analyze a Message</h3>

<p style="color:#94a3b8;">
Paste an SMS below and let the classifier analyze it.
</p>

""", unsafe_allow_html=True)

#========================================================
input_sms = st.text_area(
    'Enter the message',
    placeholder="Example: Congratulations! You have won a prize...",
    height=160,
    label_visibility="collapsed"
)


st.markdown("</div>", unsafe_allow_html=True)


# Button logic
if st.button('✨ Analyze Message'):

    if input_sms.strip() == "":
        st.warning("Please enter a message.")

    else:

        # UX animation ONLY
        animation = st.empty()

        animation.markdown("""
        <div class="analysis">

            🔍 Analyzing message...

            <div class="scanner">
                <div class="scanner-line"></div>
            </div>

        </div>
        """, unsafe_allow_html=True)

        time.sleep(1)

        animation.empty()

        # preprocess
        transformed_sms = transform_text(input_sms)

        # vectorize
        vector_input = tfidf.transform([transformed_sms])

        # predict
        prediction = model.predict(vector_input)[0]

        if prediction == 1:
            st.markdown("""
            <div class="result">

                <div class="result-icon">
                    🚨
                </div>

                <div class="result-title">
                    Spam
                </div>

                <div class="result-subtitle">
                    This message has been classified as spam.
                </div>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="result">

                <div class="result-icon">
                    🛡️
                </div>

                <div class="result-title">
                    Not Spam
                </div>

                <div class="result-subtitle">
                    This message has been classified as safe.
                </div>

            </div>
            """, unsafe_allow_html=True)


# UX / UI — Example Messages
st.markdown("""
<div class="examples-title">
    💬 Example Messages
</div>
""", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("""
    <div class="example">

        <div class="example-icon">📦</div>

        <div class="example-name">
            Delivery
        </div>

        <div class="example-text">
            Your package has been shipped and
            will arrive tomorrow.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="example">

        <div class="example-icon">💰</div>

        <div class="example-name">
            Prize
        </div>

        <div class="example-text">
            Congratulations! You have won
            a £1000 prize. Call now to claim.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="example">

        <div class="example-icon">🏦</div>

        <div class="example-name">
            Bank Alert
        </div>

        <div class="example-text">
            Your account has been credited
            with 5000. Thank you.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown("""
    <div class="example">

        <div class="example-icon">👋</div>

        <div class="example-name">
            Personal
        </div>

        <div class="example-text">
            Hey, are we still meeting
            for lunch today?
        </div>

    </div>
    """, unsafe_allow_html=True)


# Footer
st.markdown("""
<div class="footer">

    Built with
    <span>Python</span> ·
    <span>NLTK</span> ·
    <span>Scikit-learn</span> ·
    <span>Streamlit</span>

    <br><br>

    AI SMS Guard • Intelligent Message Classification

</div>
""", unsafe_allow_html=True)