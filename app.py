import streamlit as st
import pickle
import string
import time
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Email/SMS Spam Classifier",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS — UI ONLY
# =========================================================

st.markdown("""
<style>

    /* ---------- MAIN APP ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.16), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(168, 85, 247, 0.13), transparent 30%),
            radial-gradient(circle at 50% 90%, rgba(14, 165, 233, 0.08), transparent 35%),
            #050816;
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }


    /* ---------- MAIN CONTENT WIDTH ---------- */

    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* ---------- HEADINGS ---------- */

    h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -2px;
        background: linear-gradient(
            90deg,
            #ffffff,
            #a78bfa,
            #38bdf8
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.4rem;
    }

    h2 {
        color: #f8fafc !important;
    }

    h3 {
        color: #e2e8f0 !important;
    }


    /* ---------- CAPTIONS ---------- */

    .stCaption {
        color: #94a3b8 !important;
    }


    /* ---------- TEXT AREA ---------- */

    [data-testid="stTextArea"] textarea {
        background: rgba(15, 23, 42, 0.88) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(129, 140, 248, 0.35) !important;
        border-radius: 16px !important;
        padding: 18px !important;
        font-size: 16px !important;
        box-shadow:
            0 0 25px rgba(99, 102, 241, 0.08),
            inset 0 0 20px rgba(0, 0, 0, 0.15);
        transition: all 0.25s ease;
    }

    [data-testid="stTextArea"] textarea:focus {
        border: 1px solid rgba(129, 140, 248, 0.9) !important;
        box-shadow:
            0 0 25px rgba(99, 102, 241, 0.25),
            0 0 60px rgba(56, 189, 248, 0.08);
    }


    /* ---------- BUTTON ---------- */

    [data-testid="stButton"] button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(129, 140, 248, 0.45);
        background: linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6,
            #06b6d4
        );
        color: white;
        font-weight: 700;
        font-size: 17px;
        padding: 0.75rem 1rem;
        transition: all 0.25s ease;
        box-shadow:
            0 0 20px rgba(99, 102, 241, 0.20);
    }

    [data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 0 25px rgba(99, 102, 241, 0.45),
            0 0 50px rgba(6, 182, 212, 0.18);
        border-color: rgba(255, 255, 255, 0.5);
    }


    /* ---------- COLUMNS / CARDS ---------- */

    [data-testid="column"] {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 15px;
        transition: all 0.25s ease;
    }

    [data-testid="column"]:hover {
        border-color: rgba(129, 140, 248, 0.35);
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.08);
        transform: translateY(-2px);
    }


    /* ---------- SUCCESS / ERROR / INFO ---------- */

    [data-testid="stAlert"] {
        border-radius: 16px !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border-color: rgba(148, 163, 184, 0.12) !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }


    /* ---------- FOOTER ---------- */

    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 40px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# NLTK
# =========================================================

nltk.download('punkt_tab')
nltk.download('stopwords')

ps = PorterStemmer()


# =========================================================
# TEXT TRANSFORMATION
# =========================================================

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []

    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# =========================================================
# LOAD MODEL
# =========================================================

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


# =========================================================
# HERO SECTION
# =========================================================

st.caption("✦ MACHINE LEARNING POWERED")

st.title("🛡️ AI SMS Guard")

st.markdown(
    "<p style='text-align:center; color:#94a3b8; "
    "font-size:18px; margin-bottom:35px;'>"
    "Detect suspicious messages instantly with "
    "<b style='color:#a78bfa;'>machine learning powered</b> "
    "spam detection."
    "</p>",
    unsafe_allow_html=True
)


# =========================================================
# ANALYZER
# =========================================================

st.subheader("🔍 Analyze a Message")

st.caption(
    "Paste an SMS or message below and let the classifier determine "
    "whether it looks like spam."
)

input_sms = st.text_area(
    "Message",
    placeholder="Example: Congratulations! You have won a free prize...",
    height=160,
    label_visibility="collapsed"
)


# =========================================================
# PREDICT BUTTON
# =========================================================

if st.button("✨ Analyze Message"):

    if input_sms.strip() == "":
        st.warning("⚠️ Please enter a message first.")

    else:

        # -------------------------------------------------
        # UI ANIMATION ONLY
        # -------------------------------------------------

        progress = st.progress(
            0,
            text="🔍 Preparing message analysis..."
        )

        for i in range(0, 101, 10):

            if i < 40:
                message = "🔍 Reading message..."
            elif i < 70:
                message = "🧠 Processing text..."
            else:
                message = "⚡ Running spam detection..."

            progress.progress(i, text=message)
            time.sleep(0.04)

        progress.empty()


        # =================================================
        # ORIGINAL ML PIPELINE — DO NOT CHANGE
        # =================================================

        # preprocess
        transformed_sms = transform_text(input_sms)

        # vectorize
        vector_input = tfidf.transform([transformed_sms])

        # predict
        prediction = model.predict(vector_input)[0]


        # =================================================
        # RESULT
        # =================================================

        st.divider()

        if prediction == 1:

            st.error(
                "🚨 SPAM DETECTED\n\n"
                "This message has been classified as spam."
            )

            st.markdown(
                "<p style='text-align:center; color:#94a3b8;'>"
                "⚠️ Be careful with links, payments, OTP requests, "
                "and unknown senders."
                "</p>",
                unsafe_allow_html=True
            )

        else:

            st.success(
                "🛡️ NOT SPAM\n\n"
                "This message appears to be legitimate."
            )

            st.markdown(
                "<p style='text-align:center; color:#94a3b8;'>"
                "✓ The classifier did not identify this message as spam."
                "</p>",
                unsafe_allow_html=True
            )


# =========================================================
# EXAMPLE MESSAGES
# =========================================================

st.divider()

st.subheader("💬 Try Example Messages")

st.caption(
    "Test the classifier using some sample messages."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📦 Delivery")
    st.caption(
        "Your package has been shipped and will arrive tomorrow."
    )

with col2:
    st.markdown("### 🎁 Prize")
    st.caption(
        "Congratulations! You have won a free cash prize. Claim now!"
    )

with col3:
    st.markdown("### 🏦 Bank")
    st.caption(
        "Your account statement is ready. Please check your email."
    )

with col4:
    st.markdown("### 📱 Offer")
    st.caption(
        "You have been selected for an exclusive reward. Call now!"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer-text">
        AI SMS Guard &nbsp;•&nbsp; Machine Learning Spam Detection
        <br>
        Built with Python, Scikit-learn & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)