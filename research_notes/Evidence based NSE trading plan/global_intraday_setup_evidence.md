# Global evidence on intraday setups (ORB, stocks in play, intraday momentum, Aziz's setups) and how it transfers to NSE

Compiled 31 Oct 2026. **How these notes were sourced:** the network policy blocked the primary hosts: papers.ssrn.com, concretumgroup.com, quantconnect.com, wealth-lab.com, researchgate.net, sciencedirect.com, nseindia.com, sebi.gov.in, zerodha.com and most journal sites. The shared WebSearch budget then ran out before the NSE market-structure and cost checks were done. Figures for the original papers therefore come from two places:
- independent GitHub replications that quote the papers' numbers, read in full via raw.githubusercontent.com;
- search-engine summaries of papers and blogs, marked "(per search summary)" below. Check these against the PDFs before relying on them.

Source-type tags: **[PR]** peer-reviewed journal · **[WP]** working paper · **[Preprint]** · **[GitHub]** independent code replication · **[Blog/Vendor]** · **[Regulator]** · **[Press]** · **[Book-summary]**.

---

## 1. What exactly did Zarattini & Aziz (2023), Zarattini, Barbon & Aziz (2024) and "Beat the Market" (Zarattini, Aziz & Barbon 2024) find?

### Takeaway
All three are the authors' own working papers (SSRN and the Swiss Finance Institute Research Paper series). I found no journal versions. They report very strong in-sample results:
- **5-minute ORB on QQQ (2016 to Feb 2023):** about +671%, Sharpe about 1.12, maximum drawdown about 22%, 1,795 trades.
- **5-minute ORB on stocks in play (2016–2023):** +1,637% "net", Sharpe 2.81, maximum drawdown about 12–13%.
- **SPY "noise area" momentum (2007–2024):** 19.6% a year, Sharpe 1.33.

Each result depends on cheap US per-share commissions, little or no slippage and up to 4x leverage. The stocks-in-play result comes almost entirely from the relative-volume top-20 filter: the unfiltered 5-minute ORB had a Sharpe of 0.48.

### Cited Findings

**Paper A: Zarattini & Aziz (2023), "Can Day Trading Really Be Profitable? Evidence of Sustainable Long-term Profits from Opening Range Breakout (ORB) Day Trading Strategy vs. Benchmark in the US Stock Market" [WP, SSRN 4416622, first posted April 2023]**
- **Setup.** 5-minute ORB on QQQ, Jan 2016 to Feb 2023, $25,000 starting capital, maximum 4x leverage, commission $0.0005 per share, no bid-ask spread or slippage modelled — [Concretum page (per search summary)](https://concretumgroup.com/can-day-trading-really-be-profitable/); the zero-slippage assumption ("we assumed no slippage in fills") is confirmed by [Brusco replication](https://github.com/giovannibrusco/qqq-opening-bias-5min) [GitHub].
- **Rules (codeable, as replicated).**
  - If the first 5-minute bar (09:30–09:35 ET) is bullish, go long at the 09:35 open with the stop at that bar's low. If it is bearish, go short with the stop at its high. If it is a doji, no trade.
  - Exit at the stop (−1R), at a +10R target, or flat at the close.
  - Size = min(1% of equity ÷ R, 4 × equity ÷ entry price).
  - Source: [Brusco replication](https://github.com/giovannibrusco/qqq-opening-bias-5min) [GitHub].
- **Outcome distribution.** The +10R target is "nearly decorative": it was hit on only about 2–3% of trades. About 75% of trades exit on the stop and about 22% flat at the close. In practice the strategy is "intraday momentum-continuation with a 1R stop" — [Brusco replication](https://github.com/giovannibrusco/qqq-opening-bias-5min) [GitHub].
- **Headline numbers quoted from the paper.** $25k grows to $192,806 (about +671%), 1,795 trades, Sharpe 1.12, maximum drawdown 22% — [Brusco replication](https://github.com/giovannibrusco/qqq-opening-bias-5min).
- **Conflicting totals.** One summary gives a QQQ ORB total return of 675% against 169% for passive QQQ — [Concretum Research Substack (per search summary)](https://concretumgroup.substack.com/p/can-day-trading-really-be-profitable). Other summaries quote 1,484%, most likely the TQQQ version; this conflict is unresolved — [Papers With Backtest summary page (per search summary)](https://paperswithbacktest.com/strategies/can-day-trading-really-be-profitable-evidence-of-sustainable-long-term-profits-from-opening-range-breakout-orb-day-trading-strategy-vs-benchmark-in-the-us-stock-market).
- **TQQQ variants.** The authors also ran the strategy on TQQQ to get around broker leverage limits, plus a TQQQ variant with the stop at 5% of the 14-day ATR and no profit target — [Concretum page (per search summary)](https://concretumgroup.com/can-day-trading-really-be-profitable/). A secondary summary claims annualized alpha above 30% on TQQQ; I could not verify this — [Retail Traders Repository (per search summary)](https://retailtradersrepository.substack.com/p/trading-research-paper-can-day-trading-really-be-profitable).
- **Authors' own framing.** The strategy is profitable because its P&L distribution is strongly skewed: a low win rate with an asymmetric payoff — [Concretum Substack (per search summary)](https://concretumgroup.substack.com/p/can-day-trading-really-be-profitable).

**Paper B: Zarattini, Barbon & Aziz (2024), "A Profitable Day Trading Strategy For The U.S. Equity Market" [WP, SSRN 4729284, Feb 2024; Swiss Finance Institute Research Paper 24-98]**
- **Listings.** [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4729284); [IDEAS/RePEc rp2498](https://ideas.repec.org/p/chf/rpseri/rp2498.html).
- **Universe.** About 7,000 US stocks, 2016–2023 — [QuantConnect post / Tradoki (per search summary)](https://blog.tradoki.com/posts/opening-range-breakout-stocks-in-play-research).
- **Stocks-in-play filter.** All of the following:
  - opening price above $5;
  - 14-day average volume of at least 1,000,000 shares;
  - 14-day ATR above $0.50;
  - relative volume during the opening range of at least 100%, and ranked in the top 20 by that measure.
  - Source: [paper copy (per search summary)](https://www.researchgate.net/publication/379003745_A_Profitable_Day_Trading_Strategy_For_The_US_Equity_Market).
- **Relative volume definition.** The window's volume against its average over the previous 14 days, according to a GitHub implementation of the paper; verify in the paper — [jlmn-code bot README](https://github.com/jlmn-code/bot_intradia_orb) [GitHub, low-quality source].
- **Entry, stop and exit.** Stop orders at the opening-range extremes. The stop-loss sits 10% of ATR from the fill. Exit at the end of the day — [paper copy (per search summary)](https://www.wealth-lab.com/api/discussion/download/pdf/8007-ssrn-4729284-1-pdf).
- **Sizing.** Risk up to 1% of capital per position, with a 4x leverage cap — [Danfin summary (per search summary)](https://danfin.net/opening-range-breakout-research).
- **Costs.** Commission $0.0035 per share. "The paper prices commission only, and slippage never appears in its text" — [Tradoki (per search summary)](https://blog.tradoki.com/posts/opening-range-breakout-stocks-in-play-research).
- **Headline results.**
  - Top-20 relative-volume version: 1,637% total return, 41.6% annualized IRR, Sharpe 2.81, near-zero beta, 1 Jan 2016 to 31 Dec 2023 — [Quantified Strategies (per search summary)](https://quantifiedstrategies.substack.com/p/stocks-in-play-opening-range-breakout).
  - $25,000 grows to about $435,000. Maximum drawdown 13% against 34% for the S&P 500 — [ResearchGate/paper copy (per search summary)](https://www.researchgate.net/publication/379003745_A_Profitable_Day_Trading_Strategy_For_The_US_Equity_Market).
  - A table in the Wealth-Lab copy lists two rows: 13% maximum drawdown with a 41.4% hit ratio, and 12% maximum drawdown with a 48.4% hit ratio (Sharpe 2.81, 1,637%). Which row is which variant is unclear from the summary — [Wealth-Lab copy (per search summary)](https://www.wealth-lab.com/api/discussion/download/pdf/8007-ssrn-4729284-1-pdf).
  - Wikipedia describes the result as "net performance above 1,600% with a Sharpe ratio of 2.8" — [Wikipedia: Andrew Aziz](https://en.wikipedia.org/wiki/Andrew_Aziz).
- **Without the filter.**
  - The unfiltered 5-minute ORB had a Sharpe of 0.48, against 0.78 for the S&P 500 — [Quantified Strategies stocks-in-play page (per search summary)](https://www.quantifiedstrategies.com/stocks-in-play-trading-strategy-day-trading/).
  - It made about 29% in total. The relative-volume filter plus the top-20 cutoff turns this into 1,637% — [Tradoki (per search summary)](https://blog.tradoki.com/posts/opening-range-breakout-stocks-in-play-research).
- **Longer opening ranges were much weaker, and the two sources disagree on the numbers.**
  - Danfin gives totals of 272% (15-minute), 21% (30-minute) and 39% (60-minute) — [Danfin (per search summary)](https://danfin.net/opening-range-breakout-research).
  - Tradoki gives 2.3% a year (30-minute) and 4.1% a year (60-minute). It also says the shortest holds lost money after costs ("−0.82 points per trade long and −3.45 short"; the unit is ambiguous) — [Tradoki (per search summary)](https://blog.tradoki.com/posts/opening-range-breakout-stocks-in-play-research).

**Paper C: Zarattini, Aziz & Barbon (2024/2025), "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)" [WP, SSRN 4824172; Swiss Finance Institute Research Paper 24-97]**
- **Listings.** [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172); [IDEAS rp2497](https://ideas.repec.org/p/chf/rpseri/rp2497.html); the SFI 24-97 numbering is cited in the [oleksandr replication](https://github.com/oleksandr123456787654321/spy_intraday_momentum).
- **Reported results.** 19.6% annualized return and Sharpe 1.33 from 2007 through 2024, with near-zero correlation to the market — [Quant Macro review](https://quantmacro.substack.com/p/paper-review-an-effective-intraday); [Swedroe](https://larryswedroe.substack.com/p/when-beat-the-market-meets-the-real).
- **Noise area.** For each minute of the session, σ is the average absolute move from the open over the previous 14 days. The bands are UB = max(Open, previous Close) × (1+σ) and LB = min(Open, previous Close) × (1−σ) — [svettelnova replication](https://github.com/svettelnova/intraday-momentum-spy); [Brusco replication](https://github.com/giovannibrusco/zarattini-2024-momentum-spy) [GitHub].
- **Signals.** Checked only at HH:00 and HH:30 (10:00–15:30). Long above UB, short below LB. Trailing stop at the higher of UB and VWAP for longs, the lower of LB and VWAP for shorts. Flat at 16:00 — [svettelnova](https://github.com/svettelnova/intraday-momentum-spy); [Quant Macro](https://quantmacro.substack.com/p/paper-review-an-effective-intraday).
- **Sizing.** Shares N = floor(AUM × L ÷ Open), with leverage L = min(4, 0.02 ÷ σ_SPY,14d). This targets 2% daily volatility with a 4x cap — [svettelnova](https://github.com/svettelnova/intraday-momentum-spy).
- **Costs.** $0.0035 per share commission (Interactive Brokers entry tier) plus $0.001 per share slippage. The slippage figure is described as "the paper's live measurement" — [svettelnova](https://github.com/svettelnova/intraday-momentum-spy); [oleksandr](https://github.com/oleksandr123456787654321/spy_intraday_momentum); [nikolaosntinas18](https://github.com/nikolaosntinas18/spy-intraday-momentum).
- **Mechanism proposed by the authors (section 4.5).** Option dealers tend to be short gamma after market declines and amplify intraday trends. The strategy earns more when the 5-day RSI is low, but the paper does not trade on this — [nikolaosntinas18](https://github.com/nikolaosntinas18/spy-intraday-momentum).

**Conflicts of interest**
- Author affiliations are listed as "Concretum Research Lugano, Peak Capital Trading and Bear Bull Traders, Canada" — [University of St. Gallen repository PDF](https://alexandria.unisg.ch/bitstreams/a99aba00-f967-49b3-aceb-f544dc386e0b/download).
- "The original authors run day-trading education businesses" — [Brusco replication](https://github.com/giovannibrusco/qqq-opening-bias-5min).
- Bear Bull Traders, Aziz's trading community, presents these papers on a page titled "Peer-Reviewed Trading Research", although they are SSRN and SFI working papers — [bearbulltraders.com/research](https://bearbulltraders.com/research); [IDEAS rp2498](https://ideas.repec.org/p/chf/rpseri/rp2498.html).

### Inferences
- **"Net" in Paper B means net of commission only.** With a stop of 10% of ATR, the risk per share is tiny. For example, a $50 stock with a $2 ATR has a $0.20 stop, so 1¢ of slippage per side costs about 0.1R per round trip, about three times the round-trip commission of $0.007 (about 0.035R). The 1,637% should be read as an upper bound.
- **Headline totals are mostly leverage and compounding.** Replications show that volatility-targeted sizing scales return and volatility together and leaves the Sharpe almost unchanged (Q2). Compare strategies on Sharpe and R per trade, not total %.
- **Paper B's edge sits in the stock selection (top-20 relative volume on a ~7,000-stock universe), not in the ORB trigger.** The generic ORB (Sharpe 0.48) is weak. On NSE, the question to test is whether an equivalent "stocks in play" selection exists, not whether ORB works.
- **Paper B's hit ratios (41–48%) may be computed per day across a 20-stock portfolio.** They should not be read as per-trade win rates for a 10%-ATR stop, where per-trade win rates would normally be much lower.

### Gaps
- For Paper B I found no trade count, per-trade win rate, average win and loss in R, long/short split or yearly breakdown.
- Secondary summaries say Paper B takes the long side only when the first 5-minute candle is bullish and the short side only when it is bearish. I could not confirm this.
- Commonly cited figures I could not verify this session:
  - Paper C: total return (often quoted as about 1,985%) and maximum drawdown.
  - Paper B: about 36% a year alpha.
  - Paper A: the TQQQ figures.
- A Zarattini & Aziz VWAP paper on QQQ was summarized as "maximum drawdown of just 9.4% and a Sharpe Ratio of 2.1", but the source behind that snippet was not identifiable. Treat as unverified.
- The PDFs could not be opened (SSRN, Concretum and Wealth-Lab were blocked).

---

## 2. Have these strategies been independently replicated, tested out of sample or after publication, or tested outside the US (especially India)? What happens after realistic costs?

### Takeaway
The gross patterns largely replicate; the net edges largely do not.
- **QQQ ORB.** The replication matches the paper closely (1,775 vs 1,795 trades; Sharpe 1.06 vs 1.12). But it breaks even at about 2.2¢ per share of slippage (QQQ's spread is about 1¢), and much of the profit comes from 2022.
- **Index CFDs and futures.** An index-CFD replication found +0.131R per trade gross on NQ, with nothing distinguishable from zero after costs in any of five markets. A pre-registered 225-cell futures study found no net edge.
- **Stocks in play.** There is no full independent replication: the closest, on QuantConnect, covers only 2016.
- **"Beat the Market".** It replicates in-sample (Sharpe 1.11–1.34), but post-publication Sharpe was about 0.35–0.39 (May 2024 to 2026), with losses in 2025 and 2026 in one replication.
- **India.** I found no rigorous test. Blog-level Bank Nifty ORB backtests were unprofitable after costs.

### Cited Findings

**ORB on QQQ and on indices (Paper A family)**
- **Brusco replication** [GitHub, Jan 2016 to Feb 2023]:
  - 1,775 trades vs 1,795 in the paper; Sharpe 1.06 vs 1.12; maximum drawdown 22.4% vs 22%; final equity $164k vs $193k.
  - Edge with no slippage: $0.070 per share. Net PnL crosses zero at about 2.2¢ per share of entry slippage (stop slippage set at 2x), "only about two spreads of execution cost".
  - With $0.02 entry and $0.04 stop slippage: net PnL $4,860, Sharpe 0.23, CAGR 2.7%, maximum drawdown 43.9%. QQQ buy-and-hold over the same period: Sharpe 0.72, CAGR 15.3%, maximum drawdown 35.6%.
  - 2022 accounts for 38% of the replication's PnL. Requiring the NQ 09:25 pre-open bar to agree lifts the edge to $0.125 per share (t = 2.05), but that filter was chosen in-sample, makes 76% of its PnL in 2022 and loses in 2017, 2020 and early 2023.
  - A run of the unfiltered rule on ES futures, Mar–Sep 2026, "found no edge even before costs" (short sample).
  - Source: [Brusco replication](https://github.com/giovannibrusco/qqq-opening-bias-5min).
- **mericck out-of-sample study** (QQQ, 15-minute opening range, close-confirmed entry, 2R target, flat at 15:00; a modified rule rather than an exact replication) [GitHub]:
  - Development period 2017–2022: 1,472 trades, average +0.0558R, profit factor 1.127, maximum drawdown 17.57R.
  - Out-of-sample, Jan 2023 to Sep 2026, gross:
    - baseline: 928 trades, win rate 46.66%, average +0.0701R, profit factor 1.156, maximum drawdown 25.54R;
    - primary (10-minute range, 3R target, 10:30 cutoff): 906 trades, win rate 42.60%, average +0.0742R, profit factor 1.146, maximum drawdown 30.76R;
    - walk-forward: maximum drawdown 13.47R.
  - 2026 to 30 September was negative (−7.70R primary, −1.78R baseline).
  - With a 4¢ round-trip cost, the net average was +0.0535R and the 95% block-bootstrap confidence interval included zero.
  - Monte Carlo pass probabilities for a prop-firm challenge ($2,500 target, $1,500 loss limit) were mostly in single digits.
  - Source: [mericck QQQ ORB study](https://github.com/mericck/QQQ-Opening-Range-Breakout).
- **MQL5 replication, 25 Sep 2026** (the paper's ORB on NQ, SPX, Dow, DAX and FTSE CFDs, 2015–2026) [Blog]: gross reproduces (+0.131R on NQ, "as in the paper"). Net, "no market is distinguishable from zero, four of five are negative"; NQ nets +0.002R. "The pattern survives but the trade does not" — [MQL5 blog (per search summary)](https://www.mql5.com/en/blogs/post/776235).
- **Papers With Backtest:** a replication of "the most-cited recent version" on common data gives a full-sample Sharpe of −0.06 for 2010–2026 ("one variant on one instrument") — [Papers With Backtest ORB page (per search summary)](https://paperswithbacktest.com/strategies/orb-trading-strategy).
- **Pre-registered 225-cell futures study** [Preprint]:
  - Median gross edge of −0.01 ticks per trade. At $25 per round trip, a +$1.57M gross result becomes −$6.49M net.
  - The 5-minute opening range, reported as optimal on equities by Zarattini et al., was the worst window in its grid, with 28% of its cells "powered-negative".
  - Source: [ResearchGate preprint (per search summary)](https://www.researchgate.net/publication/414294507_Opening-Range_Breakout_Does_Not_Survive_Trading_Costs_A_Pre-Registered_225-Cell_Study_on_Sixteen_Years_of_Futures_Data).
- **Contrary evidence on a different rule:** Tsai et al. (IEEE Access, 2019) tested a "timely" ORB on index futures and report more than 8% annual returns with p-values below 3% in all five markets. This is not the Zarattini rule — [ResearchGate (per search summary)](https://www.researchgate.net/publication/331076454_Assessing_the_Profitability_of_Timely_Opening_Range_Breakout_on_Index_Futures_Markets). An earlier Umeå working paper, "Assessing the profitability of intraday opening range breakout strategies", also exists; I did not see its results — [IDEAS](https://ideas.repec.org/p/hhs/umnees/0845.html).

**Stocks-in-play ORB (Paper B)**
- **QuantConnect research post #18444:** covers 2016 only, the first year of the paper's own window, so it is not out-of-sample. Universe of 1,000 stocks, top 20 "in play". Sharpe 2.396 against 0.836 for SPY, beta −0.042; an ATR-percentage variant had Sharpe 2.237 and a 97% Probabilistic Sharpe Ratio — [QuantConnect](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/); [CoursIA issue noting 2016-only](https://github.com/jsboige/CoursIA/issues/16355); [Tradoki](https://blog.tradoki.com/posts/opening-range-breakout-stocks-in-play-research) (per search summary).
- **Separate QuantConnect community backtest** (different implementation, 2023–2025, 200-stock universe): Sharpe −0.502 — [QuantConnect embedded backtest (per search summary)](https://www.quantconnect.com/terminal/cache/embedded_backtest_01b8fa640b519cbc4a61330ce572c66c.html).
- **Critiques:** the stock-selection filter does most of the work, the 2016–2023 sample was volatile, the results rely on leverage and tight stops, and slippage assumptions matter a lot — [Papers With Backtest / commentary (per search summary)](https://paperswithbacktest.com/strategies/orb-trading-strategy).

**"Beat the Market" noise-area momentum on SPY (Paper C)**
- **Brusco replication** (SPY via Alpaca, Jul 2020 to Jul 2026; ES via Interactive Brokers, May 2024 to Jul 2026) [GitHub]:
  - Sharpe 1.11, alpha +16.7% a year (t 2.85), beta about 0. +2.6 bps per trade, win rate 41%, payoff ratio 1.69. The Quantitativo replication on ES found +2 bps, 36% and 2.1.
  - 2020–2024: Sharpe 1.4–2.0 every year; 2022 returned +25.8% while SPY fell 19.5%.
  - 2025: −4.9% (Sharpe −0.27). 2026 to date: −12.9% (Sharpe −1.91). ES results are almost identical (correlation 0.97), so the data feed is ruled out. Costs (about 0.4 bps per round trip) are ruled out too, since expectancy was −0.6 bps per trade.
  - Maróy (2025) claimed Sharpe above 3 through parameter optimization. A disciplined 27-variant grid picked the paper's own configuration, and quarterly walk-forward reselection destroyed value (Sharpe 0.57 vs 0.92 for the fixed configuration).
  - Verdict: "Not allocable today, not dismissible as dead either."
  - Source: [Brusco replication](https://github.com/giovannibrusco/zarattini-2024-momentum-spy); [Brusco CONCLUSIONS.md](https://github.com/giovannibrusco/zarattini-2024-momentum-spy/blob/main/docs/CONCLUSIONS.md).
- **Paz (Swedroe calls the author "Paz Serpa"), SSRN, June 2026** [WP]: the in-sample replication matches (Sharpe 1.34 over 2015–2024). Out of sample, May 2024 to Mar 2026, the strategy returned 9.4% in total against 29.5% for buy-and-hold, with a Sharpe of 0.39 — [SSRN 7290621 (per search summary)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7290621); [Swedroe Substack](https://larryswedroe.substack.com/p/when-beat-the-market-meets-the-real).
- **Delgado (Aug 2026), reported by QuantifiedStrategies:** Sharpe 0.35 from May 2024 to Aug 2026 — [QuantifiedStrategies on X (per search summary)](https://x.com/QuantifiedStrat/status/2096985725254205461).
- **nikolaosntinas18 replication** (1-minute SPY, 2016 to Sep 2026, paper's costs) [GitHub]:
  - Volatility-sized: train 2016–2021 at 16.0% a year, Sharpe 1.07; test 2022–2026 at 10.3% a year, Sharpe 0.75. SPY buy-and-hold in the test period: Sharpe 0.67.
  - Average leverage was 2.66. "The paper's headline return is mostly a result of leverage."
  - Source: [nikolaosntinas18](https://github.com/nikolaosntinas18/spy-intraday-momentum).
- **oleksandr replication** (Aug 2020 to Oct 2026, after costs; test period from 1 Jan 2024) [GitHub]:
  - The Band+VWAP version had a train Sharpe of 1.43 and a test Sharpe of −0.01. The dynamic-sizing version went from 1.55 to 0.00. SPY buy-and-hold in the test period: Sharpe 1.31.
  - Costs were 7–11% of gross profit.
  - Caveat: the IEX feed gives an approximate VWAP.
  - Source: [oleksandr](https://github.com/oleksandr123456787654321/spy_intraday_momentum).
- **Papers With Backtest:** in its library, "intraday time-series momentum replicates at −0.94" Sharpe and intraday time-series reversal at −0.91 — [Papers With Backtest (per search summary)](https://paperswithbacktest.com/strategies/orb-trading-strategy).

**India (NSE stocks, Nifty, Bank Nifty)**
- I found no peer-reviewed or working-paper replication of the Zarattini ORB or stocks-in-play strategy on NSE. Search results were blogs and vendors — see the next three items.
- **Bank Nifty ORB, 2015–2023:** 352% total return with a 48% drawdown before costs. After 0.03% slippage, ₹20 brokerage per lot and government charges, the author concluded it was "not profitable at all" — [saimohanreddy.com](https://saimohanreddy.com/orb-backtest-on-banknifty/) [Blog].
- **Nifty 50 ORB:** 2,122 trades from Jul 2017 to Mar 2026 on 15-minute data, with **no** costs or slippage modelled — [intradaylab.com](https://intradaylab.com/blog/nifty-orb-breakout-strategy-backtest) [Blog/Vendor].
- **Cost example:** a worked example puts the round-trip intraday futures cost for one Bank Nifty lot at about ₹255–280, against a gross winning trade of ₹1,680 — [onetradejournal.com](https://onetradejournal.com/learn/how-to-trade-the-opening-range) [Vendor].

### Inferences
- **Gross edges and Indian retail costs are the same size.** Replicated gross edges are about 0.07–0.13R per trade for index ORB and about 2–3 bps per trade for SPY noise-area momentum. Realistic retail costs are of that size or larger, which is why net results cluster around zero.
- **There are signs of decay after publication** for Paper C (2025–2026) and for the QQQ ORB (2026 negative in the mericck study; no edge on ES in 2026). But out-of-sample windows of about 2 years carry a Sharpe standard error of roughly 0.6, so "regime pause" and "arbitraged away" cannot yet be told apart. Brusco and oleksandr both make this point.
- **For NSE, every one of these strategies is an untested hypothesis.** The only Indian figures are blog backtests, and the one that included costs was unprofitable.

### Gaps
- No independent full-period (2016–2023) replication of Paper B with realistic slippage, and no 2024–2026 out-of-sample test of Paper B, was found.
- The Paz/Serpa figures and the MQL5 figures come from search summaries; the documents themselves were not readable here.
- The search budget ran out before further India-specific searches (for example Indian academic theses on ORB, or Nifty futures ORB studies with full cost modelling).

---

## 3. What does the academic literature show for intraday momentum, intraday reversal, opening-gap continuation vs fade, VWAP entries and time-of-day patterns, and how much survives costs?

### Takeaway
- **Market intraday momentum is a robust, peer-reviewed index-level effect:** the first half-hour return and the rest-of-day return predict the last 30 minutes. It holds in the US (1993–2013), in 16 developed markets and across 60+ futures. It is strongest when volatility is high, liquidity is low and dealers are short gamma. But the tradable payoff is a few basis points per trade, it is concentrated in crisis years, and implementations have weakened since 2024.
- **For single stocks, the dominant academic pattern is overnight-to-intraday reversal (gaps tend to fade).** This cuts against "gap-and-go", except possibly in extreme high-relative-volume catalyst names.
- **VWAP and time-of-day setups** have essentially no independent peer-reviewed evidence.
- **India** has one non-peer-reviewed study of intraday momentum linked to hedging demand.

### Cited Findings

**Market intraday momentum**
- **Gao, Han, Li & Zhou (2018), "Market intraday momentum", JFE 129(2):394–414** [PR]:
  - SPY, 1 Feb 1993 to 31 Dec 2013. The first half-hour return (measured from the previous close) predicts the last half-hour return. Adding the 12th half-hour return raises R² to 2.6%.
  - The effect is stronger on high-volatility days, recession days and some macro-news days, and is significant in- and out-of-sample.
  - The authors attribute it to day-trader behaviour and late informed trading.
  - Sources: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351); [working-paper PDF](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf); [Alpha Architect summary](https://alphaarchitect.com/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/).
- **Li, Sakkas & Urquhart (2022), Journal of Financial Markets 57, 100619** [PR]:
  - 16 developed markets; no emerging markets.
  - Intraday time-series momentum is "economically sizable and statistically significant both in- and out-of-sample in most countries". Evidence is weak in Austria, Canada, Ireland and New Zealand.
  - It is stronger when liquidity is low and volatility is high, and is linked to information discreteness and to how individualistic the country's culture is.
  - Sources: [IDEAS](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html); [Birmingham repository](https://research.birmingham.ac.uk/en/publications/intraday-time-series-momentum-global-evidence-and-links-to-market/). The working-paper version reports the effect in 12 of 16 markets — [FoFI 2020 WP](http://wp.lancs.ac.uk/fofi2020/files/2020/04/FoFI-2020-092-Zeming-Li.pdf).
- **Baltussen, Da, Lammers & Martens (2021), "Hedging demand and market intraday momentum", JFE 142(1):377–403** [PR]:
  - More than 60 futures on equities, bonds, commodities and currencies, 1974–2020.
  - The last 30 minutes are predicted by the rest of the day's return. The authors link this to gamma hedging by options market makers and leveraged-ETF rebalancing. The predictability reverses over the following days.
  - Sources: [SSRN abstract](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365); [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403). A secondary source says the effect is pronounced only in the negative-gamma regime — [Danfin (per search summary)](https://danfin.net/intraday-momentum-final-30-minutes).
- **India: Motwani(a), Burrin & Sharma, "Hedging Demand and Intraday Momentum within the Indian Stock Market"** [publication status unknown]: splits the 09:15–15:30 NSE session into half-hours. The first half-hour return is more predictive when it has the same sign as the overnight and prior-day signals, and the paper cites a 13% Sharpe-ratio improvement — [ResearchGate](https://www.researchgate.net/publication/383567351_Hedging_Demand_and_Intraday_Momentum_within_the_Indian_Stock_Market).
- **Other India evidence (weak or indirect):**
  - A short six-month, 30-minute-data study says Indian last-half-hour returns depend on the first half-hour and the prior day's last hour — [Scribd (secondary, weak)](https://www.scribd.com/document/670520471/MomentumTrading).
  - Murphy & Thirumalai (2017) find interday cross-sectional momentum in India, partly driven by institutions executing large orders — [cited in EFMA 2024 paper](http://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2024-Lisbon/papers/Interday_Cross_Sectional_Momentum.pdf).
- **How much survives costs:** the US noise-area implementation earned about +2.6 bps per trade gross (Brusco) and +2 bps on ES (Quantitativo). It survived institutional costs of about 0.4 bps per round trip on ES through 2024, but turned negative in 2025–26 — [Brusco](https://github.com/giovannibrusco/zarattini-2024-momentum-spy/blob/main/docs/CONCLUSIONS.md).

**Intraday reversal and the overnight-to-intraday relationship (gap fade vs continuation)**
- **Branch & Ma:** overnight returns are negatively related to the following intraday return — [ResearchGate](https://www.researchgate.net/publication/256033323_Overnight_Return_the_Invisible_Hand_behind_Intraday_Returns).
- **An extension of Branch & Ma on US stocks** finds a "very strong negative autocorrelation between overnight and intraday returns". "The more extreme the overnight movement, the greater the intraday reversal." It cites Stoll & Whaley (1990) for the NYSE, with the strongest reversal in the morning — [Tilburg thesis (per search summary; attribution likely)](http://arno.uvt.nl/show.cgi?fid=144554).
- **Akbas, Boehmer, Jiang & Koch (2022)** document strong intraday-vs-overnight reversal in stocks. **Baltussen, Da & Soebhag** document sharp "end-of-day reversal" in the last 30 minutes — [EFMA 2024 End-of-Day Reversal paper](http://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2024-Lisbon/papers/EndofDayReversal_withnames.pdf) [WP].
- **Della Corte & Kosowski:** a naive overnight-to-intraday reversal strategy earns an average excess return, but the pattern "is more likely induced by firm specific liquidity" — [CICF paper](https://www.cicfconf.org/sites/default/files/paper_357.pdf) [WP].
- **arXiv 2507.04481:** continuation from intraday to intraday and from overnight to overnight, with a negative contemporaneous correlation between intraday and overnight returns, which produces reversal between the two — [arXiv](https://arxiv.org/pdf/2507.04481) [Preprint].
- **Gap trades in futures (MNQ):** after friction, all gap-fill fades failed; gap-continuation shorts were the "most credible near-miss" — [arXiv 2605.04004 (per search summary; attribution uncertain)](https://arxiv.org/pdf/2605.04004) [Preprint].
- **Nifty:** a popular analysis says overnight returns drove most of the index's long-run gains while intraday-only returns were weak — [Multibagg, citing Capitalmind](https://www.multibagg.ai/market-pulse/articles/nifty-overnight-intraday-returns-study-cmqxr9lq34t09o20jum5tsveq) [Blog, not peer-reviewed].

**VWAP-based entries**
- In Paper C, VWAP is used only as a trailing stop. Replications conflict on whether it helps:
  - "The VWAP condition helps in both periods" — [nikolaosntinas18](https://github.com/nikolaosntinas18/spy-intraday-momentum).
  - The VWAP-stop advantage "is gone" in the 2024–26 test period, possibly because the IEX feed gives an approximate VWAP — [oleksandr](https://github.com/oleksandr123456787654321/spy_intraday_momentum).
- Aziz's books treat VWAP as a buyer/seller control line, with short setups when sellers take control — [Book-summary: Goodreads](https://www.goodreads.com/book/show/60679643-how-to-day-trade-for-a-living).
- I found no independent peer-reviewed test of VWAP reversal or VWAP false-breakout entries.

**Time-of-day and opening-range length**
- **Aziz's timing guidance:** bull-flag and VWAP trades in the first 1.5 hours; reversal, VWAP, moving-average and support/resistance trades at midday; "never" bull flags at midday or at the close — [Goodreads listing (Book-summary)](https://www.goodreads.com/book/show/60679643-how-to-day-trade-for-a-living).
- **Opening-range length results conflict:**
  - In the authors' own stocks-in-play test, the 5-minute range was best (Q1).
  - In the 225-cell futures grid, the 5-minute range was worst — [ResearchGate preprint (per search summary)](https://www.researchgate.net/publication/414294507_Opening-Range_Breakout_Does_Not_Survive_Trading_Costs_A_Pre-Registered_225-Cell_Study_on_Sixteen_Years_of_Futures_Data).
  - On QQQ 2017–2026, 10- and 15-minute ranges were positive gross, and the best development-period configuration did not beat the plain baseline out of sample — [mericck](https://github.com/mericck/QQQ-Opening-Range-Breakout).
- **Heston, Korajczyk & Sadka**, "Intraday Patterns in the Cross-section of Stock Returns", is the standard reference on half-hour periodicity — [arXiv 1005.3535](https://arxiv.org/pdf/1005.3535). I did not verify its details this session.

### Inferences
- **The academic intraday-momentum effect is an index effect in the last 30 minutes that depends on volatility and gamma.** It is not a single-stock opening-breakout effect.
  - On NSE, the natural analog is Nifty or Bank Nifty timing in the last half-hour (15:00–15:30 IST). NSE's very large index-options market makes the gamma-hedging channel plausible, and the Motwani et al. study points the same way.
  - Implementing it needs index futures or options, or an ETF where costs relative to small moves are severe. Index-futures lot sizes are likely far beyond a ₹20,000 account (verify).
- **Gap trading.** The stock-level literature on average favours fading overnight moves, especially large ones. Aziz-style "gap-and-go" momentum therefore stands against the base rate. Any continuation edge would have to come from conditioning on catalyst and extreme relative volume, which is Paper B's claim, and that claim lacks independent replication.
- **Survival after costs.** Index momentum survives only at institutional costs (around 0.4 bps per round trip on futures). Retail cash-equity costs in India, roughly 8–11 bps per round trip before slippage (see Q6), are 20 or more times the per-trade edge of a few bps found in the SPY studies.

### Gaps
- Gao et al.'s trading-strategy annualized return and Sharpe were not retrieved; I did not find the commonly cited figures in this session. I also found no direct study of whether market intraday momentum decayed after 2013 or after publication, other than the Paper C replications.
- I found no peer-reviewed NSE study of gap fade vs continuation, VWAP entries, or the cross-section of intraday stock reversal.
- Heston–Korajczyk–Sadka's findings and their cost survival were not verified (search budget exhausted).

---

## 4. Which setups in Aziz's books have codeable rules, and does quantitative evidence exist for each?

### Takeaway
Only the opening-range breakout (and the VWAP-trend and noise-area relatives) has precise published rules and quantitative tests, and those tests are by Aziz's own research group (Q1–Q2). ABCD, bull flag, red-to-green, fallen angel, top/bottom reversal, support/resistance and moving-average trend are described as discretionary chart patterns. They need explicit parameter choices before they can be coded, and I found no rigorous quantitative evidence for any of them as intraday stock setups. The bull-flag studies that exist use daily index data and give mixed results.

### Cited Findings
- **Strategies in "How to Day Trade for a Living":** ABCD Pattern; Bull Flag Momentum; Reversal Trading (two chapters: top and bottom reversal); Moving Average Trend Trading; VWAP Trading; Support or Resistance Trading; Red-to-Green Trading; Opening Range — [Goodreads listing](https://www.goodreads.com/book/show/60679643-how-to-day-trade-for-a-living) [Book-summary]. Chapter numbering differs between summaries — [TraderLion](https://traderlion.com/trading-books/how-to-day-trade-for-a-living/); [Bookey](https://www.bookey.app/book/day-trading-for-a-living).
- **Bull flag:** long-only, "should not be shorted", "mostly a momentum and scalping setup" — [Goodreads listing](https://www.goodreads.com/book/show/60679643-how-to-day-trade-for-a-living). Described as a close relative of ABCD with a tighter, channel-like pullback — [Shortform overview (per search summary)](https://www.shortform.com/books/blog/how-to-day-trade-for-a-living-by-andrew-aziz.html).
- **ABCD:** a strong initial move to new highs (A to B), then a pullback, with the trade typically taken near C on a bet that the pullback ends there — [Snappchart ABCD explainer](https://www.snappchart.app/blog/beginner-playbook/andrew-aziz-trading-strategy); [Shortform](https://www.shortform.com/summary/how-to-day-trade-for-a-living-summary-andrew-aziz) [Book-summary].
- **Moving averages:** one secondary source says Aziz uses the 9 and 20 EMAs; not verified against the book — [Book-summary (per search summary)](https://traderlion.com/trading-books/how-to-day-trade-for-a-living/).
- **"Advanced Techniques in Day Trading", Chapter 6 "Advanced Day Trading Strategies":**
  - The strategies listed are Strategy 1 Fallen Angel, 2 ABCD / Reverse ABCD, 3 Bull Flag / Bear Flag, 4 Opening Range Breakout and 5 VWAP Trading, according to a table-of-contents excerpt seen via search — [Goodreads](https://www.goodreads.com/book/show/57760551); [Shortform overview](https://www.shortform.com/books/blog/advanced-techniques-in-day-trading.html) (per search summary).
  - Excerpts say VWAP Reversal and VWAP False Breakout are best late-morning, and VWAP Moving Average Trend and VWAP False Breakout best at midday — (per search summary of book excerpts) [Shortform](https://www.shortform.com/pdf/advanced-techniques-in-day-trading-pdf-andrew-aziz).
  - The publisher's description says each strategy comes with "entry, exit, stop loss" — [Better World Books listing](https://www.betterworldbooks.com/product/detail/advanced-techniques-in-day-trading-a-practical-guide-to-high-probability-strategies-and-methods-9781721151264).
- **Bull-flag quantitative evidence (daily data, not intraday):**
  - Leigh and coauthors (2002) built a template-matching bull-flag recognizer that "generated profits that exceeded random trading". Wang & Chan (2007) applied it to TAIEX, and a thesis reports "the exact opposite was true for the TAIEX" (the snippet is truncated).
  - The two papers define the flag differently: Wang & Chan use a horizontal flag.
  - Source: [Porto master's thesis reviewing both (per search summary)](https://repositorio-aberto.up.pt/bitstream/10216/146608/2/597048.pdf); [figure of the Leigh et al. template](https://www.researchgate.net/figure/Representation-of-a-stock-price-chart-showing-the-bull-flag-stock-pattern_fig3_220508078).
- **ORB and VWAP-trend evidence** comes from the authors' group (Papers A–C and a VWAP paper). Independent replications are mixed to negative after costs (Q2).

**Codeability and evidence by setup.** Rule status is my assessment; evidence entries refer to the citations above.

| Setup (book) | Can it be coded as written? | What must be pinned down to code it | Quantitative evidence found |
|---|---|---|---|
| Opening Range Breakout (HTDTFAL "Open Range"; Advanced Techniques Strategy 4) | **Yes.** Published rules in Papers A and B | Range length (5, 10, 15 or 30 min); relative volume = range-window volume ÷ 14-day mean of the same window; top-N; direction filter (first-candle colour); stop (range extreme vs 10% of 14-day ATR); end-of-day exit; 1% risk; leverage cap | Authors' working papers strong; independent tests: gross yes, net about zero for index products; stocks-in-play version not independently replicated (Q2) |
| VWAP trading / VWAP false breakout / VWAP reversal | **Partly.** VWAP is objective; "false breakout" and "reversal" are not | Bars allowed beyond VWAP before a close back across it; confirmation candle; stop beyond the swing extreme; target (previous high/low, 9/20 EMA) | Only as a trailing-stop component in Paper C (replications conflict); authors' VWAP-trend paper (figures unverified); nothing independent |
| Moving-average trend (9/20 EMA per secondary source) | **Yes**, once lengths and timeframe are fixed | EMA lengths; 1- vs 5-minute bars; entry on pullback to the EMA; exit on a close below | None found |
| ABCD / Reverse ABCD | **Only after operationalizing** | Swing-point (zigzag) algorithm; minimum A→B move (e.g. ×ATR); C must hold above A; retracement bounds (e.g. 38–62%); entry on break of the C-bar high or of B; stop below C; target projection | None found |
| Bull / bear flag | **Only after operationalizing** (template matching possible) | Pole (minimum % move and volume surge within N bars); flag (maximum retracement, maximum bars, declining volume); breakout trigger; stop below the flag low | Daily-index template studies only, mixed (Leigh et al. vs Wang & Chan); none on intraday stocks |
| Top / bottom reversal | **Partly** | Extension measure (consecutive same-colour candles, distance from VWAP or Bollinger, RSI extreme; the book's exact thresholds were not verified); key-level proximity; reversal-candle trigger | Indirect support only, from the stock overnight→intraday and end-of-day reversal literature (Q3); no test of the setup itself |
| Red-to-green (cross of the previous close) | **Yes**, mechanically | Gap-down condition; trigger on trade above the previous close; stop below the intraday low or VWAP; target next level; "in play" filter | None found |
| Fallen angel (Advanced Techniques Strategy 1) | Unknown (rules not retrieved) | n/a | None found |
| Support / resistance | **Subjective** unless levels come from an algorithm | Level source (previous-day high/low/close, pre-open high/low, round numbers, pivots); touch tolerance; rejection candle | None found |

### Inferences
- **For the user's tool:** only ORB (with a stocks-in-play-style relative-volume filter) and VWAP/noise-area trend rules are specified precisely enough to backtest without many arbitrary choices.
  - Every other Aziz setup needs 4–8 free parameters. Tuning them on the same data invites the multiple-testing problem that the Maróy and walk-forward experiments exposed (Q2).
  - Freeze each setup's parameters before evaluating its paper trades.
- **None of Aziz's setups has independent evidence of net profitability after costs.** "Codeable" should not be confused with "validated".

### Gaps
- I could not access the books' exact rule text (entry trigger, stop, target, RSI or candle thresholds for reversals; the fallen-angel definition; red-to-green specifics). Summaries were secondhand and sometimes inconsistent.
- I found no backtests of ABCD, red-to-green, fallen angel or support/resistance setups beyond vendor marketing. The search budget was exhausted before targeted searches on these.
- The setups from Gujral & Vaidya's "How to Make Money in Intraday Trading" were not researched in this session.

---

## 5. What is the base rate of profitability for retail day traders in rigorous studies, and what distinguished the few profitable ones?

### Takeaway
Rigorous population studies put persistent, predictable day-trading profitability at about 1% of traders or fewer:
- Taiwan: fewer than 1% reliably earn positive abnormal returns net of fees.
- Brazil: 97% of those who persisted more than 300 days lost money, and only 1.1% earned more than the minimum wage.
- India: SEBI found 71% of intraday cash-equity traders lost money in FY23, and more than 91% of individual F&O traders lost money in FY25.

The few winners were mostly those who had already shown persistent past success. Frequent trading is associated with worse outcomes in India.

### Cited Findings
- **Barber, Lee, Liu & Odean (2014), "The cross-section of speculator skill: Evidence from day trading", Journal of Financial Markets 18:1–24** [PR]:
  - Taiwan, 1992–2006. Day traders account for 17% of TSE volume.
  - "Less than 1% of the total population of day traders is able to predictably and reliably earn positive abnormal returns net of fees."
  - The spread between top- and bottom-ranked traders exceeds 70 bps per day. Heavy day traders' trades are profitable before costs. "The trades of previously successful traders are profitable even after accounting for costs."
  - Sources: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1386418113000190); [eScholarship](https://escholarship.org/uc/item/7k75v0qx).
- **Aggregate performance:** day traders' net-of-fee performance was negative in each of the 15 years studied — [Barber et al. (per search summary)](https://escholarship.org/content/qt7k75v0qx/qt7k75v0qx.pdf). A related paper on learning: [Barber, Lee, Liu, Odean & Zhang, "Learning, fast or slow" (SSRN)](https://dx.doi.org/10.2139/ssrn.2535636).
- **Chague, De-Losso & Giovannetti, "Day Trading for a Living?"** [WP, FGV / SSRN 3423101]:
  - Brazil equity (mini-index) futures, individuals who started in 2013–2015.
  - "97% of all individuals who persisted for more than 300 days lost money." Only 1.1% earned more than the Brazilian minimum wage, and only 0.5% more than a bank teller's starting salary; one summary says 0.4%.
  - "No evidence of learning."
  - Sources: [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101); [FGV WP](https://repositorio.fgv.br/server/api/core/bitstreams/0f00dd78-6909-4f91-84d5-aef8803e6436/content).
  - A summary reports 19,646 individuals and a top trader averaging about US$310 a day with a standard deviation of US$2,560 — [Tradicted summary](https://www.tradicted.com/research/chagu-day-2020/).
  - A 2025 follow-up on the COVID-era cohort reportedly found similarly poor results — [CurrentMarketValuation review (per search summary)](https://www.currentmarketvaluation.com/posts/the-data-on-day-trading.php).
- **SEBI (July 2024), intraday trading in the equity cash segment** [Regulator]:
  - 71% of individual intraday traders made net losses in FY23, up from 65% in FY19.
  - The average loss per loss-making trader was ₹5,371.
  - Traders under 30 made up 48% of intraday traders in FY23, against 18% in FY19.
  - 80% of those making more than 500 trades a year lost money.
  - Sources: [SEBI PDF](https://www.sebi.gov.in/sebi_data/attachdocs/jul-2024/1721818140715.pdf); [ThePrint](https://theprint.in/economy/71-of-intraday-traders-incur-losses-finds-sebi-report-impact-higher-among-young-small-traders/2192598/); [Business Standard](https://www.business-standard.com/amp/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html) [Press].
- **SEBI (July 2025), equity derivatives:** individual traders' net losses after transaction costs rose to ₹1,05,603 crore in FY25 from ₹74,812 crore in FY24. More than 91% of traders lost money. The study covered the top 13 brokers, with about 96 lakh unique traders — [Business Standard](https://www.business-standard.com/amp/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html) [Press, reporting Regulator].

### Inferences
- **The prior for a new manual intraday trader on NSE is a net loss.** The specific risk factors SEBI documented (high trade frequency, small accounts, young traders) argue for a low-frequency, pre-registered rule set in the user's tool, rather than many discretionary flags a day.
- **Persistence is the one marker of the profitable minority in Taiwan,** that is, previously successful traders. Paper trading every flag is consistent with this: it builds a track record before risking money. But see the sample-size arithmetic in Q6: a few hundred trades cannot confirm a small edge.

### Gaps
- What separated profitable traders beyond past success (strategy type, holding period, trading style) was not retrieved. Studies of SOES-era profitable day traders and the details of "Learning, fast or slow" were not obtained because the search budget ran out.
- The SEBI PDFs could not be opened directly (sebi.gov.in blocked); the figures are from press coverage of the studies.

---

## 6. Which ingredients of these edges depend on US market structure and may weaken on NSE? What does this mean for a ₹20,000 account risking ₹200 per trade?

### Takeaway
The edges with documented results rest on several US-specific supports:
- a ~7,000-stock universe from which to pick the top-20 relative-volume names;
- per-share commissions of $0.0005–0.0035 and 1¢ ticks, with zero or near-zero assumed slippage;
- 4x intraday leverage;
- easy two-sided trading with no daily price limits;
- premarket information (the NQ 09:25 filter);
- a dealer-gamma channel in US index options and leveraged ETFs.

On NSE, percentage-based taxes and brokerage make costs measured in R roughly ten times larger for the same tight stop. For a ₹200 R with a 10%-ATR-style stop, charges alone are about 0.3–0.45R per trade, and about 0.5–0.8R once realistic slippage is added. That is larger than any replicated gross edge (0.07–0.13R). Tight-stop intraday setups from these papers are therefore very unlikely to be net-profitable for this account.

### Cited Findings
- **The stocks-in-play edge comes from top-20 relative-volume selection** out of about 7,000 US stocks with price above $5, ATR above $0.50 and average volume of at least 1M shares — [Tradoki](https://blog.tradoki.com/posts/opening-range-breakout-stocks-in-play-research); [paper copy](https://www.researchgate.net/publication/379003745_A_Profitable_Day_Trading_Strategy_For_The_US_Equity_Market) (per search summary).
- **The QQQ ORB depends on execution:** break-even at about 2.2¢ per share of slippage against a QQQ spread of about 1¢. The paper's zero-slippage assumption is "the single load-bearing input" — [Brusco](https://github.com/giovannibrusco/qqq-opening-bias-5min).
- **Premarket and overnight information:** the NQ futures 09:25 bar added information beyond QQQ's own pre-open move (t = 2.05 vs t = 1.27 for the placebo), in-sample — [Brusco](https://github.com/giovannibrusco/qqq-opening-bias-5min).
- **US cost model:** $0.0035 per share commission (Interactive Brokers entry tier) and $0.001 per share slippage — [svettelnova](https://github.com/svettelnova/intraday-momentum-spy). Leverage: 1%-risk sizing under a 4x FINRA day-trading cap — [Brusco](https://github.com/giovannibrusco/qqq-opening-bias-5min).
- **Mechanism:** index intraday momentum is linked to options market-maker and leveraged-ETF gamma hedging — [Baltussen et al. (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365). It is stronger in low-liquidity, high-volatility markets — [Li, Sakkas & Urquhart (IDEAS)](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html). An Indian study links intraday momentum to hedging demand — [Motwani et al. (ResearchGate)](https://www.researchgate.net/publication/383567351_Hedging_Demand_and_Intraday_Momentum_within_the_Indian_Stock_Market).
- **NSE cost evidence:** a Bank Nifty ORB became unprofitable after 0.03% slippage plus ₹20 per lot and government charges — [saimohanreddy.com](https://saimohanreddy.com/orb-backtest-on-banknifty/). One Bank Nifty futures lot costs about ₹255–280 per intraday round trip — [onetradejournal.com](https://onetradejournal.com/learn/how-to-trade-the-opening-range).
- **Drawdowns in R units:** a QQQ ORB with positive gross out-of-sample expectancy (+0.07R per trade) still had maximum drawdowns of 25.5–30.8R; the walk-forward version had 13.5R. The development-period maximum drawdown was 17.6R — [mericck](https://github.com/mericck/QQQ-Opening-Range-Breakout).
- **Frequent trading is associated with higher loss rates in India** (80% loss-makers among those making more than 500 trades a year) — [Business Standard on SEBI study](https://www.business-standard.com/amp/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html).

### Inferences
NSE market-structure facts below are my background knowledge and were **not verified this session** (nseindia.com, sebi.gov.in and zerodha.com were blocked and the search budget was exhausted). They are flagged "(verify)".

**Ingredients likely to weaken or break on NSE**
1. **Universe breadth and the stocks-in-play filter.** A top-20 relative-volume screen on NSE would be dominated by illiquid small caps, many with daily price bands (verify: 2/5/10/20% for non-F&O stocks; F&O stocks use dynamic bands). A stock locked at its circuit limit traps positions and makes stop orders meaningless.
   - Restricting the screen to F&O stocks or a liquid MIS-eligible list (roughly the top 200 by turnover) keeps it tradable but shrinks the pool of real "in play" names.
   - The paper's relative-volume ≥ 100% and top-20 thresholds were tuned on the US cross-section and should not be assumed to carry over.
2. **No US-style premarket.** NSE has only a 15-minute pre-open call auction (verify: 09:00–09:15), with no continuous extended-hours trading in which US gappers form. The pre-open equilibrium price and GIFT Nifty may partly stand in for the NQ 09:25 information, which is untested.
3. **Catalyst timing differs.** US earnings and news cluster before the open and after the close. Indian corporate results and filings often land during market hours or after the close (verify), so the "news gap at the open" structure behind stocks-in-play is less systematic.
4. **Shorting.** Papers A, B and C all trade both directions. Intraday MIS shorting on NSE is allowed but must be squared off the same day; this does not bind an end-of-day-exit strategy. Two risks: upper-circuit locks can trap shorts, and failure to square off risks short-delivery auction penalties (verify broker auto square-off times).
5. **Costs are percentage-based, not per share.** This is the decisive difference; see the arithmetic below.
6. **Leverage.** The US papers use up to 4x. NSE MIS leverage is about 5x (verify), so a ₹20,000 account can hold at most about ₹1,00,000 of notional. With ₹200 risk, the tightest feasible stop is therefore about ₹200 ÷ ₹1,00,000 = 0.2% of price. A 10%-of-ATR stop on a liquid NSE stock with a 2–3% ATR (about 0.2–0.3%) sits right at that limit.
7. **Index-level momentum (the Paper C / Gao family)** is the most plausibly transferable mechanism, given NSE's huge index-options gamma, but it is hard to use at ₹20,000. Index-futures lot notional and margin are likely many times the account (verify current lot sizes after SEBI's 2024 contract-size changes). Option-premium versions face flat brokerage plus STT on option sales, which is large relative to a ₹200 R (verify current STT rates, including any 2026 Budget changes).

**Cost measured in R for a ₹200-risk account (illustrative; verify current charges)**
- **The formula.** With fixed rupee risk, notional = ₹200 ÷ stop%. So **cost in R ≈ round-trip friction % ÷ stop distance %**.
- **Assumed Zerodha intraday-equity rates** (as I understand them; verify): brokerage the lower of ₹20 and 0.03% per order; STT 0.025% on the sell side; exchange charge about 0.003% per side; stamp duty 0.003% on the buy side; GST 18% on brokerage and fees.
  - That gives statutory plus brokerage friction of about **0.08% (large orders, ₹20 cap) to 0.11% (small orders) per round trip**.
  - Adding realistic slippage for manual market and stop orders of about 0.02–0.05% per side gives a total of about **0.12–0.20%**.
- **Resulting cost per trade:**

| Stop distance (% of price) | Notional at ₹200 risk | Approx. cost per trade in R |
|---|---|---|
| 0.25% (≈10% of a 2.5% ATR, the Paper B rule) | ₹80,000 | **≈0.5–0.8R** |
| 0.5% | ₹40,000 | ≈0.25–0.4R |
| 1.0% (ORB-extreme stop on a volatile name) | ₹20,000 | ≈0.12–0.2R |
| 2.0% (wide intraday or swing stop) | ₹10,000 | ≈0.06–0.1R |

- **Compared with the US paper's cost model:** a $50 stock with a $0.20 stop has round-trip commission of $0.007, about 0.035R. Indian retail friction in R is therefore roughly **10x higher** for the same stop geometry.
- **Implication:** only setups with gross expectancy of at least about 0.2R per trade and stops of at least 1–2% of price can plausibly carry NSE retail costs. No replicated intraday evidence found here shows gross expectancy that large.

**Risk of hitting the 10R (₹2,000) trial stop, and sample size**
- **Assumption:** treat the R outcomes as a random walk with per-trade mean μ and standard deviation σ. The probability of ever falling 10R below the start is about exp(−2μ·10/σ²).
- **For the best-documented gross ORB numbers** (μ ≈ +0.07R, σ ≈ 1.3R for a 2R-target system with about 45% wins), that probability is about exp(−0.83) ≈ **44% even with a real pre-cost edge**.
- **With costs taking μ to zero or below,** hitting −10R becomes near-certain over a long enough trial. For tight-stop, low-win-rate systems (σ ≈ 2–3R), it is about 60–80% even at μ = +0.1R.
- The observed 13–31R maximum drawdowns of a positive-expectancy QQQ ORB (mericck) show the same thing: **a 10R stop rule will usually end a trial by variance alone.** It cannot tell a small edge from no edge.
- **Detecting an edge:** distinguishing μ = +0.07R from zero at about 2 standard errors needs about (2 × 1.3 ÷ 0.07)² ≈ **1,400 trades**. For μ = +0.15R it needs about 300 trades.
- A few months of paper trading flags can only rule out large negative or large positive edges. The tool should log, for every flag: gross R, an explicit cost in R (charges plus slippage against the signal price), time-of-day, relative volume and setup parameters, so that net expectancy is measured rather than assumed.

**What transfers best (ranked by evidence quality; still unproven on NSE)**
1. **Index intraday momentum (last half-hour).** Peer-reviewed in many markets, with a plausible mechanism in India, but impractical at ₹20,000 and weakening post-2024 in the US.
2. **ORB on liquid instruments, with wider stops.** Gross edges replicate on US index products, but net results are about zero. On NSE it needs a frozen rule set and a large paper-trade sample.
3. **Stocks-in-play ORB with a tight ATR stop.** No independent replication, and on cost-in-R grounds it should be considered **not viable** for this account.
4. **Discretionary Aziz patterns (ABCD, bull flag, red-to-green, reversal).** No quantitative evidence; treat as hypotheses to log, not edges.

### Gaps
- Current NSE and Zerodha facts were not verified this session and should come from sibling notes or direct checks:
  - exact charges as of Oct 2026, including any STT changes in the Feb 2026 Budget;
  - MIS leverage and auto square-off time;
  - tick-size rules, including reported 2025 changes;
  - price-band and dynamic-band rules for F&O vs non-F&O stocks;
  - pre-open session timings;
  - F&O ban-list mechanics;
  - current Nifty and Bank Nifty lot sizes and margins.
- I found no data on typical NSE bid-ask spreads or slippage for manual Kite orders during the 09:15–09:20 opening window. This is the single most important unknown for any ORB-type rule on NSE.
- No study tests whether US "stocks in play" thresholds (relative volume, ATR, price, top-N) carry over to the NSE cross-section, or how often NSE in-play names hit circuit limits intraday.
