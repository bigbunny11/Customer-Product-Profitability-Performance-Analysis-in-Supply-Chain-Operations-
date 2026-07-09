import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="APL Logistics | Profitability Intelligence",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark navy background */
.stApp {
    background-color: #070d1a;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d1627;
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] * {
    color: #c8d0e0 !important;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #0d1e35 0%, #122240 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4ff, #0077ff);
    border-radius: 16px 16px 0 0;
}
.kpi-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: #7a8faa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 12px;
    color: #4a9eff;
    margin-top: 6px;
    font-weight: 500;
}

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    margin: 32px 0 16px 0;
    padding-left: 12px;
    border-left: 3px solid #0077ff;
}

/* Chart container */
.chart-box {
    background: #0d1627;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 16px;
}

/* Divider */
hr { border-color: #1e2d4a !important; }

/* Plotly chart bg */
.js-plotly-plot { border-radius: 12px; }

/* Selectbox & slider labels */
.stSelectbox label, .stSlider label, .stMultiSelect label {
    color: #7a8faa !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #0a1628 0%, #0d2044 50%, #091420 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.header-banner::after {
    content: '🚢';
    position: absolute;
    right: 36px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 64px;
    opacity: 0.15;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
}
.header-sub {
    font-size: 14px;
    color: #4a7aaa;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    file_id = "1kKQx31z9i1eG1unARyh0iI-C8aGJR7Ws"
url = f"https://drive.google.com/uc?export=download&confirm=yes&id={file_id}"
df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

with st.spinner("Loading dashboard data..."):
    df = load_data()

# ─── SIDEBAR FILTERS ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    st.markdown("---")

    segments = ["All"] + sorted(df["Customer Segment"].dropna().unique().tolist())
    selected_segment = st.selectbox("Customer Segment", segments)

    markets = ["All"] + sorted(df["Market"].dropna().unique().tolist())
    selected_market = st.selectbox("Market", markets)

    categories = ["All"] + sorted(df["Category Name"].dropna().unique().tolist())
    selected_category = st.selectbox("Product Category", categories)

    shipping_modes = ["All"] + sorted(df["Shipping Mode"].dropna().unique().tolist())
    selected_shipping = st.selectbox("Shipping Mode", shipping_modes)

    st.markdown("---")
    st.markdown("### 💸 Discount Filter")
    max_discount = st.slider(
        "Max Discount Rate (%)",
        min_value=0, max_value=100,
        value=100, step=5
    )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("<small style='color:#4a7aaa'>APL Logistics — KWE Group<br>Profitability Intelligence Dashboard<br>Supply Chain Analytics</small>", unsafe_allow_html=True)

# ─── APPLY FILTERS ───────────────────────────────────────────────────────────
filtered = df.copy()
if selected_segment != "All":
    filtered = filtered[filtered["Customer Segment"] == selected_segment]
if selected_market != "All":
    filtered = filtered[filtered["Market"] == selected_market]
if selected_category != "All":
    filtered = filtered[filtered["Category Name"] == selected_category]
if selected_shipping != "All":
    filtered = filtered[filtered["Shipping Mode"] == selected_shipping]
filtered = filtered[filtered["Order Item Discount Rate"] <= (max_discount / 100)]

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <p class="header-title">APL Logistics — Profitability Intelligence</p>
    <p class="header-sub">Customer · Product · Market · Discount Analysis | Supply Chain Commercial Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ─── KPI SECTION ─────────────────────────────────────────────────────────────
total_revenue  = filtered["Sales"].sum()
total_profit   = filtered["Order Profit Per Order"].sum()
profit_margin  = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
avg_discount   = filtered["Order Item Discount Rate"].mean() * 100
total_orders   = filtered.shape[0]
loss_orders    = (filtered["Order Profit Per Order"] < 0).sum()
loss_pct       = (loss_orders / total_orders * 100) if total_orders > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
kpis = [
    (col1, "Total Revenue",    f"${total_revenue/1e6:.2f}M",  "Gross Sales"),
    (col2, "Total Profit",     f"${total_profit/1e6:.2f}M",   "Net Profit"),
    (col3, "Profit Margin",    f"{profit_margin:.1f}%",        "Revenue → Profit"),
    (col4, "Avg Discount",     f"{avg_discount:.1f}%",         "Mean Discount Rate"),
    (col5, "Loss Orders",      f"{loss_pct:.1f}%",             f"{loss_orders:,} orders"),
]
for col, label, value, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ─── PLOTLY THEME ────────────────────────────────────────────────────────────
PLOT_BG   = "#0d1627"
PAPER_BG  = "#0d1627"
FONT_CLR  = "#c8d0e0"
GRID_CLR  = "#1e2d4a"
PALETTE   = ["#0077ff","#00d4ff","#00c48c","#ff6b6b","#ffd166","#a78bfa","#f97316","#34d399"]

def chart_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne", size=15, color="#ffffff"), x=0.01),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans", color=FONT_CLR, size=12),
        height=height,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_CLR)),
        xaxis=dict(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — REVENUE & PROFIT OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Revenue & Profit Overview</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    # Revenue vs Profit by Market
    mkt = filtered.groupby("Market").agg(
        Revenue=("Sales","sum"),
        Profit=("Order Profit Per Order","sum")
    ).reset_index().sort_values("Revenue", ascending=False)

    fig = go.Figure()
    fig.add_bar(name="Revenue", x=mkt["Market"], y=mkt["Revenue"],
                marker_color=PALETTE[0], opacity=0.85)
    fig.add_bar(name="Profit",  x=mkt["Market"], y=mkt["Profit"],
                marker_color=PALETTE[2], opacity=0.9)
    fig.update_layout(barmode="group")
    chart_layout(fig, "Revenue vs Profit by Market")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    # Profit Margin by Market (gauge-style bar)
    mkt["Margin_%"] = (mkt["Profit"] / mkt["Revenue"] * 100).round(2)
    fig2 = px.bar(mkt, x="Margin_%", y="Market", orientation="h",
                  color="Margin_%", color_continuous_scale=["#ff6b6b","#ffd166","#00c48c"],
                  text=mkt["Margin_%"].apply(lambda x: f"{x:.1f}%"))
    fig2.update_traces(textposition="outside")
    fig2.update_coloraxes(showscale=False)
    chart_layout(fig2, "Profit Margin % by Market")
    st.plotly_chart(fig2, use_container_width=True)

# Shipping mode profit breakdown
col_c, col_d = st.columns(2)
with col_c:
    ship = filtered.groupby("Shipping Mode").agg(
        Revenue=("Sales","sum"),
        Profit=("Order Profit Per Order","sum"),
        Orders=("Sales","count")
    ).reset_index()
    ship["Margin_%"] = (ship["Profit"] / ship["Revenue"] * 100).round(2)
    fig3 = px.pie(ship, names="Shipping Mode", values="Revenue",
                  color_discrete_sequence=PALETTE, hole=0.45)
    fig3.update_traces(textinfo="percent+label", textfont_size=12)
    chart_layout(fig3, "Revenue Share by Shipping Mode")
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    # Order status profit impact
    status = filtered.groupby("Order Status").agg(
        Profit=("Order Profit Per Order","sum"),
        Orders=("Sales","count")
    ).reset_index().sort_values("Profit", ascending=False)
    fig4 = px.bar(status, x="Order Status", y="Profit",
                  color="Profit", color_continuous_scale=["#ff6b6b","#ffd166","#00c48c"],
                  text=status["Profit"].apply(lambda x: f"${x/1e3:.0f}K"))
    fig4.update_traces(textposition="outside")
    fig4.update_coloraxes(showscale=False)
    fig4.update_xaxes(tickangle=-30)
    chart_layout(fig4, "Profit by Order Status")
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — CUSTOMER VALUE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">👥 Customer Value Dashboard</div>', unsafe_allow_html=True)

cust = filtered.groupby("Customer Id").agg(
    Total_Sales=("Sales","sum"),
    Total_Profit=("Order Profit Per Order","sum"),
    Orders=("Sales","count")
).reset_index()
cust["Margin_%"] = (cust["Total_Profit"] / cust["Total_Sales"] * 100).round(2)
cust["Value_Tier"] = pd.qcut(cust["Total_Profit"], q=4,
                              labels=["Low Value","Mid Value","High Value","Top Performer"],
                              duplicates="drop")

col_e, col_f = st.columns(2)
with col_e:
    # Top 15 customers by profit
    top15 = cust.nlargest(15, "Total_Profit")
    fig5 = px.bar(top15, x="Total_Profit", y=top15["Customer Id"].astype(str),
                  orientation="h", color="Total_Profit",
                  color_continuous_scale=["#0044aa","#0077ff","#00d4ff"],
                  text=top15["Total_Profit"].apply(lambda x: f"${x:,.0f}"))
    fig5.update_traces(textposition="outside")
    fig5.update_coloraxes(showscale=False)
    chart_layout(fig5, "Top 15 Customers by Profit", height=420)
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    # Bottom 15 (loss-making)
    bot15 = cust.nsmallest(15, "Total_Profit")
    fig6 = px.bar(bot15, x="Total_Profit", y=bot15["Customer Id"].astype(str),
                  orientation="h", color="Total_Profit",
                  color_continuous_scale=["#ff2244","#ff6b6b","#ffd166"],
                  text=bot15["Total_Profit"].apply(lambda x: f"${x:,.0f}"))
    fig6.update_traces(textposition="outside")
    fig6.update_coloraxes(showscale=False)
    chart_layout(fig6, "Bottom 15 Customers (Loss-Making)", height=420)
    st.plotly_chart(fig6, use_container_width=True)

col_g, col_h = st.columns(2)
with col_g:
    # Customer segment contribution
    seg = filtered.groupby("Customer Segment").agg(
        Revenue=("Sales","sum"),
        Profit=("Order Profit Per Order","sum")
    ).reset_index()
    fig7 = px.bar(seg, x="Customer Segment", y=["Revenue","Profit"],
                  barmode="group", color_discrete_map={"Revenue":PALETTE[0],"Profit":PALETTE[2]},
                  text_auto=".2s")
    chart_layout(fig7, "Revenue & Profit by Customer Segment")
    st.plotly_chart(fig7, use_container_width=True)

with col_h:
    # Value tier distribution
    tier_counts = cust["Value_Tier"].value_counts().reset_index()
    tier_counts.columns = ["Tier","Count"]
    fig8 = px.pie(tier_counts, names="Tier", values="Count",
                  color_discrete_sequence=["#ff6b6b","#ffd166","#0077ff","#00c48c"], hole=0.4)
    fig8.update_traces(textinfo="percent+label")
    chart_layout(fig8, "Customer Value Tier Distribution")
    st.plotly_chart(fig8, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — PRODUCT & CATEGORY PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📦 Product & Category Performance</div>', unsafe_allow_html=True)

cat = filtered.groupby("Category Name").agg(
    Revenue=("Sales","sum"),
    Profit=("Order Profit Per Order","sum"),
    Orders=("Sales","count"),
    Avg_Discount=("Order Item Discount Rate","mean")
).reset_index()
cat["Margin_%"] = (cat["Profit"] / cat["Revenue"] * 100).round(2)
cat = cat.sort_values("Profit", ascending=False)

col_i, col_j = st.columns(2)
with col_i:
    fig9 = px.bar(cat, x="Category Name", y="Margin_%",
                  color="Margin_%", color_continuous_scale=["#ff2244","#ffd166","#00c48c"],
                  text=cat["Margin_%"].apply(lambda x: f"{x:.1f}%"))
    fig9.update_traces(textposition="outside")
    fig9.update_coloraxes(showscale=False)
    fig9.update_xaxes(tickangle=-45)
    chart_layout(fig9, "Profit Margin % by Category", height=420)
    st.plotly_chart(fig9, use_container_width=True)

with col_j:
    # Bubble: Revenue vs Profit, size = Orders
    fig10 = px.scatter(cat, x="Revenue", y="Profit", size="Orders",
                       color="Margin_%", text="Category Name",
                       color_continuous_scale=["#ff6b6b","#ffd166","#00c48c"],
                       size_max=50)
    fig10.update_traces(textposition="top center", textfont_size=9)
    chart_layout(fig10, "Revenue vs Profit Bubble (Category)", height=420)
    st.plotly_chart(fig10, use_container_width=True)

# Top & Bottom Products
col_k, col_l = st.columns(2)
prod = filtered.groupby("Product Name").agg(
    Revenue=("Sales","sum"),
    Profit=("Order Profit Per Order","sum")
).reset_index()
prod["Margin_%"] = (prod["Profit"] / prod["Revenue"] * 100).round(2)

with col_k:
    top_prod = prod.nlargest(12, "Profit")
    fig11 = px.bar(top_prod, x="Profit", y="Product Name", orientation="h",
                   color="Margin_%", color_continuous_scale=["#0077ff","#00d4ff"],
                   text=top_prod["Profit"].apply(lambda x: f"${x:,.0f}"))
    fig11.update_traces(textposition="outside")
    fig11.update_coloraxes(showscale=False)
    chart_layout(fig11, "Top 12 Products by Profit", height=420)
    st.plotly_chart(fig11, use_container_width=True)

with col_l:
    bot_prod = prod.nsmallest(12, "Profit")
    fig12 = px.bar(bot_prod, x="Profit", y="Product Name", orientation="h",
                   color="Margin_%", color_continuous_scale=["#ff2244","#ff6b6b"],
                   text=bot_prod["Profit"].apply(lambda x: f"${x:,.0f}"))
    fig12.update_traces(textposition="outside")
    fig12.update_coloraxes(showscale=False)
    chart_layout(fig12, "Bottom 12 Products (Loss-Making)", height=420)
    st.plotly_chart(fig12, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 4 — DISCOUNT IMPACT ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">💸 Discount Impact Analyzer</div>', unsafe_allow_html=True)

disc = filtered.copy()
disc["Discount_Bin"] = pd.cut(
    disc["Order Item Discount Rate"],
    bins=[-0.01, 0.05, 0.10, 0.20, 0.30, 1.01],
    labels=["0–5%","5–10%","10–20%","20–30%","30%+"]
)
disc_grp = disc.groupby("Discount_Bin", observed=True).agg(
    Avg_Profit_Ratio=("Order Item Profit Ratio","mean"),
    Avg_Profit=("Order Profit Per Order","mean"),
    Orders=("Sales","count"),
    Total_Profit=("Order Profit Per Order","sum")
).reset_index()

col_m, col_n = st.columns(2)
with col_m:
    fig13 = px.bar(disc_grp, x="Discount_Bin", y="Avg_Profit_Ratio",
                   color="Avg_Profit_Ratio",
                   color_continuous_scale=["#ff2244","#ffd166","#00c48c"],
                   text=disc_grp["Avg_Profit_Ratio"].apply(lambda x: f"{x:.3f}"))
    fig13.update_traces(textposition="outside")
    fig13.update_coloraxes(showscale=False)
    chart_layout(fig13, "Avg Profit Ratio by Discount Band")
    st.plotly_chart(fig13, use_container_width=True)

with col_n:
    fig14 = px.scatter(disc, x="Order Item Discount Rate", y="Order Profit Per Order",
                       color="Order Item Profit Ratio",
                       color_continuous_scale=["#ff2244","#ffd166","#00c48c"],
                       opacity=0.4, size_max=4)
    fig14.add_hline(y=0, line_dash="dash", line_color="#ff6b6b",
                    annotation_text="Break-even", annotation_font_color="#ff6b6b")
    fig14.update_coloraxes(showscale=False)
    chart_layout(fig14, "Discount Rate vs Profit Per Order (Scatter)")
    st.plotly_chart(fig14, use_container_width=True)

# What-if Discount Scenario
st.markdown("#### 🔮 What-If Discount Scenario")
col_o, col_p, col_q = st.columns([1, 1, 2])
with col_o:
    what_if_disc = st.slider("Simulate Discount Rate (%)", 0, 50, 15, 1)
with col_p:
    base_margin = profit_margin
    sim_revenue = total_revenue
    # Simple linear impact estimate
    disc_impact = (what_if_disc / 100) * sim_revenue
    sim_profit  = total_profit - disc_impact * 0.6
    sim_margin  = (sim_profit / sim_revenue * 100) if sim_revenue > 0 else 0
    st.metric("Simulated Profit", f"${sim_profit/1e6:.2f}M",
              delta=f"{sim_margin - base_margin:.1f}% margin change")
with col_q:
    # Waterfall
    fig15 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","total"],
        x=["Current Profit","Discount Impact","Simulated Profit"],
        y=[total_profit, -(disc_impact * 0.6), 0],
        connector={"line":{"color":"#1e2d4a"}},
        increasing={"marker":{"color":"#00c48c"}},
        decreasing={"marker":{"color":"#ff6b6b"}},
        totals={"marker":{"color":"#0077ff"}}
    ))
    chart_layout(fig15, f"Waterfall: Impact of {what_if_disc}% Discount", height=300)
    st.plotly_chart(fig15, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 5 — MARKET & REGIONAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🌍 Market & Regional Profit Analysis</div>', unsafe_allow_html=True)

region = filtered.groupby("Order Region").agg(
    Revenue=("Sales","sum"),
    Profit=("Order Profit Per Order","sum"),
    Orders=("Sales","count")
).reset_index()
region["Margin_%"] = (region["Profit"] / region["Revenue"] * 100).round(2)
region = region.sort_values("Profit", ascending=False)

col_r, col_s = st.columns(2)
with col_r:
    fig16 = px.bar(region, x="Margin_%", y="Order Region", orientation="h",
                   color="Margin_%", color_continuous_scale=["#ff2244","#ffd166","#00c48c"],
                   text=region["Margin_%"].apply(lambda x: f"{x:.1f}%"))
    fig16.update_traces(textposition="outside")
    fig16.update_coloraxes(showscale=False)
    chart_layout(fig16, "Profit Margin % by Region", height=420)
    st.plotly_chart(fig16, use_container_width=True)

with col_s:
    fig17 = px.treemap(region, path=["Order Region"], values="Revenue",
                       color="Margin_%",
                       color_continuous_scale=["#ff2244","#ffd166","#00c48c"])
    chart_layout(fig17, "Revenue Treemap by Region (color=Margin%)", height=420)
    st.plotly_chart(fig17, use_container_width=True)

# Country-level geo scatter
country = filtered.groupby(["Order Country","Latitude","Longitude"]).agg(
    Profit=("Order Profit Per Order","sum"),
    Revenue=("Sales","sum")
).reset_index()
country["Margin_%"] = (country["Profit"] / country["Revenue"] * 100).round(2)

fig18 = px.scatter_geo(country, lat="Latitude", lon="Longitude",
                        size=country["Revenue"].clip(lower=1),
                        color="Margin_%",
                        hover_name="Order Country",
                        color_continuous_scale=["#ff2244","#ffd166","#00c48c"],
                        projection="natural earth", size_max=30)
fig18.update_layout(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    geo=dict(bgcolor=PLOT_BG, landcolor="#1a2a40",
             showland=True, showocean=True, oceancolor="#0a1222",
             lakecolor="#0a1222", showcountries=True,
             countrycolor="#1e3a5f", showcoastlines=True,
             coastlinecolor="#1e3a5f"),
    height=450,
    margin=dict(l=0, r=0, t=50, b=0),
    title=dict(text="Global Profit Margin Map", font=dict(family="Syne", size=15, color="#fff"), x=0.01),
    coloraxis_colorbar=dict(tickfont=dict(color=FONT_CLR), title=dict(text="Margin%", font=dict(color=FONT_CLR)))
)
st.plotly_chart(fig18, use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#2a4a6a; font-size:12px; font-family:DM Sans'>"
    "APL Logistics (KWE Group) · Supply Chain Profitability Intelligence Dashboard · Built with Streamlit & Plotly"
    "</p>", unsafe_allow_html=True
)
