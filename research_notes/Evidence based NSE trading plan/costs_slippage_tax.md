# Costs, slippage and tax for a ₹20,000 Zerodha account risking ₹200 (1R) per trade: NSE equity intraday, delivery, MTF and F&O (as of 31 Oct 2026)

How these notes were made, and how far to trust them: the session's network policy blocked direct page reads. WebFetch failed DNS resolution for both hosts tried (zerodha.com and www.businesstoday.in), and a curl through the egress proxy got a 403 policy denial for zerodha.com. So every figure below comes from search-engine extracts of the cited pages, not from reading the full pages. The web-search budget for the turn also ran out before SEBI's trader-loss studies could be checked. Primary-source pages (zerodha.com/charges, NSE circular FA73061, Finance Act 2026) are cited where the extract quoted them, but their full text was not read. Before hard-coding these numbers, check the tool's constants against zerodha.com/charges (zerodha.com must be allowed in the session's network settings) and the NSE circular PDFs. All rupee calculations were run in a Python script (`cost_model.py`, kept in the session scratchpad) and appear in full below.

## Q1. What are the current rates for every charge by segment, and when did they take effect?

### Takeaway
Zerodha brokerage has not changed: ₹0 on delivery, 0.03% or ₹20 per executed order (whichever is lower) on intraday and futures, and a flat ₹20 per order on options. The only addition is a reported ₹40 per order on intraday F&O orders when cash collateral is below 50% of margin, from 1 Apr 2026. That does not apply to a cash-only ₹20,000 account. The big statutory changes are:
- STT on F&O went up again on 1 Apr 2026: futures 0.05% on the sell side, options 0.15% of sell premium, exercise 0.15% of intrinsic value.
- NSE moved money between transaction charges and IPFT on 1 Mar 2026, leaving the total unchanged: ₹307 per crore for cash, ₹183 per crore for futures, ₹3,553 per crore of premium for options.
- STT on equity delivery (0.1% on both sides) and intraday (0.025% on the sell side) is unchanged.

### Cited Findings

**Summary table of rates (per side unless stated; the ₹ per crore figures convert to % as ₹307/crore = 0.00307%)**

| Charge | Equity intraday (MIS) | Equity delivery (CNC) | MTF | Equity futures | Equity options |
|---|---|---|---|---|---|
| Zerodha brokerage | 0.03% or ₹20 per executed order, whichever lower | ₹0 | 0.3% or ₹20 per executed order, whichever lower | 0.03% or ₹20, whichever lower (₹40 per order for intraday if cash collateral <50%, reported from 1 Apr 2026) | Flat ₹20 per executed order (same ₹40 caveat) |
| STT | 0.025% on sell | 0.1% on buy and sell | 0.1% on buy and sell (delivery product) | 0.05% on sell (from 1 Apr 2026; was 0.02%) | 0.15% of sell premium (from 1 Apr 2026; was 0.1%); 0.15% of intrinsic value on exercise (was 0.125%) |
| NSE transaction charge, including IPFT | ₹307/crore (0.00307%) | ₹307/crore | ₹307/crore | ₹183/crore (0.00183%) | ₹3,553/crore of premium (0.03553%) |
| SEBI turnover fee | ₹10/crore (0.0001%) on both sides | same | same | same | same (on premium) |
| GST | 18% of (brokerage + transaction charges + SEBI fee) | same | same | same | same |
| Stamp duty (buy side only) | 0.003% | 0.015% | 0.015% | 0.002% | 0.003% of premium |
| DP charge (on sell from demat) | none | ₹15.34 per scrip (₹13 + 18% GST) | ₹15.34 per scrip | none | none |
| Other | Auto square-off ₹50 + GST per order (MIS auto square-off at 3:25 PM since 26 Dec 2025) | none | Interest 0.04%/day on funded amount from T+1; pledge ₹15 + GST per ISIN per day | Auto square-off ₹50 + GST | Auto square-off ₹50 + GST |

Sources for each cell are listed below.

**Brokerage**
- Equity delivery brokerage is ₹0; intraday is "0.03% or ₹20 per executed order (whichever is lower) on equity intraday and futures"; options are a flat ₹20 per executed order. Sources: [Zerodha charges page (via search extract)](https://zerodha.com/charges/); [StockCalc Zerodha 2026 breakdown](https://stockcalc.in/blog/zerodha-brokerage-charges-2026-full-breakdown); [Cashoverflow Zerodha charges 2026](https://www.cashoverflow.in/zerodha-charges/).
- From 1 Apr 2026, Zerodha reportedly charges ₹40 instead of ₹20 per order on intraday F&O trades in accounts whose cash and cash-equivalent collateral is below 50% of the margin needed (the SEBI 50:50 cash-collateral rule). — [Inc42](https://inc42.com/buzz/zerodha-raises-fo-charges-to-%E2%82%B940-per-order-for-certain-intraday-trades/); [Business Standard](https://www.business-standard.com/markets/news/zerodha-doubles-brokerage-fees-on-select-f-o-trades-from-april-1-report-126032500517_1.html)
  - Indiahood says the higher fee does not apply to equity intraday trades or to clients who meet margin with cash. — [Indiahood](https://www.indiahood.com/zerodha-raises-intraday-fo-fees-to-%E2%82%B940-per-order-for-non-compliant-traders-starting-april-1/)
  - Inc42 reported, before 1 April, that Zerodha had "not implemented this till now". Whether it was actually implemented is unconfirmed. — [Inc42](https://inc42.com/buzz/zerodha-raises-fo-charges-to-%E2%82%B940-per-order-for-certain-intraday-trades/); also [Free Press Journal](https://www.freepressjournal.in/business/zerodha-raises-intraday-fee-to-40-from-april-1-brokers-may-follow-as-fo-volumes-fall)
- MTF brokerage is "₹20 or 0.3% per MTF order execution, whichever is lower for both intraday and delivery trades". A search extract says this rate was revised on 1 Mar 2025 and that older third-party pages still show 0.03%. — [Zerodha MTF FAQs](https://support.zerodha.com/category/trading-and-markets/margins/margin-trading-facility/articles/margin-trading-facility-mtf-faqs); [Zerodha MTF terms](https://zerodha.com/tos/mtf/)

**STT/CTT**
- Equity intraday STT is 0.025% (₹25 per lakh) on the sell side only. Zerodha's STT article says "Equity delivery and intraday rates remain unchanged" for 2026. — [Zerodha support: how STT is calculated](https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated)
- Budget 2026 (presented 1 Feb 2026) made these F&O STT changes:
  - Futures: 0.02% → 0.05%.
  - Options premium: 0.1% → 0.15%.
  - Options exercise: 0.125% → 0.15%.
  - Sources: [Business Standard, 1 Feb 2026](https://www.business-standard.com/markets/news/markets-fm-hikes-stt-on-fo-trades-surprise-move-126020100888_1.html) ("second increase in STT since 2024"); [Taxscan](https://www.taxscan.in/top-stories/budget-proposes-hike-in-securities-transaction-tax-on-futures-and-options-1442614).
- The new rates took effect on 1 April 2026 and apply to transactions entered into on or after that date. — [5paisa news](https://www.5paisa.com/news/stt-hike-on-fo-to-take-effect-from-april-1-amid-rising-options-activity); [Outlook Money](https://www.outlookmoney.com/invest/stt-hike-from-april-1-2026-budget-what-it-means-for-futures-and-options-traders); [5paisa forum, "Revision in STT rates w.e.f. 1st April 2026"](https://tradebetter.5paisa.com/t/important-update-revision-in-stt-rates-w-e-f-1st-april-2026/872) (cites NSE Circular 02/2026)
- Taxscan's Budget-day report said the date would be notified after the Finance Bill was enacted; later coverage converged on 1 Apr 2026. — [Taxscan](https://www.taxscan.in/top-stories/budget-proposes-hike-in-securities-transaction-tax-on-futures-and-options-1442614)
- Exercise STT is 0.15% of intrinsic value, paid by the buyer who exercises. Sources disagree on who pays. — [PL India](https://www.plindia.com/news/stt-hike-on-fo-in-april-2026-what-can-traders-expect/); [Patron Accounting](https://www.patronaccounting.com/blog/stt-hike-2026-securities-transaction-tax-fo-traders)
- The government said there is no review of the STT structure, and F&O volumes rose despite the hike. — [Basis Point Insight](https://www.basispointinsight.com/Story/govt-says-no-review-of-stt-structure--f-o-volumes-rise-despite-budget-tax-hike_9c6d75f3c414.html)
- Budget 2026 also raised STT (CTT) on commodity futures; the extract did not give the rate. — [Angel One](https://www.angelone.in/news/taxation/union-budget-2026-ltcg-tax-unchanged-at-12-5-stt-on-commodity-futures-hiked)

**NSE transaction charges and IPFT**
- From 1 Oct 2024, under SEBI's uniform-fee mandate, NSE charges per side were:
  - Cash: ₹2.97 per lakh.
  - Equity futures: ₹1.73 per lakh.
  - Equity options: ₹35.03 per lakh of premium.
  - Source: [Business Standard](https://www.business-standard.com/markets/stock-market-news/nse-and-bse-revise-their-transaction-fees-to-comply-with-sebi-circular-124092701207_1.html)
- From April 2023, the IPFT contribution was ₹10 per crore for cash and futures and ₹50 per crore for options. — NSE 2023 circular as quoted in a search extract, [NSE FA56129](https://nsearchives.nseindia.com/content/circulars/FA56129.pdf) (the circular number is inferred from the search listing)
- NSE circular NSE/FA/73061 (27 Feb 2026, effective 1 Mar 2026) rolled the IPFT contribution back to the pre-April-2023 level of ₹0.01 per crore per side and raised transaction charges to match. The total outflow per crore is unchanged:
  - Cash: ₹307.
  - Equity futures: ₹183.
  - Equity options: ₹3,553 per crore of premium.
  - Sources: [NSE FA73061 PDF](https://nsearchives.nseindia.com/content/circulars/FA73061.pdf); [TeamLease RegTech](https://www.teamleaseregtech.com/updates/article/53156/nse-issued-a-circular-regarding-the-revision-in-transaction-charges/); [Navia exchange update](https://navia.co.in/announcement-details?title=Exchange+Update+%E2%80%93+Revision+in+Transaction+Charges&atime=1772442875)
- Secondary sites disagree on the cash transaction charge Zerodha now shows. One lists 0.00307% for delivery; others still show 0.00297% (or older figures). — [search extract across Cashoverflow / KnowYourBrokerage / StockCalc](https://www.cashoverflow.in/zerodha-charges/)
- No NSE transaction-charge circular after March 2026 turned up in searches. — [search of NSE circular mirrors](https://rhnvrm.github.io/stock-market-circulars/circulars/nse/2026/nse-2026-02-27-f0042baf6ef37ea8-revision-in-transaction-charges)

**SEBI fee, GST and stamp duty**
- The SEBI turnover fee is ₹10 per crore (0.0001%), charged on both the buy and sell sides. — [Angel One charges page](https://www.angelone.in/exchange-transaction-charges); [Share India](https://www.shareindia.com/pricing/other-trading-charges)
- Zerodha charges GST at 18% of (brokerage + SEBI charges + transaction charges). — [Zerodha charges page (via search extract)](https://zerodha.com/charges/)
- Stamp duty is charged on the buy side only:
  - Delivery: 0.015%.
  - Intraday: 0.003% (₹300 per crore).
  - Futures: 0.002%.
  - Options: 0.003% of premium.
  - Sources: [Angel One](https://www.angelone.in/exchange-transaction-charges); [Share India](https://www.shareindia.com/pricing/other-trading-charges); [Zerodha charges (search extract)](https://zerodha.com/charges/)

**DP, pledge, MTF and penalty charges**
- The DP charge is ₹15.34 per scrip (₹3.50 CDSL + ₹9.50 Zerodha + ₹2.34 GST), charged when a holding is sold. Zerodha's own post states it as "₹13 + 18% GST (₹9.50 Zerodha fee + ₹3.50 CDSL fee)". — [Zerodha on X](https://x.com/zerodhaonline/status/1909141317135085972); [Zerodha charges page (search extract)](https://zerodha.com/charges/)
- MTF interest is 0.04% per day on the funded amount, charged from T+1 until the stock is sold (≈14.6% a year simple). — [Zerodha support: MTF interest](https://support.zerodha.com/category/trading-and-markets/margins/margin-trading-facility/articles/interest-calculation-for-mtf); the 14.6% p.a. figure is from a third party, [Downstox](https://downstox.com/mtf/zerodha)
- The MTF pledge fee is ₹15 + 18% GST per ISIN per pledge request, charged once per ISIN per day; unpledge is also ₹15 + GST. — [Zerodha MTF FAQs](https://support.zerodha.com/category/trading-and-markets/margins/margin-trading-facility/articles/margin-trading-facility-mtf-faqs); [Zerodha MTF terms](https://zerodha.com/tos/mtf/)
- Separately, the main charges page lists ₹30 + GST per pledge request per ISIN. A search extract read this as the fee for pledging holdings as collateral margin (for example, to buy or sell options), not the MTF pledge. The two sources conflict, and the scope should be checked on the page itself. — [Zerodha charges (search extract)](https://zerodha.com/charges/); [Zerodha support: options using collateral](https://support.zerodha.com/category/console/portfolio/pledging/articles/options-buying-using-collateral)
- Auto square-off costs ₹50 + 18% GST for each order Zerodha squares off. — [Zerodha support: auto square-off](https://support.zerodha.com/category/account-opening/charges-at-zerodha/articles/auto-square-off)
- Equity intraday auto square-off moved to 3:25 PM from 26 Dec 2025. Some older Zerodha pages still say 3:20 PM. — [Z-Connect: changes to auto square-off timings](https://zerodha.com/z-connect/updates/changes-to-the-auto-square-off-timings-for-equity-and-fo)

**F&O contract facts that decide feasibility**
- NSE cut index lot sizes: Nifty 50 from 75 to 65, Bank Nifty from 35 to 30, Fin Nifty to 60, Midcap Select to 120; Nifty Next 50 stays at 25 and Sensex at 20. Timing:
  - Weekly contracts: from the 6 Jan 2026 expiry.
  - Monthly contracts: from the 27 Jan 2026 expiry.
  - Sources: [Angel One](https://www.angelone.in/news/market-updates/nse-revises-lot-sizes-for-index-derivatives-from-december-2025-nifty-lot-size-to-reduce-to-65); [HDFC Sky](https://hdfcsky.com/news/nse-revises-market-lot-sizes-for-major-index-derivatives-effective-january-2026)

### Inferences
- **Use the combined NSE rate (₹307 / ₹183 / ₹3,553 per crore) in the tool.** It is the correct all-in exchange cost both before 1 Mar 2026 (when it was split as transaction charge + IPFT) and after it. Zerodha's brokerage calculator may show the old 0.00297% for a while. The difference is ₹10 per crore, i.e. ₹0.13 on a ₹66,667 round trip, so the label does not matter.
- **The ₹40 F&O surcharge should not apply to this account.** A cash-only ₹20,000 account has 100% cash collateral, above the 50% threshold. Keep ₹20 per order as the default and ₹40 as a switch.
- **Which charges dominate:**
  - Intraday: brokerage (about 56% of costs below the ₹20 cap) and STT.
  - Delivery: STT (0.2% round trip) and, for small positions, the fixed ₹15.34 DP charge.
  - Options at small size: the flat ₹40 round-trip brokerage plus ₹7.20 GST on it (about 75% of the ₹62.61 cost of a ₹6,500-premium round trip).
- The 1 Apr 2026 F&O STT rise makes Nifty futures STT 2.5× the 2024 rate. For this account, futures are ruled out by margin anyway (see Q2).

### Gaps
- **Call-and-trade fee:** commonly quoted as ₹50 + GST per order, from memory of Zerodha's charges page. Not verified this session; one search extract said the call-and-trade section showed something else.
- **Demat AMC:** about ₹300 + GST a year, and BSDA eligibility for small holdings. Not verified. If it applies, it is a fixed ~₹354 a year (≈1.8R a year) regardless of trading.
- **Rounding:** whether Zerodha rounds STT and stamp duty to the nearest rupee per contract note was not verified. I recall the calculator rounds STT; the difference is under ₹1 per trade.
- **Effective dates not verified this session:**
  - SEBI ₹10/crore fee (believed in force since 2020).
  - Stamp-duty rates (believed effective 1 Jul 2020 under the amended Indian Stamp Act).
  - 18% GST (since 2017).
  - The 1 Oct 2024 STT increase (believed effective 1 Oct 2024 under the Finance (No. 2) Act 2024: futures 0.0125%→0.02%, options 0.0625%→0.1%). The 2026 sources only confirm the pre-2026 rates of 0.02% and 0.1%.
- **Was the ₹40 F&O-intraday surcharge actually implemented?** Unconfirmed.
- **Auto square-off time for F&O:** not confirmed. Only the equity time (3:25 PM) was confirmed.
- **Budget 2025:** no STT change was found for it (consistent with the 2026 coverage calling 2026 the second increase since 2024), but no source stated this explicitly.

## Q2. What does a round trip cost in ₹, as % of notional and as a fraction of the ₹200 risk (1R)?

### Takeaway
- **Intraday (MIS):** statutory and brokerage costs are a flat ~0.106% of notional while brokerage stays below the ₹20 cap (notional below ₹66,667). Because position size is ₹200 ÷ stop%, cost in R is 0.106% ÷ stop%:
  - 0.354R at a 0.3% stop.
  - 0.213R at a 0.5% stop.
  - 0.106R at a 1% stop.
  - 0.053R at a 2% stop.
- **Swing delivery (CNC) with 3–8% stops:** 0.10–0.15R, and the fixed ₹15.34 DP charge is half or more of that.
- **CNC with tight stops is expensive:** 0.30R at a 1% stop, because of 0.2% round-trip STT.
- **MTF:** 0.77–1.25R. Not worth it for this account.
- **Nifty option buying is feasible** at 1 lot of 65 (premium paid upfront). Costs are 0.25–0.31R before slippage, and ₹200 of risk means a stop of only 3.08 premium points.
- **Nifty futures are not feasible:** a round trip costs ≈4.8R and needs far more margin than ₹20,000.

### Cited Findings
- All rates used in this question are the Q1 rates, with their sources listed there.
- Nifty lot size is 65 from the January 2026 series. — [Angel One](https://www.angelone.in/news/market-updates/nse-revises-lot-sizes-for-index-derivatives-from-december-2025-nifty-lot-size-to-reduce-to-65)
- MTF interest is 0.04% per day from T+1; pledge is ₹15 + GST per ISIN per day; MTF brokerage is 0.3% or ₹20. — [Zerodha MTF FAQs](https://support.zerodha.com/category/trading-and-markets/margins/margin-trading-facility/articles/margin-trading-facility-mtf-faqs); [Zerodha MTF interest](https://support.zerodha.com/category/trading-and-markets/margins/margin-trading-facility/articles/interest-calculation-for-mtf)
- Zerodha publishes its intraday (MIS) leverage list on its marketintel bulletin. — [Zerodha bulletin: latest intraday leverages](https://zerodha.com/marketintel/bulletin/249809/latest-intraday-leverages-mis-bo-co)

### Inferences
(All numbers come from the scratchpad script. Position size N = ₹200 ÷ stop%. These are long trades. "Flat" means the cost if the exit price equals the entry price. At other exit prices the cost differs by under ₹0.5, because sell-side STT changes slightly.)

#### Step-by-step formulas to code (NSE, rates as of Oct 2026)
```
B = buy value, S = sell value (₹); the same formulas apply to shorts, with the buy-side items on the buy leg
Brokerage  MIS/FUT : min(0.0003*B, 20) + min(0.0003*S, 20)   # per executed order
           OPT     : 20 per executed order (40 if the cash-collateral<50% surcharge applies)
           CNC     : 0 ;  MTF : min(0.003*B, 20) + min(0.003*S, 20)
STT        MIS 0.00025*S ; CNC/MTF 0.001*(B+S) ; FUT 0.0005*S ; OPT 0.0015*S_premium
           (OPT exercised ITM: 0.0015*intrinsic value, paid by the buyer)
Exch txn   EQ 0.0000307*(B+S) ; FUT 0.0000183*(B+S) ; OPT 0.0003553*(B+S premium)
SEBI       0.000001*(B+S)
GST        0.18*(brokerage + exch txn + SEBI)
Stamp      MIS 0.00003*B ; CNC/MTF 0.00015*B ; FUT 0.00002*B ; OPT 0.00003*B_premium
DP         CNC/MTF sells: 15.34 per scrip per sell day
MTF extra  0.0004*funded_amount*days(T+1..sale) + 17.70 pledge per ISIN per buy day (+17.70 unpledge if charged)
Penalty    auto square-off 59.00 per order (50 + 18% GST)
Intraday all-in % below the brokerage cap = 0.06+0.025+0.00614+0.0002+0.18*(0.06634)+0.003 = 0.10628% of N
Delivery variable % = 0.2+0.00614+0.0002+0.18*(0.00634)+0.015 = 0.22248% of N, plus ₹15.34 DP
```

#### Intraday (MIS), cost per round trip

| Stop | Notional N | Margin at 20% (≈5×) | Brokerage | STT | Exch | SEBI | GST | Stamp | **Total ₹** | % of N | **Cost in R** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.3% | ₹66,667 | ₹13,333 | 40.00 | 16.67 | 4.09 | 0.13 | 7.96 | 2.00 | **70.85** | 0.106% | **0.354R** |
| 0.5% | ₹40,000 | ₹8,000 | 24.00 | 10.00 | 2.46 | 0.08 | 4.78 | 1.20 | **42.51** | 0.106% | **0.213R** |
| 1% | ₹20,000 | ₹4,000 | 12.00 | 5.00 | 1.23 | 0.04 | 2.39 | 0.60 | **21.26** | 0.106% | **0.106R** |
| 2% | ₹10,000 | ₹2,000 | 6.00 | 2.50 | 0.61 | 0.02 | 1.19 | 0.30 | **10.63** | 0.106% | **0.053R** |

Worked example, 0.3% stop:
1. N = 200 ÷ 0.003 = ₹66,667.
2. Brokerage per side = min(0.0003 × 66,667, 20) = ₹20. Round trip = ₹40.
3. STT = 0.00025 × 66,667 = ₹16.67.
4. Exchange charge = 0.0000307 × 1,33,333 = ₹4.09.
5. SEBI fee = ₹0.13.
6. GST = 0.18 × (40 + 4.09 + 0.13) = ₹7.96.
7. Stamp duty = 0.00003 × 66,667 = ₹2.00.
8. Total = ₹70.85, which is 0.1063% of N and 0.354R.

At a stop-out the total is ₹70.73; at a +3R exit it is ₹71.03.

A 0.2% stop (N = ₹1,00,000, using the whole ₹20,000 as 5× margin) costs ₹82.7 (0.41R) before slippage.

Adding slippage, as a fraction of R (scenario definitions are in Q3):

| Stop | S1 0.04% RT | S2 0.10% RT | S3 0.25% RT | S4 0.50% RT | All-in R (costs + S2) |
|---|---|---|---|---|---|
| 0.3% | +0.133R | +0.333R | +0.833R | +1.667R | **0.688R** |
| 0.5% | +0.080R | +0.200R | +0.500R | +1.000R | **0.413R** |
| 1% | +0.040R | +0.100R | +0.250R | +0.500R | **0.206R** |
| 2% | +0.020R | +0.050R | +0.125R | +0.250R | **0.103R** |

#### Swing (CNC delivery), cost per round trip, including the DP charge

| Stop | Notional N | STT | Exch | SEBI | GST | Stamp | DP | **Total ₹** | % of N | **Cost in R** | + S2 slip (0.10% RT) | + S3 slip (0.25% RT) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3% | ₹6,667 | 13.33 | 0.41 | 0.01 | 0.08 | 1.00 | 15.34 | **30.17** | 0.453% | **0.151R** | 0.184R | 0.234R |
| 4% | ₹5,000 | 10.00 | 0.31 | 0.01 | 0.06 | 0.75 | 15.34 | **26.46** | 0.529% | **0.132R** | 0.157R | 0.195R |
| 5% | ₹4,000 | 8.00 | 0.25 | 0.01 | 0.05 | 0.60 | 15.34 | **24.24** | 0.606% | **0.121R** | 0.141R | 0.171R |
| 6% | ₹3,333 | 6.67 | 0.20 | 0.01 | 0.04 | 0.50 | 15.34 | **22.76** | 0.683% | **0.114R** | 0.130R | 0.155R |
| 8% | ₹2,500 | 5.00 | 0.15 | 0.01 | 0.03 | 0.37 | 15.34 | **20.90** | 0.836% | **0.105R** | 0.117R | 0.136R |
| *1% (for comparison)* | ₹20,000 | 40.00 | 1.23 | 0.04 | 0.23 | 3.00 | 15.34 | **59.84** | 0.299% | **0.299R** | | |
| *2% (for comparison)* | ₹10,000 | 20.00 | 0.61 | 0.02 | 0.11 | 1.50 | 15.34 | **37.59** | 0.376% | **0.188R** | | |

- **Positions are small.** With 3–8% stops each position uses only ₹2,500–₹6,667 of the ₹20,000, so several positions can be open at once without MTF. A 1% stop already needs the full ₹20,000.
- **Each extra sell day costs another DP charge.** Scaling out of one scrip over two days adds ₹15.34 (0.077R).
- **Overnight gaps are the main swing risk.** If a stock opens 1% beyond the stop, the loss is 1.33R on a 3% stop, 1.20R on a 5% stop and 1.12R on an 8% stop, before costs.

#### MTF, for comparison (50% own margin assumed)

| Position (implied stop) | Funded | 1 day | 5 days | 10 days |
|---|---|---|---|---|
| ₹30,000 (0.67%) | ₹15,000 | ₹152.98 = 0.765R | ₹176.98 = 0.885R | ₹206.98 = 1.035R |
| ₹40,000 (0.5%) | ₹20,000 | ₹177.23 = 0.886R | ₹209.23 = 1.046R | ₹249.23 = 1.246R |

The 5-day ₹30,000 case breaks down as: STT ₹60 + brokerage ₹40 + GST ₹7.54 + stamp ₹4.50 + exchange ₹1.84 + DP ₹15.34 + pledge ₹17.70 + interest ₹30.

MTF only becomes necessary when an overnight position must exceed ₹20,000, which at ₹200 risk means a stop under 1%. That is an unrealistic overnight stop, so MTF should be excluded for this account.

#### F&O: Nifty option buying (lot 65; ₹200 risk = 200 ÷ 65 = 3.08 premium points)

| Premium | Buy value | Stop as % of premium | Brokerage | STT | Exch | GST | Stamp | **Total ₹** | **Cost in R** |
|---|---|---|---|---|---|---|---|---|---|
| ₹100 | ₹6,500 | 3.1% | 40.00 | 9.75 | 4.62 | 8.03 | 0.20 | **62.61** | **0.313R** |
| ₹50 | ₹3,250 | 6.2% | 40.00 | 4.88 | 2.31 | 7.62 | 0.10 | **54.91** | **0.275R** |
| ₹20 | ₹1,300 | 15.4% | 40.00 | 1.95 | 0.92 | 7.37 | 0.04 | **50.28** | **0.251R** |

- **Slippage cost:** each 1 point of round-trip slippage per unit adds ₹65, which is 0.325R.
- **With the ₹40-per-order surcharge** (not expected for this account), the ₹100-premium round trip would cost ₹109.81 (0.55R).
- **Feasibility:** ₹20,000 buys 1–3 lots at a ₹100 premium. Option selling and futures need margins far above ₹20,000 (not quantified this session).

#### F&O: Nifty futures, to show why they are infeasible
At an illustrative Nifty level of 25,000, one lot of 65 is a contract value of ₹16.25 lakh. A round trip costs:
- Brokerage ₹40.
- STT ₹812.50 (0.05% of the sell side).
- Exchange charge ₹59.48.
- SEBI fee ₹3.25.
- GST ₹18.49.
- Stamp duty ₹32.50.
- **Total ₹966.22 ≈ 4.83R.**

₹200 of risk is only 3.08 index points (0.012%), well within normal tick-by-tick noise. Futures are not feasible for this account.

#### Avoidable penalty
A forgotten MIS position squared off by Zerodha costs ₹59 per order, which is 0.295R. The tool should warn before 3:25 PM.

#### Cost-model spec for tradingtool (Python sketch)
```python
RATES = dict(  # as of 31-Oct-2026; verify vs zerodha.com/charges + NSE FA73061
    brk_pct=0.0003, brk_cap=20.0, opt_brk=20.0, mtf_brk_pct=0.003,
    stt={"MIS": ("S", 0.00025), "CNC": ("BS", 0.001), "MTF": ("BS", 0.001),
         "FUT": ("S", 0.0005), "OPT": ("S", 0.0015)},          # FUT/OPT since 2026-04-01
    txn={"MIS": 307e-7, "CNC": 307e-7, "MTF": 307e-7, "FUT": 183e-7, "OPT": 3553e-7},
    sebi=10e-7, gst=0.18,
    stamp={"MIS": 3e-5, "CNC": 15e-5, "MTF": 15e-5, "FUT": 2e-5, "OPT": 3e-5},
    dp=15.34, mtf_int_day=0.0004, pledge=17.70, auto_sqoff=59.0)

def round_trip_cost(prod, B, S, n_buy_orders=1, n_sell_orders=1, funded=0.0, days=0, sell_days=1):
    r = RATES
    if prod in ("MIS", "FUT"):
        brk = min(r["brk_pct"]*B/n_buy_orders, r["brk_cap"])*n_buy_orders + \
              min(r["brk_pct"]*S/n_sell_orders, r["brk_cap"])*n_sell_orders
    elif prod == "OPT":
        brk = r["opt_brk"]*(n_buy_orders + n_sell_orders)
    elif prod == "MTF":
        brk = min(r["mtf_brk_pct"]*B, r["brk_cap"]) + min(r["mtf_brk_pct"]*S, r["brk_cap"])
    else:
        brk = 0.0
    side, rate = r["stt"][prod]
    stt = rate*(S if side == "S" else B + S)
    txn = r["txn"][prod]*(B + S)
    sebi = r["sebi"]*(B + S)
    gst = r["gst"]*(brk + txn + sebi)
    stamp = r["stamp"][prod]*B
    dp = r["dp"]*sell_days if prod in ("CNC", "MTF") else 0.0
    mtf = (r["mtf_int_day"]*funded*days + r["pledge"]) if prod == "MTF" else 0.0
    return brk + stt + txn + sebi + gst + stamp + dp + mtf
```

### Gaps
- **MIS margin:** assumed to be 20% (5× leverage) for liquid stocks. Zerodha's per-stock MIS leverage list was not read, and many midcaps have higher margins (lower leverage). This could stop a 0.3% stop from being sized to ₹66,667 on some stocks.
- **Option-selling and futures margins** were not quantified from a primary source. Only the contract-value argument is shown.
- **Options are priced on a hypothetical ₹100/₹50/₹20 premium.** Actual premiums depend on strike, expiry and India VIX, which were not checked.

## Q3. How much slippage should a manual trader expect (Nifty 50 vs midcap, at the open, entering seconds to a minute after a flag), and when should they use market or limit orders?

### Takeaway
At ₹20,000–₹1,00,000 per order the trade is tiny compared with NSE's impact-cost benchmarks (₹10 crore baskets). So the cost is the half-spread plus the move between the flag and the click. The move matters most:
- About 0.04–0.10% (1σ) for a large-cap with 15–60 seconds of delay.
- About 0.08–0.16% for a volatile midcap.
- Several times more in the first minutes after the open, when spreads are also widest.

The figures I could source are tick sizes, index eligibility thresholds and intraday spread patterns. The scenario figures below (S1–S4) are assumptions, and tradingtool should replace them with slippage measured in its own logs.

### Cited Findings
- **Tick sizes (NSE cash):**
  - ₹0.01 for stocks priced under ₹250, effective 10 Jun 2024. — [Angel One](https://www.angelone.in/news/market-updates/nse-to-announce-1-paisa-tick-size-for-stocks-below-rs-250); [Business Standard](https://www.business-standard.com/amp/markets/news/nse-lowers-tick-size-to-1-paisa-over-1-300-stocks-to-be-impacted-124052700463_1.html)
  - From 15 Apr 2025: ₹0.05 for ₹250–1,000, ₹0.10 for ₹1,000–5,000, ₹0.50 for ₹5,000–10,000. — [Fyers notice](https://fyers.in/notice-board/tick-size-revision-for-nse-derivatives-cash-segment-effective-april-15-2025/)
  - Stock options priced under ₹250 moved to a ₹0.01 tick on 3 Nov 2025. — [Angel One](https://www.angelone.in/announcements/market/revision-in-tick-size-for-stock-options-contracts-by-nse)
- **Impact-cost benchmarks:**
  - To be in the Nifty 50, a stock must have an average impact cost of ≤0.50% for a ₹10 crore basket in 90% of observations. The equivalent midcap limit is looser, about 1% (the extract was garbled). — [NSE index methodology](https://nsearchives.nseindia.com/content/indices/Method_NIFTY_Equity_Indices.pdf)
  - Impact cost is "closer to the true cost of execution" than the quoted spread. — [NSE Indices: impact cost](https://www.niftyindices.com/resources/index-concepts/impact-cost)
  - A forum post says NSE samples bids and asks at 5 points a day for Nifty 50 and Next 50 stocks, at an order value of ₹50 lakh, and publishes monthly averages. — [TradingQnA thread](https://tradingqna.com/t/realistic-assumption-for-slippage-bid-ask-spread-for-stocks-in-nifty50/67221)
- **Spread levels in older NSE data:** a microstructure paper hosted by NSE reports a median limit-order-book spread of ₹0.45 (₹0.72 by the Roll estimator) across all listed stocks. It does not split by market cap. — [NSE research paper 128](https://nsearchives.nseindia.com/content/research/comppaper128.pdf)
- **When in the day spreads are widest:**
  - A study using a year of NSE intraday data found U-shaped intraday liquidity (wider spreads at the open and the close). — [Monash-hosted paper](https://www.monash.edu/__data/assets/pdf_file/0008/925811/intraday_liquidity_patterns_in_indian_stock_market.pdf)
  - A study of 30 NSE midcaps found an L-shaped pattern, with spreads widest early in the session. — [Analysis of liquidity, Indian midcaps](https://www.researchgate.net/publication/282446636_Analysis_of_Liquidity-Study_on_Indian_Mid-Cap_Stocks)
  - For CNX 500 stocks, spreads depend on price, volume and trading frequency; for small caps only price, volume and market cap were significant. — [Cogent Economics & Finance 2021](https://www.tandfonline.com/doi/full/10.1080/23322039.2021.1898735)
- **Market orders on Kite:**
  - Kite's market protection turns a market order into a limit order capped a set percentage from the last traded price. Any unfilled part stays pending at that cap. — [Z-Connect: order placement simplified](https://zerodha.com/z-connect/featured/order-placement-simplified)
  - Kite Connect forum posts say exchanges required a non-zero market protection on all algo or API market orders, including SL-M, from 1 Apr 2026. Execution is "still not guaranteed" and subject to exchange limit-price-protection checks. — [Kite forum](https://kite.trade/forum/discussion/comment/52159/)

### Inferences
- **Half-spread cost:**
  - Liquid Nifty 50 stocks typically quote 1–2 ticks wide. That is about 0.3–1.5 basis points on a ₹700–₹3,000 stock, or 0.4–1 bp for stocks under ₹250 since the 1-paisa tick.
  - Midcaps and small caps quote wider and thinner books, so a ₹1 lakh order may take 2–3 price levels.
  - These are my estimates from tick sizes and the cited spread studies, not measurements.
- **Delay drift dominates for a manual trader.** With σ₁min ≈ σ_daily ÷ √375, the 1σ move during the delay is:

  | Daily volatility (typical stock) | 15 s delay | 30 s delay | 60 s delay |
  |---|---|---|---|
  | 1.5% (Nifty 50 type) | 0.039% | 0.055% | 0.077% |
  | 2.0% | 0.052% | 0.073% | 0.103% |
  | 3.0% (midcap type) | 0.077% | 0.110% | 0.155% |

  Breakout or momentum flags are biased: the price is more likely to keep moving the way of the signal. So the expected adverse drift is a sizeable fraction (assumed 0.5–1.0×) of these 1σ values, not zero. In the first 5–15 minutes after 9:15, intraday volatility runs about 2–3× the session average, and so does the drift (my assumption, consistent with the cited open-heavy spread patterns).
- **Slippage scenarios (assumptions, per round trip, % of price):**

  | Scenario | Round trip | Conditions |
  |---|---|---|
  | S1 tight | 0.04% | Nifty 50 stock; marketable limit entry within a few seconds; stop exit in a calm market |
  | S2 base | 0.10% | Nifty 50 stock; manual entry 15–30 s after the flag; SL-M exit with market protection |
  | S3 midcap/delay | 0.25% | Midcap; 30–60 s delay |
  | S4 open | 0.50% | Midcap in the first minutes after the open, with a manual delay |

  Swing (CNC) round trips can be modelled at S2/S3 spread levels, plus gap risk on the stop (see the Q2 gap rows).
- **Market vs limit orders:**
  - A market order with protection guarantees a fill. It pays the half-spread plus the drift and, in fast markets, may only part-fill at the protection cap.
  - A limit order at the flag price costs nothing when filled. But it suffers adverse selection: it misses the breakouts that run (the winners) and fills on the ones that reverse. A paper trade that assumes a fill at the flag price will therefore overstate edge.
  - A sensible middle ground is a marketable limit order: limit = last price ± a buffer of about 2–5 ticks or 0.05–0.1%, cancelled if not filled within N seconds.
  - Stops: SL-M (with protection) exits reliably but slips. SL-limit orders can be skipped in gaps and turn a 1R loss into more.
- **Paper-trade fill rule for tradingtool:**
  - Buy fill = (ask at flag time + t_react) + k × σ_daily × √(t_react/22,500 s) × price, with the drift term floored at 0. Mirror it for sells.
  - Stop exit = min(stop price, next traded price) − 1–2 ticks.
  - Target exit = the target only if price trades through it by at least 1 tick.
  - Log, for every flag: time and price at the flag (LTP, bid, ask), the human-click time, the fill, and realized slippage in basis points by bucket (Nifty 50 / midcap / first 15 minutes). After 30–50 trades, replace S1–S4 with the measured medians and 80th percentiles.
- **Size is not the constraint at this account size; timing and stock choice are.** The ₹10 crore impact-cost thresholds mean even midcaps absorb a ₹20,000–₹1,00,000 order with little price impact beyond the touch.

### Gaps
- I found no study measuring NSE spreads in basis points for Nifty 50 versus midcaps today (after the 2024–25 tick changes), and none minute by minute for the first 15–30 minutes. NSE's monthly impact-cost reports would answer this but were not reached.
- No primary source on how much retail traders slip on manual entry in India was found. The delay-drift figures are a model, not data.
- NSE pre-open call auction timing (09:00–09:08 order entry, continuous trading from 09:15) is general knowledge, not verified this session.
- Whether Zerodha blocks SL-M orders on options, and its default market-protection percentage on manual Kite orders, were not verified.

## Q4. What win rate is needed to break even at 1:1, 1:1.5, 1:2 and 1:3 after costs and slippage, for each stop distance?

### Takeaway
If c is the all-in cost per trade in R (fees plus slippage), the break-even win rate is (1 + c) ÷ (1 + RR), against 1 ÷ (1 + RR) before costs (50% / 40% / 33.3% / 25%).
- **Intraday with 0.3–0.5% stops is close to impossible for a hand-placed account:** base slippage needs 70–84% wins at 1:1, or 47–56% at 1:2.
- **Intraday with stops of 1% or more, and CNC swing with 3–8% stops,** need only about 2–10 percentage points more than the gross break-even.

### Cited Findings
- The rate inputs are from Q1 and the cost results are computed in Q2. No external source was used for the break-even arithmetic.

### Inferences
Formula (exact, used for the tables): a win pays RR·R − c_win and a loss costs R + c_loss, so p* = (R + c_loss) ÷ ((RR·R − c_win) + (R + c_loss)). Costs at the actual exit price are used, so c_win is slightly larger than c_loss because sell-side STT is bigger.

Intraday (MIS), break-even win rate at 1:1 / 1:1.5 / 1:2 / 1:3 (">100%" means no win rate can break even):

| Stop | Fees only | +S1 (0.04% RT) | +S2 (0.10% RT) | +S3 (0.25% RT) | +S4 (0.50% RT) |
|---|---|---|---|---|---|
| 0.3% | 67.7 / 54.2 / 45.1 / 33.9 | 74.4 / 59.5 / 49.6 / 37.2 | 84.4 / 67.5 / 56.3 / 42.2 | >100 / 87.5 / 72.9 / 54.7 | >100 / >100 / >100 / 75.5 |
| 0.5% | 60.6 / 48.5 / 40.4 / 30.3 | 64.6 / 51.7 / 43.1 / 32.3 | 70.6 / 56.5 / 47.1 / 35.3 | 85.7 / 68.5 / 57.1 / 42.8 | >100 / 88.5 / 73.8 / 55.3 |
| 1% | 55.3 / 44.3 / 36.9 / 27.7 | 57.3 / 45.9 / 38.2 / 28.7 | 60.3 / 48.3 / 40.2 / 30.2 | 67.8 / 54.3 / 45.2 / 33.9 | 80.3 / 64.3 / 53.6 / 40.2 |
| 2% | 52.7 / 42.1 / 35.1 / 26.3 | 53.7 / 42.9 / 35.8 / 26.8 | 55.2 / 44.1 / 36.8 / 27.6 | 58.9 / 47.1 / 39.3 / 29.5 | 65.2 / 52.1 / 43.4 / 32.6 |

Swing (CNC), break-even win rate at 1:1 / 1:1.5 / 1:2 / 1:3:

| Stop | Fees only (incl. DP) | +S2 (0.10% RT) | +S3 (0.25% RT) |
|---|---|---|---|
| 3% | 57.6 / 46.0 / 38.4 / 28.8 | 59.2 / 47.4 / 39.5 / 29.6 | 61.7 / 49.4 / 41.1 / 30.9 |
| 4% | 56.6 / 45.3 / 37.7 / 28.3 | 57.9 / 46.3 / 38.6 / 28.9 | 59.8 / 47.8 / 39.8 / 29.9 |
| 5% | 56.1 / 44.9 / 37.4 / 28.0 | 57.1 / 45.7 / 38.0 / 28.5 | 58.6 / 46.9 / 39.0 / 29.3 |
| 6% | 55.7 / 44.6 / 37.1 / 27.8 | 56.5 / 45.2 / 37.7 / 28.3 | 57.8 / 46.2 / 38.5 / 28.9 |
| 8% | 55.2 / 44.2 / 36.8 / 27.6 | 55.9 / 44.7 / 37.2 / 27.9 | 56.8 / 45.4 / 37.9 / 28.4 |

CNC swing figures exclude gap-through losses. A strategy whose stops gap by an average of 0.5% would add about 0.06–0.17R to c on losing trades (0.17R at a 3% stop, 0.06R at an 8% stop).

Nifty option buy (1 lot of 65, stop 3.08 points), break-even win rate at 1:1 / 1:1.5 / 1:2 / 1:3:

| Premium | No slippage | 0.5 pt RT (+0.16R) | 1 pt RT (+0.33R) | 2 pt RT (+0.65R) |
|---|---|---|---|---|
| ₹100 | 65.7 / 52.5 / 43.8 / 32.8 | 73.8 / 59.1 / 49.2 / 36.9 | 82.0 / 65.6 / 54.6 / 41.0 | 98.2 / 78.6 / 65.5 / 49.1 |
| ₹50 | 63.8 / 51.0 / 42.5 / 31.9 | 71.9 / 57.5 / 47.9 / 35.9 | 80.0 / 64.0 / 53.4 / 40.0 | 96.3 / 77.1 / 64.2 / 48.2 |
| ₹20 | 62.6 / 50.1 / 41.7 / 31.3 | 70.7 / 56.6 / 47.2 / 35.4 | 78.9 / 63.1 / 52.6 / 39.4 | 95.2 / 76.1 / 63.4 / 47.6 |

What these costs mean for the 10R (₹2,000) trial stop: with zero gross edge, the expected number of trades to lose 10R is about 10 ÷ c. This ignores variance; with real variance, a run of losses usually hits the stop sooner.

| Setup | Fees only | + S2 slippage | + S3 slippage |
|---|---|---|---|
| MIS, 0.3% stop | ~28 trades | ~15 | ~8 |
| MIS, 0.5% stop | ~47 | ~24 | ~14 |
| MIS, 1% stop | ~94 | ~48 | ~28 |
| MIS, 2% stop | ~188 | ~97 | ~56 |
| CNC, 3% stop | ~66 | ~54 | ~43 |
| CNC, 5% stop | ~83 | ~71 | ~58 |
| CNC, 8% stop | ~96 | ~85 | ~74 |

Conclusions for this account:
- Costs alone (before any edge or variance) would use up most of a 10R trial within 15–30 tight-stop intraday trades.
- Wider-stop intraday setups (1–2%) and CNC swing setups (3–8% stops) cost about 0.1–0.2R per trade all-in. They are the only formats here where a realistic book-setup edge of a few tenths of an R could survive costs.
- Option buying at ₹200 risk has fixed costs of 0.25–0.31R plus fast premium moves during a manual delay (an ATM Nifty option moves several points a minute; my estimate). In practice it behaves like the 0.3% intraday case.
- Paper trades must record the R-multiple net of all of the above. A setup should not be promoted unless its net expectancy is above zero after at least S2 slippage.

### Gaps
- Real break-even rates depend on how trades actually exit (scratches, time stops, partial exits, each of which costs c with no win). The tables assume a clean win or loss at the target or stop.
- Gap-through statistics for swing stops in NSE stocks were not found. Measure them from data, for example how often and how far the next open lands beyond the stop.
- SEBI's studies on intraday and F&O trader losses and costs (I recall a July 2024 intraday study and Sept 2024 / July 2025 F&O studies) would show how costs bite in practice, but could not be checked because the search budget ran out.

## Q5. How is each segment taxed, and did the new Income-tax Act 2025 (effective April 2026) change anything?

### Takeaway
- **Intraday equity:** speculative business income, taxed at slab rates. Losses can only be set off against speculative income and carried forward for 4 years (old Act s.73, new Act s.113).
- **F&O:** non-speculative business income, taxed at slab rates. Losses can be carried forward for 8 years.
- **Delivery equity:** STCG at 20% (holding up to 12 months); LTCG at 12.5% above ₹1.25 lakh a year. Budget 2026 left these rates unchanged and did not touch the trading classifications. The section 87A rebate does not cover special-rate STCG/LTCG under the new regime.
- **Income-tax Act 2025 (from 1 Apr 2026):** renumbered the sections (44AB → s.63; 44AD/44ADA/44AE → s.58; 234B/C → s.424/425) and introduced the "tax year". It did not change how trading income is classified or the carry-forward periods.
- **ITR-3** is needed whenever there is intraday or F&O income.
- **Tax audit** applies above ₹10 crore turnover when at least 95% of transactions are non-cash (true for trading), or under the presumptive-income rules. At this account's size, turnover will be in the lakhs at most.

### Cited Findings
**Classification and losses**
- Intraday is speculative; F&O is non-speculative business income. The Income Tax Act 2025 replaced the 1961 Act from 1 April 2026 with "no change in F&O and intraday classifications". — [Groww: how traders are taxed (AY 2026-27)](https://groww.in/blog/how-traders-are-taxed-in-india); [AllIndiaITR](https://www.allindiaitr.com/fno-intraday-trading-income-tax) (secondary)
- Speculative losses can be set off only against speculative profits and carried forward 4 years (s.73(4) of the old Act / s.113 of the 2025 Act). The Income Tax Department page confirms that s.113 of the 2025 Act covers "set off and carry forward of losses computed in respect of speculation business". — [Income Tax Department, s.113](https://www.incometaxindia.gov.in/w/section-113-98); [Patron Accounting](https://www.patronaccounting.com/blog/speculative-business-losses-section-73-rules)
- Non-speculative (F&O) business losses carry forward 8 years. Losses must be carried forward by filing the return on time. — [Patron Accounting: set-off mapping under the 2025 Act](https://www.patronaccounting.com/blog/set-off-losses-income-tax-act-2025-section-mapping); [Sahi: advance tax for traders](https://www.sahi.com/blogs/advance-tax-for-traders-fno-intraday-rules-fy-2026-27)
- F&O losses can be set off against intraday (speculative) profit, but not the other way round. — [FnOTax guide](https://fnotax.pages.dev/articles/fo-loss-set-off-against-intraday-profit-the-2026-tax-guide/) (secondary)

**Delivery capital gains**
- STCG on listed equity (s.111A) is 20% and LTCG (s.112A) is 12.5% (rates set in July 2024). The s.112A exemption of ₹1.25 lakh is applied first. — [Harun Raaj on 87A and capital gains](https://www.harunraaj.com/blog/section-87a-rebate-new-regime-capital-gains); [ClearTax STCG](https://cleartax.in/s/short-term-capital-gains-stcg-tax)
- Union Budget 2026 made no change to LTCG rates. Listed-equity LTCG stays at 12.5% with the ₹1.25 lakh carve-out, STCG stays at 20%, and the long-term threshold is still 12 months. The notable Budget 2026 change was that buybacks are now taxed as capital gains. — [Business Standard](https://www.business-standard.com/budget/news/budget-2026-ltcg-tax-rates-unchanged-for-fy27-fm-sitharaman-126020100424_1.html); [Angel One](https://www.angelone.in/news/taxation/union-budget-2026-ltcg-tax-unchanged-at-12-5-stt-on-commodity-futures-hiked)
- Intraday profits are business income, not STCG. — [search extract, Precize/Sahi Budget 2026 pages](https://www.precize.in/blogs/capital-gains-tax-on-shares-in-india-ltcg-stcg-rates-holding-periods-and-budget-2026)
- One STCG calculator page claims Budget 2026 raised STCG. That conflicts with all the other sources and should be treated as unreliable. — [StockCalc STCG](https://stockcalc.in/calculator/stcg-calculator)

**Section 87A rebate (new regime)**
- Finance Act 2025 raised the rebate to ₹60,000 for total income up to ₹12 lakh (from FY 2025-26). It excluded special-rate income (s.111A STCG, s.112A LTCG) from the rebate. Capital gains still count toward the ₹12 lakh test. — [Harun Raaj](https://www.harunraaj.com/blog/section-87a-rebate-new-regime-capital-gains); [FirstReports](https://www.firstreports.in/blog/section-87a-rebate-capital-gains-stcg-ltcg-2025-26); [TaxGarden](https://taxgarden.in/blog/section-87a-rebate-ay-2026-27-eligibility-limit)

**Turnover, tax audit and presumptive income**
- Under the 2025 Act, s.44AB becomes s.63 and s.44AD/44ADA/44AE are folded into s.58. Audit thresholds:
  - Business turnover above ₹1 crore.
  - The higher ₹10 crore limit applies only if both cash receipts and cash payments are each ≤5% of the totals.
  - Sources: [Fintrac Advisors](https://fintracadvisors.com/tax-audit-under-section-63-of-the-income-tax-act-2025-turnover-thresholds-5-cash-test-and-compliance-guide/); [Regitom](https://www.regitom.com/tax-audit-section-44ab-ay-2026-27-complete-guide); [Wikipedia: Income-tax Act 2025](https://en.wikipedia.org/wiki/Income-tax_Act,_2025)
- Presumptive scheme: an audit is needed if declared profit is below the deemed rate and total income exceeds the basic exemption (s.58(3)). Commentary notes that the s.63(1) table appears to lack the basic-exemption safeguard; this is unresolved. — [Verotus LLP](https://www.verotusllp.com/2026/08/tax-audit-under-section-63-of-income.html); [Fintrac Advisors](https://fintracadvisors.com/tax-audit-under-section-63-of-the-income-tax-act-2025-turnover-thresholds-5-cash-test-and-compliance-guide/)
- Under the new regime, one Form 26 (Parts A–D) replaces Forms 3CA/3CB/3CD. For tax year 2026-27 the audit report is due by 30 Sep 2027. — [Fintrac Advisors / search extract](https://fintracadvisors.com/tax-audit-under-section-63-of-the-income-tax-act-2025-turnover-thresholds-5-cash-test-and-compliance-guide/)
- **How turnover is computed (ICAI guidance, via secondary sources):** for F&O, turnover = absolute profits + absolute losses (not contract value); intraday uses the same basis per scrip per day. Sources disagree on whether premium received on options sold is included. — [TaxGuru: F&O turnover for 44AB](https://taxguru.in/chartered-accountant/fo-derivative-turnover-calculation-tax-audit-section-44ab.html); [FnOTax](https://fnotax.com/articles/fo-turnover-calculation-tax-audit-limits-ay-2026-27-guide/)
- **Which ICAI guidance edition applies:** sources cite the 8th edition (Aug 2022), a "Revised 2025" or "Revised 2026" edition, and an ICAI exposure draft of a revised guidance note issued 9 Jul 2026 (comments due 25 Jul 2026). — [ICAI exposure draft](https://www.icai.org/post/icai-dtc-exp-draft-09072026); [CAalley](https://www.caalley.com/reference-updates/icai-guidance-note-on-tax-audit-u-s-44ab-of-the-income-tax-act-1961-revised-2026-edition); [TaxGuru](https://taxguru.in/income-tax/icai-issues-exposure-draft-revised-section-44ab-tax-audit-guidance-note.html)

**Returns and advance tax**
- ITR-3 is the form for intraday or F&O (business) income. — [TaxSocial](https://taxsocial.pro/article/fno-intraday-trading-taxation-ay-2026-27-itr-3-audit-44ad); [TaxGarden](https://taxgarden.in/blog/fno-intraday-trading-tax-itr-audit-india)
- Advance tax instalments (cumulative): 15 Jun 15%, 15 Sep 45%, 15 Dec 75%, 15 Mar 100%. It is required if tax after TDS exceeds ₹10,000; brokers deduct no TDS on intraday or F&O profits. Old s.234B/234C are now s.424/425 with interest unchanged (generally 1% a month). — [JM Financial](https://www.jmfinancialservices.in/blogs-and-articles/advance-tax-deadline-fy-2026-27-who-is-exempt-and-who-should-pay); [Sahi](https://www.sahi.com/blogs/advance-tax-for-traders-fno-intraday-rules-fy-2026-27); [Zerodha Z-Connect: advance tax](https://zerodha.com/z-connect/console-3/all-you-need-to-know-about-advance-tax); [Quicko 234B](https://learn.quicko.com/non-payment-of-advance-tax-section-234b)
- The new Income-tax Act and the higher F&O STT both started on 1 Apr 2026 (FY 2026-27). — [Free Press Journal](https://www.freepressjournal.in/business/new-income-tax-act-from-april-1-higher-stt-on-fo-and-20-year-data-centre-tax-holiday-begin-with-fy27)

### Inferences
- **Which Act applies to which year:**
  - Income earned from 1 Apr 2026 falls under the 2025 Act (tax year 2026-27), with its return filed in 2027.
  - FY 2025-26 income (AY 2026-27) is still governed by the 1961 Act.
  - Code references should carry both section numbers, e.g. "s.73 / s.113", "s.44AB / s.63", "s.234C / s.425".
- **Per-segment tax rules for tradingtool:**
  - MIS intraday P&L → speculative bucket, taxed at the slab rate. Net speculative loss carries forward 4 years against speculative profit only.
  - Options and futures P&L → non-speculative business bucket, taxed at the slab rate. Net loss can be set off against other non-salary income in the year (s.71(2A) rule, from memory; see Gaps), then carried forward 8 years against business income.
  - CNC sells held ≤12 months → STCG at 20% plus cess.
  - CNC sells held >12 months → LTCG at 12.5% on gains above ₹1.25 lakh.
  - MTF trades are delivery trades, so the same capital-gains treatment applies. A trader whose delivery activity is frequent and short-term may face scrutiny that treats it as business income; treat this as a judgement call.
- **The rebate treats intraday/F&O profit differently from delivery gains.** Under the new regime the 87A rebate applies to normal-rate income, so intraday and F&O profit for someone whose total income is ≤ ₹12 lakh may be fully rebated. Delivery STCG is taxed at 20% even then, because special-rate income is excluded from the rebate.
- **Audit and advance tax are unlikely to matter at this scale.** Turnover is absolute P&L: 300 trades averaging ±₹250 is about ₹75,000, nowhere near ₹1 crore or ₹10 crore. Audit is a risk only if the trader opts into presumptive taxation (s.44AD / s.58) and later declares profit below the deemed rate with income above the exemption limit; with losses, do not opt into s.44AD. Advance tax applies only if extra tax on trading profit, after salary TDS, exceeds ₹10,000.
- **Business-income traders should still file ITR-3 on time, even with a loss.** It preserves the 4-year and 8-year loss carry-forwards. STT on business-income trades is generally deductible as a business expense (old s.36(1)(xv); from memory, see Gaps). Capital-gains trades get no such deduction.

### Gaps
- **New-regime slabs:** I recall nil up to ₹4 lakh, 5% for ₹4–8 lakh, 10% for ₹8–12 lakh, 15% for ₹12–16 lakh, 20% for ₹16–20 lakh, 25% for ₹20–24 lakh and 30% above ₹24 lakh, plus 4% cess, from Finance Act 2025. Not verified this session, and Finance Act 2026 slab changes, if any, were not checked.
- **New-Act section numbers:** the exact numbers for the speculation definition (reported as s.66(31)/(33)) and for carrying forward non-speculative losses were not confirmed from the statute.
- **Rules recalled but not verified:**
  - Losses arising before 2026 keep their original character (reported as s.536 of the 2025 Act; the source page was not confirmed).
  - Non-speculative losses can be set off against any head except salary.
  - STT is deductible for business-income trades.
  - Capital-loss set-off (STCL against STCG or LTCG; LTCL only against LTCG; 8-year carry-forward).
- **Return due date (non-audit):** sources conflict for AY 2026-27, giving 31 Jul 2026 or 31 Aug 2026 (the latter said to be via Finance Act 2026). ITR forms for tax year 2026-27 under the new Act were not checked.
- **ICAI turnover guidance:** which edition is final for 2026-27, and whether option-sale premium counts toward turnover, could not be read from ICAI directly.
- **234C proviso:** not verified. I recall that shortfalls caused by capital gains arising after an instalment date are excused if paid in the next instalment, and that this does not cover speculative or F&O income.
