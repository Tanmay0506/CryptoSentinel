import streamlit as st
import pandas as pd
import requests
from datetime import datetime

from model import CryptoSentinelModel

st.set_page_config(
    page_title="CryptoSentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Custom Dark Theme + Effects
# ----------------------------
st.markdown("""
<style>
    /* App background */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 255, 170, 0.08), transparent 25%),
            radial-gradient(circle at top right, rgba(0, 140, 255, 0.10), transparent 20%),
            linear-gradient(180deg, #0b1020 0%, #0a0f1a 100%);
        color: #e8eefc;
    }

    /* Hide default menu/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #00f5d4, #4ea8de, #9b5de5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #aab7d6;
        margin-bottom: 1.2rem;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.1rem 1.2rem;
        border-radius: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 245, 212, 0.35);
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(145deg, rgba(10,15,26,0.95), rgba(16,24,40,0.92));
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem 1rem;
        border-radius: 20px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.22);
    }

    .kpi-title {
        color: #9fb0d0;
        font-size: 0.88rem;
        margin-bottom: 0.25rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
    }

    .kpi-note {
        color: #72f1b8;
        font-size: 0.82rem;
        margin-top: 0.25rem;
    }

    /* Status pills */
    .pill {
        display: inline-block;
        padding: 0.28rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.2px;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    .pill-normal { background: rgba(34, 197, 94, 0.16); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.25); }
    .pill-low { background: rgba(59, 130, 246, 0.16); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.25); }
    .pill-medium { background: rgba(250, 204, 21, 0.16); color: #facc15; border: 1px solid rgba(250, 204, 21, 0.25); }
    .pill-high { background: rgba(249, 115, 22, 0.16); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.25); }
    .pill-critical { background: rgba(239, 68, 68, 0.16); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.25); }

    /* Transaction cards */
    .tx-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255,255,255,0.07);
        border-left: 5px solid rgba(0, 245, 212, 0.8);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 10px 24px rgba(0,0,0,0.2);
    }

    .tx-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: #f8fbff;
        margin-bottom: 0.3rem;
    }

    .tx-meta {
        color: #b2bfdc;
        font-size: 0.86rem;
        line-height: 1.5;
    }

    .tx-amount {
        font-size: 1.15rem;
        font-weight: 800;
        color: #00f5d4;
    }

    .small-label {
        color: #92a3c8;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10,15,26,0.98), rgba(12,18,32,0.98));
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #00f5d4, #4ea8de);
        color: #08101f !important;
        font-weight: 800;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 10px 20px rgba(0,245,212,0.15);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(0,245,212,0.25);
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stMultiSelect div {
        border-radius: 12px !important;
    }

    /* Horizontal line */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        margin: 1rem 0 1.1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.markdown("## 🛡️ CryptoSentinel")
st.sidebar.caption("Cryptocurrency Monitoring and Analysis System")

mode = st.sidebar.radio(
    "Choose Mode",
    ["📡 Real-Time Monitoring", "📤 Upload Dataset", "📊 Insights"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Controls")

limit = st.sidebar.slider("Max Transactions", 20, 5000, 200, step=20)
auto_refresh = st.sidebar.checkbox("Auto refresh every 60 seconds", value=False)
refresh_btn = st.sidebar.button("🔁 Refresh Data")
severity_filter = st.sidebar.multiselect(
    "Filter Severity",
    ["Normal", "Low", "Medium", "High", "Critical"],
    default=["Low", "Medium", "High", "Critical"]
)

search_text = st.sidebar.text_input("Search address / txid", placeholder="Enter address or txid")

st.sidebar.markdown("---")
st.sidebar.info("Live monitoring depends on external blockchain API availability.")

# ----------------------------
# Data Fetch
# ----------------------------
@st.cache_data(ttl=60)
def fetch_transactions(limit=100):
    try:
        base_url = "https://blockchain.info"
        latest = requests.get(f"{base_url}/latestblock", timeout=15)
        latest.raise_for_status()
        block_hash = latest.json()["hash"]

        block = requests.get(f"{base_url}/rawblock/{block_hash}", timeout=15)
        block.raise_for_status()
        block_json = block.json()

        txs = []
        for tx in block_json.get("tx", [])[:limit]:
            inputs = tx.get("inputs", [])
            outputs = tx.get("out", [])

            input_value = sum(i.get("prev_out", {}).get("value", 0) for i in inputs)
            output_value = sum(o.get("value", 0) for o in outputs)

            txs.append({
                "txid": tx.get("hash", ""),
                "amount_btc": round(output_value / 1e8, 8),
                "fee": round((input_value - output_value) / 1e8, 8) if input_value > 0 else 0.0,
                "inputs": len(inputs),
                "outputs": len(outputs),
                "timestamp": tx.get("time"),
                "block_height": block_json.get("height"),
                "from_address": inputs[0].get("prev_out", {}).get("addr", "coinbase") if inputs else "coinbase",
                "to_address": outputs[0].get("addr", "unknown") if outputs else "unknown",
            })

        df = pd.DataFrame(txs)
        if not df.empty:
            df["timestamp_readable"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")
        return df

    except Exception:
        return pd.DataFrame()

@st.cache_resource
def train_model(df):
    model = CryptoSentinelModel()
    model.fit(df[["amount_btc", "fee", "inputs", "outputs"]])
    return model

def severity_badge(sev: str) -> str:
    sev = str(sev).strip().lower()
    if sev == "critical":
        return '<span class="pill pill-critical">CRITICAL</span>'
    if sev == "high":
        return '<span class="pill pill-high">HIGH</span>'
    if sev == "medium":
        return '<span class="pill pill-medium">MEDIUM</span>'
    if sev == "low":
        return '<span class="pill pill-low">LOW</span>'
    return '<span class="pill pill-normal">NORMAL</span>'

def status_badge(status: str) -> str:
    if str(status).lower() == "normal":
        return '<span class="pill pill-normal">NORMAL</span>'
    return '<span class="pill pill-high">FLAGGED</span>'

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()
    if "severity" in out.columns:
        out = out[out["severity"].isin(severity_filter)]

    if search_text.strip():
        q = search_text.strip().lower()
        mask = (
            out["txid"].astype(str).str.lower().str.contains(q, na=False) |
            out["from_address"].astype(str).str.lower().str.contains(q, na=False) |
            out["to_address"].astype(str).str.lower().str.contains(q, na=False)
        )
        out = out[mask]

    return out

def render_kpis(full: pd.DataFrame):
    total = len(full)
    suspicious = int((full["status"] != "Normal").sum())
    critical = int((full["severity"] == "Critical").sum()) if "severity" in full.columns else 0
    avg_risk = float(full["risk_score"].mean()) if "risk_score" in full.columns and not full.empty else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Transactions</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-note">Fetched from live block</div>
        </div>
    """, unsafe_allow_html=True)
    c2.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Flagged Transactions</div>
            <div class="kpi-value">{suspicious}</div>
            <div class="kpi-note">Model-detected anomalies</div>
        </div>
    """, unsafe_allow_html=True)
    c3.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Critical Alerts</div>
            <div class="kpi-value">{critical}</div>
            <div class="kpi-note">Highest severity cases</div>
        </div>
    """, unsafe_allow_html=True)
    c4.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Risk Score</div>
            <div class="kpi-value">{avg_risk:.1f}</div>
            <div class="kpi-note">0 to 100 scale</div>
        </div>
    """, unsafe_allow_html=True)

def prepare_full_df(df: pd.DataFrame) -> pd.DataFrame:
    model = train_model(df)
    result = model.predict(df[["amount_btc", "fee", "inputs", "outputs"]])
    full = pd.concat([df.reset_index(drop=True), result[["risk_score", "severity", "status"]].reset_index(drop=True)], axis=1)
    return full

def render_transaction_cards(df: pd.DataFrame, max_cards: int = 12):
    if df.empty:
        st.info("No transactions match the current filters.")
        return

    show_df = df.head(max_cards)
    for _, row in show_df.iterrows():
        sev_html = severity_badge(row.get("severity", "Normal"))
        status_html = status_badge(row.get("status", "Normal"))
        ts = row.get("timestamp_readable")
        ts_text = ts.strftime("%Y-%m-%d %H:%M:%S") if pd.notna(ts) else str(row.get("timestamp", "N/A"))

        st.markdown(f"""
            <div class="tx-card">
                <div class="tx-title">TXID: {str(row.get("txid", ""))[:18]}...</div>
                <div style="margin-bottom: 0.5rem;">
                    {sev_html} {status_html}
                </div>
                <div class="tx-meta">
                    <b>From:</b> {row.get("from_address", "unknown")}<br>
                    <b>To:</b> {row.get("to_address", "unknown")}<br>
                    <b>Timestamp:</b> {ts_text}<br>
                    <b>Block:</b> {row.get("block_height", "N/A")}
                </div>
                <div style="margin-top: 0.65rem;" class="tx-amount">
                    Amount: {row.get("amount_btc", 0):.8f} BTC
                </div>
                <div class="tx-meta">
                    Fee: {row.get("fee", 0):.8f} BTC &nbsp; | &nbsp; Inputs: {row.get("inputs", 0)} &nbsp; | &nbsp; Outputs: {row.get("outputs", 0)} &nbsp; | &nbsp; Risk: {row.get("risk_score", 0):.1f}
                </div>
            </div>
        """, unsafe_allow_html=True)

# ----------------------------
# App Header
# ----------------------------
st.markdown('<div class="main-title">CryptoSentinel</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Cryptocurrency Monitoring and Analysis System • Real-time Bitcoin anomaly detection • Severity-based alerts</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Optional auto refresh using rerun
if auto_refresh:
    st.caption("Auto refresh is enabled. Refreshing every 60 seconds.")
    st.autorefresh(interval=60_000, key="crypto_sentinel_refresh")

# ----------------------------
# Mode: Real-Time Monitoring
# ----------------------------
if mode == "📡 Real-Time Monitoring":
    tab1, tab2, tab3 = st.tabs(["📡 Live Transactions", "🚨 Flagged Transactions", "📈 Insights"])

    if refresh_btn:
        st.cache_data.clear()

    with st.spinner("Fetching the latest Bitcoin transactions..."):
        df = fetch_transactions(limit)

    if df.empty:
        st.error("❌ Failed to fetch data. The API may be unavailable or rate-limited.")
    else:
        full = prepare_full_df(df)
        full = apply_filters(full)

        with tab1:
            render_kpis(full)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            left, right = st.columns([1.3, 1])
            with left:
                st.subheader("Live Transaction Table")
                display_cols = [
                    "txid", "from_address", "to_address", "amount_btc", "fee",
                    "inputs", "outputs", "timestamp_readable", "block_height",
                    "severity", "status", "risk_score"
                ]
                st.dataframe(
                    full[display_cols].sort_values("risk_score", ascending=False),
                    use_container_width=True,
                    height=520
                )

            with right:
                st.subheader("Transaction Overview")
                st.markdown("### Quick Summary")
                st.write("Transactions analyzed:", len(full))
                st.write("Flagged:", int((full["status"] != "Normal").sum()))
                st.write("Critical:", int((full["severity"] == "Critical").sum()))
                st.write("Highest risk:", f'{full["risk_score"].max():.1f}' if not full.empty else "N/A")

                st.markdown("### Filtered Cards")
                render_transaction_cards(full, max_cards=8)

        with tab2:
            flagged = full[full["status"] != "Normal"].sort_values("risk_score", ascending=False)

            st.subheader("🚨 Flagged Transactions")
            st.caption("These transactions were identified as anomalous by the model.")
            st.dataframe(
                flagged[[
                    "txid", "from_address", "to_address", "amount_btc", "fee",
                    "timestamp_readable", "block_height", "severity", "risk_score"
                ]],
                use_container_width=True,
                height=420
            )

            st.markdown("### Flagged Cards")
            render_transaction_cards(flagged, max_cards=12)

        with tab3:
            st.subheader("Model Insights")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Average Amount", f'{full["amount_btc"].mean():.8f} BTC')
                st.metric("Average Fee", f'{full["fee"].mean():.8f} BTC')
            with c2:
                st.metric("Unique Senders", full["from_address"].nunique())
                st.metric("Unique Receivers", full["to_address"].nunique())

            st.markdown("### Risk Score Distribution")
            st.bar_chart(full["risk_score"].value_counts(bins=10).sort_index())

# ----------------------------
# Mode: Upload Dataset
# ----------------------------
elif mode == "📤 Upload Dataset":
    st.title("📤 Upload Transaction Dataset")
    st.caption("Upload a CSV with columns: amount_btc, fee, inputs, outputs")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip().str.lower()

        required_cols = ["amount_btc", "fee", "inputs", "outputs"]

        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain columns: {required_cols}")
        else:
            with st.spinner("Analyzing uploaded transactions..."):
                full = prepare_full_df(df[required_cols])

                # attach extra cols if present
                extra_cols = [c for c in df.columns if c not in required_cols]
                if extra_cols:
                    full = pd.concat([df.reset_index(drop=True), full[["risk_score", "severity", "status"]]], axis=1)
                else:
                    full = pd.concat([df[required_cols].reset_index(drop=True), full[["risk_score", "severity", "status"]]], axis=1)

            st.success("✅ Dataset analyzed successfully")

            render_kpis(full)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["📄 Full Data", "🚨 Flagged Only", "📈 Insights"])

            with tab1:
                st.dataframe(full, use_container_width=True, height=480)

            with tab2:
                flagged = full[full["status"] != "Normal"].sort_values("risk_score", ascending=False)
                st.dataframe(flagged, use_container_width=True, height=360)
                st.markdown("### Flagged Cards")
                render_transaction_cards(flagged, max_cards=10)

            with tab3:
                st.markdown("### Risk Score Distribution")
                st.bar_chart(full["risk_score"].value_counts(bins=10).sort_index())

                st.markdown("### Download Results")
                st.download_button(
                    "⬇️ Download Results CSV",
                    full.to_csv(index=False).encode("utf-8"),
                    "analyzed_transactions.csv",
                    "text/csv"
                )
    else:
        st.info("Upload a CSV to start analysing your transactions.")

# ----------------------------
# Mode: Insights
# ----------------------------
elif mode == "📊 Insights":
    st.title("📊 CryptoSentinel Insights")
    st.markdown("""
    <div class="glass-card">
        <b>What CryptoSentinel does:</b><br><br>
        • Monitors Bitcoin transactions in near real time<br>
        • Detects unusual transaction patterns using Isolation Forest<br>
        • Assigns a risk score and severity level<br>
        • Shows flagged transactions with sender, receiver, timestamp, amount, and block number<br>
        • Supports CSV upload for offline analysis
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Severity Levels")
    cols = st.columns(4)
    with cols[0]:
        st.markdown('<div class="pill pill-low">LOW</div>', unsafe_allow_html=True)
        st.write("Minor anomalies with low risk.")
    with cols[1]:
        st.markdown('<div class="pill pill-medium">MEDIUM</div>', unsafe_allow_html=True)
        st.write("Moderate deviations from normal behavior.")
    with cols[2]:
        st.markdown('<div class="pill pill-high">HIGH</div>', unsafe_allow_html=True)
        st.write("Strong anomaly signals.")
    with cols[3]:
        st.markdown('<div class="pill pill-critical">CRITICAL</div>', unsafe_allow_html=True)
        st.write("Highest-risk suspicious transactions.")

    st.markdown("### UI Enhancements Included")
   