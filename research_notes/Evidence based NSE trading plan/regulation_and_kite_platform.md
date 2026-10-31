# Indian regulation and Zerodha Kite Connect platform limits for a data-only NSE setup scanner (status at 31 Oct 2026)

How these notes were gathered: full-page fetches were blocked from this session for kite.trade, support.zerodha.com and taxguru.in (DNS/policy denial), and the session's shared web-search budget ran out before a final verification pass. Kite docs, Zerodha support pages and circular reproductions were therefore read through search-engine extracts, not as full text, and several primary SEBI/NSE PDFs were not opened. Tags: **[2025]** / **[2026]** mark changes made in that year. **[unverified]** marks a claim from one source or a weak source, or one not checked against the primary text. Context used for the inferences: ₹20,000 capital, ₹200 risk per trade (1R), trial stops at a ₹2,000 drawdown (10R), every order placed by hand in Kite, and a Python tool that only reads data.

## Q1. SEBI's Feb-2025 retail-algo framework and the exchange/broker rules that implement it: does a data-only tool with manual orders fall under it, and what do brokers now require for API access?

### Takeaway
The framework is built around **orders sent through an API**. NSE's FAQ treats every order received via API as an algo order, and registration, algo-ID tagging, the 10-orders-per-second threshold and static-IP whitelisting all apply to those orders. A tool that only streams and pulls data and never places, modifies or cancels orders through the API sits outside the parts that bind. Zerodha requires a static IP from 1 Apr 2026, but only for order placement. The WebSocket and the other non-order APIs work from any IP. What still applies is a daily authenticated login (the token dies at about 6 AM the next day) and Kite Connect's personal-use, no-redistribution terms. The framework became fully applicable on **1 Apr 2026**, after two postponements **[2025]**.

### Cited Findings
**The SEBI circular and its timeline**
- The circular is **SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013, dated 4 Feb 2025**, "Safer participation of retail investors in Algorithmic trading" — [Mondaq](https://mondaq.com:443/india/commoditiesderivativesstock-exchanges/1581380/sebi-circular-safeguarding-retail-investors-in-algorithmic-trading); [IndiaLaw](https://www.indialaw.in/blog/civil/sebi-retail-investors-algorithmic-trading/). One newsletter cites the number as ".../2025/51" — [Mondaq newsletter May 2025](https://www.mondaq.com/india/securities/1622512/general-newsletter-may-2025).
- Core provisions, as law-firm summaries describe them:
  - open APIs are prohibited;
  - API access is allowed only through a unique vendor-client-specific API key and a static IP that the broker whitelists;
  - OAuth-based authentication and two-factor authentication are mandatory for API access;
  - every algo order flowing through an API is tagged with a unique identifier issued by the exchange;
  - "tech-savvy retail investors" who build their own algos must register them with the exchange through their broker **only if they exceed a specified orders-per-second threshold**.
  
  Sources: [IndiaLaw](https://www.indialaw.in/uncategorized/sebi-retail-investors-algorithmic-trading); [Mondaq](https://mondaq.com:443/india/commoditiesderivativesstock-exchanges/1581380/sebi-circular-safeguarding-retail-investors-in-algorithmic-trading).
- A registered self-built algo may be used by the investor and by their spouse, dependent children and dependent parents, and no one else — [Finsec Law Advisors](https://finseclaw.com/article/finsec-tracker-on-sebi-issues-guidelines-on-retail-participation-in-algorithmic-trading).
- Brokers stay the primary point of contact for client grievances. Exchanges keep supervising algo trading, including making sure brokers can tell algo orders from non-algo orders — [QuantInsti summary](https://blog.quantinsti.com/sebi-algo-trading-guidelines-retail-investors).
- Timeline:
  - The original effective date was 1 Aug 2025 — [5paisa](https://www.5paisa.com/news/nse-issues-new-compliance-standards-for-retail-algo-trading-from-august-2025).
  - SEBI circular **SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/108 of 29 Jul 2025** extended the timeline **[2025]** — [Taxscan copy](https://images.taxscan.in/feeds/2025/07/31/2071293-algotradingsafetymeasureswatermark.pdf).
  - A **SEBI circular of 30 Sep 2025** set a glide path, with full applicability from **1 Apr 2026** **[2025]** — [SEBI PDF](https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf); [Business Standard, 1 Oct 2025](https://www.business-standard.com/markets/news/sebi-extends-timeline-to-roll-out-algo-trading-rules-for-retail-investors-125100100278_1.html).
- Glide-path milestones for brokers:

  | Date | What brokers had to do |
  |---|---|
  | 31 Oct 2025 | Apply to register at least one retail algo product or strategy |
  | 30 Nov 2025 | Finish registering their retail algo products and strategies, in-house and vendor |
  | From 5 Jan 2026 | Brokers who missed the milestones may not onboard new retail clients for API-based algo trading |
  | 1 Apr 2026 | The whole framework applies, including the exchanges' operational modalities |

  Sources: [Upstox News](https://upstox.com/news/market-news/financial-regulations/sebi-extends-timeline-for-retail-algo-trading-framework-sets-glide-path-for-brokers/article-182285/); [Bajaj Broking](https://www.bajajbroking.in/share-market-news/sebi-extends-algo-trading-implementation-timeline); [BSE milestone notice of 24 Nov 2025 (mirror)](https://rhnvrm.github.io/stock-market-circulars/circulars/bse/2025/bse-2025-11-24-e6eac9e12bd239db-adherence-to-milestones-and-the-rules-related-to-retail-algo/).

**NSE implementation standards and later circulars**
- NSE's **implementation standards, NSE/INVG/67858 of 5 May 2025** **[2025]**, as secondary summaries describe them:
  - the threshold is **10 orders per second (OPS) per exchange**;
  - each client using API access must link a **static IP** (one, with a backup allowed), which can be **changed no more than once per calendar week**;
  - several API keys can map to one client;
  - **every API session must be logged out daily**.
  
  Sources: [javajack deep dive](https://javajack.github.io/broking-kyc/deep-dives/trading-day/retail-algo-framework/); [Flattrade](https://flattrade.in/kosh/?p=42319); [Finsec Law on NSE standards](https://www.finseclaw.com/article/nse-releases-implementation-standards-for-retail-participation-in-algorithmic-trading); [Kotak Securities](https://www.kotaksecurities.com/investing-guide/articles/retail-algo-trading-rules-nse-circular).
- Zerodha's reading of the NSE circular:
  - only one API key per user may run an unregistered algo below 10 OPS, and extra keys don't get around this;
  - the static-IP rule comes from SEBI, so moving to another broker doesn't avoid it;
  - every algo order carries an Algo ID, registered or not.
  
  Source: [Zerodha Z-Connect overview](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework).
- Later NSE circulars **[2025]**:
  - **NSE/INVG/69255 of 22 Jul 2025** set the operational modalities for empanelling algo providers and registering retail algo strategies — [X post quoting the circular](https://x.com/algotradingdesk/status/1949680634840105411).
  - A corrigendum, **NSE/INVG/70309 of 19 Sep 2025**, adjusted some clauses — [Complinity](https://complinity.com/legal-update/nse-corrigendum-to-safer-participation-of-retail-investors-in-algorithmic-trading-detailed-operational-modalities--20275/).
- **NSE FAQ of 3 Nov 2025** (read through a search extract):
  - "all orders received via API from clients are considered algo orders", citing NSE/INVG/69255;
  - under 69255, algos must run on the broker's servers;
  - in that hosted context, the static IP named in 67858 is the trading member's server IP.
  
  Source: [NSE FAQ PDF](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAQ_Retail%20Algo_03112025_NSE.pdf).
- Sources disagree on hosting: all retail algos on Indian servers ([AlgoBulls](https://algobulls.com/blog/industry-insights-and-updates/sebi-new-algotrading-regulations-for-retail-investors-2026)) versus on exchange-approved servers ([Kotak Neo](https://www.kotakneo.com/investing-guide/articles/retail-algo-trading-rules-nse-circular)).
- **[2026]** NSE's algo page points members who offer algo access to retail investors under the **"Client Direct API" category** to document requirements in **NSE/INVG/73992 of 30 Apr 2026** — [NSE algo trading page](https://www.nseindia.com/static/trade/platform-services-non-neat-decision-support-tools-algorithm-trading). AlgoBulls says the Client Direct API definition was widened to cover broker front-ends and web and mobile apps, not only raw API access — [AlgoBulls](https://algobulls.com/blog/industry-insights-and-updates/sebi-new-algotrading-regulations-for-retail-investors-2026) **[unverified]**.

**What brokers now require for API access**
- **Zerodha [2026]:** "effective 1 April 2026, you must have a static IP for API-based order placement". The requirement covers all API-based order placement under NSE/SEBI algo rules. **The WebSocket market-data stream and other APIs, such as orderbook and positions, can still be reached from any IP address** — [Zerodha support: Static IP](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip). Zerodha staff on the forum: the static IP will apply only to the order place/modify/cancel endpoints — [Kite forum: static IP for data-only use](https://kite.trade/forum/discussion/15359/query-regarding-static-ip-requirement-for-kite-connect-api-data-only-usage).
- **Ventura [2026]:** from 1 Apr 2026, algo or API orders are accepted only from the client's registered primary static IP — [Ventura](https://www.venturasecurities.com/blog/whats-changing-in-venturas-easeapi-access-from-april-1-2026/).
- **Angel One [2026]:** published "What's changing in SmartAPI access from April 1, 2026". The content was not retrieved — [Angel One](https://www.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026).
- **ICICI Breeze:** orders must come from the static IP registered with ICICI Direct, with a combined cap of 10 orders per second — [breeze-connect on PyPI](https://pypi.org/project/breeze-connect/).
- **Kite Connect:** by default it serves a single user. Multi-user access needs approval from Zerodha compliance — [Kite forum: API rate limits](https://kite.trade/forum/discussion/comment/51556).

### Inferences
- tradingtool streams data, calls Claude, keeps an internal paper-trade log and leaves every real order to be typed into the Kite app. It produces **no API orders**, so on the order-centric definitions above it is not an algo: no registration, no algo ID, no OPS budget and no static IP. A dynamic home IP on the Mac works for the WebSocket and for historical data.
- The line that matters is **any order call through the API**. Once the tool places, modifies or cancels even one order via Kite Connect (a "one-click execute" button, say), the trader moves into the static-IP regime (a fixed ISP IP or a VPS, changeable at most weekly), Algo-ID tagging, the one-key rule for unregistered algos under 10 OPS, and the daily-logout rules. Keeping the tool order-free is the cheapest way to stay outside the framework.
- The daily-logout and authentication rules still shape the tool's design. It needs a daily manual login step (see Q5), and after each new token it has to build a fresh ticker.

### Gaps
- None of the primary SEBI or NSE PDFs (the 4 Feb 2025 circular, 67858, 69255, 70309, 73992 or the FAQ) was opened in full. The details above come from summaries and search extracts.
- The new deadline set by the 29 Jul 2025 extension is not in the extracts (it is believed to be 1 Oct 2025; **[unverified]**).
- One secondary source reports an NSE extension circular "NSE/INVG/70541" moving the date to 1 Apr 2026, but the page could not be identified. A 3 Jan 2026 "mock session" milestone appears in only one secondary source.
- I found no official SEBI, NSE or Zerodha text that explicitly addresses **data-only** API keys. The conclusion rests on the order-centric definitions and on Zerodha's statement that only order placement needs a static IP.
- Not found: how compliance and enforcement went after 1 Apr 2026, and the requirements in NSE/INVG/73992.
- Not researched: whether orders started from Kite Publisher or basket links (the user confirms them inside Kite's UI) count as API or algo orders.
- Not verified: the circular's requirement, as I recall it, that **black-box** algo providers register as Research Analysts.

## Q2. Intraday margin and leverage under the peak-margin rules, Zerodha MIS leverage and auto square-off times, intraday short selling and short-delivery penalties

### Takeaway
Since 1 Sep 2021 brokers must collect **100% of exchange-prescribed margins upfront**: VaR plus ELM in the cash segment, and SPAN plus exposure in F&O. Compliance is checked against the highest of four random intraday snapshots. Intraday equity leverage is therefore at most 1/(VaR+ELM), which is **5x at the 20% floor**. **F&O gets no extra intraday leverage.**

At Zerodha, MIS gives up to 5x on equities and 1x (NRML margin) on F&O. Auto square-off now runs at **3:25 PM for equity and 3:26 PM for F&O**, moved from 3:20 PM and 3:25 PM around December 2025 **[2025]**, and costs **₹50 + 18% GST per order**.

Retail investors may short-sell, intraday included. Naked short selling is banned. An intraday short that cannot be covered (for example, the stock locks in its upper circuit) becomes a **short delivery**: the shares go to a T+1 auction, and a failed auction is closed out at the higher of the highest price from the trade day to the auction day, or **20% above the auction-day close**.

### Cited Findings
**Peak-margin framework**
- The framework comes from the SEBI circular of **20 Jul 2020 (SEBI/HO/MRD2/DCAP/CIR/P/2020/127)**. Peak-margin reporting began on 1 Dec 2020 and was phased up to **100% from 1 Sep 2021**:

  | Phase | Share of peak margin required |
  |---|---|
  | From 1 Dec 2020 | 25% (from prior knowledge; not in the extracts, **[unverified]**) |
  | Next phase | 50% |
  | June 2021 | 75% |
  | From 1 Sep 2021 | 100% |

  Sources: [Business Standard, 20 Jul 2020](https://www.business-standard.com/article/markets/market-regulator-issues-guidelines-on-leveraged-intra-day-trades-120072001421_1.html); [Moneylife explainer](https://moneylife.in/article/explainer-how-sebis-new-peak-margin-norms-impact-traders-from-1st-september/64993.html); [5paisa](https://5paisa.com/blog/peak-margin-rules-sebi-100percent-from-september-1st).
- Clearing corporations take four random margin snapshots a day, and the highest becomes the peak-margin requirement. Clients must post 100% of VaR and ELM upfront, and brokers can no longer lend against those components — [Angel One](https://www.angelone.in/news/market-updates/sebi-peak-margin-norms-to-kick-in-from-september-1); [Moneylife](https://moneylife.in/article/explainer-how-sebis-new-peak-margin-norms-impact-traders-from-1st-september/64993.html).
- SEBI relaxed how peak margins are calculated in 2022 after brokers lobbied for it — [Business Standard, May 2022](https://www.business-standard.com/amp/article/markets/relief-for-brokers-as-sebi-relaxes-norms-for-calculating-peak-margins-122051100516_1.html). The details were not retrieved.
- On the leverage cap, one source gives **5x** for intraday equity — [Bajaj Finserv](https://www.bajajfinserv.in/sebi-new-margin-rules-intraday-trading). A broker's phase-4 table gives **4x** for stocks whose margin requirement is above 20% and below 25%, and **3x** above 25% — [PhillipCapital intraday leverage table](https://m.phillipcapital.in/uploads/pdf/phillip-9/Intraday_Leverages.pdf). Both fit a cap of 1/(VaR+ELM) with a 20% floor.

**Zerodha MIS leverage and auto square-off**
- Leverage:
  - Zerodha offers **up to 5x (20% margin)** for intraday equity through MIS and Cover Orders — [Zerodha support: margins/leverage](https://support.zerodha.com/category/trading-and-markets/margin-leverage-and-product-and-order-types/articles/how-much-margins-leverage-does-zerodha-provide).
  - Index and stock F&O get **1x, i.e. 100% of NRML margin (SPAN + Exposure)** — [Zerodha bulletin, 26 Jul 2024](https://zerodha.com/marketintel/bulletin/249809/latest-intraday-leverages-mis-bo-co).
  - Zerodha says that under SEBI's peak-margin rules there is no leverage in equity F&O, currency or commodities — [Zerodha support](https://support.zerodha.com/category/trading-and-markets/margin-leverage-and-product-and-order-types/articles/how-much-margins-leverage-does-zerodha-provide).
- **[2025]** Auto square-off times:

  | Segment | Old time | Current time |
  |---|---|---|
  | Equity intraday (MIS) | 3:20 PM | 3:25 PM |
  | F&O intraday | 3:25 PM | 3:26 PM |

  Zerodha's help page lists the current times and says they "are subject to change" and are posted on zerodha.com/marketintel/bulletin — [Zerodha support: intraday auto square-off timings](https://support.zerodha.com/category/trading-and-markets/trading-faqs/market-sessions/articles/intraday-auto-square-off-timings). A Z-Connect update dated **26 Dec 2025** records the change — [Z-Connect](https://zerodha.com/z-connect/updates/changes-to-the-auto-square-off-timings-for-equity-and-fo). Some older Zerodha pages still show 3:20 PM and 3:25 PM.
- Auto square-off costs **₹50 + 18% GST per order squared off**. At most 30,000 units go out in each auto square-off order, so large positions can be charged more than once — [Zerodha support: auto square-off charges](https://support.zerodha.com/category/account-opening/charges-at-zerodha/articles/auto-square-off).

**Short selling and short delivery**
- The **Framework for Short Selling** is SEBI circular **SEBI/HO/MRD/MRD-PoD-3/P/CIR/2024/1, dated 5 Jan 2024**:
  - all classes of investors, retail and institutional, may short sell;
  - **naked short selling is prohibited**, and every investor must deliver at settlement;
  - institutional investors must disclose upfront when they place a short-sell order, and may not day-trade.
  
  Sources: [Moneylife](https://www.moneylife.in/article/sebi-allows-short-selling-by-all-investors-ban-on-naked-short-selling-continues/73065.html); [IndiaCorpLaw](https://indiacorplaw.in/2024/02/03/navigating-the-maze-scrutinising-sebis-framework-for-short-selling/); [TeamLease RegTech](https://www.teamleaseregtech.com/updates/article/28961/sebi-issued-a-circular-regarding-the-framework-for-short-selling/); [Businessworld](https://businessworld.in/article/sebi-regulates-short-selling-trades-prohibits-naked-short-selling-504909).
- Short delivery: Zerodha lists, as one cause, an intraday short that cannot be squared off because the stock is locked in its upper circuit. The clearing corporation runs an **auction on T+1**. If the auction fails, the account is credited cash at the close-out price, and Zerodha blocks a **120% short-delivery margin** on T day — [Zerodha support: short delivery](https://support.zerodha.com/category/trading-and-markets/trading-faqs/general/articles/what-is-short-delivery-and-what-are-its-consequences).
- The close-out rate is the **higher of the stock's highest price from the trade date to the auction day, or 20% above the auction-day (T+1) close**. Equity delivery settles T+1 — [Z-Connect: consequences of short delivery](https://zerodha.com/z-connect/trending/consequences-of-short-delivery-nse-bse).
- **[2026]** SEBI added a **Closing Auction Session (CAS)** to the equity cash segment by circular dated **16 Jan 2026**; it went live on **3 Aug 2026**. A **15 Oct 2026** circular revises it to a 3:30–3:40 PM auction, effective **7 Dec 2026** (more under Q3) — [Angel One](https://www.angelone.in/news/market-updates/sebi-revises-equity-market-closing-auction-rules-retains-30-minute-vwap-for-expiry); [Outlook Business](https://www.outlookbusiness.com/markets/sebi-revises-closing-auction-session-rules-retains-30-minute-vwap-settlement-method).

### Inferences
- **Intraday (MIS) sizing for ₹20k:** buying power is about ₹1,00,000 in stocks with a 20% margin, and less in more volatile names.
  - At 1R = ₹200, the position size is ₹200 divided by the stop distance.
  - A 0.5% stop gives a ₹40,000 position, needing about ₹8,000 of margin. A 0.25% stop gives ₹80,000, needing about ₹16,000.
  - Stops tighter than about 0.2% would need more than ₹1 lakh of exposure, so they cannot be sized to a full 1R.
  - The cap is per account, so two simultaneous 0.25%-stop trades don't fit.
- **The auto square-off fee is large against 1R:** ₹59 per order is about 0.3R. The trader (and any paper-trade rules in the tool) should treat 3:20 PM as the last exit for MIS positions.
- **Swing (CNC) has no leverage:** with ₹20k the largest position is ₹20k. At 1R = ₹200 the stop must be at least 1% away, which is easy for swing setups. Short swings are not possible in the cash segment, because overnight shorts need delivery or stock borrowing (SLB) and must not be naked.
- **Intraday shorts carry tail risk:** if the stock locks in its upper circuit, the auction close-out can cost up to 20% or more above the close, far beyond 1R. The tool could stop flagging shorts in stocks near their upper circuit band, in thinly traded names, and in names in trade-to-trade or ASM/GSM surveillance categories.
- From 3 Aug 2026 the official cash close comes out of the CAS. Backtests and replays that use the "close" price, or end-of-day exits, should account for the regime change (reference prices change again on 7 Dec 2026).

### Gaps
- Not confirmed: whether **retail** short sellers must disclose by end of day under the Jan 2024 framework (none of the extracts mention it), and the details of the 2022 peak-margin relaxation.
- Not found: the exact effective date of Zerodha's equity move from 3:20 PM to 3:25 PM, and whether the CAS (from 3 Aug 2026) led to any further change in square-off times.
- Not researched: per-stock MIS margins (Zerodha publishes a daily list), MTF terms, and current exchange auction-penalty circulars.

## Q3. SEBI's October 2024 F&O measures and the 2025–2026 changes that matter to a small account

### Takeaway
Since late 2024, equity derivatives have moved steadily out of a small account's reach:
- **Index contracts must be worth at least ₹15 lakh at launch** (₹15–20 lakh band).
- One weekly expiry per exchange (Nifty, on **Tuesdays** since 1 Sep 2025).
- Option premium is collected upfront, and calendar-spread benefit is removed on expiry day.
- An extra expiry-day ELM applies, and position limits are monitored intraday.
- **[2025]** Delta-based OI and new position limits took effect, and Nifty and Bank Nifty lots were cut (Nifty 65, Bank Nifty 30).
- **[2026]** STT on futures and options rose from 1 Apr 2026, and a Closing Auction Session arrived (live 3 Aug 2026, revised from 7 Dec 2026).

On ₹20,000, futures and short options are impossible because of margin. Only long options fit, with a ₹200 1R allowing just a few rupees of premium per unit.

### Cited Findings
**The October 2024 circular**
- The circular is **SEBI/HO/MRD/TPD-1/P/CIR/2024/132, dated 1 Oct 2024**, "Measures to strengthen Equity Index Derivatives framework". Its measures:
  - weekly index derivatives rationalised to one benchmark index per exchange;
  - option premium collected upfront from buyers;
  - larger contract sizes;
  - calendar-spread benefit removed on expiry day;
  - additional ELM on expiry day;
  - intraday monitoring of position limits.
  
  Sources: [Business Standard](https://www.business-standard.com/amp/markets/capital-market-news/sebi-tightens-norms-for-equity-derivatives-trading-124100300354_1.html); [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing); [Gale.in](https://gale.in/sebi-fo-rules-explained/).
- Contract size: at least **₹15 lakh at launch**, with lot sizes set so the value stays between ₹15 and 20 lakh at review. The previous band, set in 2015, was ₹5–10 lakh. The new size took effect on **20 Nov 2024** (Zerodha says 21 Nov) — [Businessworld](https://businessworld.in/article/sebi-unveils-measures-to-tighten-fo-trading-to-be-effective-in-phases-534994); [TaxGuru circular reproduction](https://taxguru.in/?p=932936); [Zerodha](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing).
- Per the circular text reproduced by TaxGuru: calendar-spread treatment applies **from 1 Feb 2025**, and intraday position-limit monitoring for index derivatives **from 1 Apr 2025** — [TaxGuru](https://taxguru.in/?p=932936).
- NSE kept a weekly expiry only on Nifty 50. Weekly expiries on Bank Nifty, Nifty Financial Services, Nifty Midcap Select and Nifty Next 50 were dropped — [RootNivesh](https://rootnivesh.in/blog/sebi-new-fno-rules-lot-size-weekly-expiry); [Gale.in](https://gale.in/sebi-fo-rules-explained/) (secondary sources).

**2025 changes**
- **[2025] Expiry day:** a SEBI circular of **26 May 2025** required each exchange to pick **Tuesday or Thursday** for its equity-derivative expiries. **NSE moved to Tuesday from 1 Sep 2025** and BSE to Thursday — [5paisa](https://www.5paisa.com/news/sebi-gives-green-light-for-nses-weekly-fo-expiry-shift-to-tuesday); [Business Today, 17 Jun 2025](https://www.businesstoday.in/markets/stocks/story/nse-receives-sebi-nod-for-tuesday-expiry-bse-thursday-480736-2025-06-17); [Bigul on NSE circular 103/2025](https://bigul.co/blog/market-update/revision-of-expiry-day-for-index-and-stock-derivatives-nse-circular-1032025). NSE's earlier Monday proposal was deferred and never implemented — [Angel One](https://www.angelone.in/news/market-updates/nse-delays-expiry-shift-to-monday-in-response-to-sebi-consultation); [Bajaj Finserv](https://www.bajajfinserv.in/nse-revises-nifty-expiry-day).
- **[2025] SEBI circular of 29 May 2025** on risk monitoring in equity derivatives:
  - Open interest is now measured at portfolio level in **delta-based "future-equivalent" terms**.
  - Index-option limits per entity: end of day, **₹1,500 crore net and ₹10,000 crore gross**; intraday, **₹5,000 crore net and ₹10,000 crore gross**.
  - Single-stock MWPL is the lower of **15% of free float or 65× average daily cash volume** (from 1 Oct 2025, per Navia).
  - Once a stock is in the F&O ban, new trades must reduce delta-based OI.
  - Index-futures limits for each participant type are the higher of a fixed rupee amount or a percentage of market-wide OI.
  
  Sources: [Outlook Business](https://www.outlookbusiness.com/markets/sebi-shakes-up-derivatives-game-with-new-rules-for-measuring-open-interest-mwpl); [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-fo-revamp-new-oi-metric-position-limits-july-december-rollout-125052901798_1.html); [Navia](https://navia.co.in/blog/sebis-latest-guidelines-on-fo-trading/); [Value Research](https://www.valueresearchonline.com/stories/224848/sebi-rewrites-fo-rules-to-curb-expiry-day-speculation/). Sources disagree on entity limits for single stocks: individuals at 10% of MWPL ([Bajaj Broking](https://www.bajajbroking.in/blog/sebi-notifies-new-f-and-o-rules-with-higher-index-limits-and-risk-measures)) against mutual funds at 30% and proprietary traders at 20% ([Business Standard](https://www.business-standard.com/markets/capital-market-news/sebi-overhauls-f-o-regulations-to-boost-risk-monitoring-and-market-alignment-125053000758_1.html)).
- **[2025]** NSE started a **pre-open session for equity derivatives (current-month futures) on 8 Dec 2025** — [Business Standard](https://www.business-standard.com/amp/markets/news/nse-pre-open-session-equity-derivatives-december-8-2025-125110401569_1.html). One source gives 6 Dec, which was a Saturday, so that date is likely wrong.
- **[2025] Lot sizes:**
  - Nifty went from 25 to 75 in Nov 2024.
  - A mid-2025 revision took Bank Nifty from 30 to 35 and Midcap Nifty from 120 to 140 — [TradingQnA (Zerodha)](https://tradingqna.com/t/revision-in-lot-size-of-bank-nifty-from-30-to-35-and-midcap-nifty-from-120-to-140/181535).
  - NSE circular **NSE/FAOP/70616 (Oct 2025)** cut **Nifty 75 → 65, Bank Nifty 35 → 30, Fin Nifty 65 → 60 and Midcap Select 140 → 120**.
  - Effective dates differ by source: 28 Oct 2025 EOD ([Angel One](https://www.angelone.in/news/market-updates/nse-reduces-lot-sizes-in-nifty-and-bank-nifty-derivatives); [Bajaj Broking](https://www.bajajbroking.in/share-market-news/nse-revises-lot-sizes-for-index-derivatives)); 30 Dec 2025 EOD for quarterly and half-yearly contracts ([Bigul](https://bigul.co/blog/nse-implements-new-lot-sizes-for-nifty-bank-nifty-and-other-index-derivatives)); January 2026 contracts ([HDFC Sky](https://hdfcsky.com/news/nse-revises-market-lot-sizes-for-major-index-derivatives-effective-january-2026)).

**2026 changes**
- **[2026] STT:** the Union Budget of 1 Feb 2026 raised STT on derivatives from **1 Apr 2026**. Rates on equity delivery are unchanged.

  | Leg | Old rate | New rate |
  |---|---|---|
  | Futures | 0.02% | 0.05% |
  | Options premium | 0.10% | 0.15% |
  | Exercised options (of intrinsic value) | 0.125% | 0.15% |

  Sources: [Business Standard, 1 Feb 2026](https://www.business-standard.com/markets/news/markets-fm-hikes-stt-on-fo-trades-surprise-move-126020100888_1.html); [Business Today](https://www.businesstoday.in/markets/story/stt-hike-on-fo-trades-to-take-effect-from-april-1-trading-costs-to-rise-522428-2026-03-26); [Outlook Money](https://www.outlookmoney.com/invest/stt-hike-from-april-1-2026-budget-what-it-means-for-futures-and-options-traders).
- **[2026] Closing auction and expiry settlement:**
  - SEBI added the CAS by circular of **16 Jan 2026**; it went live on **3 Aug 2026**.
  - Traders and brokers then complained about settlement-price spikes and thin liquidity.
  - SEBI's **15 Oct 2026 circular** sets the CAS at **3:30–3:40 PM**, effective **7 Dec 2026**.
  - The CAS reference price will be the VWAP of the last 15 minutes of continuous trading.
  - **Index-derivative expiry settlement stays at the VWAP of index constituents over the last 30 minutes (3:00–3:30 PM)**. Stock derivatives settle at the underlying's 30-minute VWAP across exchanges.
  
  Sources: [Angel One](https://www.angelone.in/news/market-updates/sebi-revises-equity-market-closing-auction-rules-retains-30-minute-vwap-for-expiry); [Outlook Business](https://www.outlookbusiness.com/markets/sebi-revises-closing-auction-session-rules-retains-30-minute-vwap-settlement-method); [CorpLaw Updates](https://www.corplawupdates.in/updates/sebi-closing-auction-session-final-framework-cas-october-2026-2); [Goodreturns](https://www.goodreturns.in/news/sebi-revises-closing-auction-session-timings-vwap-settlement-rules-011-1541885.html). An earlier panel proposal also floated extending the derivatives trading window to 3:45 PM — [Business Upturn](https://businessupturn.com/finance/stock-market/nse-bse-in-focus-sebi-panel-backs-30-minute-vwap-for-f-o-expiry-settlement-puts-closing-auction-linked-formula-on-hold/).
- In Sep 2025 there was market talk that SEBI might end weekly F&O contracts — [Business Standard](https://www.business-standard.com/markets/capital-market-news/bse-tumbles-on-buzz-sebi-weighs-end-of-weekly-f-o-contracts-125091100596_1.html). The sources found still describe Nifty weekly expiries on Tuesday — [Bajaj Finserv](https://www.bajajfinserv.in/nse-revises-nifty-expiry-day).
- Secondary explainers say SEBI's own studies found more than 9 in 10 individual F&O traders losing money, with losses heaviest in cheap, short-dated options — [Gale.in](https://gale.in/sebi-fo-rules-explained/).

### Inferences
- **Futures and option selling are out of reach on ₹20,000.** Index contracts are worth at least ₹15 lakh, F&O margin is 1x SPAN + Exposure with no MIS leverage, and the minimum margin for one futures lot is several multiples of the whole account (a rough estimate, not sourced).
- **Long options do fit, but the risk budget is tiny.** At 1R = ₹200, the stop is about ₹3.1 of premium per unit on a Nifty lot (65) and about ₹6.7 on a Bank Nifty lot (30), where Bank Nifty has no weekly expiry. Premium noise can reach those amounts within minutes, so stops would be driven by noise, a structural handicap.
- **Costs have risen since 1 Apr 2026.** The 0.15% STT on options premium adds to the cost of every round trip.
- The institutional position-limit changes (₹1,500 crore and above) don't bind a ₹20k account. The parts that matter are contract size, the expiry calendar, STT, the CAS and expiry-settlement mechanics, and the end of multiple weekly expiries.
- For replay, F&O data from before Nov 2024 and Sep 2025 reflects different lot sizes, expiry days and margins. Option strategies backtested on 2019–2024 data would overstate what is possible today.

### Gaps
- Not confirmed in this session (believed from prior knowledge, **[unverified]**):
  - the expiry-day ELM is **2%** on short options;
  - upfront premium collection began on **1 Feb 2025**;
  - the effective date of the intraday limits from the 29 May 2025 circular (sources cite both 1 Oct 2025 and December 2025).
- A claimed **May 2026 SEBI circular "SEBI/HO/MRD/TPD/CIR/2026/034"** that would tighten retail position limits appears only on weak sites ([Multibagg](https://www.multibagg.ai/market-pulse/articles/sebi-fo-limits-margin-stt-cmsgh322a046b0zl3fi1zl5ht) and a garbled findoc page). It could not be found on SEBI's site. Treat it as **unverified, probably not real**.
- SEBI's FY24 and FY25 F&O loss studies and its intraday-cash loss study were not verified (search budget ran out).
- Not checked against the NSE circulars: the exact current lot sizes for every index (the Midcap figures conflict) and whether the 3:45 PM derivatives window was adopted.

## Q4. If the trader ever shares flags or AI verdicts with others: RA/IA rules, limits on recent price data in "education", and SEBI's AI/ML guidance

### Takeaway
Using Claude privately for the trader's own decisions is outside SEBI's AI/ML rules, which apply to regulated entities. Sharing flags or take/skip verdicts on named securities is a different matter. Doing it publicly, in a group, or especially for any consideration is research or advice territory, which needs **Research Analyst or Investment Adviser registration**. RAs who use AI must disclose it, and stay solely responsible for the output.

SEBI's "education" carve-out bans recent price data. From Jan 2025 that meant **data from the past 3 months**. It is replaced **from 1 Jul 2026 by a uniform 30-day lag** for both sharing and using price data **[2026]**. SEBI's broader AI/ML guidelines were still "to be issued shortly" in Oct 2026.

### Cited Findings
**Research Analyst and Investment Adviser rules**
- **[2024–25] RA rules:** SEBI notified the **SEBI (Research Analysts) (Third Amendment) Regulations, 2024 on 16 Dec 2024**, effective on publication in the Gazette — [SCC Online](https://www.scconline.com/blog/post/2024/12/19/sebi-research-analyst-third-amendment-regulations-2024/). The related IA amendments are dated about 17 Dec — [AZB & Partners](https://www.azbpartners.com/bank/overhaul-of-the-regulatory-framework-for-investment-advisers-and-research-analysts/).
- Under the amended rules:
  - part-time RAs are capped at **75 clients** at any time (Reg. 13(iv));
  - **new Reg. 19(vii) requires RAs to disclose how far they use AI tools**, at the time of entering an agreement;
  - "the responsibility of investment advisory services/research services lies solely with the IA/RA, irrespective of the scale and scenario of usage of AI tools".
  
  Sources: [Compliance Calendar](https://www.compliancecalendar.in/learn/sebi-research-analyst-third-amendment-regulations-2024); [Daily Pioneer](https://www.dailypioneer.com/2024/business/investment-advisers--research-analysts--should-disclose-ai-tool-usage-to-clients--sebi.html); [Moneylife](https://www.moneylife.in/article/sebi-introduces-major-reforms-for-investment-advisers-and-research-analysts/75888.html).

**Price-data limits for "education" and ties to unregistered finfluencers**
- **[2025] Circular of 29 Jan 2025:** people who provide only education may use price data only if it is **at least three months old**. They may not discuss or display security names, codes or recent price data in a way that could suggest advice. The circular tightened the rule barring regulated entities (exchanges, brokers, mutual funds, advisers and so on) from direct or indirect ties with unregistered advisers or "finfluencers". Sources date that earlier rule to 29 Aug 2024 or "October 2024" — [Business Standard, 30 Jan 2025](https://www.business-standard.com/markets/news/sebi-finfluencer-circular-live-stock-data-market-education-rules-125013000571_1.html); [FoxMandal](https://foxmandal.in/news/cutting-ties-with-finfluencers-sebi-distinguishes-between-education-advice/); [exchange4media](https://www.exchange4media.com/influence-zone-news/sebi-restricts-finfluencers-from-using-live-stock-market-data-educational-content-140505.html); [Mondaq](https://mondaq.com:443/india/securities/1580788/securities-law-update-%7C-clarification-on-intermediaries-and-other-associates-persons-regulated-by-sebi).
- **[2026] The 30-day lag:**
  - SEBI's consultation paper of **6 Jan 2026** proposed a uniform 30-day lag — [The Week](https://www.theweek.in/news/biz-tech/2026/01/07/sebi-mulls-30-day-lag-on-sharing-stock-market-data-for-investor-education-here-is-why.html).
  - A circular of **8 May 2026** (one source says 9 May) **replaces both the 1-day sharing lag (May 2024) and the 3-month usage lag (Jan 2025) with a single 30-day lag**, **effective 1 Jul 2026**.
  - The NISM simulation lab gets a 1-day carve-out, and data-sharing agreements must now include an audit trail.
  
  Sources: [Outlook Money](https://www.outlookmoney.com/invest/sebi-revises-norms-for-sharing-and-usage-of-price-data-for-educational-purposes); [Outlook Business](https://www.outlookbusiness.com/economy-and-policy/sebi-revises-norms-to-allow-30-day-lag-for-market-data-use-for-educational-purposes); [CorpLaw Updates](https://www.corplawupdates.in/updates/sebi-30-day-lag-educational-price-data-norms-2026); [Kotak Neo](https://www.kotakneo.com/news/market-news/sebi-30-day-lag-market-data-educational-content-2026/); [Bigul](https://bigul.co/blog/market-update/sebis-30day-rule-for-market-data-what-stock-market-educators-must-know-before-july-1).

**Exchange data rules (via Kite)**
- Zerodha's FAQ says that displaying or redistributing Kite Connect API data on outside platforms breaches exchange data-vending policies (see Q5) — [Zerodha Kite Connect API FAQs](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs).

**SEBI's AI/ML guidance**
- A **4 Jan 2019** SEBI circular requires brokers, depositories and other intermediaries to report the AI/ML applications they offer or use — [Business Standard, 2019](https://www.business-standard.com/amp/article/markets/sebi-asks-brokers-depositories-using-ai-tools-to-make-security-disclosures-119010401096_1.html).
- SEBI has made entities that use AI/ML tools responsible for data security, AI-generated outputs and compliance with applicable laws — [Lexplosion](https://lexplosion.in/sebi-issues-guidelines-on-ai-usage-entities-using-ai-ml-tools-responsible-for-data-security-ai-generated-outputs-and-compliance-with-applicable-laws/). The date and instrument were not captured (believed to be the Feb 2025 amendment to the Intermediaries Regulations, **[unverified]**).
- **[2025]** A SEBI consultation paper of **20 Jun 2025**, "Guidelines for Responsible Usage of AI/ML in Indian Securities Markets", proposed:
  - human oversight, model validation and documentation;
  - disclosure of AI use to clients;
  - fairness and non-discrimination;
  - data controls;
  - a lighter "regulatory lite" regime for internal uses.
  
  Comments closed on 11 Jul 2025 — [Business Standard](https://www.business-standard.com/markets/news/sebi-proposes-ai-ml-guidelines-for-market-participants-125062001137_1.html); [Taxmann](https://www.taxmann.com/post/blog/analysis-sebis-ai-ml-framework-ensuring-fair-and-safe-use-in-stock-markets); [FoxMandal](https://foxmandal.in/News/sebi-floats-paper-on-responsible-ai-use-in-indian-securities-market/).
- **[2026]** In **Oct 2026** SEBI chair Tuhin Kanta Pandey said the AI/ML guidelines would be issued "shortly", with kill-switch and human-in-the-loop controls plus data controls. He said every regulated entity stays fully responsible for AI tools, whether built in-house or bought in. **No final circular was found** — [NewKerala](https://www.newkerala.com/news/a/sebi-issue-ai-machine-learning-guidelines-shortly-eyes-586.htm); [CA Alley](https://caalley.com/news-updates/indian-news/sebi-to-issue-ai-machine-learning-guidelines-shortly-eyes-expiry-day-settlement-rules-within-a-week-tuhin-kanta-pandey); [Outlook Money](https://www.outlookmoney.com/invest/sebi-to-issue-aiml-guidelines-for-capital-markets-mandatory-kill-switch-and-human-oversight-framework-explained).

### Inferences
- For **private, personal use**, nothing in the RA, IA or AI rules applies. The trader is not a regulated entity, and the AI/ML framework targets intermediaries and market infrastructure institutions.
- For **sharing**, the risk depends on what is shared:
  - The risky output is the tool's core product: a named stock, a live price, a setup and a take/skip verdict. Posting that to a Telegram/WhatsApp group, X or YouTube, especially with any monetisation (paid group, ads, affiliate or referral links, courses), looks like unregistered research or advice.
  - "Education" framing does not help if the content uses price data from the last 30 days (from 1 Jul 2026), or the last 3 months before that.
  - Even unpaid sharing is risky if any link to a regulated entity exists, such as a broker referral programme.
  - The safe zone is sharing **methodology** (code without signals) or **stale case studies** whose price data is more than 30 days old, with no securities recommended.
- If the trader ever registered as an RA, Reg. 19(vii) would require telling clients how much of the analysis comes from Claude, and responsibility for the output would stay entirely with the trader.

### Gaps
- Not retrieved or verified: the statutory definitions of "investment adviser" and "research analyst", and how SEBI interprets "for consideration" for free or ad-monetised content.
- Not researched: PFUTP and front-running cases against finfluencers.
- Not found: the content and date of the Jan 2025 RA/IA "guidelines" circular, and the number of the 8 May 2026 circular.
- Not confirmed: whether the 30-day rule covers people who are not associated with any regulated entity. The sources describe it in the context of regulated entities and the people they associate with.
- No final SEBI AI/ML circular was found as of late Oct 2026.

## Q5. Kite Connect today: price, plans, WebSocket, ticks, historical API, rate limits, login and token, terms

### Takeaway
**Plans:**
- **Kite Connect (paid): ₹500 per month per API key** **[2025]**. It includes the live WebSocket and historical candles; the separate ₹2,000 historical add-on is gone.
- **Personal (free):** order, portfolio and funds APIs only. **No live or historical market data**, so tradingtool needs the paid plan.
- **[2026] Credit scheme (secondary report):** from Oct 2026, users who generate at least ₹2,000 brokerage in a month get ₹500 of Kite Connect credit.

**Live data:**
- **3 WebSocket connections per key, 3,000 instruments per connection.**
- Modes are LTP, quote and full; only full mode fills every field, including timestamps and 5-level depth.
- Ticks are snapshots, about **1 per second per instrument** at most (sometimes 2 for very liquid instruments), not every trade.

**Historical data:**
- Intervals from minute to day. **Minute candles: 60 days per request, going back to about 2015.** About 3 requests per second.
- Prices are **adjusted for splits, bonuses and other corporate actions, with no unadjusted series offered**.

**Login and terms:**
- **The access token expires at 6 AM the next day.** Zerodha says automating login, TOTP included, is "against the exchange regulations", so a manual login once a day is expected.
- **Data is for personal use only. No redistribution or display to others.**

### Cited Findings
**Pricing and plans**
- **[2025]** The paid Kite Connect API costs **₹500 per month per API key**. It includes all Personal API features plus live market data and historical data at no extra cost. The free **Personal** plan covers placing orders and tracking positions, holdings and funds, with **no live or historical market data** — [Zerodha support: payment plan](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/historical-data-and-live-market-data-payment-plan).
- **Pricing history [2025]:**
  - The ₹2,000 historical add-on was dropped, making historical data free with the base subscription — [Kite forum: "Historical data is now free"](https://kite.trade/forum/discussion/14806/historical-data-is-now-free).
  - On 24 Apr 2025 Zerodha wrote: "We've made the execution APIs free, and we only charge ₹2000 for data" — [Z-Connect update, 24 Apr 2025](https://zerodha.com/z-connect/?p=411859).
  - In **May 2025**, after NSE's algo circular, Zerodha cut data APIs (real-time and historical) to **₹500 per month**, saying regulatory risk was "greatly reduced". Order and account APIs are free — [Business Today, 6 May 2025](https://www.businesstoday.in/markets/stocks/story/for-traders-who-can-code-zerodha-cuts-rates-as-nithin-kamath-explains-nses-new-rulebook-474897-2025-05-06); [Kite forum: "Revising Kite Connect fees from ₹2000 to ₹500 per month"](https://kite.trade/forum/discussion/comment/49630).
  - A "Personal" app costs nothing; the fee applies only to "Connect" apps — [same thread](https://kite.trade/forum/discussion/comment/49630).
- **[2026]** From Oct 2026, users who generate **₹2,000 or more in brokerage in a calendar month get ₹500 of Kite Connect credits** — [TradingQnA post](https://tradingqna.com/t/free-kite-connect-subscription-for-active-users/198623) (secondary, **[unverified]** against Zerodha's own announcement).

**WebSocket limits, modes and fields**
- Limits:
  - **Up to 3 WebSocket connections per API key**, each subscribing to **at most 3,000 instrument tokens**. Staff describe the connection cap as a soft limit.
  - Subscribing beyond 3,000 returns an error for the extra tokens, and the existing connection stays up.
  
  Sources: [Kite forum](https://kite.trade/forum/discussion/comment/51532); [kiteticker-async-manager README](https://docs.rs/crate/kiteticker-async-manager/0.4.0/source/README.md). An older thread gives 1,000 instruments per connection — [Kite forum 3620](https://kite.trade/forum/discussion/3620/how-many-instruments-can-we-subscribe-maximum-using-kite-connect-3-0).
- REST quote limits are **500 instruments per `/quote` request and 1,000 per `/quote/ltp` request** — [Kite forum](https://kite.trade/forum/discussion/comment/51532).
- Every mode uses the same Tick structure, but **only "full" mode fills in every value** — [Kite forum](https://kite.trade/forum/discussion/comment/45100).
- Packet layout as parsed by a third-party Rust client:
  - full-mode packets for tradable instruments are **184 bytes**, with the last-trade timestamp at bytes 44–48;
  - index packets carry the exchange timestamp at bytes 28–32.
  
  Source: [kiteticker-async models.rs](https://docs.rs/crate/kiteticker-async/0.1.1/source/src/models.rs). An older JS gist lists 164-byte full and 52-byte quote packets, an earlier layout — [gist](https://gist.github.com/ajinasokan/b36d17da1a58af62782978c16bca309a).

**Tick frequency**
- There is no fixed interval: data arrives "when ticks happen at the exchange", from several per second to none — [Kite forum: frequency of ticks](https://kite.trade/forum/discussion/1291/frequency-of-ticks).
- Zerodha staff: **at most about 1 tick per second per instrument**, with liquid instruments such as NIFTY 50 sometimes reaching 2 per second — [Kite forum](https://kite.trade/forum/discussion/comment/43580/).
- LTP mode sends a tick only when the last price changes — [Kite forum 9945](https://kite.trade/forum/discussion/9945/kite-tick-data-in-an-interval).
- There is no built-in time-sampled stream; staff suggest building your own sampling or polling the quote API — [Kite forum 5368](https://kite.trade/forum/discussion/5368/how-to-change-tick-data-kiteticker-interval).

**Historical API**
- Per-request caps by interval (forum post from 2018, last edited 2020):

  | Interval | Max days per request |
  |---|---|
  | minute | 60 |
  | 3minute, 5minute, 10minute | 100 |
  | 15minute, 30minute | 200 |
  | 60minute | 400 |
  | day | 2,000 |

  Sources: [Kite forum 3105](https://kite.trade/forum/discussion/3105/historical-api-frequency-and-limit-on-number-of-candles-fetched); [Kite forum 9129](https://kite.trade/forum/discussion/9129/how-many-past-days-historical-data-can-be-fetched-for-minute-candle); endpoint docs at [kite.trade/docs/connect/v3/historical](https://kite.trade/docs/connect/v3/historical/) (numbers not visible in the extracts).
- How far back: a 2024 staff reply says there is no fixed start date for day candles, and **minute data "starts somewhere around early 2015"** — [Kite forum: historical data retention policy](https://kite.trade/forum/discussion/14149/historical-data-retention-policy). Other secondary claims of "up to 3 years" conflict with this and are unverified.
- The forum gives the historical rate limit as **3 requests per second** — [Kite forum: "Historical data is now free"](https://kite.trade/forum/discussion/14806/historical-data-is-now-free). Historical data is **not available for expired option contracts** — [same thread](https://kite.trade/forum/discussion/14806/historical-data-is-now-free).
- Corporate-action adjustments:
  - Zerodha (Aug 2025): Kite Connect historical prices "are adjusted for corporate actions such as bonuses, stock splits, rights issues, spin-offs, and extraordinary dividends" — [Zerodha on X](https://x.com/zerodha/status/1952292763929874868).
  - A **Sep 2026** staff reply repeats this (extraordinary dividends meaning those above 2%) and says **Kite Connect offers no unadjusted price-and-volume series** — [Kite forum 16280](https://kite.trade/forum/discussion/16280/historical-5-minute-api-data-corporate-action-price-and-volume-adjustments).
  - Older caveats: a 2020 reply said very old data was adjusted only in **day** candles, not intraday, and intraday adjustment for all contracts was not applied **before 2019**. A 2023 reply said only splits and bonuses were adjusted. Adjustments were historically applied weekly — [Kite forum 5004](https://kite.trade/forum/discussion/5004/is-historical-data-corporate-action-adjusted-upto-the-current-date-at-any-time).
  - A Nov 2025 user found Kite's OHLC consistently higher than TradingView's adjusted data, and Zerodha attributed this to different methods — [Kite forum 15250](https://kite.trade/forum/discussion/15250/adjusted-histroical-data).

**Rate limits and order caps**
- Rate limits apply per **API key**, with a combined ceiling of **10 requests per second**. Reported per-endpoint figures: **orders 10/s, quotes 1/s, historical candles 3/s** — [Kite forum: API rate limit](https://kite.trade/forum/discussion/comment/51556); [follow-up](https://kite.trade/forum/discussion/comment/51563/).
- Zerodha's RMS sets daily caps of **2,000 MIS orders and 2,000 BO/CO orders** per account — [same thread](https://kite.trade/forum/discussion/comment/51556).

**Access token and login flow**
- From the official docs: unless invalidated through the API or by a master logout from Kite Web, the access token "will expire at 6 AM on the next day (regulatory requirement)". The request_token lives only a few minutes and must be exchanged for an access token straight away — [Kite Connect docs: User](https://kite.trade/docs/connect/v3/user/).
- In practice, old staff replies put the overnight flush at 06:45–07:30 AM or 7–8 AM — [Kite forum 7610](https://kite.trade/forum/discussion/7610/when-exactly-does-the-access-token-expire-for-the-day).
- Generating a new token invalidates the previous one. After expiry, WebSocket reconnects fail with a 403, so a fresh ticker is needed — [Kite forum 7759](https://kite.trade/forum/discussion/7759/access-token-validity); [Kite forum 14628](https://kite.trade/forum/discussion/14628/kiteconnect-exceptions-tokenexception-token-is-invalid-or-has-expired).
- On automating login, Zerodha staff have said:
  - "We don't allow automating login, it is against the exchange regulations";
  - automating authentication "is against exchange regulations and using unofficial APIs will lead to unforeseen disruptions";
  - "it is mandatory by the exchange that a trader has to log in manually at least once in a day".
  
  Sources: [Kite forum comment 45535](https://kite.trade/forum/discussion/comment/45535); [comment 45547](https://kite.trade/forum/discussion/comment/45547); [comment 19940](https://kite.trade/forum/discussion/comment/19940/).
- Unofficial pyotp and Selenium auto-login scripts exist, for example [rajivgpta/kite-api-autologin](https://github.com/rajivgpta/kite-api-autologin/blob/main/login.py) and [DEV article](https://dev.to/sagamantus/automating-zerodha-login-without-selenium-a-pythonic-approach-3b8o). These are exactly what staff warn against.

**Terms of use**
- From Zerodha's FAQ: "Displaying or redistributing Kite Connect API data on external platforms violates exchange data vending policies. Kite Connect is an order execution platform, not a data distribution service" — [Zerodha Kite Connect API FAQs](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs).
- WebSocket data "is provided for personal use only" and cannot be redistributed. Platforms that want to show data must buy it from an exchange-authorised vendor. A forum reply says breaking the terms can get the account suspended — [Kite forum 4870](https://kite.trade/forum/discussion/4870/show-realtime-streaming-data-on-website-or-application); [Kite forum comment 17520](https://kite.trade/forum/discussion/comment/17520/); [Kite forum comment 42658](https://kite.trade/forum/discussion/comment/42658).
- A 2026 forum thread asks specifically about keeping NSE historical data for personal quantitative research. The answer was not visible in the extracts — [Kite forum 16295](https://kite.trade/forum/discussion/16295/clarification-on-historical-nse-equity-data-retention-and-personal-quantitative-research).

### Inferences
- **Field layout (recalled from the Kite v3 docs; consistent with the 44- and 184-byte offsets above; re-verify):**

  | Mode | Size | Fields |
  |---|---|---|
  | LTP | 8 bytes | token, last price |
  | Quote | 44 bytes | adds last traded quantity, average traded price, **cumulative volume for the day**, total buy and sell quantity, and day OHLC (the OHLC "close" is the previous close) |
  | Full | 184 bytes | adds **last-trade time**, OI, OI day high and low, **exchange timestamp** and **5-level depth** (quantity, price, orders) |

  Index packets carry OHLC and change, and the exchange timestamp only in full mode.
- **Consequences for tradingtool:**
  - Subscribe to the 15–20 symbols in **full** mode. One connection uses less than 1% of the cap.
  - Use the exchange timestamp or last-trade time, not the Mac's clock, to assign ticks to 1-minute bars.
  - Get bar volume from differences in the cumulative day volume.
  - Expect tick-built bars to differ slightly from historical-API candles, because ticks are roughly 1-second snapshots. Volume and high/low can drift, so the paper-trading engine should be reconciled against historical candles at the end of each day.
- **Bulk history is fast to pull.** Ten years of 1-minute data for 20 symbols is about 61 windows of 60 days per symbol, roughly 1,220 requests. At 3 per second that is about 7 minutes, so one paid month is enough to pull history.
  - The data is adjusted, which suits backtests.
  - Intraday adjustment before 2019 may be inconsistent, and no unadjusted series exists to check against.
  - Delisted symbols and expired options are not served.
- **Daily login becomes part of the routine.** The tool should open the Kite login URL for the trader every morning after the overnight flush (about 7:30 AM IST) and before 9:15 AM, then capture the request_token through a local redirect and exchange it. It should not script TOTP.
- **Cost against the trial budget:** ₹500 a month is 2.5R. A 4-month trial costs ₹2,000 in data, equal to the whole 10R drawdown stop. The trial should count the data fee separately, or use a free live feed (Q6), or rely on the ₹500 credit if the trader's brokerage reaches ₹2,000 a month (about 100 executed orders at ₹20 each, which is probably not desirable).
- **Keep everything private.** Shared screenshots, alerts or dashboards with live Kite data would breach the redistribution terms as well as touching the SEBI issues in Q4.

### Gaps
- The official field table, the exact current per-request day caps, the historical rate limit and the full rate-limit table could not be read directly (kite.trade was blocked). The figures come from forum posts, some years old.
- Not found: the order caps I recall (about 200 per minute and 3,000 per day), whether GST is added to the ₹500, and the exact date historical data became free (some time before 24 Apr 2025).
- Not verified: the Oct 2026 credit scheme against a Zerodha announcement.
- A thread titled "Kite Connect Historical API — Missing Last 15 Minutes of NSE Intraday Data" exists ([Kite forum 16324](https://kite.trade/forum/discussion/16324/kite-connect-historical-api-missing-last-15-minutes-of-nse-intraday-data)). Its content and timing (whether it relates to the CAS) are unknown, and it is worth checking before relying on the final bars of the session.
- Not confirmed: Zerodha's written position on storing downloaded history for personal research.

## Q6. Alternatives and costs for live NSE data and multi-year 1-minute NSE history for replay

### Takeaway
**Live data:**
- Kite Connect costs ₹500 a month and has the most generous limits.
- Free alternatives exist, each with caveats:
  - **Fyers Standard (free):** 100 symbols on its data socket.
  - **Upstox (free API access):** WebSocket limits unclear and varying by plan.
  - **Angel One SmartAPI (free):** limits not verified.
- **Dhan** charges ₹499 plus tax a month for its Data APIs.
- Vendors (TrueData, Global Datafeeds) are the licensed route but cost more: about ₹2,600–4,000 a month in 2024 for TrueData through Fyers.

**1-minute history:**

| Source | 1-minute depth | Cost |
|---|---|---|
| Kite | about 2015 onwards, adjusted, 60 days per request | ₹500 a month |
| Upstox V3 | from Jan 2022, 1 month per request | free |
| Dhan | up to 5 years, active instruments only | ₹499 a month |
| ICICI Breeze | claims 10 years, including 1-second bars | price not checked, **[unverified]** |
| TrueData | 5 years intraday | ₹2,599 a month for history only (2024) |
| NSE direct | institutional products | in USD thousands per year |

Broker history generally leaves out delisted or expired instruments.

### Cited Findings
**Broker APIs**
- **Upstox:**
  - API access is not metered or charged; developers pay normal brokerage per executed order — [apis.io Upstox pricing](https://apis.io/plans/upstox/upstox-plans-pricing/).
  - A promotional flat ₹10 per API order ran until 31 Mar 2026; whether it was extended to 30 Sep 2026 is unclear — [Upstox community](https://community.upstox.com/t/stay-ahead-of-the-curve-we-re-extending-10-order-api-pricing-till-march-2026/13277); [AlgoTest](https://algotest.in/blog/upstox-vs-zerodha-charges-api-and-which-is-better-in-2026/). An older ₹499 API fee on Chittorgarh is out of date — [Chittorgarh](https://chittorgarh.com/broker/upstox/api-for-algo-trading-review/33).
  - Historical Candle Data V3: **minute data available from January 2022**. Intervals of 1–15 minutes allow at most **1 month per request**; longer intervals allow 1 quarter. An Intraday V3 endpoint covers the current day — [Upstox V3 historical docs](https://upstox.com/developer/api-documentation/v3/get-historical-candle-data); [Upstox community: custom time frames](https://community.upstox.com/t/get-historical-data-in-any-time-frame-you-wished-we-built-new-releases-at-upstox-api/8845).
  - WebSocket limits conflict: older posts say 3 connections × 100 instruments. The Plus plan announcement says 5 concurrent connections per user, with full_d30 mode capped at 50 instruments. A staff reply mentions 1,500 instruments across connections — [Upstox WebSocket Plus](https://upstox.com/developer/api-documentation/announcements/websocket-plus); [Upstox community 8459](https://community.upstox.com/t/websocket-connection-limits-and-scrip-subscription-cap/8459); [Upstox community 6348](https://community.upstox.com/t/when-can-we-expect-the-100-instrument-limit-on-websocket-to-be-increased/6348).
- **Dhan:**
  - Trading APIs are free. **Data APIs cost ₹499 plus taxes a month**, renewing every 30 days. The free-with-enough-trades promotion has been **discontinued**. Data APIs include the Live Market Feed (LTP, trades, depth, volume, OI), historical data and option chains — [Dhan: subscription](https://dhan.co/support/platforms/dhanhq-api/how-does-the-dhanhq-data-api-subscription-work/); [Dhan: waiver discontinued](https://dhan.co/support/platforms/dhanhq-api/is-the-dhanhq-data-api-subscription-free-if-i-execute-a-minimum-number-of-trades-every-month/); [Dhan: live market data](https://dhan.co/support/platforms/dhanhq-api/how-can-i-access-live-market-data-through-dhan/).
  - **1-minute intraday history is available for up to 5 years, for active contracts only**; expired futures are not available — [Dhan: expired futures](https://dhan.co/support/platforms/dhanhq-api/how-can-i-retrieve-data-for-expired-futures-contracts-using-the-apis/).
  - An unofficial client gives 90 days per request, with 1, 5, 15, 25 and 60-minute intervals — [dhan-rs](https://docs.rs/crate/dhan-rs/0.1.7/source/src/api/historical.rs).
- **Fyers (official Plans & Limits page)** — [Fyers API v3 Plans & Limits](https://fyers.in/api-docs/v3/getting-started/plans-and-limits/):

  | Item | Standard (free) | Prime (paid) |
  |---|---|---|
  | Data socket | **100 symbols** | 5,000 symbols |
  | Tick-by-tick socket | 1 symbol | 15 symbols |
  | Daily history | 5 years (from 2021) | entire history |
  | Data API rate limit | **5 req/s, 50/min, 5,000/day** | higher (not specified) |

  Symbol limits apply per user across all connections. The page lists no intraday history window.
- **Angel One SmartAPI (forum reports only):**
  - users quote the docs as allowing 30 days of ONE_MINUTE data per call, but many report getting back at most about 500 candles;
  - rate-limit "access denied" errors on the historical endpoint;
  - the latest 1-minute candle appears about 5 seconds after the minute closes.
  
  Sources: [SmartAPI forum 13202](https://smartapi.angelone.in/smartapi/forum/post/13202); [SmartAPI forum 13093](https://smartapi.angelone.in/smartapi/forum/post/13093).
- **ICICI Breeze:**
  - a PyPI listing claims "10 years of historical market data including 1 sec OHLCV" — [breeze-connect 1.0.38](https://pypi.org/project/breeze-connect/1.0.38/);
  - the SDK documents 1minute, 5minute, 30minute and 1day intervals and `get_historical_data_v2` for NSE cash — [Breeze Python SDK](https://github.com/Idirect-Tech/Breeze-Python-SDK);
  - orders must come from a registered static IP, at most 10 per second — [breeze-connect](https://pypi.org/project/breeze-connect/).

**Data vendors and NSE**
- **TrueData:**
  - an authorised NSE/BSE/MCX data vendor, with a free Workspace plan on 15-minute delayed data and paid real-time plans — [TrueData](https://www.truedata.in/);
  - through Fyers, from **1 Jul 2024**, history-only rose from ₹1,599 to **₹2,599**, and real-time plus history from ₹2,599 to **₹3,999** a month;
  - it covers **25 years of daily and 5 years of intraday data** for equities — [Fyers notice](https://fyers.in/notice-board/revision-in-truedata-subscription-pricing).
- **Global Datafeeds:**
  - NimbleData products are priced by symbols and segments (plans "from 225" and "from 15 symbols/segments"; some are AmiBroker-only), with real-time NSE F&O, currency and MCX — [marketcalls](https://www.marketcalls.in/services/globaldatafeeds);
  - user and review reports say real-time subscriptions include only about 1 month of intraday history and about 1 calendar week of tick history — [TradingTuitions](https://tradingtuitions.com/the-best-amibroker-datafeed-services-in-india).
- **NSE itself:**
  - NSE Data & Analytics sells real-time data at levels 1, 2 and 3 and tick-by-tick, and links a historical trade-data tariff — [NSE Data & Analytics](https://nseindia.com/nsedataandanalytics);
  - **[2026]** NSE's international price list, effective 1 Apr 2026, includes a **1-minute snapshot product (15-minute delayed) for Capital Market at USD 7,500 a year per medium** — [NSE pricing file (Mar 2026)](https://nsearchives.nseindia.com//web/mediaattachment/2026-03/NSE_Pricing_file_-_International_clients_20260309171502.pdf);
  - an older domestic schedule, effective Apr 2022, also exists — [NSE Other Data Product Pricing](https://archives.nseindia.com/content/press/Other_Data_Product_Pricing_effective_Apr012022.pdf).
- Other sellers of NSE history exist, such as [Tickstory](https://tickstory.com/product/historical-price-data-for-nse-equities/) and [ProCharting](https://procharting.in/trading/market-data/nse). Their coverage and prices were not checked.

### Inferences
- **Best fit for this account:** keep **Kite Connect (₹500 a month)** as the single source for live data and history, because the trader already executes in Kite.
  - The cheapest route is one paid month to download 2015–2026 1-minute history for the watchlist, plus continued paid months only while the live trial runs.
  - Alternatively, **open a free Fyers or Upstox account and use its free live feed**. Fyers' 100-symbol cap is enough for 15–20 stocks.
  - Orders stay manual in Kite either way.
- **For replay that goes back before 2022**, Kite (about 2015 onwards) or Dhan (5 years) beat Upstox (from Jan 2022). TrueData's history-only plan (₹2,599 a month in 2024) only makes sense if exchange-licensed tick or 1-minute history with clear rights is needed.
- **Survivorship bias:** broker history covers active instruments only (Dhan says so explicitly; Kite has no expired options). Universe-level backtests of book setups will leave out delisted losers. A fixed watchlist of current large caps reduces but does not remove look-ahead bias in how the watchlist was chosen.
- **Adjustments differ by source.** Kite adjusts, with no unadjusted series. Others may not. Mixing sources without reconciling them will create false gaps and jumps around splits and bonuses.

### Gaps
- Not verified: current Angel One SmartAPI WebSocket token and connection limits, Upstox free-tier WebSocket caps, and Global Datafeeds prices.
- Not found: current TrueData pricing after 2024, whether Breeze history is free, how deep Breeze's 1-second and 1-minute history goes, and Fyers' intraday-history depth and per-request caps.
- The NSE historical trade-data tariff PDF was not opened.
- Exchange licensing terms for storing broker-sourced data for personal backtesting are not documented beyond Zerodha's personal-use, no-redistribution wording.
