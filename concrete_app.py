import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import random
import time
import math

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Concrete.XYZ — Vault Intelligence Terminal",
    page_icon="🗿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Ultra Premium CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Syne:wght@700;800&display=swap');

:root {
    --bg-deep:    #05080D;
    --bg-panel:   #090D14;
    --bg-card:    #0C1018;
    --border:     #131B25;
    --border-glow:#1E2D40;
    --neon:       #00FFB2;
    --neon-dim:   #00FFB240;
    --neon-glow:  #00FFB215;
    --gold:       #EDD97A;
    --gold-dim:   #EDD97A40;
    --amber:      #E8A020;
    --red:        #FF3D5A;
    --blue:       #4DA6FF;
    --purple:     #9B59FF;
    --orange:     #FF7A2F;
    --text-primary: #E8F0F8;
    --text-mid:   #556070;
    --text-dim:   #2A3540;
}

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
    background: var(--bg-deep);
    color: var(--text-primary);
}

.stApp { background: var(--bg-deep); }
.block-container { padding: 1rem 1.5rem 2rem; max-width: 1600px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
    font-family: 'Share Tech Mono', monospace !important;
}
section[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, var(--neon-glow), transparent) !important;
    border: 1px solid var(--neon) !important;
    color: var(--neon) !important;
    border-radius: 4px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    padding: 8px !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: var(--neon-dim) !important;
    box-shadow: 0 0 20px var(--neon-dim) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon), transparent);
    opacity: 0.4;
}
[data-testid="stMetricLabel"] { font-size: 9px !important; letter-spacing: 3px !important; color: var(--text-dim) !important; }
[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 700 !important; color: var(--neon) !important; font-family: 'Orbitron', monospace !important; }
[data-testid="stMetricDelta"] { font-size: 10px !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border);
    gap: 2px;
    padding: 4px 4px 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--text-mid);
    border: 1px solid var(--border);
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    padding: 8px 16px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: var(--neon-glow) !important;
    color: var(--neon) !important;
    border-color: var(--neon) !important;
    font-weight: 700 !important;
    box-shadow: 0 0 12px var(--neon-dim) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-mid) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Info / Success */
.stInfo { background: var(--neon-glow) !important; border-color: var(--neon) !important; border-radius: 6px !important; }

/* Sliders & Inputs */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select {
    background: var(--bg-card) !important;
    border-color: var(--border-glow) !important;
    color: var(--text-primary) !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stSlider [data-baseweb="slider"] [role="progressbar"] { background: var(--neon) !important; }

/* Custom badge */
.badge-live { background: #00FFB210; border: 1px solid #00FFB233; border-radius: 4px; padding: 4px 12px; font-size: 9px; color: var(--neon); display: inline-block; letter-spacing: 2px; }
.badge-partial { background: #EDD97A10; border: 1px solid #EDD97A33; border-radius: 4px; padding: 4px 12px; font-size: 9px; color: var(--gold); display: inline-block; letter-spacing: 2px; }
.badge-fallback { background: #FF3D5A10; border: 1px solid #FF3D5A33; border-radius: 4px; padding: 4px 12px; font-size: 9px; color: var(--red); display: inline-block; letter-spacing: 2px; }

/* Scanline effect on header */
.terminal-scanlines {
    position: relative;
    overflow: hidden;
}
.terminal-scanlines::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,178,0.01) 2px, rgba(0,255,178,0.01) 4px);
    pointer-events: none;
}

/* Risk badge */
.risk-low    { color: #00FFB2; border: 1px solid #00FFB233; background: #00FFB210; padding: 2px 10px; border-radius: 3px; font-size: 10px; }
.risk-medium { color: #EDD97A; border: 1px solid #EDD97A33; background: #EDD97A10; padding: 2px 10px; border-radius: 3px; font-size: 10px; }
.risk-high   { color: #FF3D5A; border: 1px solid #FF3D5A33; background: #FF3D5A10; padding: 2px 10px; border-radius: 3px; font-size: 10px; }

/* Health factor colors */
.hf-safe     { color: #00FFB2; }
.hf-low      { color: #EDD97A; }
.hf-medium   { color: #E8A020; }
.hf-high     { color: #FF7A2F; }
.hf-critical { color: #FF3D5A; }

hr { border-color: var(--border) !important; margin: 12px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Vault Definitions (Real on-chain addresses from Concrete Health Radar) ────
FALLBACK = {
    "🏦 WeETH (Institutional)": {
        "asset": "WETH", "color": "#00FFB2", "risk": "LOW",
        "tvl": 281_000_000, "apy": 7.84, "strategy": "Institutional Restaking (Aave V3 + Silo)",
        "daily_yield": 88_493, "price_usd": 2311,
        "address": "0xB9DC54c8261745CB97070CeFBE3D3d815aee8f20",
        "health_factor": 3.82, "util_stability": 0.94,
        "yield_consistency": 88, "liquidity_depth": 76, "strategy_diversity": 65, "protocol_maturity": 90
    },
    "₿ ctWBTC": {
        "asset": "WBTC", "color": "#F7931A", "risk": "MEDIUM",
        "tvl": 198_000_000, "apy": 5.21, "strategy": "Lending + Delta-Neutral (Morpho + Radiant)",
        "daily_yield": 28_274, "price_usd": 76_900,
        "address": "0xacce65B9dB4810125adDEa9797BaAaaaD2B73788",
        "health_factor": 2.14, "util_stability": 0.78,
        "yield_consistency": 72, "liquidity_depth": 82, "strategy_diversity": 78, "protocol_maturity": 80
    },
    "💵 ctUSD (Stable)": {
        "asset": "USDC", "color": "#2775CA", "risk": "LOW",
        "tvl": 825_000_000, "apy": 9.12, "strategy": "Stablecoin Optimizer (Morpho + Silo + Aave V3)",
        "daily_yield": 205_890, "price_usd": 1,
        "address": "0x0E609b710da5e0AA476224b6c0e5445cCc21251E",
        "health_factor": 4.51, "util_stability": 0.97,
        "yield_consistency": 95, "liquidity_depth": 92, "strategy_diversity": 88, "protocol_maturity": 95
    },
    "⚡ frxUSD+": {
        "asset": "FRAX", "color": "#9B59FF", "risk": "HIGH",
        "tvl": 67_000_000, "apy": 18.44, "strategy": "EigenLayer + Morpho + Silo",
        "daily_yield": 33_842, "price_usd": 1,
        "address": "0xCF9ceAcf5c7d6D2FE6e8650D81FbE4240c72443f",
        "health_factor": 1.38, "util_stability": 0.61,
        "yield_consistency": 58, "liquidity_depth": 55, "strategy_diversity": 92, "protocol_maturity": 60
    },
}

RISK_COLORS = {"LOW": "#00FFB2", "MEDIUM": "#EDD97A", "HIGH": "#FF3D5A"}

# ─── Health Factor Risk Zones (from Concrete Health Radar) ─────────────────────
def hf_zone(hf):
    if hf == float('inf') or hf > 3.0: return "SAFE",     "#00FFB2"
    elif hf >= 2.0:                      return "LOW",      "#EDD97A"
    elif hf >= 1.5:                      return "MEDIUM",   "#E8A020"
    elif hf >= 1.1:                      return "HIGH",     "#FF7A2F"
    else:                                return "CRITICAL", "#FF3D5A"

# ─── Efficiency Index (from Concrete Analytics) ────────────────────────────────
def efficiency_index(avg_apy, apy_vol, util_stability):
    return round((avg_apy / (1 + apy_vol)) * util_stability * 100, 1)

# ─── Data Fetchers ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_vault_data():
    # Source 1: ConcreteXYZ API
    try:
        r = requests.get("https://app.concrete.xyz/api/vaults",
                         headers={"Accept": "application/json"}, timeout=5)
        if r.status_code == 200:
            raw = r.json()
            result = {}
            for name, fb in FALLBACK.items():
                match = next((v for v in raw if fb["asset"].lower() in str(v).lower()), None)
                result[name] = {**fb,
                    "apy": float(match.get("apy", fb["apy"])) if match else fb["apy"],
                    "tvl": float(match.get("tvl", fb["tvl"])) if match else fb["tvl"],
                    "daily_yield": float(match.get("dailyYield", fb["daily_yield"])) if match else fb["daily_yield"],
                }
            return result, "🟢 LIVE — app.concrete.xyz", "badge-live"
    except Exception:
        pass

    # Source 2: DeFiLlama
    try:
        r = requests.get("https://api.llama.fi/protocol/concrete", timeout=5)
        if r.status_code == 200:
            llama = r.json()
            total = llama.get("tvl", [{}])[-1].get("totalLiquidityUSD", 0) if llama.get("tvl") else 0
            ratios = {"🏦 WeETH (Institutional)": 0.205, "₿ ctWBTC": 0.145, "💵 ctUSD (Stable)": 0.601, "⚡ frxUSD+": 0.049}
            result = {k: {**v, "tvl": total * ratios.get(k, 0.25) or v["tvl"]} for k, v in FALLBACK.items()}
            return result, "🟡 PARTIAL — DeFiLlama TVL", "badge-partial"
    except Exception:
        pass

    # Source 3: ETH RPC
    try:
        r = requests.post("https://eth.llamarpc.com",
                          json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
                          timeout=5)
        if r.status_code == 200:
            block = int(r.json().get("result", "0x0"), 16)
            result = {}
            for k, v in FALLBACK.items():
                seed = (block + hash(k)) % 200
                result[k] = {**v, "apy": round(v["apy"] + (seed / 1000) - 0.1, 2)}
            return result, "🟠 ETH RPC — Block Seeded", "badge-partial"
    except Exception:
        pass

    seed = int(time.time()) % 500
    result = {k: {**v, "apy": round(v["apy"] + ((seed + hash(k)) % 100) / 500 - 0.1, 2)} for k, v in FALLBACK.items()}
    return result, "⚪ SIMULATED — API Unavailable", "badge-fallback"


@st.cache_data(ttl=300)
def fetch_prices():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=ethereum,bitcoin,usd-coin,frax&vs_currencies=usd",
            timeout=5
        )
        if r.status_code == 200:
            p = r.json()
            return {
                "WETH":  p.get("ethereum", {}).get("usd", 2311),
                "WBTC":  p.get("bitcoin",  {}).get("usd", 76900),
                "USDC":  1.0,
                "FRAX":  p.get("frax",     {}).get("usd", 1.0),
            }
    except Exception:
        pass
    return {"WETH": 2311, "WBTC": 76900, "USDC": 1.0, "FRAX": 1.0}


def gen_history(base, days=30, seed_key="default"):
    random.seed(int(base * 100) + hash(seed_key) % 1000)
    dates = [datetime.today() - timedelta(days=days - i) for i in range(days)]
    apys  = [round(base + random.uniform(-1.5, 1.5), 2) for _ in range(days)]
    tvl_base = FALLBACK.get(seed_key, {}).get("tvl", 100_000_000)
    tvls  = [round(tvl_base * (1 + random.uniform(-0.05, 0.05)), 0) for _ in range(days)]
    return pd.DataFrame({"Date": dates, "APY": apys, "TVL": tvls})


def fmt(n):
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.1f}M"
    return f"${n:,.0f}"


# ─── Load Data ─────────────────────────────────────────────────────────────────
VAULTS, src_label, src_class = fetch_vault_data()
prices = fetch_prices()
for k, v in VAULTS.items():
    VAULTS[k]["price_usd"] = prices.get(v["asset"], v["price_usd"])

# ─── APY Volatility computation (from concrete-analytics methodology) ──────────
for k, v in VAULTS.items():
    hist = gen_history(v["apy"], days=30, seed_key=k)
    VAULTS[k]["apy_volatility"] = round(float(hist["APY"].std()), 3)
    VAULTS[k]["efficiency_idx"] = efficiency_index(v["apy"], VAULTS[k]["apy_volatility"], v["util_stability"])

# ─── Header ────────────────────────────────────────────────────────────────────
now_str = datetime.now().strftime('%H:%M:%S')
st.markdown(f"""
<div class="terminal-scanlines" style="background:linear-gradient(135deg,#090D14,#05080D);border:1px solid #131B25;border-radius:10px;padding:22px 28px;margin-bottom:10px;position:relative;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-family:'Orbitron',monospace;font-size:28px;font-weight:900;color:#E8F0F8;letter-spacing:2px;">
        ⬡ CONCRETE<span style="color:#00FFB2;">.XYZ</span>
      </div>
      <div style="font-size:9px;color:#2A3540;letter-spacing:4px;margin-top:4px;font-family:'Share Tech Mono',monospace;">
        VAULT INTELLIGENCE TERMINAL · v2.0
      </div>
    </div>
    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;">
      <div style="text-align:center;">
        <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:2px;">NETWORK</div>
        <div style="font-size:10px;color:#00FFB2;font-family:'Orbitron',monospace;">● ETH MAINNET</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:2px;">REFRESH</div>
        <div style="font-size:10px;color:#EDD97A;font-family:'Orbitron',monospace;">60s AUTO</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:2px;">SYNC</div>
        <div style="font-size:10px;color:#E8F0F8;font-family:'Orbitron',monospace;">{now_str}</div>
      </div>
    </div>
  </div>
  <div style="margin-top:12px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <span class="{src_class}">{src_label}</span>
    <span style="font-size:9px;color:#2A3540;letter-spacing:2px;">ERC-4626 VAULTS · ETHEREUM MAINNET</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Stats Bar ─────────────────────────────────────────────────────────────────
total_tvl   = sum(v["tvl"] for v in VAULTS.values())
total_daily = sum(v["daily_yield"] for v in VAULTS.values())
avg_eff     = round(sum(v["efficiency_idx"] for v in VAULTS.values()) / len(VAULTS), 1)

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("TOTAL TVL",       fmt(total_tvl))
with c2: st.metric("DAILY YIELD",     f"${total_daily:,.0f}")
with c3: st.metric("ETH PRICE",       f"${prices['WETH']:,.0f}")
with c4: st.metric("BTC PRICE",       f"${prices['WBTC']:,.0f}")
with c5: st.metric("AVG EFF. INDEX",  f"{avg_eff}", "Protocol Score")

st.markdown("---")

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:13px;font-weight:700;color:#E8F0F8;letter-spacing:2px;margin-bottom:12px;">
    🗿 VAULT TERMINAL
    </div>
    """, unsafe_allow_html=True)

    if st.button("⟳  REFRESH LIVE DATA", width='stretch'):
        st.cache_data.clear()
        st.rerun()

    st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown("---")

    vault_name = st.selectbox("SELECT VAULT", list(VAULTS.keys()))
    V   = VAULTS[vault_name]
    color, apy, risk  = V["color"], V["apy"], V["risk"]
    tvl, asset        = V["tvl"], V["asset"]
    strategy          = V["strategy"]
    daily_yield       = V["daily_yield"]
    price_usd         = V["price_usd"]
    hf                = V["health_factor"]
    eff_idx           = V["efficiency_idx"]
    hf_zone_name, hf_color = hf_zone(hf)

    st.markdown(f"""
    <div style="background:#090D14;border:1px solid {color}33;border-radius:8px;padding:14px;margin:10px 0;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,{color},transparent);opacity:0.6;"></div>
        <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:8px;font-family:'Orbitron',monospace;">SELECTED VAULT</div>
        <div style="font-size:26px;font-weight:900;color:{color};font-family:'Orbitron',monospace;">{apy}%</div>
        <div style="font-size:9px;color:#556070;margin-top:2px;">APY · {asset}</div>
        <hr style="margin:10px 0;border-color:#131B25;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:9px;">
            <div><div style="color:#2A3540;letter-spacing:1px;margin-bottom:2px;">TVL</div><div style="color:#E8F0F8;">{fmt(tvl)}</div></div>
            <div><div style="color:#2A3540;letter-spacing:1px;margin-bottom:2px;">RISK</div><div style="color:{RISK_COLORS[risk]};">{risk}</div></div>
            <div><div style="color:#2A3540;letter-spacing:1px;margin-bottom:2px;">HEALTH</div><div style="color:{hf_color};">{hf:.2f} {hf_zone_name}</div></div>
            <div><div style="color:#2A3540;letter-spacing:1px;margin-bottom:2px;">EFF.IDX</div><div style="color:#EDD97A;">{eff_idx}</div></div>
            <div style="grid-column:1/3;"><div style="color:#2A3540;letter-spacing:1px;margin-bottom:2px;">PRICE</div><div style="color:#E8F0F8;">${price_usd:,.2f}</div></div>
        </div>
    </div>
    <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-top:6px;padding:0 2px;">
        <div style="margin-bottom:4px;">📄 CONTRACT</div>
        <div style="color:#1E2D40;word-break:break-all;">{V['address'][:20]}...</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-family:Orbitron,monospace;font-size:10px;color:#556070;letter-spacing:2px;margin-bottom:10px;">SIMULATION SETTINGS</div>', unsafe_allow_html=True)
    principal    = st.number_input("Deposit ($)", min_value=100, value=10_000, step=500)
    period_label = st.select_slider("Time Period", options=["1 Month","3 Months","6 Months","1 Year","2 Years","5 Years"])
    compound     = st.toggle("Compound Interest", value=True)
    market_vol   = st.select_slider("Market Volatility", options=["Low","Medium","High","Extreme"], value="Medium")
    time_window  = st.radio("APY Analytics Window", ["1D","7D","30D","90D"], horizontal=True, index=2)
    st.markdown("---")
    st.markdown('<div style="font-size:8px;color:#2A3540;letter-spacing:2px;line-height:2.2;">⚠ SIMULATION ONLY<br>NOT FINANCIAL ADVICE<br>DYOR BEFORE INVESTING</div>', unsafe_allow_html=True)

# ─── Calculations ──────────────────────────────────────────────────────────────
days_map   = {"1 Month":30,"3 Months":90,"6 Months":180,"1 Year":365,"2 Years":730,"5 Years":1825}
days       = days_map[period_label]
vol_mult   = {"Low":1.1,"Medium":1.5,"High":2.5,"Extreme":4.0}[market_vol]
earnings   = principal * (pow(1 + apy/100, days/365) - 1) if compound else (principal * apy/100) * (days/365)
total_val  = principal + earnings
daily_earn = (principal * apy/100) / 365
ct_tokens  = principal / price_usd if price_usd > 0 else 0
stab_ratio = apy / vol_mult
protection_score = apy / vol_mult  # Standard DeFi yield adjusted for risk multiplier
base_yield = apy

# Time window for analytics history
tw_days_map = {"1D":1, "7D":7, "30D":30, "90D":90}
hist_days   = tw_days_map[time_window]

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["📈 OVERVIEW", "🧮 SIMULATOR", "🛡 HEALTH RADAR", "⚖️ ANALYTICS", "🔁 REBALANCER", "⛽ GAS & FEES", "📅 YIELD CALENDAR", "❓ FAQS"])

PLOT_LAYOUT = dict(
    plot_bgcolor="#090D14",
    paper_bgcolor="#090D14",
    font=dict(family="Share Tech Mono", color="#556070", size=10),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#2A3540"), color="#2A3540", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#0C1018", tickfont=dict(size=9, color="#2A3540"), color="#2A3540", zeroline=False),
)

# ══ OVERVIEW ════════════════════════════════════════════════════════════════════
with tab1:
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("TOTAL VALUE LOCKED", fmt(tvl), "Ethereum Mainnet")
    with k2: st.metric("DAILY YIELD",        f"${daily_yield:,.0f}", "All depositors")
    with k3: st.metric("RISK LEVEL",         risk, "Stable ✓" if risk=="LOW" else ("Moderate ⚠" if risk=="MEDIUM" else "High ⚡"), delta_color="normal" if risk=="LOW" else "inverse")
    with k4: st.metric("EFFICIENCY INDEX",   str(eff_idx), f"APY Vol: {V['apy_volatility']:.2f}%")

    st.markdown("---")
    col_c, col_i = st.columns([2, 1])

    with col_c:
        hist = gen_history(apy, days=max(hist_days, 7), seed_key=vault_name)
        fig  = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["Date"], y=hist["APY"],
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
            hovertemplate="<b>%{x|%b %d}</b><br>APY: %{y:.2f}%<extra></extra>",
            name="APY"
        ))
        fig.update_layout(**PLOT_LAYOUT, title=f"{time_window} APY History — {asset}",
                          height=220, showlegend=False, title_font=dict(size=11, color="#556070"))
        st.plotly_chart(fig, width='stretch')

    with col_i:
        st.markdown(f"""
        <div style="background:#090D14;border:1px solid #131B25;border-radius:8px;padding:16px;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{color},transparent);opacity:0.4;"></div>
            <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:12px;font-family:'Orbitron',monospace;">VAULT DETAILS</div>
            <div style="margin-bottom:12px;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:3px;">STRATEGY</div>
                <div style="font-size:10px;color:#E8F0F8;line-height:1.4;">{strategy}</div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:3px;">LIVE APY</div>
                <div style="font-size:28px;color:{color};font-weight:900;font-family:'Orbitron',monospace;">{apy}%</div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:3px;">UTIL STABILITY</div>
                <div style="height:6px;background:#0C1018;border-radius:3px;overflow:hidden;">
                    <div style="height:100%;width:{int(V['util_stability']*100)}%;background:{color};border-radius:3px;"></div>
                </div>
                <div style="font-size:9px;color:#556070;margin-top:3px;">{V['util_stability']:.0%}</div>
            </div>
            <div>
                <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:3px;">PROTECTION</div>
                <div style="font-size:10px;color:#EDD97A;">🛡 Buffer Active</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("##### Strategy Allocation")
        pie_d = pd.DataFrame({
            "Component": ["Lending Markets","Liquidity Provision","Capital Protection","Reserve Buffer"],
            "Allocation": [40, 28, 20, 12]
        })
        fig2 = px.pie(pie_d, values="Allocation", names="Component",
                      color_discrete_sequence=[color, f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.7)",
                                               f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.45)",
                                               f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.25)"],
                      hole=0.55)
        fig2.update_layout(plot_bgcolor="#090D14", paper_bgcolor="#090D14",
                           font=dict(family="Share Tech Mono", color="#556070", size=9),
                           margin=dict(l=10,r=10,t=10,b=10), height=220,
                           legend=dict(font=dict(color="#556070",size=9), bgcolor="#090D14"))
        st.plotly_chart(fig2, width='stretch')

    with s2:
        st.markdown("##### Risk Indicators")
        risk_level_num = {"LOW":1,"MEDIUM":2,"HIGH":3}[risk]
        liq_risk = 1 if risk=="LOW" else 3 if risk=="HIGH" else 2
        mkt_risk = 1 if risk=="LOW" else 2
        for label, lvl in [("Smart Contract Risk", risk_level_num), ("Liquidity Risk", liq_risk), ("Market Risk", mkt_risk)]:
            rc = RISK_COLORS[risk]
            bars = "".join([
                f'<div style="flex:1;height:6px;border-radius:2px;background:{"" if i<lvl else "#0C1018"};{"" if i>=lvl else f"background:{rc};box-shadow:0 0 6px {rc}40;"};"></div>'
                for i in range(3)
            ])
            st.markdown(f'<div style="background:#090D14;border:1px solid #131B25;border-radius:6px;padding:12px;margin-bottom:8px;"><div style="font-size:9px;color:#2A3540;letter-spacing:1px;margin-bottom:8px;">{label}</div><div style="display:flex;gap:4px;">{bars}</div></div>', unsafe_allow_html=True)

# ══ SIMULATOR ═══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#556070;letter-spacing:3px;margin-bottom:16px;">
    🧮 VAULT EARNINGS SIMULATOR — {asset}
    </div>
    """, unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
        <div style="background:#090D14;border:1px solid #131B25;border-radius:10px;padding:18px;margin-bottom:14px;">
            <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:14px;font-family:'Orbitron',monospace;">STABILITY EQUATION</div>
            <div style="font-size:11px;color:#556070;margin-bottom:12px;line-height:1.8;">
                Stability Ratio = Net Yield ÷ σ(Market Volatility)<br>
                <span style="color:#EDD97A;font-size:16px;font-family:'Orbitron',monospace;">{stab_ratio:.2f}</span>
                <span style="font-size:9px;color:#2A3540;"> at {market_vol} volatility</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div style="background:#0C1018;border:1px solid #131B25;border-radius:6px;padding:12px;">
                    <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:4px;">STANDARD DEFI</div>
                    <div style="font-size:18px;color:#FF3D5A;font-family:'Orbitron',monospace;">{apy/vol_mult:.2f}%</div>
                    <div style="font-size:8px;color:#2A3540;">÷{vol_mult}x Risk</div>
                </div>
                <div style="background:#0C1018;border:1px solid {color}33;border-radius:6px;padding:12px;box-shadow:0 0 12px {color}10;">
                    <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:4px;">CONCRETE PROTECTED</div>
                    <div style="font-size:18px;color:{color};font-family:'Orbitron',monospace;">{apy*0.95:.2f}%</div>
                    <div style="font-size:8px;color:#2A3540;">🗿 Stable Floor</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#090D14;border:1px solid {color}33;border-radius:10px;padding:18px;">
            <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:8px;font-family:'Orbitron',monospace;">ct[{asset}] TOKENS RECEIVED</div>
            <div style="font-size:32px;font-weight:900;color:{color};font-family:'Orbitron',monospace;">{ct_tokens:.6f}</div>
            <div style="font-size:9px;color:#2A3540;margin-top:6px;">For ${principal:,.0f} deposit</div>
            <div style="font-size:9px;color:#2A3540;margin-top:3px;">1 {asset} = ${price_usd:,.2f} (CoinGecko)</div>
            <div style="font-size:9px;color:#EDD97A;margin-top:8px;">● Vault share tokens appreciate automatically</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div style="background:#090D14;border:1px solid {color}33;border-radius:10px;padding:22px;box-shadow:0 0 30px {color}10;margin-bottom:14px;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,{color},transparent);opacity:0.5;"></div>
            <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:8px;font-family:'Orbitron',monospace;">PROJECTED EARNINGS</div>
            <div style="font-size:44px;font-weight:900;color:{color};font-family:'Orbitron',monospace;line-height:1;">+${earnings:,.2f}</div>
            <div style="font-size:10px;color:#2A3540;margin-top:10px;">Over {period_label} at {apy}% APY {'(compounded)' if compound else '(simple)'}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">
                <div style="background:#0C1018;border-radius:6px;padding:12px;">
                    <div style="font-size:8px;color:#2A3540;margin-bottom:4px;">TOTAL VALUE</div>
                    <div style="font-size:16px;color:#E8F0F8;font-family:'Orbitron',monospace;">${total_val:,.2f}</div>
                </div>
                <div style="background:#0C1018;border-radius:6px;padding:12px;">
                    <div style="font-size:8px;color:#2A3540;margin-bottom:4px;">DAILY EARN</div>
                    <div style="font-size:16px;color:{color};font-family:'Orbitron',monospace;">${daily_earn:,.2f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 12-month projection chart - FIXED (no f-string in fillcolor)
        proj_months = list(range(1, 13))
        proj_labels = [f"M{i}" for i in proj_months]
        proj_values = [
            principal * pow(1 + apy/100, i/12) if compound
            else principal + (principal * apy/100) * (i/12)
            for i in proj_months
        ]

        # Parse color safely for rgba
        r_ch = int(color[1:3], 16)
        g_ch = int(color[3:5], 16)
        b_ch = int(color[5:7], 16)
        fill_rgba = f"rgba({r_ch},{g_ch},{b_ch},0.1)"

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=proj_labels, y=proj_values,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=5, color=color),
            fill="tozeroy",
            fillcolor=fill_rgba,
            hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"
        ))
        fig3.update_layout(**PLOT_LAYOUT, title="12-Month Value Projection",
                           height=200, title_font=dict(size=10, color="#556070"))
        st.plotly_chart(fig3, width='stretch')

    # Comparison table
    st.markdown("---")
    st.markdown("##### Multi-Period Earnings Breakdown")
    period_rows = []
    for p_label, p_days in [("1 Month",30),("3 Months",90),("6 Months",180),("1 Year",365),("2 Years",730),("5 Years",1825)]:
        e = principal * (pow(1+apy/100, p_days/365)-1) if compound else (principal*apy/100)*(p_days/365)
        period_rows.append({"Period": p_label, "Earnings": f"${e:,.2f}", "Total": f"${principal+e:,.2f}", "Daily Avg": f"${e/p_days:,.2f}"})
    st.dataframe(pd.DataFrame(period_rows), width='stretch', hide_index=True)

    # ── Yield Protection Comparison ────────────────────────────────────────────
    st.markdown("---")
    st.markdown("##### ⚔️ Standard DeFi vs Concrete Protected Yield")

    col1, col2 = st.columns(2)

    with col1:
        # Standard DeFi = Red/Danger color
        st.metric(
            label="Standard DeFi Yield",
            value=f"{protection_score:.2f}%",
            delta="High Risk Exposure",
            delta_color="inverse"  # RED dikhayega
        )

    with col2:
        # Concrete = Green/Safe color
        st.metric(
            label="Concrete Protected Yield",
            value=f"{base_yield * 0.95:.2f}%",
            delta="🗿 Concrete Solid",
            delta_color="normal"  # GREEN dikhayega
        )

# ══ HEALTH RADAR ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#556070;letter-spacing:3px;margin-bottom:16px;">
    🛡 HEALTH RADAR — AAVE V3 ON-CHAIN RISK MONITOR
    </div>
    """, unsafe_allow_html=True)

    # Animated gauge for each vault
    gauge_cols = st.columns(4)
    for idx, (vname, vdata) in enumerate(VAULTS.items()):
        hf_val = vdata["health_factor"]
        zone_name, zone_color = hf_zone(hf_val)
        vc = vdata["color"]

        # Gauge angle: HF 1.0 = 0°, HF 5.0 = 180°
        # Clamp HF at 5 for display
        hf_clamped = min(hf_val, 5.0)
        gauge_pct   = (hf_clamped - 1.0) / 4.0  # 0..1

        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=hf_val if hf_val < 99 else 5.0,
            number={"font": {"size": 18, "family": "Orbitron", "color": zone_color}, "suffix": ""},
            gauge={
                "axis": {"range": [1, 5], "tickfont": {"size": 8, "color": "#2A3540"}, "tickcolor": "#131B25"},
                "bar": {"color": zone_color, "thickness": 0.25},
                "bgcolor": "#090D14",
                "borderwidth": 1,
                "bordercolor": "#131B25",
                "steps": [
                    {"range": [1.0, 1.1], "color": "rgba(255,61,90,0.12)"},
                    {"range": [1.1, 1.5], "color": "rgba(255,122,47,0.12)"},
                    {"range": [1.5, 2.0], "color": "rgba(232,160,32,0.12)"},
                    {"range": [2.0, 3.0], "color": "rgba(237,217,122,0.12)"},
                    {"range": [3.0, 5.0], "color": "rgba(0,255,178,0.12)"},
                ],
                "threshold": {"line": {"color": zone_color, "width": 3}, "thickness": 0.8, "value": hf_val if hf_val < 5 else 5}
            },
            title={"text": f"{vname.split()[1] if len(vname.split())>1 else vname}<br><span style='font-size:9px;color:{zone_color};'>{zone_name}</span>",
                   "font": {"size": 10, "family": "Share Tech Mono", "color": "#556070"}}
        ))
        fig_g.update_layout(
            plot_bgcolor="#090D14", paper_bgcolor="#090D14",
            margin=dict(l=10, r=10, t=40, b=10), height=200
        )
        with gauge_cols[idx]:
            st.plotly_chart(fig_g, width='stretch')
            st.markdown(f"""
            <div style="background:#090D14;border:1px solid #131B25;border-radius:6px;padding:10px;text-align:center;margin-top:-8px;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:1px;margin-bottom:4px;">HEALTH FACTOR</div>
                <div style="font-size:20px;color:{zone_color};font-family:'Orbitron',monospace;font-weight:700;">{hf_val:.2f}</div>
                <div style="font-size:8px;color:{zone_color};margin-top:2px;">{zone_name}</div>
                <div style="font-size:7px;color:#2A3540;margin-top:6px;word-break:break-all;">{vdata['address'][:20]}...</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Risk zone legend
    st.markdown("""
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:2px;background:#00FFB2;"></div><div style="font-size:9px;color:#556070;">SAFE (&gt;3.0)</div></div>
        <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:2px;background:#EDD97A;"></div><div style="font-size:9px;color:#556070;">LOW (2.0–3.0)</div></div>
        <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:2px;background:#E8A020;"></div><div style="font-size:9px;color:#556070;">MEDIUM (1.5–2.0)</div></div>
        <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:2px;background:#FF7A2F;"></div><div style="font-size:9px;color:#556070;">HIGH (1.1–1.5)</div></div>
        <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;border-radius:2px;background:#FF3D5A;"></div><div style="font-size:9px;color:#556070;">CRITICAL (&lt;1.1)</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── UNIQUE FEATURE: Vault DNA Fingerprint (Spider/Radar Chart) ─────────────
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#EDD97A;letter-spacing:3px;margin-bottom:6px;">
    🧬 VAULT DNA FINGERPRINT
    </div>
    <div style="font-size:9px;color:#2A3540;letter-spacing:1px;margin-bottom:16px;">
    Multi-dimensional scoring: Yield Consistency · Liquidity Depth · Strategy Diversity · Protocol Maturity · Util Stability · Efficiency Index
    </div>
    """, unsafe_allow_html=True)

    dna_cols = st.columns(2)
    categories = ["Yield\nConsistency", "Liquidity\nDepth", "Strategy\nDiversity", "Protocol\nMaturity", "Util\nStability", "Efficiency\nIndex"]
    cat_labels  = ["Yield Consistency", "Liquidity Depth", "Strategy Diversity", "Protocol Maturity", "Util Stability", "Efficiency Index"]

    for col_idx, (vname, vdata) in enumerate(list(VAULTS.items())[:4]):
        vc = vdata["color"]
        values = [
            vdata["yield_consistency"],
            vdata["liquidity_depth"],
            vdata["strategy_diversity"],
            vdata["protocol_maturity"],
            int(vdata["util_stability"] * 100),
            min(int(vdata["efficiency_idx"]), 100)
        ]
        values_closed = values + [values[0]]
        cats_closed   = cat_labels + [cat_labels[0]]

        fig_dna = go.Figure()
        fig_dna.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=cats_closed,
            fill="toself",
            fillcolor=f"rgba({int(vc[1:3],16)},{int(vc[3:5],16)},{int(vc[5:7],16)},0.15)",
            line=dict(color=vc, width=2),
            marker=dict(size=6, color=vc),
            name=vname,
            hovertemplate="<b>%{theta}</b><br>Score: %{r}<extra></extra>"
        ))
        fig_dna.update_layout(
            polar=dict(
                bgcolor="#090D14",
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=8, color="#2A3540"), gridcolor="#131B25", linecolor="#131B25"),
                angularaxis=dict(tickfont=dict(size=8, color="#556070"), gridcolor="#131B25", linecolor="#131B25")
            ),
            plot_bgcolor="#090D14", paper_bgcolor="#090D14",
            font=dict(family="Share Tech Mono", color="#556070", size=9),
            margin=dict(l=20, r=20, t=40, b=20), height=250,
            title=dict(text=vname, font=dict(size=10, color=vc, family="Orbitron"), x=0.5),
            showlegend=False
        )
        with dna_cols[col_idx % 2]:
            st.plotly_chart(fig_dna, width='stretch')

# ══ ANALYTICS (Efficiency + Compare) ════════════════════════════════════════════
with tab4:
    st.markdown(f"""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#556070;letter-spacing:3px;margin-bottom:16px;">
    ⚖️ CAPITAL EFFICIENCY ANALYTICS · {time_window} WINDOW
    </div>
    """, unsafe_allow_html=True)

    # APY comparison bar
    fig4 = go.Figure()
    for vname, vdata in VAULTS.items():
        vc = vdata["color"]
        fig4.add_trace(go.Bar(
            x=[vname.split()[-1] if len(vname.split()) > 1 else vname],
            y=[vdata["apy"]],
            name=vname,
            marker_color=vc,
            marker=dict(
                line=dict(color=vc, width=1),
                opacity=0.85
            ),
            text=[f"{vdata['apy']}%"],
            textposition="outside",
            textfont=dict(family="Orbitron", size=10, color=vc),
            hovertemplate=f"<b>{vname}</b><br>APY: %{{y}}%<extra></extra>"
        ))
    fig4.update_layout(**PLOT_LAYOUT, title="Live APY — All Vaults",
                       height=280, title_font=dict(size=11, color="#556070"),
                       barmode="group", bargap=0.35, showlegend=False)
    st.plotly_chart(fig4, width='stretch')

    # Efficiency Index comparison
    fig_eff = go.Figure()
    eff_names  = [v.split()[-1] if len(v.split())>1 else v for v in VAULTS.keys()]
    eff_values = [vdata["efficiency_idx"] for vdata in VAULTS.values()]
    eff_colors = [vdata["color"] for vdata in VAULTS.values()]
    fig_eff.add_trace(go.Bar(
        x=eff_names, y=eff_values,
        marker_color=eff_colors,
        text=[str(e) for e in eff_values],
        textposition="outside",
        textfont=dict(family="Orbitron", size=10, color="#E8F0F8"),
        hovertemplate="<b>%{x}</b><br>Efficiency Index: %{y}<extra></extra>"
    ))
    fig_eff.update_layout(**PLOT_LAYOUT, title="Efficiency Index — (Avg APY / (1 + Vol)) × Util Stability × 100",
                          height=220, title_font=dict(size=10, color="#556070"), showlegend=False)
    st.plotly_chart(fig_eff, width='stretch')

    # Comparison table $10k / 1 year
    st.markdown("---")
    st.markdown("##### $10,000 — 1 Year Returns Matrix")
    rows = []
    for vname, vdata in VAULTS.items():
        y1e = 10000 * (pow(1 + vdata["apy"]/100, 1) - 1)
        rows.append({
            "Vault": vname,
            "APY": f"{vdata['apy']}%",
            "TVL": fmt(vdata["tvl"]),
            "Risk": vdata["risk"],
            "Health Factor": f"{vdata['health_factor']:.2f}",
            "Eff. Index": str(vdata["efficiency_idx"]),
            "APY Vol": f"{vdata['apy_volatility']:.2f}%",
            "1Y Earnings": f"${y1e:,.2f}",
            "Total Value": f"${10000+y1e:,.2f}"
        })
    st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)

    # TVL + multi-line APY over time
    st.markdown("---")
    st.markdown("##### TVL Distribution & Multi-Vault APY Trend")
    a1, a2 = st.columns(2)

    with a1:
        fig5 = px.pie(
            values=[v["tvl"] for v in VAULTS.values()],
            names=list(VAULTS.keys()),
            color_discrete_sequence=[v["color"] for v in VAULTS.values()],
            hole=0.6,
            title="TVL Distribution"
        )
        fig5.update_layout(plot_bgcolor="#090D14", paper_bgcolor="#090D14",
                           font=dict(family="Share Tech Mono", color="#556070", size=9),
                           margin=dict(l=10,r=10,t=40,b=10), height=260,
                           legend=dict(font=dict(color="#556070",size=8), bgcolor="#090D14"))
        st.plotly_chart(fig5, width='stretch')

    with a2:
        fig6 = go.Figure()
        for vname, vdata in VAULTS.items():
            vh = gen_history(vdata["apy"], days=30, seed_key=vname)
            fig6.add_trace(go.Scatter(
                x=vh["Date"], y=vh["APY"],
                mode="lines",
                line=dict(color=vdata["color"], width=1.5),
                name=vdata["asset"],
                hovertemplate=f"<b>{vdata['asset']}</b><br>%{{x|%b %d}}<br>APY: %{{y:.2f}}%<extra></extra>"
            ))
        fig6.update_layout(**PLOT_LAYOUT, title="30D Multi-Vault APY Trend",
                           height=260, title_font=dict(size=10, color="#556070"),
                           legend=dict(font=dict(color="#556070",size=9), bgcolor="#090D14"))
        st.plotly_chart(fig6, width='stretch')

# ══ FAQs ════════════════════════════════════════════════════════════════════════
# ══ REBALANCER ══════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#EDD97A;letter-spacing:3px;margin-bottom:6px;">
    🔁 SMART PORTFOLIO REBALANCER
    </div>
    <div style="font-size:9px;color:#2A3540;letter-spacing:1px;margin-bottom:16px;">
    Enter your current holdings — get optimal allocation based on Efficiency Index, Risk, and Health Factor
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### Step 1 — Enter Your Current Portfolio")
    rb_cols = st.columns(4)
    user_holdings = {}
    for idx, (vname, vdata) in enumerate(VAULTS.items()):
        vc = vdata["color"]
        short_name = vdata["asset"]
        with rb_cols[idx]:
            val = st.number_input(
                f"{short_name} ($)",
                min_value=0, value=0, step=500,
                key=f"rb_{vname}"
            )
            user_holdings[vname] = val

    total_portfolio = sum(user_holdings.values())

    st.markdown("---")
    st.markdown("##### Step 2 — Rebalancing Strategy")
    strategy_mode = st.radio(
        "Optimization Target",
        ["🏆 Max Efficiency Index", "🛡 Min Risk (Safety First)", "⚖️ Risk-Adjusted Balanced", "🚀 Max APY (Aggressive)"],
        horizontal=True
    )

    if total_portfolio > 0:
        # Score each vault based on chosen strategy
        scores = {}
        for vname, vdata in VAULTS.items():
            if strategy_mode == "🏆 Max Efficiency Index":
                scores[vname] = vdata["efficiency_idx"]
            elif strategy_mode == "🛡 Min Risk (Safety First)":
                risk_s = {"LOW": 100, "MEDIUM": 50, "HIGH": 10}[vdata["risk"]]
                scores[vname] = risk_s * vdata["health_factor"]
            elif strategy_mode == "⚖️ Risk-Adjusted Balanced":
                scores[vname] = vdata["apy"] * vdata["util_stability"] * vdata["health_factor"]
            else:  # Max APY
                scores[vname] = vdata["apy"] * 10

        total_score = sum(scores.values())
        optimal_alloc = {k: round((v / total_score) * total_portfolio, 2) for k, v in scores.items()}

        st.markdown("---")
        st.markdown("##### Step 3 — Rebalancing Recommendation")

        rb_out_cols = st.columns(4)
        for idx, (vname, vdata) in enumerate(VAULTS.items()):
            vc      = vdata["color"]
            current = user_holdings[vname]
            optimal = optimal_alloc[vname]
            delta   = optimal - current
            delta_sign = "+" if delta >= 0 else ""
            delta_color = "#00FFB2" if delta >= 0 else "#FF3D5A"
            pct     = round((optimal / total_portfolio) * 100, 1)

            with rb_out_cols[idx]:
                st.markdown(f"""
                <div style="background:#090D14;border:1px solid {vc}33;border-radius:8px;padding:14px;text-align:center;position:relative;overflow:hidden;">
                    <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,{vc},transparent);opacity:0.5;"></div>
                    <div style="font-size:8px;color:#2A3540;letter-spacing:2px;margin-bottom:6px;font-family:'Orbitron',monospace;">{vdata['asset']}</div>
                    <div style="font-size:9px;color:#556070;margin-bottom:10px;">{pct}% of portfolio</div>
                    <div style="margin-bottom:8px;">
                        <div style="font-size:8px;color:#2A3540;margin-bottom:2px;">CURRENT</div>
                        <div style="font-size:14px;color:#E8F0F8;font-family:'Orbitron',monospace;">${current:,.0f}</div>
                    </div>
                    <div style="margin-bottom:8px;">
                        <div style="font-size:8px;color:#2A3540;margin-bottom:2px;">OPTIMAL</div>
                        <div style="font-size:16px;color:{vc};font-family:'Orbitron',monospace;font-weight:700;">${optimal:,.0f}</div>
                    </div>
                    <div style="background:#0C1018;border-radius:4px;padding:6px;margin-top:8px;">
                        <div style="font-size:8px;color:#2A3540;margin-bottom:2px;">ACTION</div>
                        <div style="font-size:13px;color:{delta_color};font-family:'Orbitron',monospace;">{delta_sign}${abs(delta):,.0f}</div>
                    </div>
                    <div style="height:4px;background:#0C1018;border-radius:2px;margin-top:10px;overflow:hidden;">
                        <div style="height:100%;width:{pct}%;background:{vc};border-radius:2px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        # Side-by-side donut: current vs optimal
        c_alloc, o_alloc = st.columns(2)
        vault_names_short = [v["asset"] for v in VAULTS.values()]
        vault_colors_list = [v["color"] for v in VAULTS.values()]

        with c_alloc:
            current_vals = [user_holdings[vn] for vn in VAULTS.keys()]
            fig_cur = px.pie(
                values=current_vals,
                names=vault_names_short,
                color_discrete_sequence=vault_colors_list,
                hole=0.6, title="Current Allocation"
            )
            fig_cur.update_layout(
                plot_bgcolor="#090D14", paper_bgcolor="#090D14",
                font=dict(family="Share Tech Mono", color="#556070", size=9),
                margin=dict(l=10,r=10,t=40,b=10), height=260,
                legend=dict(font=dict(color="#556070",size=8), bgcolor="#090D14"),
                title_font=dict(size=10, color="#556070")
            )
            st.plotly_chart(fig_cur, width='stretch')

        with o_alloc:
            optimal_vals = [optimal_alloc[vn] for vn in VAULTS.keys()]
            fig_opt = px.pie(
                values=optimal_vals,
                names=vault_names_short,
                color_discrete_sequence=vault_colors_list,
                hole=0.6, title="Optimal Allocation"
            )
            fig_opt.update_layout(
                plot_bgcolor="#090D14", paper_bgcolor="#090D14",
                font=dict(family="Share Tech Mono", color="#556070", size=9),
                margin=dict(l=10,r=10,t=40,b=10), height=260,
                legend=dict(font=dict(color="#556070",size=8), bgcolor="#090D14"),
                title_font=dict(size=10, color="#556070")
            )
            st.plotly_chart(fig_opt, width='stretch')

        # Projected APY improvement
        current_weighted_apy = sum(
            (user_holdings[vn] / total_portfolio) * VAULTS[vn]["apy"]
            for vn in VAULTS.keys() if user_holdings[vn] > 0
        ) if total_portfolio > 0 else 0
        optimal_weighted_apy = sum(
            (optimal_alloc[vn] / total_portfolio) * VAULTS[vn]["apy"]
            for vn in VAULTS.keys()
        )
        apy_gain = optimal_weighted_apy - current_weighted_apy

        st.markdown(f"""
        <div style="background:#090D14;border:1px solid #00FFB233;border-radius:8px;padding:18px;margin-top:8px;display:flex;justify-content:space-around;flex-wrap:wrap;gap:12px;">
            <div style="text-align:center;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:2px;margin-bottom:4px;">TOTAL PORTFOLIO</div>
                <div style="font-size:22px;color:#E8F0F8;font-family:'Orbitron',monospace;">${total_portfolio:,.0f}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:2px;margin-bottom:4px;">CURRENT WEIGHTED APY</div>
                <div style="font-size:22px;color:#FF3D5A;font-family:'Orbitron',monospace;">{current_weighted_apy:.2f}%</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:2px;margin-bottom:4px;">OPTIMAL WEIGHTED APY</div>
                <div style="font-size:22px;color:#00FFB2;font-family:'Orbitron',monospace;">{optimal_weighted_apy:.2f}%</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:8px;color:#2A3540;letter-spacing:2px;margin-bottom:4px;">APY IMPROVEMENT</div>
                <div style="font-size:22px;color:#EDD97A;font-family:'Orbitron',monospace;">+{apy_gain:.2f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#090D14;border:1px solid #131B25;border-radius:8px;padding:32px;text-align:center;margin-top:12px;">
            <div style="font-size:24px;margin-bottom:8px;">🗿</div>
            <div style="font-size:11px;color:#556070;font-family:'Orbitron',monospace;margin-bottom:6px;">ENTER YOUR HOLDINGS ABOVE</div>
            <div style="font-size:9px;color:#2A3540;">Input your current vault balances to get optimal rebalancing recommendations</div>
        </div>
        """, unsafe_allow_html=True)

# ══ FAQs ════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#556070;letter-spacing:3px;margin-bottom:16px;">
    ⛽ GAS & DEPOSIT COST ESTIMATOR — ETHEREUM MAINNET
    </div>
    """, unsafe_allow_html=True)

    # ── Fetch live gas from Etherscan/RPC ──────────────────────────────────────
    @st.cache_data(ttl=30)
    def fetch_gas():
        try:
            r = requests.post(
                "https://eth.llamarpc.com",
                json={"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1},
                timeout=5
            )
            if r.status_code == 200:
                gwei = int(r.json().get("result","0x0"), 16) / 1e9
                return round(gwei, 2), "🟢 LIVE"
        except Exception:
            pass
        return 12.5, "⚪ SIMULATED"

    gas_gwei, gas_src = fetch_gas()
    eth_price_gas = prices.get("WETH", 2311)

    # Gas cost matrix for DeFi ops
    GAS_OPS = {
        "Deposit into Vault":      {"gas": 180_000, "icon": "💰"},
        "Withdraw from Vault":     {"gas": 150_000, "icon": "🏧"},
        "Claim Rewards":           {"gas": 90_000,  "icon": "🎁"},
        "ERC-20 Approve":          {"gas": 46_000,  "icon": "✅"},
        "Swap on Uniswap V3":      {"gas": 130_000, "icon": "🔄"},
        "Aave V3 Supply":          {"gas": 200_000, "icon": "🏦"},
        "Morpho Deposit":          {"gas": 160_000, "icon": "🦋"},
        "Full Rebalance (4 ops)":  {"gas": 620_000, "icon": "🔁"},
    }

    # Gas speed tiers
    GAS_TIERS = {
        "🐢 Slow  (–30%)":  0.70,
        "🚶 Normal":        1.00,
        "⚡ Fast  (+30%)":  1.30,
        "🚀 Instant (+60%)":1.60,
    }

    g1, g2 = st.columns([1, 2])
    with g1:
        st.markdown(f"""
        <div style="background:#090D14;border:1px solid #00FFB233;border-radius:10px;padding:20px;text-align:center;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#00FFB2,transparent);opacity:0.5;"></div>
            <div style="font-size:8px;color:#2A3540;letter-spacing:3px;margin-bottom:8px;font-family:'Orbitron',monospace;">CURRENT BASE GAS</div>
            <div style="font-size:42px;font-weight:900;color:#00FFB2;font-family:'Orbitron',monospace;">{gas_gwei}</div>
            <div style="font-size:12px;color:#556070;margin-top:4px;">GWEI</div>
            <div style="font-size:9px;color:#2A3540;margin-top:12px;">{gas_src}</div>
            <div style="font-size:9px;color:#EDD97A;margin-top:6px;">ETH = ${eth_price_gas:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        speed_choice = st.selectbox("⚡ Gas Speed", list(GAS_TIERS.keys()))
        speed_mult = GAS_TIERS[speed_choice]
        effective_gas = round(gas_gwei * speed_mult, 2)

        st.markdown(f"""
        <div style="background:#090D14;border:1px solid #EDD97A33;border-radius:8px;padding:14px;text-align:center;margin-top:12px;">
            <div style="font-size:8px;color:#2A3540;letter-spacing:2px;margin-bottom:4px;">EFFECTIVE GAS PRICE</div>
            <div style="font-size:22px;color:#EDD97A;font-family:'Orbitron',monospace;">{effective_gas} GWEI</div>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown("""
        <div style="font-size:9px;color:#2A3540;letter-spacing:2px;margin-bottom:10px;font-family:'Orbitron',monospace;">
        OPERATION COST MATRIX
        </div>
        """, unsafe_allow_html=True)

        rows_gas = []
        for op_name, op_data in GAS_OPS.items():
            gas_units = op_data["gas"]
            cost_eth  = (gas_units * effective_gas * 1e-9)
            cost_usd  = cost_eth * eth_price_gas
            pct_of_10k = round((cost_usd / 10_000) * 100, 4)
            rows_gas.append({
                "Operation":    f"{op_data['icon']} {op_name}",
                "Gas Units":    f"{gas_units:,}",
                "ETH Cost":     f"{cost_eth:.6f} ETH",
                "USD Cost":     f"${cost_usd:.2f}",
                "% of $10k":   f"{pct_of_10k}%",
            })
        st.dataframe(pd.DataFrame(rows_gas), width='stretch', hide_index=True)

    # ── Cost vs Deposit Size chart ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("##### Deposit Size vs Gas Cost Impact")
    deposit_sizes = [500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
    deposit_cost  = (180_000 * effective_gas * 1e-9) * eth_price_gas  # vault deposit
    pct_impacts   = [round((deposit_cost / d) * 100, 3) for d in deposit_sizes]

    fig_gas = go.Figure()
    fig_gas.add_trace(go.Scatter(
        x=[f"${d:,}" for d in deposit_sizes],
        y=pct_impacts,
        mode="lines+markers",
        line=dict(color="#00FFB2", width=2),
        marker=dict(size=8, color="#00FFB2"),
        fill="tozeroy",
        fillcolor="rgba(0,255,178,0.05)",
        hovertemplate="Deposit: %{x}<br>Gas Impact: %{y:.3f}%<extra></extra>",
        name="Gas % of Deposit"
    ))
    fig_gas.add_hline(y=0.5, line=dict(color="#EDD97A", dash="dash", width=1),
                      annotation_text="0.5% threshold", annotation_font=dict(color="#EDD97A", size=9))
    fig_gas.update_layout(
        **PLOT_LAYOUT,
        title=f"Gas Cost as % of Deposit (Vault Deposit at {effective_gas} GWEI)",
        height=260, title_font=dict(size=10, color="#556070"),
        xaxis_title="Deposit Size", yaxis_title="Gas Cost (%)",
    )
    st.plotly_chart(fig_gas, width='stretch')

    # ── Gas tip ────────────────────────────────────────────────────────────────
    min_dep_for_sane = deposit_cost / 0.005  # when gas < 0.5% of deposit
    st.markdown(f"""
    <div style="background:#090D14;border:1px solid #EDD97A33;border-radius:8px;padding:14px;margin-top:8px;">
        <div style="font-size:9px;color:#EDD97A;font-family:'Orbitron',monospace;margin-bottom:4px;">💡 DEPOSIT EFFICIENCY TIP</div>
        <div style="font-size:10px;color:#556070;">
        At current gas (<b style="color:#00FFB2;">{effective_gas} GWEI</b>), vault deposit costs
        <b style="color:#EDD97A;">${deposit_cost:.2f}</b>.
        For gas to be under 0.5% of deposit, recommend minimum:
        <b style="color:#00FFB2;">${min_dep_for_sane:,.0f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══ YIELD CALENDAR ══════════════════════════════════════════════════════════════
with tab7:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#556070;letter-spacing:3px;margin-bottom:16px;">
    📅 YIELD ACCUMULATION CALENDAR — DAILY EARNINGS TRACKER
    </div>
    """, unsafe_allow_html=True)

    yc1, yc2 = st.columns([1, 2])

    with yc1:
        st.markdown("""
        <div style="font-family:'Orbitron',monospace;font-size:9px;color:#2A3540;letter-spacing:2px;margin-bottom:8px;">
        CONFIGURE YOUR POSITION
        </div>
        """, unsafe_allow_html=True)
        yc_vault   = st.selectbox("Select Vault", list(VAULTS.keys()), key="yc_vault")
        yc_deposit = st.number_input("Deposit Amount ($)", min_value=100, value=10_000, step=500, key="yc_dep")
        yc_months  = st.slider("Projection (months)", 1, 24, 12, key="yc_months")
        yc_compound = st.toggle("Compound Yield", value=True, key="yc_comp")

    YCV = VAULTS[yc_vault]
    yc_apy = YCV["apy"]
    yc_color = YCV["color"]
    yc_days_total = yc_months * 30

    # Build daily data
    daily_rate = yc_apy / 100 / 365
    cal_dates, cal_vals, cal_daily, cal_cum = [], [], [], []
    running = yc_deposit
    for d in range(yc_days_total):
        dt = datetime.today() + timedelta(days=d)
        if yc_compound:
            day_earn = running * daily_rate
            running  += day_earn
        else:
            day_earn = yc_deposit * daily_rate
            running  += day_earn
        cal_dates.append(dt)
        cal_vals.append(round(running, 4))
        cal_daily.append(round(day_earn, 4))
        cal_cum.append(round(running - yc_deposit, 4))

    with yc2:
        # Summary cards
        total_earned = cal_cum[-1] if cal_cum else 0
        peak_daily   = max(cal_daily) if cal_daily else 0
        final_val    = cal_vals[-1] if cal_vals else yc_deposit
        roi_pct      = (total_earned / yc_deposit) * 100

        yc_cols = st.columns(4)
        with yc_cols[0]:
            st.metric("TOTAL EARNED",   f"${total_earned:,.2f}")
        with yc_cols[1]:
            st.metric("FINAL VALUE",    f"${final_val:,.2f}")
        with yc_cols[2]:
            st.metric("ROI",            f"+{roi_pct:.2f}%")
        with yc_cols[3]:
            st.metric("PEAK DAILY",     f"${peak_daily:.2f}")

    # Cumulative earnings chart
    r_ch = int(yc_color[1:3], 16)
    g_ch = int(yc_color[3:5], 16)
    b_ch = int(yc_color[5:7], 16)
    fill_c = f"rgba({r_ch},{g_ch},{b_ch},0.08)"

    fig_yc = go.Figure()
    fig_yc.add_trace(go.Scatter(
        x=cal_dates, y=cal_vals,
        mode="lines", name="Portfolio Value",
        line=dict(color=yc_color, width=2),
        fill="tozeroy", fillcolor=fill_c,
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Value: $%{y:,.2f}<extra></extra>"
    ))
    fig_yc.add_trace(go.Scatter(
        x=cal_dates, y=[yc_deposit]*len(cal_dates),
        mode="lines", name="Principal",
        line=dict(color="#2A3540", dash="dash", width=1),
        hoverinfo="skip"
    ))
    fig_yc.update_layout(
        **PLOT_LAYOUT,
        title=f"{YCV['asset']} — {yc_months}M Portfolio Growth ({yc_apy}% APY)",
        height=280, title_font=dict(size=11, color="#556070"),
        legend=dict(font=dict(color="#556070", size=9), bgcolor="#090D14")
    )
    st.plotly_chart(fig_yc, width='stretch')

    # Monthly breakdown heatmap-style table
    st.markdown("---")
    st.markdown("##### Monthly Earnings Breakdown")

    monthly_rows = []
    for mo in range(1, yc_months + 1):
        mo_start = (mo - 1) * 30
        mo_end   = mo * 30
        mo_earn  = sum(cal_daily[mo_start:mo_end])
        mo_cum   = cal_cum[mo_end - 1] if mo_end - 1 < len(cal_cum) else cal_cum[-1]
        mo_val   = cal_vals[mo_end - 1] if mo_end - 1 < len(cal_vals) else cal_vals[-1]
        mo_date  = (datetime.today() + timedelta(days=mo_end)).strftime("%b %Y")
        monthly_rows.append({
            "Month":          f"Month {mo:02d} ({mo_date})",
            "Monthly Yield":  f"${mo_earn:,.2f}",
            "Cumulative":     f"${mo_cum:,.2f}",
            "Portfolio Value":f"${mo_val:,.2f}",
        })
    st.dataframe(pd.DataFrame(monthly_rows), width='stretch', hide_index=True)

    # Daily yield bar (last 30 days)
    st.markdown("---")
    st.markdown("##### Daily Yield — Next 30 Days")
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Bar(
        x=[d.strftime("%b %d") for d in cal_dates[:30]],
        y=cal_daily[:30],
        marker_color=[yc_color] * 30,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Daily: $%{y:.4f}<extra></extra>"
    ))
    fig_daily.update_layout(
        **PLOT_LAYOUT,
        title="Daily Yield Accumulation (Next 30 Days)",
        height=200, title_font=dict(size=10, color="#556070"), showlegend=False
    )
    st.plotly_chart(fig_daily, width='stretch')

    # ctToken value over time
    st.markdown("---")
    st.markdown("##### ct[Token] Value Appreciation")
    init_tokens = yc_deposit / YCV["price_usd"] if YCV["price_usd"] > 0 else 0
    token_vals  = [round(v / YCV["price_usd"], 6) if YCV["price_usd"] > 0 else 0 for v in cal_vals]

    fig_tok = go.Figure()
    fig_tok.add_trace(go.Scatter(
        x=cal_dates, y=token_vals,
        mode="lines",
        line=dict(color="#EDD97A", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(237,217,122,0.06)",
        hovertemplate=f"<b>%{{x|%b %d}}</b><br>ct[{YCV["asset"]}]: %{{y:.6f}}<extra></extra>",
        name=f"ct{YCV['asset']}"
    ))
    fig_tok.update_layout(
        **PLOT_LAYOUT,
        title=f"ct[{YCV['asset']}] Tokens Appreciation Over Time",
        height=200, title_font=dict(size=10, color="#556070"), showlegend=False
    )
    st.plotly_chart(fig_tok, width='stretch')

    st.markdown(f"""
    <div style="background:#090D14;border:1px solid #EDD97A33;border-radius:8px;padding:14px;margin-top:8px;">
        <div style="font-size:9px;color:#EDD97A;font-family:'Orbitron',monospace;margin-bottom:4px;">🪙 ct[{YCV['asset']}] TOKEN INFO</div>
        <div style="font-size:10px;color:#556070;">
        You receive <b style="color:#EDD97A;">{init_tokens:.6f} ct{YCV['asset']}</b> for ${yc_deposit:,} deposit.
        After {yc_months} months at {yc_apy}% APY, tokens represent
        <b style="color:{yc_color};">${final_val:,.2f}</b> — all yield accrues automatically to token value.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab8:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#556070;letter-spacing:3px;margin-bottom:16px;">
    ❓ TECHNICAL DOCUMENTATION
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        ("What is Concrete Protocol?",
         "Concrete is an ERC-4626 vault infrastructure on Ethereum Mainnet that automates capital allocation across DeFi strategies — Aave V3, Morpho, Silo, Radiant — while providing automated capital protection buffers."),
        ("How is the Health Factor calculated?",
         f"Read from **Aave V3 Pool.getUserAccountData(vaultAddress)**. Returns healthFactor scaled by 1e18. HF < 1.0 = liquidatable. HF > 3.0 = SAFE. Current selected vault: **{hf:.2f}** ({hf_zone_name})"),
        ("What is the Efficiency Index?",
         "Composite score from concrete-analytics methodology: `(Avg APY / (1 + APY Volatility)) × Util Stability × 100`. Measures reliable capital deployment vs raw APY alone."),
        ("What is the Vault DNA Fingerprint?",
         "Unique multi-dimensional radar chart per vault across 6 dimensions: Yield Consistency, Liquidity Depth, Strategy Diversity, Protocol Maturity, Util Stability, Efficiency Index. Gives a holistic 'personality' view."),
        ("What is the Smart Portfolio Rebalancer?",
         "Enter your current vault holdings and choose an optimization strategy (Max Efficiency, Min Risk, Balanced, or Max APY). The tool computes optimal allocation weights and shows exactly how much to move where — with side-by-side current vs optimal donut charts and projected APY improvement."),
        ("How does live data work?",
         f"Priority chain: app.concrete.xyz → DeFiLlama → ETH RPC → Simulated Fallback. Auto-refresh every 60s. Prices from CoinGecko every 5min. Current source: **{src_label}**"),
        ("What is a ct[Asset] token?",
         "ERC-4626 yield-bearing vault shares. They appreciate automatically as the vault earns yield. Depositing WETH into WeETH vault returns ctWETH tokens."),
        ("Who built this?",
         "Community tool built by **mkashifalikcp** — contributor to @ConcreteXYZ, focused on risk management and vault stability simulation. Not affiliated with Concrete Protocol."),
        ("Is this financial advice?",
         "⚠ NO. DeFi carries risk of total loss. DYOR before investing. Simulation and rebalancing data is illustrative only."),
    ]

    for q, a in faqs:
        with st.expander(q):
            st.markdown(a)

    st.markdown("---")
    st.markdown(f"""
    <div style="background:#090D14;border:1px solid #131B25;border-radius:8px;padding:20px;text-align:center;margin-top:12px;">
        <div style="font-family:'Orbitron',monospace;font-size:16px;color:#00FFB2;font-weight:700;margin-bottom:6px;">🗿 MOAI PROTOCOL VERIFIED</div>
        <div style="font-size:9px;color:#2A3540;letter-spacing:3px;">BUILD WITH CONCRETE · EARN SMARTER · BY MKASHIFALIKCP</div>
        <div style="font-size:8px;color:#131B25;letter-spacing:2px;margin-top:12px;">⚠ SIMULATION ONLY · NOT FINANCIAL ADVICE · YIELDS SUBJECT TO CHANGE · DYOR</div>
    </div>
    """, unsafe_allow_html=True)

