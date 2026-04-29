import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Concrete Vault Intelligence Terminal",
    page_icon="🗿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
    background-color: #080B10;
    color: #E8EAF0;
}
.stApp { background-color: #080B10; }
.block-container { padding: 1.5rem 2rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0A0D12;
    border-right: 1px solid #0D1117;
}
section[data-testid="stSidebar"] * { color: #E8EAF0 !important; font-family: 'IBM Plex Mono', monospace !important; }

/* Inputs */
.stNumberInput input, .stSelectbox select, .stSlider {
    background-color: #0D1117 !important;
    color: #E8EAF0 !important;
    border: 1px solid #1E2530 !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #0D1117;
    border: 1px solid #1E2530;
    border-radius: 10px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] { font-size: 10px !important; letter-spacing: 2px !important; color: #444 !important; }
[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 700 !important; color: #00FFB2 !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0A0D12;
    border-bottom: 1px solid #0D1117;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #444;
    border: 1px solid #1E2530;
    border-radius: 5px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 6px 18px;
}
.stTabs [aria-selected="true"] {
    background-color: #00FFB2 !important;
    color: #080B10 !important;
    font-weight: 700 !important;
    border-color: #00FFB2 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #0D1117 !important;
    border: 1px solid #1E2530 !important;
    border-radius: 8px !important;
    color: #888 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.streamlit-expanderContent {
    background: #080B10 !important;
    border: 1px solid #1E2530 !important;
    border-radius: 0 0 8px 8px !important;
}

/* Info/Success boxes */
.stInfo { background: #00FFB215 !important; border-color: #00FFB2 !important; border-radius: 8px !important; }
.stSuccess { background: #00FFB215 !important; border-radius: 8px !important; }
.stWarning { background: #FFB80015 !important; border-radius: 8px !important; }

/* Divider */
hr { border-color: #0D1117 !important; }

/* Header card */
.header-card {
    background: linear-gradient(135deg, #0D1117 0%, #0A0D12 100%);
    border: 1px solid #1E2530;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 20px;
}
.vault-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}
.stat-box {
    background: #0D1117;
    border: 1px solid #111;
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ─── Vault Data ────────────────────────────────────────────────────────────────
VAULTS = {
    "🏦 WeWETH (Institutional)": {
        "asset": "WETH", "color": "#00FFB2", "risk": "LOW",
        "tvl": 412_000_000, "apy": 7.84,
        "strategy": "Institutional Restaking",
        "daily_yield": 88_493,
        "price_usd": 3200,
    },
    "₿ ctWBTC": {
        "asset": "WBTC", "color": "#F7931A", "risk": "MEDIUM",
        "tvl": 198_000_000, "apy": 5.21,
        "strategy": "Lending + Delta-Neutral",
        "daily_yield": 28_274,
        "price_usd": 105_000,
    },
    "💵 ctUSD (Stable)": {
        "asset": "USDC", "color": "#2775CA", "risk": "LOW",
        "tvl": 825_000_000, "apy": 9.12,
        "strategy": "Stablecoin Yield Optimizer",
        "daily_yield": 205_890,
        "price_usd": 1,
    },
    "⚡ sEIGEN": {
        "asset": "EIGEN", "color": "#9B59FF", "risk": "HIGH",
        "tvl": 67_000_000, "apy": 18.44,
        "strategy": "EigenLayer Restaking",
        "daily_yield": 33_842,
        "price_usd": 3.8,
    },
}

RISK_COLORS = {"LOW": "#00FFB2", "MEDIUM": "#FFB800", "HIGH": "#FF4D4D"}

def fmt_tvl(n):
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.1f}M"
    return f"${n:,.0f}"

def generate_apy_history(base_apy, days=30):
    random.seed(42)
    dates = [datetime.today() - timedelta(days=days-i) for i in range(days)]
    apys = [round(base_apy + random.uniform(-1.5, 1.5), 2) for _ in range(days)]
    return pd.DataFrame({"Date": dates, "APY": apys})

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-card">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
      <div style="font-family:'Syne',sans-serif; font-size:26px; font-weight:800; color:#fff; letter-spacing:1px;">
        ⬡ CONCRETE<span style="color:#00FFB2;">.XYZ</span>
      </div>
      <div style="font-size:10px; color:#333; letter-spacing:3px; margin-top:2px;">VAULT INTELLIGENCE TERMINAL</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:11px; color:#00FFB2;">● LIVE · ETH MAINNET</div>
      <div style="font-size:10px; color:#333; margin-top:2px;">Simulation Mode — No Wallet Needed</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Protocol Stats Bar ────────────────────────────────────────────────────────
total_tvl = sum(v["tvl"] for v in VAULTS.values())
total_daily = sum(v["daily_yield"] for v in VAULTS.values())

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("TOTAL TVL", fmt_tvl(total_tvl))
with c2:
    st.metric("DAILY YIELD", f"${total_daily:,.0f}")
with c3:
    st.metric("ACTIVE VAULTS", "4")
with c4:
    st.metric("NETWORK", "Ethereum")

st.markdown("---")

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗿 Vault Configuration")
    st.markdown("---")

    vault_name = st.selectbox("Select Vault", list(VAULTS.keys()))
    vault = VAULTS[vault_name]

    st.markdown(f"""
    <div style="background:#0D1117; border:1px solid #1E2530; border-radius:8px; padding:12px; margin:12px 0;">
        <div style="font-size:9px; color:#333; letter-spacing:2px; margin-bottom:6px;">SELECTED VAULT</div>
        <div style="font-size:18px; font-weight:700; color:{vault['color']};">{vault['apy']}% APY</div>
        <div style="font-size:10px; color:#444; margin-top:4px;">{vault['strategy']}</div>
        <div style="font-size:10px; color:#555; margin-top:4px;">TVL: {fmt_tvl(vault['tvl'])}</div>
        <div style="font-size:10px; color:{RISK_COLORS[vault['risk']]}; margin-top:4px;">Risk: {vault['risk']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Simulation Settings")

    principal = st.number_input("Deposit Amount ($)", min_value=100, value=10_000, step=500)
    period_label = st.select_slider("Time Period", options=["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years"])
    compound = st.toggle("Compound Interest", value=True)

    period_days = {"1 Month": 30, "3 Months": 90, "6 Months": 180,
                   "1 Year": 365, "2 Years": 730, "5 Years": 1825}[period_label]

    st.markdown("---")
    market_volatility = st.select_slider(
        "Market Volatility",
        options=["Low", "Medium", "High", "Extreme"],
        value="Medium"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:9px; color:#333; letter-spacing:1px; line-height:1.8;">
    ⚠ SIMULATION ONLY<br>NOT FINANCIAL ADVICE<br>DATA IS ILLUSTRATIVE<br>YIELDS SUBJECT TO CHANGE
    </div>
    """, unsafe_allow_html=True)

# ─── Calculations ──────────────────────────────────────────────────────────────
apy = vault["apy"]
vol_multiplier = {"Low": 1.1, "Medium": 1.5, "High": 2.5, "Extreme": 4.0}[market_volatility]
standard_yield = round(apy / vol_multiplier, 2)
concrete_yield = round(apy * 0.95, 2)

if compound:
    earnings = principal * (pow(1 + apy / 100, period_days / 365) - 1)
else:
    earnings = (principal * apy / 100) * (period_days / 365)

total_value = principal + earnings
daily_earnings = (principal * apy / 100) / 365
ct_tokens = principal / vault["price_usd"]
stability_ratio = apy / vol_multiplier

# ─── Main Tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 OVERVIEW", "🧮 SIMULATOR", "⚖️ COMPARE", "❓ FAQS"])

# ═══ TAB 1: OVERVIEW ══════════════════════════════════════════════════════════
with tab1:
    # Key Stats
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("TOTAL VALUE LOCKED", fmt_tvl(vault["tvl"]), "Ethereum Mainnet")
    with k2:
        st.metric("DAILY YIELD", f"${vault['daily_yield']:,.0f}", "All depositors")
    with k3:
        st.metric("RISK LEVEL", vault["risk"],
                  delta="Stable ✓" if vault["risk"] == "LOW" else ("Moderate ⚠" if vault["risk"] == "MEDIUM" else "High Risk ⚡"),
                  delta_color="normal" if vault["risk"] == "LOW" else "inverse")

    st.markdown("---")

    col_chart, col_info = st.columns([2, 1])

    with col_chart:
        # APY History Chart
        hist = generate_apy_history(apy)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["Date"], y=hist["APY"],
            mode="lines",
            line=dict(color=vault["color"], width=2),
            fill="tozeroy",
            fillcolor=f"{vault['color']}22",
            name="APY",
            hovertemplate="<b>%{x|%b %d}</b><br>APY: %{y:.2f}%<extra></extra>"
        ))
        fig.update_layout(
            title="30-Day APY History",
            plot_bgcolor="#0D1117",
            paper_bgcolor="#0D1117",
            font=dict(family="IBM Plex Mono", color="#444", size=10),
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#333"), color="#333"),
            yaxis=dict(showgrid=True, gridcolor="#111", tickfont=dict(size=9, color="#333"), color="#333"),
            margin=dict(l=10, r=10, t=40, b=10),
            height=220,
            showlegend=False,
            title_font=dict(size=11, color="#444"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid #111; border-radius:10px; padding:16px; height:100%;">
            <div style="font-size:9px; color:#333; letter-spacing:2px; margin-bottom:12px;">VAULT DETAILS</div>
            <div style="margin-bottom:10px;">
                <div style="font-size:10px; color:#444;">Strategy</div>
                <div style="font-size:12px; color:#fff; font-weight:600;">{vault['strategy']}</div>
            </div>
            <div style="margin-bottom:10px;">
                <div style="font-size:10px; color:#444;">Base Asset</div>
                <div style="font-size:14px; color:{vault['color']}; font-weight:700;">{vault['asset']}</div>
            </div>
            <div style="margin-bottom:10px;">
                <div style="font-size:10px; color:#444;">Current APY</div>
                <div style="font-size:24px; color:{vault['color']}; font-weight:700;">{apy}%</div>
            </div>
            <div>
                <div style="font-size:10px; color:#444;">Volatility Buffer</div>
                <div style="font-size:12px; color:#FFB800;">Active 🛡</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Strategy Breakdown
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("#### Strategy Breakdown")
        strategy_data = pd.DataFrame({
            "Component": ["Lending Markets", "Liquidity Provision", "Protection Reserve"],
            "Allocation": [45, 30, 25]
        })
        fig2 = px.pie(strategy_data, values="Allocation", names="Component",
                      color_discrete_sequence=[vault["color"], f"{vault['color']}99", f"{vault['color']}55"],
                      hole=0.5)
        fig2.update_layout(
            plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
            font=dict(family="IBM Plex Mono", color="#888", size=10),
            margin=dict(l=10, r=10, t=10, b=10),
            height=200,
            showlegend=True,
            legend=dict(font=dict(color="#444", size=9), bgcolor="#0D1117")
        )
        fig2.update_traces(textfont=dict(family="IBM Plex Mono", size=10))
        st.plotly_chart(fig2, use_container_width=True)

    with sc2:
        st.markdown("#### Risk Indicators")
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid #111; border-radius:10px; padding:16px;">
        """, unsafe_allow_html=True)

        risks = [
            ("Smart Contract Risk", {"LOW": 1, "MEDIUM": 2, "HIGH": 3}[vault["risk"]]),
            ("Liquidity Risk", 1 if vault["risk"] == "LOW" else 3 if vault["risk"] == "HIGH" else 2),
            ("Market Risk", 1 if vault["risk"] == "LOW" else 2),
        ]
        risk_color = RISK_COLORS[vault["risk"]]
        for label, level in risks:
            bars = "".join([
                f'<div style="flex:1; height:6px; border-radius:2px; background:{"' + risk_color + '" if i < level else "#111"}"></div>'
                for i in range(3)
            ])
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="font-size:10px; color:#555; margin-bottom:6px;">{label}</div>
                <div style="display:flex; gap:4px;">
                    {"".join([f'<div style="flex:1; height:6px; border-radius:2px; background:{risk_color if i < level else "#111"};"></div>' for i in range(3)])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ═══ TAB 2: SIMULATOR ═════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### 🧮 Vault Earnings Simulator")

    r1, r2 = st.columns(2)

    with r1:
        # Stability Equation
        st.markdown("""
        #### The Stability Equation
        """)
        st.latex(r'''
        \text{Stability Ratio} = \frac{\text{Net Yield}}{\sigma(\text{Market Volatility})}
        ''')

        # Yield Comparison
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Standard DeFi Net Yield", f"{standard_yield:.2f}%", f"÷{vol_multiplier}x Risk Impact", delta_color="inverse")
        with m2:
            st.metric("Concrete Protected Yield", f"{concrete_yield:.2f}%", "🗿 Stable Floor")

        st.info(f"At **{market_volatility}** volatility, Concrete's buffer keeps your floor solid. Stability Ratio: **{stability_ratio:.2f}**")

        # ct Token Calculator
        st.markdown("---")
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid #1E2530; border-radius:10px; padding:16px;">
            <div style="font-size:9px; color:#333; letter-spacing:2px; margin-bottom:8px;">ct[{vault['asset']}] TOKENS RECEIVED</div>
            <div style="font-size:28px; font-weight:700; color:{vault['color']};">{ct_tokens:.6f}</div>
            <div style="font-size:10px; color:#333; margin-top:4px;">Yield-bearing vault shares for ${principal:,.0f} deposit</div>
            <div style="font-size:10px; color:#444; margin-top:4px;">1 {vault['asset']} = ${vault['price_usd']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        # Earnings Results
        st.markdown(f"""
        <div style="background:#0D1117; border:1px solid {vault['color']}33; border-radius:12px; padding:20px; box-shadow: 0 0 20px {vault['color']}15; margin-bottom:14px;">
            <div style="font-size:9px; color:#333; letter-spacing:2px; margin-bottom:6px;">PROJECTED EARNINGS</div>
            <div style="font-size:42px; font-weight:700; color:{vault['color']}; line-height:1.1;">+${earnings:,.2f}</div>
            <div style="font-size:11px; color:#444; margin-top:8px;">Over {period_label} at {apy}% APY {'(compounded)' if compound else '(simple interest)'}</div>
        </div>
        """, unsafe_allow_html=True)

        e1, e2 = st.columns(2)
        with e1:
            st.metric("Total Portfolio Value", f"${total_value:,.2f}")
        with e2:
            st.metric("Daily Earnings", f"${daily_earnings:,.2f}")

        # 12-Month Projection Chart
        proj_months = list(range(1, 13))
        proj_values = [
            principal * pow(1 + apy/100, m/12) if compound
            else principal + (principal * apy/100) * (m/12)
            for m in proj_months
        ]
        proj_df = pd.DataFrame({"Month": [f"M{m}" for m in proj_months], "Value": proj_values})

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=proj_df["Month"], y=proj_df["Value"],
            mode="lines",
            line=dict(color=vault["color"], width=2),
            fill="tozeroy",
            fillcolor=f"{vault['color']}22",
            hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"
        ))
        fig3.update_layout(
            title="12-Month Portfolio Projection",
            plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
            font=dict(family="IBM Plex Mono", color="#444", size=10),
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#333"), color="#333"),
            yaxis=dict(showgrid=True, gridcolor="#111", tickfont=dict(size=9, color="#333"), color="#333"),
            margin=dict(l=10, r=10, t=40, b=10),
            height=200,
            title_font=dict(size=11, color="#444"),
        )
        st.plotly_chart(fig3, use_container_width=True)

# ═══ TAB 3: COMPARE ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### ⚖️ All Vaults Comparison")

    # APY Bar Chart
    vault_names = list(VAULTS.keys())
    vault_apys = [v["apy"] for v in VAULTS.values()]
    vault_colors = [v["color"] for v in VAULTS.values()]

    fig4 = go.Figure(data=[
        go.Bar(
            x=vault_names,
            y=vault_apys,
            marker_color=vault_colors,
            text=[f"{a}%" for a in vault_apys],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono", size=11, color="#fff"),
            hovertemplate="<b>%{x}</b><br>APY: %{y}%<extra></extra>"
        )
    ])
    fig4.update_layout(
        title="Live APY — All Vaults",
        plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
        font=dict(family="IBM Plex Mono", color="#444", size=10),
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#555"), color="#333"),
        yaxis=dict(showgrid=True, gridcolor="#111", tickfont=dict(size=9, color="#333"), color="#333", title="APY %"),
        margin=dict(l=10, r=10, t=50, b=10),
        height=260,
        title_font=dict(size=12, color="#555"),
        bargap=0.35,
    )
    st.plotly_chart(fig4, use_container_width=True)

    # $10k Comparison Table
    st.markdown("#### $10,000 Deposited — 1 Year Returns")
    compare_data = []
    for name, v in VAULTS.items():
        earn = 10000 * (pow(1 + v["apy"]/100, 1) - 1)
        compare_data.append({
            "Vault": name,
            "APY": f"{v['apy']}%",
            "TVL": fmt_tvl(v["tvl"]),
            "Risk": v["risk"],
            "1Y Earnings": f"${earn:,.2f}",
            "Total Value": f"${10000 + earn:,.2f}",
        })
    df = pd.DataFrame(compare_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # TVL Share
    st.markdown("#### TVL Distribution")
    tvl_vals = [v["tvl"] for v in VAULTS.values()]
    fig5 = px.pie(
        values=tvl_vals,
        names=vault_names,
        color_discrete_sequence=vault_colors,
        hole=0.55
    )
    fig5.update_layout(
        plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
        font=dict(family="IBM Plex Mono", color="#888", size=10),
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
        legend=dict(font=dict(color="#444", size=9), bgcolor="#0D1117")
    )
    st.plotly_chart(fig5, use_container_width=True)

# ═══ TAB 4: FAQs ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("#### 📌 Technical FAQs")

    faqs = [
        ("Who developed this tool?",
         "This tool is developed by **mkashifalikcp**, a dedicated contributor to the @ConcreteXYZ community focusing on risk-management, vault stability, and yield simulation."),
        ("How does Concrete protect my capital?",
         "Concrete uses automated vault infrastructure to create a protective buffer, absorbing slippage and volatility before it impacts the depositor. The protocol's Blueprint smart contracts actively manage risk exposure."),
        ("What is a ct[Asset] token?",
         "ct tokens (e.g. ctWETH, ctUSD) are yield-bearing vault shares. When you deposit into a Concrete vault, you receive ct tokens that automatically appreciate in value as the vault earns yield."),
        ("What is the WeWETH vault?",
         "WeWETH is Concrete's institutional-grade restaking vault with $400M+ TVL. It is designed for large depositors seeking stable, low-risk ETH yield through a diversified restaking strategy."),
        ("How is APY calculated?",
         "The displayed APY is a 7-day rolling average derived from on-chain yield data across all active strategies inside the vault. Actual returns may vary based on market conditions."),
        ("Is this financial advice?",
         "No — this is a simulation tool built to demonstrate the mathematical edge of risk-adjusted yield. Always do your own research (DYOR) before investing."),
    ]

    for q, a in faqs:
        with st.expander(q):
            st.markdown(a)

    st.markdown("---")
    st.success("🗿 Moai Protocol Verified — Build with Concrete.")
    st.markdown("""
    <div style="text-align:center; font-size:9px; color:#222; letter-spacing:2px; margin-top:10px;">
    ⚠ SIMULATION ONLY · NOT FINANCIAL ADVICE · DATA IS ILLUSTRATIVE · YIELDS SUBJECT TO CHANGE
    </div>
    """, unsafe_allow_html=True)
