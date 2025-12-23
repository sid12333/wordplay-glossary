#!/usr/bin/env python3
"""
基于 Investopedia 金融术语词典创建 financial.json
从网页内容中提取的术语列表
"""

import json
import re
from typing import List, Dict

# 从 Investopedia 网页内容中提取的金融术语列表
# 基于 https://www.investopedia.com/financial-term-dictionary-4769738
FINANCIAL_TERMS = [
    # Numbers
    "1%/10 Net 30", "10-K", "10-Q SEC Form", "10-Year Treasury Note",
    "1040 IRS Form", "1040A Form", "1040EZ Form", "11th District Cost of Funds Index (COFI)",
    "12B-1 Fee", "183-Day Rule", "30-Year Treasury", "401(a) Plan",
    "401(k) Plan", "403(b) Plan", "457 Plan", "5/1 Hybrid Adjustable-Rate Mortgage (5/1 Hybrid ARM)",
    "501(c)(3) Organizations", "52-Week High/Low", "529 Plan", "8-K (Form 8K)",
    "80-20 Rule", "83(b) Election",
    
    # A
    "Absolute Advantage", "Accounting Equation", "Accounting Rate of Return (ARR)",
    "Acid-Test Ratio", "Acquisition", "Adverse Selection", "After-Hours Trading",
    "Alpha", "Amalgamation", "American Depositary Receipt (ADR)", "American Dream",
    "Analysis of Variance (ANOVA)", "Angel Investor", "Annual Percentage Rate (APR)",
    "Annuity", "Applicable Federal Rate (AFR)", "Artificial Intelligence (AI)",
    "Asset", "Asset Management", "Asset Turnover Ratio", "Assets Under Management (AUM)",
    "Automated Clearing House (ACH)", "Automated Teller Machine (ATM)", "Average True Range (ATR)",
    
    # B
    "Balanced Scorecard", "Balance Sheet", "Bank Identification Numbers", "Bankruptcy",
    "Baye's Theorem", "Bear Market", "Berkshire Hathaway", "Bernie Madoff", "Beta",
    "Bill of Lading", "Bitcoin Mining", "Blockchain", "Bollinger Band", "Bond",
    "Break-Even Analysis", "Brexit", "Budget", "Budget Deficit", "Bull Market",
    "Business Cycle", "Business Ethics", "Business Model", "Business-to-Consumer",
    "Business Valuation",
    
    # C
    "Capital", "Capital Asset Pricing Model (CAPM)", "Capital Expenditure", "Capitalism",
    "Central Limit Theorem (CLT)", "Chartered Financial Analyst (CFA)",
    "Chief Executive Officer (CEO)", "Code of Ethics", "Coefficient of Variation (CV)",
    "Collateral", "Command Economy", "Comparative Advantage",
    "Compound Annual Growth Rate (CAGR)", "Compound Interest", "Conflict Theory",
    "Consumer Price Index (CPI)", "Contribution Margin", "Correlation",
    "Correlation Coefficient", "Cost of Goods Sold (COGS)", "Creative Destruction",
    "Credit Default Swap (CDS)", "Current Ratio", "Customer Service",
    
    # D
    "Days Payable Outstanding (DPO)", "Days Sales Outstanding (DSO)", "Debenture",
    "Debt Ratio", "Debt-Service Coverage Ratio (DSCR)", "Debt-to-Equity Ratio (D/E)",
    "Deferred Compensation", "Delivered-at-Place (DAP)", "Delivered Duty Paid (DDP)",
    "Delivered Duty Unpaid (DDU)", "Demand", "Demand Elasticity", "Demonetization",
    "Derivative", "Dilution", "Disbursement", "Discount Rate", "Diversification",
    "Dividend", "Dividend Payout Ratio", "Dividend Yield",
    "Dow Jones Industrial Average (DJIA)", "Due Diligence", "DuPont Analysis",
    
    # E
    "Earnest Money", "Earnings Before Interest and Taxes (EBIT)",
    "Earnings Before Interest, Taxes, Depreciation and Amortization (EBITDA)",
    "Earnings Per Share (EPS)", "EBITA", "Economic Growth", "Economic Moat",
    "Economics", "Economies of Scale", "Employee Stock Ownership Plan (ESOP)",
    "Endowment Fund", "Enterprise Resource Planning (ERP)", "Enterprise Value (EV)",
    "Entrepreneur", "Environmental Protection Agency (EPA)",
    "Environmental, Social, and Governance (ESG) Criteria", "Equity",
    "Equivalent Annual Cost (EAC)", "Escrow", "European Union (EU)", "Ex-Dividend",
    "Exchange Rate", "Exchange-Traded Fund (ETF)", "Externality",
    
    # F
    "FAANG Stocks", "Factors of Production", "FANG Stocks", "Feasibility Study",
    "Federal Deposit Insurance Corporation (FDIC)", "Federal Funds Rate",
    "Federal Housing Administration Loan (FHA)", "Federal Insurance Contributions Act (FICA)",
    "Fiat Money", "Fiduciary", "Finance", "Financial Institution (FI)",
    "Financial Statements", "Financial Technology (Fintech)", "Fiscal Policy",
    "Fixed Income", "Fixed-Income Security", "Four Ps", "Free Carrier (FCA)",
    "Free Market", "Free on Board (FOB)", "Free Trade", "Fringe Benefits", "Futures",
    
    # G
    "Game Theory", "Gamma", "General Agreement on Tariffs and Trade (GATT)",
    "General Data Protection Regulation (GDPR)", "General Ledger",
    "Generally Accepted Accounting Principles (GAAP)", "Generation X (Gen X)",
    "Geometric Mean", "Giffen Good", "Gini Index", "Globalization",
    "Goods and Services Tax (GST)", "Goodwill", "Gordon Growth Model",
    "Government Bond", "Government Shutdown", "Great Depression",
    "Gross Domestic Product (GDP)", "Gross Income", "Gross Margin",
    "Gross National Product (GNP)", "Gross Profit", "Gross Profit Margin", "Guarantor",
    
    # H
    "Hard Skills", "Harmonic Mean", "Head And Shoulders Pattern",
    "Health Maintenance Organizations (HMOs)", "Health Savings Account (HSA)",
    "Hedge", "Hedge Fund", "Herfindahl-Hirschman Index (HHI)", "Heteroskedasticity",
    "High-Low Method", "High-Net-Worth Individual (HNWI)", "Hold Harmless Clause",
    "Holding Company", "Home Equity Loan", "Homeowners Association (HOA)",
    "Homeowners Association Fee (HOA Fee)", "Homestead Exemption",
    "Horizontal Integration", "Hostile Takeover", "Housing Bubble", "Human Capital",
    "Hurdle Rate", "Hyperinflation", "Hypothesis Testing",
    
    # I
    "Income", "Income Statement", "Indemnity", "Index", "Index Fund",
    "Individual Retirement Account (IRA)", "Inflation", "Initial Public Offering (IPO)",
    "Insider Trading", "Insurance", "Interest Rate", "Internal Rate of Return (IRR)",
    "International Monetary Fund (IMF)", "Investment", "Investment Bank",
    "Investment Banking", "IPO", "IRA",
    
    # J-K
    "Joint Venture", "Junk Bond", "Korea Composite Stock Price Indexes (KOSPI)",
    "Kurtosis", "Kuwaiti Dinar (KWD)", "Kyoto Protocol",
    
    # L
    "Laissez-Faire", "Law of Demand", "Law of Supply", "Law of Supply and Demand",
    "Leadership", "Letter of Intent (LOI)", "Letters of Credit", "Leverage",
    "Leverage Ratio", "Leveraged Buyout (LBO)", "Liability", "Liability Insurance",
    "Limit Order", "Limited Government", "Limited Liability Company (LLC)",
    "Limited Partnership (LP)", "Line of Credit (LOC)", "Liquidation", "Liquidity",
    "Liquidity Coverage Ratio (LCR)", "Liquidity Ratio", "Loan-To-Value Ratio (LTV)",
    "London Inter-Bank Offered Rate (LIBOR)", "Ltd. (Limited)",
    
    # M
    "Macroeconomics", "Magna Cum Laude", "Management by Objectives (MBO)", "Margin",
    "Margin Call", "Market Share", "Marketing", "Marketing Strategy",
    "Master Limited Partnership (MLP)", "Memorandum of Understanding (MOU)",
    "Mercantilism", "Mergers and Acquisitions (M&A)", "Milton Friedman",
    "Mixed Economic System", "Monetary Policy", "Money Laundering",
    "Money Market Account", "Monopolistic Competition", "Monte Carlo Simulation",
    "Moore's Law", "Moving Average Convergence Divergence (MACD)",
    "Multilevel Marketing", "Mutual Fund", "Mutually Exclusive",
    
    # N
    "Nasdaq", "Nash Equilibrium", "Negative Correlation", "Neoliberalism",
    "Net Asset Value (NAV)", "Net Income (NI)", "Net Operating Income (NOI)",
    "Net Present Value (NPV)", "Net Profit Margin", "Net Worth", "Netting",
    "Network Marketing", "Networking", "New York Stock Exchange (NYSE)",
    "Next of Kin", "NINJA Loan", "Nominal", "Non-Disclosure Agreement (NDA)",
    "Normal Distribution", "North American Free Trade Agreement (NAFTA)",
    "Not for Profit", "Notional Value", "Novation", "Null Hypothesis",
    
    # O
    "Offset", "Old Age, Survivors, and Disability Insurance (OASDI)", "Oligopoly",
    "Onerous Contract", "Online Banking", "Open Market Operations",
    "Operating Income", "Operating Leverage", "Operating Margin",
    "Operations Management", "Opportunity Cost", "Option",
    "Organization of the Petroleum Exporting Countries (OPEC)",
    "Organizational Behavior (OB)", "Organizational Structure",
    "Original Equipment Manufacturer (OEM)", "Original Issue Discount (OID)",
    "Out Of The Money (OTM)", "Outsourcing", "Over-The-Counter (OTC)",
    "Over-The-Counter Market", "Overdraft", "Overhead", "Overnight Index Swap",
    
    # P
    "P-Value", "Partnership", "Penny Stocks Trade", "Per Capita GDP",
    "Perfect Competition", "Personal Finance", "Phillips Curve", "Ponzi Scheme",
    "Porter's 5 Forces", "Positive Correlation", "Pre-Market", "Preference Shares",
    "Preferred Stock", "Present Value", "Price-to-Earnings Ratio (P/E Ratio)",
    "Price/Earnings-to-Growth (PEG) Ratio", "Pro Rata", "Producer Price Index (PPI)",
    "Profit", "Profit and Loss Statement (P&L)", "Promissory Note", "Prospectus",
    "Public Limited Company (PLC)", "Put Option",
    
    # Q
    "Q Ratio (Tobin's Q)", "Quadruple Witching", "Qualified Dividend",
    "Qualified Institutional Buyer (QIB)", "Qualified Institutional Placement (QIP)",
    "Qualified Longevity Annuity Contract (QLAC)", "Qualified Opinion",
    "Qualified Retirement Plan", "Qualified Terminable Interest Property (QTIP) Trust",
    "Qualitative Analysis", "Quality Control", "Quality of Earnings", "Quality Management",
    "Quantitative Analysis (QA)", "Quantitative Easing", "Quantitative Trading",
    "Quantity Demanded", "Quarter (Q1, Q2, Q3, Q4)", "Quarter on Quarter (QOQ)",
    "Quasi Contract", "Quick Assets", "Quick Ratio", "Quintiles", "Quota",
    
    # R
    "R-Squared", "Racketeering", "Rate of Return", "Rational Choice Theory",
    "Real Estate", "Real Estate Investment Trust (REIT)",
    "Real Gross Domestic Product (GDP)", "Receivables Turnover Ratio",
    "Registered Investment Advisor (RIA)", "Regression",
    "Relative Strength Index (RSI)", "Renewable Resource",
    "Repurchase Agreement (Repo)", "Requests for Proposal (RFP)",
    "Required Minimum Distribution (RMD)", "Retained Earnings",
    "Return on Assets (ROA)", "Return on Equity (ROE)",
    "Return on Invested Capital (ROIC)", "Return on Investment (ROI)",
    "Roth 401(k)", "Roth IRA", "Rule of 72", "Russell 2000 Index",
    
    # S
    "S&P 500 Index (Standard & Poor's 500 Index)", "Sarbanes-Oxley (SOX) Act of 2002",
    "Securities and Exchange Commission (SEC)", "Security", "Series 63", "Series 7",
    "Sharpe Ratio", "Short Selling", "Social Media", "Social Responsibility",
    "Solvency Ratio", "Spread", "Standard Deviation", "Stochastic Oscillator",
    "Stock", "Stock Keeping Unit (SKU)", "Stock Market", "Stop-Limit Order",
    "Straddle", "Strength, Weakness, Opportunity, and Threat (SWOT) Analysis",
    "Subsidiary", "Supply Chain", "Sustainability", "Systematic Sampling",
    
    # T
    "T-Test", "Tariff", "Technical Analysis", "Tenancy in Common (TIC)",
    "Term Life Insurance", "Terminal Value (TV)", "Third World",
    "Total-Debt-to-Total-Assets", "Total Expense Ratio (TER)",
    "Total Quality Management (TQM)", "Total Shareholder Return (TSR)",
    "Trade Deficit", "Trailing 12 Months (TTM)", "Tranches", "Transaction",
    "Treasury Bills (T-Bills)", "Treasury Inflation-Protected Security (TIPS)",
    "Triple Bottom Line (TBL)", "Troubled Asset Relief Program (TARP)",
    "Trust", "Trust Fund", "Trustee", "TSA PreCheck", "Turnover",
    
    # U
    "Underlying Asset", "Underwriter", "Underwriting", "Unearned Income",
    "Unemployment", "Unemployment Rate", "Unicorn",
    "Unified Managed Account (UMA)", "Uniform Distribution",
    "Uniform Gifts to Minors Ac (UGMA)", "Uniform Transfers to Minors Act (UTMA)",
    "Unilateral Contract", "Unit Investment Trust (UIT)", "United Nations (UN)",
    "Universal Life Insurance", "Unlevered Beta", "Unlevered Free Cash Flow (UFCF)",
    "Unlimited Liability", "Unsecured Loan", "Upside", "U.S. Dollar Index (USDX)",
    "U.S. Savings Bonds", "Utilities Sector", "Utility",
    
    # V
    "Valuation", "Value Added", "Value Chain", "Value Investing",
    "Value Proposition", "Value at Risk (VaR)", "Value-Added Tax (VAT)",
    "Variability", "Variable Annuity", "Variable Cost", "Variance", "Vega",
    "Velocity of Money", "Venture Capital", "Venture Capitalist (VC)",
    "Vertical Analysis", "Vertical Integration", "Vesting",
    "Visual Basic for Applications (VBA)", "VIX (CBOE Volatility Index)",
    "Volatility", "Volcker Rule", "Volume Weighted Average Price (VWAP)",
    "Voluntary Employees Beneficiary Association Plan (VEBA)",
    
    # W
    "W-2 Form", "W-4 Form", "W-8 Form", "Waiver of Subrogation", "Wall Street",
    "War Bond", "Warrant", "Wash Sale", "Wash-Sale Rule", "Wealth Management",
    "Wearable Technology", "Weighted Average", "Weighted Average Cost of Capital (WACC)",
    "White-Collar Crime", "White Paper", "Wholesale Price Index (WPI)",
    "Wire Fraud", "Wire Transfers", "Withholding Allowance", "Withholding Tax",
    "Working Capital (NWC)", "Works-in-Progress (WIP)",
    "World Trade Organization (WTO)", "WorldCom",
    
    # X
    "X-Efficiency", "X-Mark Signature", "XBRL (eXtensible Business Reporting Language)",
    "XCD (Eastern Caribbean Dollar)", "XD", "Xenocurrency", "Xetra",
    "XML (Extensible Markup Language)", "XRT",
    
    # Y
    "Yacht Insurance", "Yale School of Management", "Yankee Bond", "Yankee Market",
    "Year-End Bonus", "Year-Over-Year (YOY)", "Year to Date (YTD)",
    "Year's Maximum Pensionable Earnings (YMPE)", "Yearly Rate Of Return Method",
    "Yearly Renewable Term (YRT)", "Yield", "Yield Basis", "Yield Curve",
    "Yield Curve Risk", "Yield Maintenance", "Yield on Cost (YOC)",
    "Yield on Earning Assets", "Yield Spread", "Yield to Call",
    "Yield to Maturity (YTM)", "Yield to Worst (YTW)", "Yield Variance",
    "York Antwerp Rules", "Yuppie",
    
    # Z
    "Z-Score", "Z-Test", "Zacks Investment Research", "ZCash",
    "Zero Balance Account (ZBA)", "Zero-Based Budgeting (ZBB)",
    "Zero-Beta Portfolio", "Zero-Bound", "Zero Coupon Inflation Swap",
    "Zero Coupon Swap", "Zero Cost Collar", "Zero-Coupon Bond",
    "Zero-Lot-Line House", "Zero-One Integer Programming", "Zero-Rated Goods",
    "Zero-Sum Game", "Zero-Volatility Spread (Z-spread)", "Zeta Model",
    "Zig Zag Indicator", "zk-SNARK", "Zombies", "Zoning", "Zoning Ordinance",
    "ZZZZ Best"
]

def create_financial_json(terms: List[str]) -> Dict:
    """
    创建 financial.json 文件结构
    """
    financial_terms = []
    
    for term in terms:
        # 清理术语名称
        source = term.strip()
        if not source:
            continue
        
        # 提取缩写（如果有）
        abbreviation = None
        if '(' in source and ')' in source:
            match = re.search(r'\(([^)]+)\)', source)
            if match:
                abbreviation = match.group(1)
        
        # 创建术语条目
        term_entry = {
            "source": source,
            "target": {
                "zh": "",  # 中文翻译需要后续添加
                "ja": "",
                "ko": "",
                "fr": "",
                "de": "",
                "es": "",
                "it": "",
                "pt": "",
                "ru": ""
            },
            "description": ""  # 描述需要后续添加
        }
        
        if abbreviation:
            term_entry["abbreviation"] = abbreviation
        
        financial_terms.append(term_entry)
    
    return {
        "id": "financial",
        "name": {
            "en": "Finance",
            "zh": "金融"
        },
        "terms": financial_terms
    }

def main():
    print("🔍 创建金融术语 JSON 文件...")
    
    # 去重并排序
    terms = sorted(list(set(FINANCIAL_TERMS)))
    
    print(f"📊 共 {len(terms)} 个术语")
    
    # 创建 JSON 结构
    financial_data = create_financial_json(terms)
    
    # 保存到文件
    output_path = "/Users/Sid/Desktop/github/wordplay-glossary/industries/financial.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(financial_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存到: {output_path}")
    print(f"📝 共 {len(financial_data['terms'])} 个术语条目")
    print("\n⚠️  注意: 中文翻译和描述需要后续手动添加或使用翻译 API 补充")

if __name__ == "__main__":
    main()

