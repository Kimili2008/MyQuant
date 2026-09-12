"""Create the two PDF memos from live project outputs and sourced stock-pitch text."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("TitleCustom", parent=base["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=colors.black, spaceAfter=12),
        "heading": ParagraphStyle("HeadingCustom", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=colors.black, spaceBefore=10, spaceAfter=6),
        "body": ParagraphStyle("BodyCustom", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=7, alignment=TA_LEFT),
        "small": ParagraphStyle("SmallCustom", parent=base["BodyText"], fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#444444")),
    }


def p(text: str, style: str, local):
    return Paragraph(text, local[style])


def metric_table(metrics: pd.DataFrame, period: str):
    selected = metrics[period][["cagr", "annualised_volatility", "sharpe", "max_drawdown", "annual_turnover"]]
    data = [["Strategy", "CAGR", "Vol", "Sharpe", "Max DD", "Annual turnover"]]
    for strategy, row in selected.iterrows():
        data.append([
            strategy,
            f"{row['cagr']:.1%}", f"{row['annualised_volatility']:.1%}",
            f"{row['sharpe']:.2f}", f"{row['max_drawdown']:.1%}", f"{row['annual_turnover']:.1f}x",
        ])
    table = Table(data, colWidths=[1.65 * inch, .72 * inch, .65 * inch, .65 * inch, .8 * inch, 1.1 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#D9D9D9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def build_momentum_report() -> Path:
    local = styles()
    metrics = pd.read_csv(ROOT / "momentum_research" / "results" / "metrics.csv", header=[0, 1], index_col=0)
    path = OUT / "ETF_Momentum_Research_Report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=.62 * inch, leftMargin=.62 * inch, topMargin=.62 * inch, bottomMargin=.62 * inch)
    story = [
        p("ETF Momentum Research", "title", local),
        p("Question: does volatility scaling and an SPY 200-day moving-average filter improve long-only 12-1 ETF momentum after realistic transaction costs?", "body", local),
        p("Research design", "heading", local),
        p("The study uses 24 liquid US-listed ETFs across equities, rates, credit, commodities, FX, and sectors. Signals use returns from 252 to 21 trading days before month-end. Portfolio weights become active on the following trading day. The research period is 2011-2018; the out-of-sample period is 2019 through 31 August 2026. Each rebalance applies 10 bps times one-way turnover.", "body", local),
        p("Strategies", "heading", local),
        p("The benchmark holds all available ETFs equally. The three active variants hold the six strongest 12-1 signals with equal weights, inverse-volatility weights, or inverse-volatility weights only when SPY is above its 200-day moving average. The filter otherwise holds cash.", "body", local),
        p("Research-period results", "heading", local), metric_table(metrics, "research_2011_2018"),
        p("Interpretation", "heading", local),
        p("During the research period, the regime-filtered variant produced the highest reported Sharpe ratio in this fixed design. That pattern is a hypothesis, not a trading conclusion, because the design still reflects a chosen universe and model parameters.", "body", local),
        PageBreak(),
        p("Out-of-sample results", "title", local), metric_table(metrics, "oos_2019_2026"),
        p("Key observation", "heading", local),
        p("The out-of-sample results do not support a simple claim that the regime filter improves the strategy. In this run, inverse-volatility momentum delivered the highest out-of-sample Sharpe ratio, while the filter lowered volatility and drawdown but also lowered CAGR. This is the kind of result that should change the research narrative rather than be omitted.", "body", local),
        p("What the project does well", "heading", local),
        p("The implementation separates research and out-of-sample periods, shifts weights by one trading day, records turnover, applies explicit costs, and writes all weights and daily returns to CSV. Unit tests check signal timing, weight constraints, cost application, and drawdown metrics.", "body", local),
        p("Limitations", "heading", local),
        p("The ETF universe is selected with hindsight, adjusted-close data can differ across providers, monthly close execution is stylised, and the strategy has no borrow, tax, market-impact, capacity, or point-in-time constituent model. Parameter sensitivity and alternative universes are necessary before treating the result as robust.", "body", local),
        p("Reproducibility", "heading", local),
        p("Run `python3 src/run_research.py --download --end 2026-08-31` in `momentum_research/`. The downloader uses the public Yahoo Finance chart endpoint and caches raw CSVs locally. This report is an educational research artifact, not investment advice.", "small", local),
    ]
    doc.build(story)
    return path


def build_amat_memo() -> Path:
    local = styles()
    path = OUT / "AMAT_Stock_Pitch_Memo.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=.62 * inch, leftMargin=.62 * inch, topMargin=.62 * inch, bottomMargin=.62 * inch)
    story = [
        p("Applied Materials Stock Pitch", "title", local),
        p("Status: Watchlist research memo. Educational only, not investment advice.", "body", local),
        p("View", "heading", local),
        p("Applied Materials merits close study because it serves technical process steps that become more demanding as chips adopt 3D structures, advanced packaging, and tighter process-control requirements. The current conclusion is Watchlist. Operating evidence is strong, but a defensible Long or Short call requires a current valuation against a cycle-normalised earnings base.", "body", local),
        p("Current operating evidence", "heading", local),
        p("Applied reported Q3 FY2026 revenue of $9.12bn, GAAP gross margin of 50.3%, GAAP operating income of $3.08bn, and GAAP EPS of $3.17. In FY2025, total revenue was $28.37bn, including $20.80bn from Semiconductor Systems and $6.39bn from Applied Global Services. Operating cash flow was $7.96bn and capex was $2.26bn.", "body", local),
        p("Why the business can matter", "heading", local),
        p("The 2025 10-K describes a broad semiconductor equipment portfolio across patterning, transistor and interconnect fabrication, process control, and advanced packaging. Revenue exposure spans foundry and logic, DRAM, NAND, and non-leading-edge applications. AGS adds services, spares, and factory-automation software linked to the installed base.", "body", local),
        p("Catalysts to test", "heading", local),
        p("1. Sustained spending on advanced logic, high-bandwidth memory, and advanced packaging. 2. Stronger mix or share in process-control and materials-engineering steps. 3. Service growth cushioning equipment cyclicality.", "body", local),
        p("Disconfirming risks", "heading", local),
        p("Capex cuts from memory or foundry customers, trade and export restrictions, customer concentration, technological substitution, and lower returns on newly built capacity would weaken the premise. The company itself describes the industries it serves as volatile and difficult to predict.", "body", local),
        PageBreak(),
        p("Valuation framework", "title", local),
        p("DCF inputs to complete", "heading", local),
        p("Start from FY2025 operating cash flow of $7.96bn less capex of $2.26bn, then normalise working capital and investment needs through the cycle. Forecast revenue by Semiconductor Systems, AGS, and Corporate and Other. Sensitise revenue growth, operating margin, tax, capital intensity, WACC, and terminal growth. Do not use a single-point target as the conclusion.", "body", local),
        p("Trading-comparables work", "heading", local),
        p("Compare Applied with ASML, Lam Research, KLA, and Tokyo Electron on EV/EBIT, P/E, revenue growth, gross margin, operating margin, free-cash-flow conversion, and exposure to leading-edge logic, memory, process control, and services. Document fiscal-year and accounting differences before comparing multiples.", "body", local),
        p("What the share price must be implying", "heading", local),
        p("The next research step is to use the current equity value and net-cash position to back-solve what growth and margin assumptions the market price requires. The pitch becomes differentiated only if that implied expectation differs materially from the analyst's bottom-up, evidence-supported model.", "body", local),
        p("Primary sources", "heading", local),
        p("Applied Materials, Q3 FY2026 Results, 13 August 2026: https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-third-quarter-2026-results. Applied Materials, FY2025 Form 10-K: https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm.", "small", local),
    ]
    doc.build(story)
    return path


if __name__ == "__main__":
    print(build_momentum_report())
    print(build_amat_memo())
