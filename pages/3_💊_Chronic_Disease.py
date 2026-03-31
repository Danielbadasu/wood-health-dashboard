import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_latest, load_all_years, get_trend, find_column
from utils.sidebar import render_sidebar, fetch_metric, kpi_delta, arrow, diff
from chatbot_widget import render_ai_banner, render_disclaimer, render_sidebar_chat, CHART_CONFIG, LAYOUT_BASE

st.set_page_config(page_title="👶 Maternal Health", page_icon="👶", layout="wide")

st.markdown("""
<style>
.kpi-container { display: flex; gap: 20px; margin-bottom: 30px; }
.kpi-card { flex: 1; padding: 24px 28px; border-radius: 16px; position: relative; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
.kpi-card.orange { background: linear-gradient(135deg, #f7971e, #ffd200); }
.kpi-card.red    { background: linear-gradient(135deg, #ff416c, #ff4b2b); }
.kpi-card.green  { background: linear-gradient(135deg, #11998e, #38ef7d); }
.kpi-card.blue   { background: linear-gradient(135deg, #1a6dff, #4facfe); }
.kpi-card.purple { background: linear-gradient(135deg, #6a11cb, #a855f7); }
.kpi-label { font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.75); margin-bottom: 10px; font-weight: 600; }
.kpi-value { font-size: 36px; font-weight: 800; letter-spacing: -1px; margin-bottom: 6px; color: #ffffff; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
.kpi-sub { font-size: 12px; color: rgba(255,255,255,0.65); }
.kpi-delta { font-size: 10px; margin-top: 4px; }
.kpi-icon { position: absolute; top: 18px; right: 20px; font-size: 42px; opacity: 0.25; }
.chip-tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 1px; background: rgba(247,151,30,0.2); color: #ffd200; border: 1px solid rgba(247,151,30,0.4); margin-bottom: 16px; }
.headline-insight { background: linear-gradient(135deg, rgba(247,151,30,0.1), rgba(247,151,30,0.05)); border: 1px solid rgba(247,151,30,0.3); border-left: 4px solid #ffd200; border-radius: 12px; padding: 18px 24px; margin-bottom: 28px; font-size: 15px; color: rgba(255,255,255,0.9); line-height: 1.6; }
.section-title { font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: 16px; margin-top: 32px; }
.year-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; background: rgba(255,210,0,0.2); color: #ffd200; border: 1px solid rgba(255,210,0,0.3); margin-left: 8px; vertical-align: middle; }
</style>
""", unsafe_allow_html=True)

latest   = load_latest()
all_data = load_all_years()

selected_year, compare_year, show_ohio, selected_charts = render_sidebar(
    page_name="👶 Maternal Health",
    all_data=all_data,
    chart_options=["Maternal & Infant Comparison", "Infant Mortality Trend", "Low Birth Weight Trend", "Prenatal Care Trend"]
)

def gm(col, county='Wood', sheet='additional'):
    return fetch_metric(all_data, latest, selected_year, col, county, sheet)

def gmc(col, county='Wood', sheet='additional'):
    if compare_year is None: return None
    return fetch_metric(all_data, latest, compare_year, col, county, sheet)

infant_h     = gm('Infant Mortality Rate')
infant_o     = gm('Infant Mortality Rate', county='Ohio')
lbw_h        = gm('% Low Birth Weight', sheet='select')
lbw_o        = gm('% Low Birth Weight', county='Ohio', sheet='select')
child_mort_h = gm('Child Mortality Rate')
child_mort_o = gm('Child Mortality Rate', county='Ohio')
life_exp_h   = gm('Life Expectancy')
life_exp_o   = gm('Life Expectancy', county='Ohio')
uninsured_h  = gm('% Uninsured', sheet='select')
uninsured_o  = gm('% Uninsured', county='Ohio', sheet='select')
pcp_h_raw    = gm('Primary Care Physicians Rate', sheet='select')
pcp_o_raw    = gm('Primary Care Physicians Rate', county='Ohio', sheet='select')
pcp_h        = round(pcp_h_raw) if pcp_h_raw else 0
pcp_o        = round(pcp_o_raw) if pcp_o_raw else 0

infant_c     = gmc('Infant Mortality Rate')
lbw_c        = gmc('% Low Birth Weight', sheet='select')
child_mort_c = gmc('Child Mortality Rate')
life_exp_c   = gmc('Life Expectancy')

st.markdown(f"# 👶 Maternal & Infant Health <span class='year-badge'>Showing: {selected_year}</span>", unsafe_allow_html=True)
st.markdown('<div class="chip-tag">🏥 CHIP PRIORITY 3</div>', unsafe_allow_html=True)
st.markdown("Birth outcomes, infant mortality, prenatal care, and child health for Wood County vs Ohio.")

st.markdown(f"""
<div class="headline-insight">
    💡 <strong>Key Finding ({selected_year}):</strong> Wood County's infant mortality rate is
    <strong>{infant_h} per 1,000 live births</strong> vs Ohio's {infant_o}.
    Low birth weight stands at <strong>{lbw_h}%</strong> vs {lbw_o}% statewide.
    Life expectancy is <strong>{life_exp_h} years</strong> vs {life_exp_o} for Ohio overall.
    These maternal and infant outcomes are central to CHIP Priority 3.
</div>
""", unsafe_allow_html=True)

render_ai_banner("Maternal & Infant Health")

st.markdown('<div class="section-title">Key Indicators</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card orange">
        <div class="kpi-icon">👶</div>
        <div class="kpi-label">Infant Mortality Rate</div>
        <div class="kpi-value">{infant_h}</div>
        <div class="kpi-sub">Per 1,000 live births · Ohio: {infant_o} · {arrow(infant_h, infant_o)} {diff(infant_h, infant_o)} vs state</div>
        <div class="kpi-delta">{kpi_delta(infant_h, infant_c, compare_year=compare_year, lower_is_better=True)}</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-icon">⚖️</div>
        <div class="kpi-label">Low Birth Weight</div>
        <div class="kpi-value">{lbw_h}%</div>
        <div class="kpi-sub">Ohio: {lbw_o}% · {arrow(lbw_h, lbw_o)} {diff(lbw_h, lbw_o)}% vs state</div>
        <div class="kpi-delta">{kpi_delta(lbw_h, lbw_c, compare_year=compare_year, lower_is_better=True)}</div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-icon">🧒</div>
        <div class="kpi-label">Child Mortality Rate</div>
        <div class="kpi-value">{child_mort_h}</div>
        <div class="kpi-sub">Per 100k · Ohio: {child_mort_o} · {arrow(child_mort_h, child_mort_o)} {diff(child_mort_h, child_mort_o)} vs state</div>
        <div class="kpi-delta">{kpi_delta(child_mort_h, child_mort_c, compare_year=compare_year, lower_is_better=True)}</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-icon">❤️</div>
        <div class="kpi-label">Life Expectancy</div>
        <div class="kpi-value">{life_exp_h} yrs</div>
        <div class="kpi-sub">Ohio: {life_exp_o} yrs · {arrow(life_exp_h, life_exp_o, lower_is_better=False)} {diff(life_exp_h, life_exp_o)} vs state</div>
        <div class="kpi-delta">{kpi_delta(life_exp_h, life_exp_c, compare_year=compare_year, lower_is_better=False)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title"> </div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card purple">
        <div class="kpi-icon">🩺</div>
        <div class="kpi-label">Primary Care Physicians</div>
        <div class="kpi-value">{pcp_h}</div>
        <div class="kpi-sub">Per 100k · Ohio: {pcp_o} · {pcp_o - pcp_h} fewer than state</div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-icon">💳</div>
        <div class="kpi-label">Uninsured Rate</div>
        <div class="kpi-value">{uninsured_h}%</div>
        <div class="kpi-sub">Ohio: {uninsured_o}% · {arrow(uninsured_h, uninsured_o)} {diff(uninsured_h, uninsured_o)}% vs state</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

def make_trend_chart(trend_df, col, color_map, y_label, value_suffix=""):
    df = trend_df[trend_df['year'] <= selected_year].copy()
    if not show_ohio:
        df = df[df['geography'] == 'Wood County']
    if df.empty:
        return None
    fig = px.scatter(df, x='year', y=col, color='geography',
                     color_discrete_map=color_map, template='plotly_dark')
    for trace in fig.data:
        geo_data = df[df['geography'] == trace.name]
        trace.mode = 'lines+markers' if len(geo_data) > 1 else 'markers'
        trace.line = dict(width=3)
        trace.marker = dict(size=9)
        trace.hovertemplate = '<b>%{fullData.name}</b><br>Year: %{x}<br>' + f'{y_label}: %{{y:.1f}}{value_suffix}<extra></extra>'
    fig.update_layout(**LAYOUT_BASE, xaxis=dict(tickformat='d', dtick=1), yaxis=dict(title=y_label))
    return fig

if "Maternal & Infant Comparison" in selected_charts:
    st.markdown(f'<div class="section-title">Maternal & Infant Indicators — Wood County vs Ohio ({selected_year})</div>', unsafe_allow_html=True)
    compare_df = pd.DataFrame({
        'Indicator': ['Infant Mortality Rate', 'Low Birth Weight %', 'Child Mortality Rate'],
        'Wood County': [infant_h, lbw_h, child_mort_h],
        'Ohio': [infant_o, lbw_o, child_mort_o]
    })
    cols_to_show = ['Wood County', 'Ohio'] if show_ohio else ['Wood County']
    melted = compare_df[['Indicator'] + cols_to_show].melt(id_vars='Indicator', var_name='Geography', value_name='Value')
    fig1 = px.bar(melted, x='Indicator', y='Value', color='Geography', barmode='group',
                  color_discrete_map={'Wood County': '#ffd200', 'Ohio': '#4ECDC4'},
                  labels={'Value': 'Rate / %', 'Indicator': ''}, template='plotly_dark')
    fig1.update_traces(hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:.1f}<extra></extra>')
    fig1.update_layout(**LAYOUT_BASE)
    st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)

if "Infant Mortality Trend" in selected_charts:
    st.markdown('<div class="section-title">Infant Mortality — Trend Up To Selected Year</div>', unsafe_allow_html=True)
    col = find_column(all_data['additional'], ['Infant Mortality Rate'])
    if col:
        fig = make_trend_chart(get_trend(all_data['additional'], col), col,
                               {'Wood County': '#ffd200', 'Ohio': '#4ECDC4'}, 'Infant Mortality Rate', '')
        if fig:
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
        else:
            st.info("No infant mortality data available.")

if "Low Birth Weight Trend" in selected_charts:
    st.markdown('<div class="section-title">Low Birth Weight — Trend Up To Selected Year</div>', unsafe_allow_html=True)
    col = find_column(all_data['select'], ['% Low Birth Weight'])
    if col:
        fig = make_trend_chart(get_trend(all_data['select'], col), col,
                               {'Wood County': '#ffd200', 'Ohio': '#4ECDC4'}, 'Low Birth Weight', '%')
        if fig:
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
        else:
            st.info("No low birth weight data available.")

if "Prenatal Care Trend" in selected_charts:
    st.markdown('<div class="section-title">Primary Care Access — Trend Up To Selected Year</div>', unsafe_allow_html=True)
    col = find_column(all_data['select'], ['Primary Care Physicians Rate', 'Primary Care Physician Rate'])
    if col:
        fig = make_trend_chart(get_trend(all_data['select'], col), col,
                               {'Wood County': '#38ef7d', 'Ohio': '#4ECDC4'}, 'Physicians per 100k', '')
        if fig:
            st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
        else:
            st.info("No PCP data available.")

st.markdown("---")
export_df = pd.DataFrame({
    'Indicator': ['Infant Mortality Rate', 'Low Birth Weight %', 'Child Mortality Rate', 'Life Expectancy', 'PCP per 100k', 'Uninsured %'],
    'Wood County': [infant_h, lbw_h, child_mort_h, life_exp_h, pcp_h, uninsured_h],
    'Ohio': [infant_o, lbw_o, child_mort_o, life_exp_o, pcp_o, uninsured_o]
})
csv = export_df.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Maternal Health Data as CSV", data=csv,
                   file_name=f"wood_maternal_health_{selected_year}.csv", mime="text/csv")
if st.checkbox("Show raw comparison data"):
    st.dataframe(export_df, use_container_width=True)

render_disclaimer("Maternal & Infant Health")
render_sidebar_chat("Maternal & Infant Health")
