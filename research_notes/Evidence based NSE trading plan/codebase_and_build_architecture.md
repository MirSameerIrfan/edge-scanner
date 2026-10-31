# Codebase review and build architecture for "tradingtool" (NSE, Kite Connect, Python 3.13)

_How this was researched (31 Oct 2026). I read both local repositories directly. I read the official pykiteconnect 5.2.2 source from its PyPI wheel/sdist, plus the official Kite JS (npm 5.3.0) and Go (v4.4.3) clients. I queried PyPI metadata for every candidate library and ran small in-session experiments: kiteconnect on Python 3.13.18, DuckDB vs SQLite cross-process access, NSE trading calendars, and the Textual API. I also fetched the Claude Code headless docs. kite.trade, zerodha.com and duckdb.org could not be fetched: they are outside this session's allowed network domains and would have to be allowed in the session's network settings. The GitHub API was limited to the two configured repos, and this turn's shared web-search budget ran out, so facts that normally come from those sources are listed under Gaps rather than stated._

---

## 1. What /home/user/tradingtool already contains, decides and constrains

### Takeaway
tradingtool is a one-commit design seed of 389 lines. It holds a glossary, one ADR that fixes the human-in-the-loop flow, a news reader with 7 tests that uses only the standard library, and a pyproject that requires Python ≥3.13 under uv with no runtime dependencies. The flow the ADR fixes is: code raises flags → the model gives a verdict → the trader makes the final call → every flag is paper traded → a three-line scoreboard. The repo pins down vocabulary and the decision flow. It leaves open everything about time (candle size, flag timestamp, entry price), storage, the shadow Haiku verdict, trial and pass-mark metrics, and holding periods other than intraday.

### Cited Findings
**Inventory and project settings**
- The whole repo is `CONTEXT.md` (64 lines), `docs/adr/0001-setups-are-code-model-judges-trader-decides.md` (14), `src/tradingtool/news.py` (183), `tests/test_news.py` (108), `pyproject.toml` (19), `src/tradingtool/__init__.py`, `.python-version` (`3.13`), `.gitignore` and `uv.lock`. It has one commit, `0fb5ab4` "Add trading tool design docs and news reader" (2026-10-31, Mir Sameer) — [tradingtool git log](/home/user/tradingtool)
- pyproject sets name `tradingtool` 0.1.0, with description *"Personal intraday tool: flags book setups on a watchlist of NSE stocks and records the verdicts on them."*. It also sets `requires-python = ">=3.13"`, `dependencies = []`, build backend `uv_build>=0.11.23,<0.12.0`, and dev group `pytest>=9.1.1` — [pyproject.toml](/home/user/tradingtool/pyproject.toml)
- `.gitignore` excludes `.env` and `.env.*`, so secrets are meant to stay out of git — [.gitignore](/home/user/tradingtool/.gitignore)

**Glossary decisions (CONTEXT.md)** — [CONTEXT.md](/home/user/tradingtool/CONTEXT.md)
- **Trader** (avoid "User"): the one person who uses the tool and places every order by hand.
- **Watchlist** (avoid "Universe"): the fixed set of stocks the tool watches, chosen by the trader from the screen's proposals.
- **Screen** (avoid "Scanner"): the periodic filter that proposes watchlist candidates by how tradable, liquid and active they are.
- **In play**: a watchlist stock that passes a setup's daily selection test on a given morning. Setups that have such a test flag only stocks in play.
- **Setup** (avoid "rule, strategy, pattern"): a coded condition, taken from a trading book, that marks a moment in one stock as worth a look.
- **Setup card**: a one-page statement of a setup giving its conditions, entry, exit and stop, the book passage behind each, and every gap the book left. *"The trader signs it off before the setup is coded."*
- **Flag** (avoid "signal, alert, opportunity"): *"One occurrence of a setup being met by one stock at one candle."*
- **Verdict**: the model's take-or-skip on one flag, with its reasons and the book passage it relied on. **Final call** (avoid "Decision"): the trader's take-or-skip, made *after seeing the verdict*.
- **Intraday trade** (avoid "Day trade"). **Replay** (avoid "Backtest"): running a setup over past candles to measure its raw result; *"It never decides a trade."* **Paper trade**: *"A simulated trade recorded at market prices with no real money at risk."* **Trial**: the period in which a setup's flags are paper traded against the pass mark. **Scoreboard**: *"all of them, those the verdict took, and those the final call took."* **Pass mark**: the paper-trading result, *"fixed before a trial starts"*, that a setup must reach before it trades real money.

**ADR 0001** — [ADR 0001](/home/user/tradingtool/docs/adr/0001-setups-are-code-model-judges-trader-decides.md)
- Why: a model that decides on its own *"can't be tested on history: it answers differently from run to run, and for past dates it already knows how the market turned out."*
- Decision: setups are deterministic code that raises flags. The model gives take-or-skip, its reasons and a book passage. The trader makes the final call after seeing the verdict. *"Every flag is paper traded whatever the verdict and final call say, so the scoreboard shows whether the raw setup, the model's filtering or the trader's final calls actually make money."*
- Rejected options: the model deciding alone; coded rules deciding alone; and the trader giving a verdict before seeing the model's (the trader rejected this one).
- Consequences: *"The trader's unaided judgement is never measured. The scoreboard can only show whether overriding the model helps."* *"The model never raises flags, so replay measures setups alone; verdicts can only be scored on paper, forward in time."*

**news.py and its tests** — [news.py](/home/user/tradingtool/src/tradingtool/news.py), [test_news.py](/home/user/tradingtool/tests/test_news.py)
- It reads three feeds:
  - NSE corporate announcements RSS (`nsearchives.nseindia.com/content/RSS/Online_announcements.xml`)
  - Economic Times markets RSS (`…/rssfeeds/1977021501.cms`)
  - Google News RSS searched per company (`"<main name>" when:1d`, `hl=en-IN`, `gl=IN`)
- *"Full article text is not fetched here; that happens at a flag, through Firecrawl."*
- All timestamps are timezone-aware IST (`ZoneInfo("Asia/Kolkata")`). NSE dates carry no zone and are treated as IST; other feeds are parsed with `parsedate_to_datetime` and converted to IST.
- Requests send a browser User-Agent because *"NSE's archive refuses requests that don't look like a browser."*
- Matching rules:
  - An NSE item matches only if its whole company name equals one of the stock's names, after dropping "limited"/"ltd". "KSB Pumps Limited" does not match "KSB Ltd."
  - Other sources match any of the names as whole words, case-insensitive.
- Parsing details: ET's double-escaped entities are unescaped twice, and Google's HTML is stripped. A feed that fails is reported to stderr and skipped.
- It uses only the standard library (urllib, ElementTree, zoneinfo).
- There are 7 tests, all deterministic with inline XML fixtures dated 16-Oct-2026. They cover IST parsing, skipping bad dates, entity decoding, HTML stripping, name matching, newest-first recency filtering, and the Google URL parameters.

### Inferences
- **Hard constraints for the architecture:**
  - Setups must be pure functions of candles plus explicit state, with no wall-clock reads, because the ADR requires replayable, deterministic setups.
  - Storage must be append-only and complete, with no dedupe or trimming, because every flag is paper traded.
  - The UI must not accept a final call until the verdict has been shown, and must timestamp both.
  - Verdict rows must record the model, a hash of the prompt and its context, and timings, because verdicts are scored forward only.
- **Style:** news.py works with no dependencies. That argues for keeping the core (candles, setups, paper engine) dependency-light and pushing pandas, DuckDB and Polars into analysis code.
- **Intraday bias:** the pyproject says "Personal intraday tool" and the glossary defines only "Intraday trade". The trader is open to swing or F&O, so horizon-neutral terms are needed before any swing or F&O setup is coded.

### Gaps
- **No term for the logged Haiku verdict.** Something like "Shadow verdict" is needed so it never enters the "verdict" scoreboard line or appears before the final call.
- **"A flag at one candle" names no candle size** (1, 5 or 15-minute, or daily) and no timestamp convention (candle start or close). Recommendation: each setup card states its candle size, and a flag is stamped with the **close time** of the candle that completes the condition.
- **"Paper trade at market prices" leaves the trade itself undefined:** which price (next candle open, or LTP at the final call), slippage, costs, quantity (sizing for 1R = ₹200), and product (MIS, CNC or NRML).
- **Scoreboard lines don't cover flags with no verdict** (timeout, error or model refusal) **or no final call** (timer expired). They also omit the "skipped" lines and the override subsets, which the ADR says are the only measurable effect of the trader's judgement.
- **Trial and money rules are missing:** the pass mark's metric and minimum sample are unspecified, and the **1R = ₹200** and **₹2,000 (10R) trial stop** rules are not in CONTEXT.md.
- **Screen and In-play timing:** how often the screen runs, and when the in-play test runs relative to the 09:00–09:08 pre-open and on what data, are unspecified.
- **Overlapping flags:** if the same setup flags the same stock on consecutive candles, it is not stated whether each flag becomes a separate paper position.
- **Book passages:** there is no store for them and no ID scheme for a verdict to cite.
- **Missing ADRs:** time zone and market clock, storage, data provider and login, and the verdict runner.

---

## 2. Which parts of /home/user/edge-scanner are worth adapting, and which US-specific assumptions must not be copied

### Takeaway
edge-scanner is MIT-licensed (© 2026 Tape to Edge), at v1.3.6 with its last commit on 2026-10-24, and has about 14k lines of Python plus a React dashboard. It is a US scanner that builds minute bars from several providers. The parts worth adapting are small and portable:
- the quote-to-bar builder's rules for cumulative volume and day-extreme correction
- `SymbolSeries`, a multi-timeframe candle ring with SMA-seeded EMAs
- `EvalCtx` once/edge latches with scoping and priming
- the split between triggers (edge) and conditions (level), and between static and dynamic conditions
- the session-roll guard that drops stale bars
- the procedure for seeding and priming on a late start
- the side-by-side feed-comparison approach, which fits tradingtool's parity checks

The JSON trigger catalog, profiles and gates, the dashboard and API, the AlertSink cooldown and trim, and the AlertStore file deletion should not be copied. Every New York time, SPY, premarket, round-lot, Alpaca and Schwab constant must be replaced.

### Cited Findings
**Project facts**
- MIT License, *"Copyright (c) 2026 Tape to Edge"*. NOTICE lists TradingView Lightweight Charts (Apache-2.0) and schwabdev (MIT) — [LICENSE](/home/user/edge-scanner/LICENSE), [NOTICE](/home/user/edge-scanner/NOTICE)
- Python 3.11+, with dependencies alpaca-py, pandas<4, numpy, pyarrow<27, python-dotenv, requests, lxml, fastapi, uvicorn, websockets<18, yfinance and schwabdev — [requirements.txt](/home/user/edge-scanner/requirements.txt)
- The last commit is 2026-10-24 (merge of PR #40), after the 1.3.6 version bump — [edge-scanner git log](/home/user/edge-scanner)

**File-by-file assessment**

`scanner/data/interface.py` (DataFeed ABC) — [interface.py](/home/user/edge-scanner/scanner/data/interface.py)
- `get_historical_daily` and `get_historical_bars` return a *"UTC-indexed DataFrame"* with columns open/high/low/close/volume/vwap/trade_count.
- `subscribe_minute_bars(symbols, callback)` *"invoke[s] callback(bar) on each bar close"*. There are also `get_snapshot` and a no-op `stop_stream`, and a `Timeframe` literal with Alpaca names (`"1Min"…"Day"`).
- `scanner/data/__init__.py` provides a lazy-import factory, `make_feed` — [data/__init__.py](/home/user/edge-scanner/scanner/data/__init__.py)

`scanner/data/quote_bars.py` (QuoteBarBuilder) — [quote_bars.py](/home/user/edge-scanner/scanner/data/quote_bars.py)
- Open and close are the first and last trade prices in the minute; high and low are the extremes *"SEEN"*; volume is the growth of the day's cumulative volume.
- Day-extreme correction: *"when the quote's own high or low OF THE DAY moves, that extreme is known precisely, so a new high or low of day is never missed however slowly the quotes arrive."*
- *"Bars … stamped at the start of their minute in UTC, emitted once after the minute ends, and only for minutes that traded. A minute with no trade produces no bar."*
- Volume reset versus correction (`_RESET_FRACTION = 0.2`, L66): *"Only a collapse to a small fraction of the previous total is a reset; a small decrease is a correction and adds nothing, and volume counts again only above the highest total seen."*
- `set_scale` exists because Schwab's own minute bars *"carry 60 to 85 percent"* of the cumulative volume.
- Odd lots are filtered with SEC round-lot tiers (`round_lot()`, L69–77).
- Each symbol has a per-symbol `grace` (L96). `flush()` is to be called *"about once a second"*.
- **The minute is taken from the injectable wall clock, `minute = int(self._clock() // 60)` (L182), not from exchange time.**
- Tests inject a fake `Clock` — [tests/test_quote_bars.py](/home/user/edge-scanner/tests/test_quote_bars.py)

`scanner/trigger_catalog.py` — [trigger_catalog.py](/home/user/edge-scanner/scanner/trigger_catalog.py)
- Constants (L33–39): `TIMEFRAMES = (1, 2, 3, 5, 15, 30, 60)`, `_RTH_OPEN = 9*60+30`, `_RTH_CLOSE = 16*60`, `_PRE_OPEN = 4*60`, and `_M1_RING = 800` (*"04:00-16:00 is 720 one-minute bars"*). `_CANDLE_RING = 128`, sized for a lookback of 50+1 and convergence of a 21-period EMA.
- `candle_key` (L434): *"Clock-aligned candle id anchored at 04:00 (premarket) or 09:30 (RTH)."* `et_minutes` (L442) converts to `America/New_York`.
- `_Ema` (L457): *"Incremental EMA seeded with an SMA of the first `period` values."*
- `SymbolSeries` (L478+):
  - `seed_daily` computes daily EMA 9/21/50 and a 52-week high/low over 252 days.
  - `seed_intraday` builds 5/15/30/60-minute candles from 5-minute history, regular session only (*"1-, 2- and 3-min candles are session-only"*).
  - `on_bar` clears the 1/2/3-minute rings and the latch memory on a day change. **A timeframe candle is marked complete only when a 1-minute bar with a new candle key arrives**: `if p is None or p["key"] != key: … self.completed[tf] = True`.
  - Helpers: `last_completed`, `atr`, `swing`, `session_open`, `pm_levels`.
- Shared arithmetic: `candle_rel_volume`, `rolling_rel_volume` (with a session filter), `consec_streak`.
- Edge versus level (L661–672): *"a TRIGGER has EDGE semantics: it fires once, on the transition, and latches its state in `series.mem`; a CONDITION has LEVEL semantics … no latching and no memory."*
- `level_value`: one resolver, so *"a trigger and a condition can never disagree about where a level is."*
- `EvalCtx` (L789–845):
  - `scope` gives each trigger configuration its own latch namespace: *"Two setups using one trigger with different settings … a shared latch let the first one silence the other."*
  - `priming`: *"latches record where the market is, but nothing fires. Used once at startup so a start after the open does not announce the morning's events."*
  - `once()`: *"True the first time `key` is seen today (per symbol and configuration)"*. `edge()`: *"True when `cond` turns True (was False or unknown before)"*. Plus `rearm()`.
- `_orb` (L1090–1113) finds today's opening candle through `session_date` and fires once per day.
- `evaluate()` (L1767) filters by session and fills in default parameters.

`scanner/custom_setups.py` (CustomEvaluator) — [custom_setups.py](/home/user/edge-scanner/scanner/custom_setups.py)
- Setups are defined in JSON (modes `or`/`and`/`atleast`, sessions pre/rth, `repeat_sec`, `and_window_min`, `size_hint`) and compiled into a plan (L376).
- `on_bar` (L494) evaluates every trigger in every session so latches follow the market: *"skipped there, an EMA cross made at 07:00 read as a new cross at the open (measured on 2026-09-22: 200 "EMA crossed above" alerts at 09:30 instead of 52)"*.
- Repeat timers use the **bar timestamp** (`now = ts.timestamp()`), not the wall clock.
- `prime()` (L609): *"Set every trigger's latches from where each symbol is now, firing nothing."* It defaults to `pd.Timestamp.now(tz="America/New_York")` and splits sessions at hard-coded `9*60+30` and `16*60`.

`scanner/conditions.py` — [conditions.py](/home/user/edge-scanner/scanner/conditions.py)
- STATIC conditions are fixed for the session (price, adv20, ATR%, float, sector) and resolved once into member sets. DYNAMIC conditions are resolved on each bar.
- *"`ConditionCtx` therefore deliberately has no `edge()` and no `once()`, so a condition physically cannot corrupt a trigger's latch."*
- Missing values: availability `"block"` (fail closed) or `"pass"` (fail open, *"Reserved for the yfinance fundamentals"*).
- The operator set is small: gte/lte/gt/lt.
- US-specific resolvers: `time_et` (L606), RRS vs SPY (L724+), `market_align` (L884), and fundamentals including short interest (L250–275).

`scanner/recent_activity.py` — [recent_activity.py](/home/user/edge-scanner/scanner/recent_activity.py)
- Answers *"why did I not get an alert on X?", which the feed alone cannot, because a blocked alert never reaches the feed"*.
- Records only events (sent, blocked, repeat, waiting, suppressed, quiet) over a 20-minute window, behind one lock.

`scanner/alert_sink.py` and `scanner/alert_store.py`
- AlertSink dedupes on (symbol, direction, trigger) within a 5-minute cooldown, keeps at most 5,000 alerts, and trims the lowest-scored — [alert_sink.py](/home/user/edge-scanner/scanner/alert_sink.py)
- AlertStore is an *"Append-only store: one JSONL file per trading day"*, but *"deletes files older than `keep_days`"* (default 5) and names each file with `date.today()` — [alert_store.py](/home/user/edge-scanner/scanner/alert_store.py)

`scripts/build_universe.py` — [build_universe.py](/home/user/edge-scanner/scripts/build_universe.py)
- Symbols come from Alpaca or Nasdaq lists. Filters: *"Price >= $15"*, 20-day average dollar volume *">= $150M/day … $7.50M on Alpaca's free IEX feed"* (`_IEX_VOLUME_SHARE = 0.05`), and ATR% ≥ 1%.
- `screen()` is a pure function that writes a diagnostics row giving *"the first filter it failed"* for each symbol.

`scanner/live_scanner.py` — [live_scanner.py](/home/user/edge-scanner/scanner/live_scanner.py)
- Lifecycle is `warmup()` → `connect()` → `reset_session()`. Warmup builds the SPY state plus a SymbolState and SymbolSeries per symbol.
- `_roll_session_if_new_day` drops a bar from an earlier New York date: *"the caller must drop it, because it would add yesterday's volume and prices to today's VWAP, volume and HOD/LOD."*
- `_on_bar` routes SPY bars to the market regime. For other symbols it updates state, advances the series once (shared), and then runs each evaluator inside its own try/except.
- `connect()` subscribes `["SPY"] + ranked symbols`.

`scripts/run_live.py` (late start) — [run_live.py L480–500, L620–640](/home/user/edge-scanner/scripts/run_live.py)
- *"Batch-fetch today's 1-min bars and replay them into each state so VWAP, high/low, and 5-min bars are all correct at startup"*.
- It then calls `custom_eval.prime()` so *"a start after the open does not alert on the morning's gap, RVOL cross or streak as if new."*

`scripts/compare_live_feeds.py` and `scripts/check_schwab_match.py`
- They compare per tier STATE (price, session volume, VWAP, RVOL, HOD/LOD, premarket levels) and ALERTS (on both, A only or B only, with time and price gaps).
- Acceptance rule: *"Ready when every overlap is >= 97%"* — [compare_live_feeds.py](/home/user/edge-scanner/scripts/compare_live_feeds.py), [check_schwab_match.py](/home/user/edge-scanner/scripts/check_schwab_match.py)

Other files
- [state.py](/home/user/edge-scanner/scanner/state.py): regular-session-anchored VWAP/HOD/LOD with constants at L45–46. Premarket bars only feed the premarket levels.
- [vwap.py](/home/user/edge-scanner/scanner/indicators/vwap.py): typical-price VWAP plus an incremental `vwap_update`.
- [market.py](/home/user/edge-scanner/scanner/market.py): regime from SPY's position against VWAP, ±0.1% band.
- [rrs.py](/home/user/edge-scanner/scanner/indicators/rrs.py): RRS against SPY, with an `XL*` sector-ETF map at L24–36.
- [gates.py L131](/home/user/edge-scanner/scanner/gates.py): market-alignment gate active after 10:00 New York time.
- [api_v2.py `session_now`](/home/user/edge-scanner/scanner/api_v2.py): 04:00/09:30/16:00/20:00, *"No holiday calendar"*.
- [stops.py](/home/user/edge-scanner/scanner/stops.py): stop at the low or high of the last `STOP_BARS` 1-minute bars.
- [timing.py](/home/user/edge-scanner/scanner/timing.py): *"20 s is the working ceiling"* of work per market minute.
- [cache/parquet.py](/home/user/edge-scanner/scanner/cache/parquet.py): one Parquet file per symbol.

**US-specific assumptions (from grepping scanner/ and scripts/)**
- `America/New_York` appears in trigger_catalog, state, live_scanner, conditions, gates, rvol, toplists, settings, api and api_v2.
- 09:30/16:00 regular hours and the 04:00 premarket appear in trigger_catalog, state, api_v2 and toplists.
- SPY is the benchmark and regime source (live_scanner L155/L406/L542, market.py, rrs.py), with `XL*` sector ETFs.
- SEC round lots (quote_bars), IEX volume share and dollar thresholds (build_universe).
- Alpaca and Schwab providers and auth scripts, and yfinance fundamentals.

**NSE facts checked in this session**
- pandas_market_calendars 5.5.0, calendar `NSE`/`XNSE`: tz `Asia/Calcutta`, open **09:15** since 2010-10-18, close **15:30** — [in-session query; pandas-market-calendars 5.5.0](https://pypi.org/project/pandas-market-calendars/5.5.0/)
- exchange_calendars 4.13.2, calendar `XBOM`: `Asia/Kolkata`, 09:15–15:30 — [in-session query; exchange-calendars 4.13.2](https://pypi.org/project/exchange-calendars/4.13.2/)
- **Kite index ticks carry no volume.** Index quote/full packets are 28/32 bytes: last_price, OHLC, change and, in full mode, exchange_timestamp only. They are marked `tradable: False` — [kiteconnect 5.2.2 `ticker.py` `_parse_binary`](https://pypi.org/project/kiteconnect/5.2.2/)

### Inferences
**US assumption → NSE replacement**

| edge-scanner assumption (where) | NSE / Kite replacement | Status |
|---|---|---|
| `America/New_York`, DST (about 10 modules) | `Asia/Kolkata`, no DST | verified (calendars) |
| Regular session 09:30–16:00 (`_RTH_OPEN/_RTH_CLOSE`, state.py L45–46, api_v2) | 09:15–15:30 | verified (two calendars) |
| 04:00–09:29 premarket with continuous trading, `pm_high/pm_low`, premarket toplists | Pre-open call auction 09:00–09:08 (per the brief). It produces one equilibrium price and volume, not candles. "Premarket levels" become previous-day H/L/C plus the pre-open price and gap | pre-open times not verified in-session |
| Postmarket bars (16:00–20:00) complete the last regular-session candle | No continuous post-market. The last candle (15:25 for 5-min, 15:15 for 15-min) needs an **explicit 15:30 finalization** | inference from code |
| 720 one-minute bars per day (`_M1_RING = 800`) | 375 one-minute bars per day; 75 five-minute; 25 fifteen-minute (09:15…15:15) | arithmetic on 09:15–15:30 |
| SPY benchmark and VWAP regime (market.py) | NIFTY 50 index. Index ticks have no volume, so index VWAP can't be built from ticks: use price vs open or EMA, or a traded proxy (NIFTY futures, an index ETF) for VWAP | no-volume fact verified |
| `XL*` sector ETFs (rrs.py) | NSE sectoral indices (per the brief, e.g. NIFTY BANK, NIFTY IT). RRS is price/ATR-based, so it still works without volume | list not verified |
| SEC round and odd lots (quote_bars L69–77) | Remove | inference |
| Schwab volume `set_scale` | Calibrate tick-built volume against Kite historical minute candles | inference |
| Alpaca/Schwab feeds, OAuth, IEX share | KiteTicker plus the Kite historical API, with a daily login | verified (pykiteconnect) |
| $15 price, $150M ADV, Nasdaq/Alpaca symbol lists | Rupee turnover thresholds; the Kite instruments dump (NSE, EQ) | inference |
| yfinance fundamentals and short interest | Drop, or use NSE sources (jugaad-data, nselib) | inference |
| 10:00 New York alignment gate, `time_et` | IST times defined on each setup card | inference |
| No holiday calendar (api_v2) | XNSE calendar | verified |

**Adapt** (copy with attribution, then rewrite for IST and the standard library)
1. **QuoteBarBuilder → KiteTickAggregator.**
   - Keep: cumulative-volume deltas with the reset/correction high-water mark, day-extreme correction (Kite full ticks carry day OHLC), grace plus flush, emit-once, no-trade-no-bar, the injectable clock and its tests.
   - Change: bucket by **exchange_timestamp** rather than the wall clock; stamp in IST; drop round lots and `set_scale`.
2. **SymbolSeries, `candle_key`, `_Ema` and helpers → CandleSeries anchored at 09:15 IST.**
   - Close a timeframe candle **at its boundary**, when the 1-minute candle ending at that boundary is processed. edge-scanner's rule (complete on the next candle's first bar) makes completion about a minute late, and on NSE the session's last candle would only complete at the next morning's first bar.
3. **EvalCtx once/edge/rearm, plus scope and priming → setup-latch helper.**
   - Keep the lesson that latches are evaluated in every session.
4. **The conditions.py splits → setup evaluation.**
   - Edge versus level: setup triggers versus filters.
   - STATIC versus DYNAMIC: the morning **In-play** test is STATIC and computed once per day; intraday filters are DYNAMIC.
   - Fail closed by default.
5. **live_scanner patterns.**
   - Drop stale earlier-date bars, and isolate each setup's exceptions.
   - On a late start, use the seed-then-catch-up idea, but **record pre-start flags as "backfill" flags instead of silently priming them away**. That keeps the "all flags" scoreboard complete.
6. **`build_universe.screen()` → Screen.** Keep the pure function and the "first filter failed" diagnostics; feed it rupee thresholds over Kite daily candles; output proposals for the trader to pick the Watchlist from.
7. **compare_live_feeds → daily parity report** (tick-built vs Kite historical candles; live flags vs replay flags).
8. **recent_activity → optional "near-miss / why not flagged" log** in a later phase. timing.py is unnecessary for a watchlist of 50 or fewer stocks.

**Do not copy**
- The JSON trigger catalog, composition UI, profiles, gates and size hints. Setups must be hand-coded from signed setup cards so each line of code traces to a book passage.
- AlertSink cooldown and trim, which would discard flags against "every flag is paper traded".
- AlertStore's 5-day deletion and its `date.today()` file names.
- stops.py's generic stop (setup cards define stops).
- FastAPI and the dashboard, the plugin system, and the Alpaca/Schwab/yfinance code.
- pandas Timestamps throughout the hot path. A preference: use `datetime` with `zoneinfo` in the core and pandas in analysis.

**Licence:** adapted code must carry edge-scanner's MIT copyright and permission notice, for example in a `NOTICE` file in tradingtool.

### Gaps
- NSE pre-open sub-phases (order entry 09:00–09:08, matching, buffer until 09:15) and the closing-session times could not be verified in-session: nseindia.com was not reachable and the search budget was exhausted.
- Unknown whether Kite's historical 09:15 minute candle includes the pre-open auction volume, and whether Kite streams ticks after 15:30 (closing session). Both affect parity, and both can be measured in Phase 2.
- The list of NSE sectoral indices was not verified.
- Not every edge-scanner file was reviewed (profiles.py, feed_hub.py, api*.py, the dashboard); they were judged out of scope.

---

## 3. Recommended architecture: live/replay parity, tick-to-candle, storage, paper trading, scoreboard, TUI, notifications, login, scheduling

### Takeaway
Build one core, `on_candle(series, candle_1m) → flags`, plus a candle-driven paper-trade engine. Feed it either from a live tick aggregator or from stored Kite historical minute candles:
- The live aggregator runs KiteTicker in full mode in its own thread and buckets ticks by exchange time.
- In both paths, derive 5- and 15-minute candles from 1-minute candles.
- Persist everything append-only in **SQLite (WAL)**, so a headless recorder and a Textual TUI can run as separate processes. Use DuckDB or Polars only offline.
- Get verdicts with `claude -p --output-format json --json-schema` (not `--bare`) under a one-candle deadline.
- Log in to Kite by hand each day through a local redirect catcher.
- Schedule from a market clock with the XNSE holiday calendar.

### Cited Findings
**Kite tick protocol (official pykiteconnect 5.2.2 source)** — [kiteconnect 5.2.2 on PyPI, `ticker.py`](https://pypi.org/project/kiteconnect/5.2.2/)
- Modes are `ltp`, `quote` and `full`. Packet lengths:

  | Packet | Bytes | Contents |
  |---|---|---|
  | LTP | 8 | last price |
  | Index quote / full | 28 / 32 | last_price, OHLC, change; full adds `exchange_timestamp`. No volume |
  | Equity quote | 44 | `last_price`, `last_traded_quantity`, `average_traded_price`, `volume_traded`, `total_buy_quantity`, `total_sell_quantity`, `ohlc`. **No timestamps** |
  | Equity full | 184 | quote fields plus `last_trade_time`, `oi`, `oi_day_high`, `oi_day_low`, `exchange_timestamp` and market depth |

- Equity prices are divided by 100 (paise to rupees).
- Timestamps are built with `datetime.fromtimestamp(epoch)`, a **naive datetime in the host machine's local timezone**.
- The parser computes `change` as last_price against `ohlc.close`.
- Reconnection:
  - *"Auto reconnection is enabled by default"*, with exponential backoff that *"starts from minimum interval which is 2 seconds"*.
  - `reconnect_max_delay` *"Defaults to 60s and minimum acceptable value is 5s"*; `reconnect_max_tries` *"Defaults to 50 attempts and maximum up to 300"*; `connect_timeout` *"Defaults to 30s"*.
  - *"reconnection mechanism cannot happen if event loop is terminated using `stop` method inside `on_close` callback."*
- `connect(threaded=False, …)`: with `threaded=True` the Twisted reactor runs in a `threading.Thread` with `installSignalHandlers=False`.

**Historical data and login** — [kiteconnect 5.2.2 `connect.py`](https://pypi.org/project/kiteconnect/5.2.2/); [npm kiteconnect 5.3.0 `types/connect.d.ts`](https://www.npmjs.com/package/kiteconnect)
- `historical_data(instrument_token, from_date, to_date, interval, continuous=False, oi=False)` calls route `/instruments/historical/{instrument_token}/{interval}`, with dates as `yyyy-mm-dd HH:MM:SS`.
- The JS typings list intervals `'minute' | 'day' | '3minute' | '5minute' | '10minute' | '15minute' | …`.
- The default API root is `https://api.kite.trade`, with a 7-second timeout.
- `login_url()` returned `https://kite.zerodha.com/connect/login?api_key=…&v=3` when run in-session.
- `generate_session` sends a checksum of SHA-256(`api_key + request_token + api_secret`). `invalidate_access_token` and `renew_access_token(refresh_token, api_secret)` also exist.
- Access token expiry: *"Unless this is invalidated using the API, or invalidated by a master-logout from the Kite Web trading terminal, it'll expire at `6 AM` on the next day (regulatory requirement)"*.

**Storage experiments (run in this session)**
- **DuckDB 2.0.0:** while one process held a read-write connection, a second process could not open the file even with `read_only=True`: *"IO Error: Could not set lock on file … Conflicting lock is h[eld]"* — [experiment; duckdb 2.0.0](https://pypi.org/project/duckdb/2.0.0/)
- **SQLite 3.53.1 in WAL mode:** a second process reading during an open, uncommitted write transaction was not blocked. It saw 0 rows before the commit and 1 after — [experiment; Python stdlib sqlite3](https://docs.python.org/3/library/sqlite3.html)
- edge-scanner itself persists alerts as daily JSONL and caches history as per-symbol Parquet — [alert_store.py](/home/user/edge-scanner/scanner/alert_store.py), [cache/parquet.py](/home/user/edge-scanner/scanner/cache/parquet.py)

**`claude -p` behaviour** — [Claude Code: Run programmatically](https://code.claude.com/docs/en/headless); [CLI reference](https://code.claude.com/docs/en/cli-reference), with flags confirmed from `claude --help` (Claude Code 2.1.316 installed here)
- Output and errors:
  - `--output-format` is `text`, `json` (*"structured JSON with result, session ID, and metadata"*) or `stream-json`.
  - With `--json-schema`, *"the structured output [is] in the `structured_output` field"*. *"If a run ends without valid structured output, for example because Claude declined the request, the response has no `structured_output` field."*
  - The JSON includes *"`total_cost_usd` and a per-model cost breakdown"*, described as *"client-side estimates"*.
  - Exit code 0 means success and non-zero means failure. A failure inside the run, *"such as missing authentication"*, is printed as the result on stdout. SIGTERM gives exit code 143.
- `--bare` and subscriptions:
  - **`--bare`**: *"bare mode doesn't use your subscription login"*; *"In bare mode, Claude Code never reads OAuth credentials or the system keychain"*.
  - *"`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."*
  - Without `--bare`, *"a `-p` session runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted."*
- Permissions: from v2.1.302, `-p` runs start in Manual mode when nothing sets a permission mode, and `dontAsk` denies every call that would prompt.
- Flags present in 2.1.316:
  - `--model`
  - `--fallback-model` (comma-separated list; the primary is retried each turn)
  - `--no-session-persistence`, `--append-system-prompt`
  - `--allowedTools` / `--disallowedTools`
  - `--input-format text|stream-json`
  - `--max-budget-usd` (only with `--print`)

**TUI, notifications, calendars, scheduling**
- Textual 8.2.8 (2026-06-30) has, as checked on the installed package:
  - `App.set_interval`, `App.set_timer`, `App.bell`
  - `App.notify(message, *, title, severity, timeout, markup)`
  - the `@work` decorator
  - `ProgressBar`, `DataTable`, `Log` and `RichLog` widgets
  - `App.run_test(headless=True, …)` with `Pilot.press` for UI tests

  [textual 8.2.8](https://pypi.org/project/textual/8.2.8/)
- desktop-notifier 6.2.0 (2025-08-08): *"`UNUserNotificationCenter` only allows signed executables to send desktop notifications … the installer from python.org provides a properly signed Python framework but **homebrew does not**"*. *"macOS requires a running CFRunLoop"* for callbacks — [desktop-notifier](https://pypi.org/project/desktop-notifier/)
- pandas_market_calendars 5.5.0 `NSE`: weekday holidays in Oct–Nov 2026 are **2026-10-02, 2026-10-20, 2026-11-10, 2026-11-24**. exchange_calendars 4.13.2 `XBOM` lists the same dates and reports `last_session` = 2026-12-31 — [pandas-market-calendars](https://pypi.org/project/pandas-market-calendars/5.5.0/), [exchange-calendars](https://pypi.org/project/exchange-calendars/4.13.2/)
- APScheduler 3.11.3 was released 2026-06-28 — [apscheduler](https://pypi.org/project/APScheduler/)

### Inferences
**A. Components and data flow**
```
KiteTicker (Twisted thread, MODE_FULL) ─ticks─► raw tick log (append-only, per day)
            └─call_soon_threadsafe─► TickAggregator (minute buckets by exchange time) ─1m candle─┐
Kite historical minute candles ─► candle store ─(replay / backfill / parity)────────1m candle─┤
                                                                                              ▼
                        Engine.on_candle: CandleSeries (1m → 5m/15m, 09:15-anchored) → setups (pure) → Flag rows
                                          PaperEngine.on_candle (entry at next candle open; stop/target/time exits)
Flag ─► NewsContext (news.py + Firecrawl) ─► VerdictRunner: claude -p Opus (primary) ∥ Haiku (shadow) ─► Verdict rows
TUI (Textual, separate process) reads flags/verdicts ─► Final call (take/skip/expired) rows
Scoreboard = SQL views (or DuckDB over a snapshot) joining trades × verdicts × final calls
```

**B. Parity rules (the one per-candle function)**
1. Only 1-minute candles cross into setups and the paper engine. Ticks never reach setups.
2. The core never reads `datetime.now()`. Time comes only from candle timestamps. The aggregator's clock is injected, as in edge-scanner's tests.
3. Derive 5- and 15-minute candles from 1-minute candles in **both** paths, anchored at 09:15. There are 25 fifteen-minute candles a day (09:15…15:15) and 75 five-minute candles.
4. A candle closes at its boundary: the 09:19 one-minute candle closes the 09:15 five-minute candle, and the flag is stamped 09:20:00. All open candles are force-closed at 15:30.
5. Every flag records the setup code version and setup-card version (git hash plus card ID).
6. Parity tests:
   - (a) golden replay days;
   - (b) a nightly comparison of tick-built candles against Kite historical candles, in the style of compare_live_feeds, accepting when for example ≥97% of minutes match within one tick;
   - (c) re-running the engine on the stored *live* candles must reproduce the live flags and trades exactly.
7. Late start: replay today's minute candles through the engine as `source=backfill`. These flags are paper traded, with no verdict or final call. Then go live. This differs from edge-scanner's silent `prime()`.

**C. Turning ticks into correct candles**
- **Mode and timestamps:**
  - Subscribe in **full** mode, the only one with `exchange_timestamp`/`last_trade_time`. For 50 or fewer instruments the 184-byte packets are no burden. Index tokens in full mode give exchange time but no volume.
  - Bucket by `exchange_timestamp` (falling back to `last_trade_time`), converted explicitly to IST. pykiteconnect returns naive host-local datetimes, so either patch parsing to `fromtimestamp(x, tz=IST)` or convert immediately. Never depend on the Mac's timezone.
- **Volume and price:**
  - Minute volume is the change in `volume_traded` across the minute. This assumes `volume_traded` is the day's cumulative volume, which is to be verified (see Gaps).
  - Take a baseline on the first tick. Ignore small downward revisions using a high-water mark, and treat a collapse to under 20% as a reset (edge-scanner's rule).
  - Highs and lows come from LTP samples, corrected whenever the day high or low in `ohlc` moves.
- **Missing and late data:**
  - A minute with no ticks produces no candle and is logged as a gap.
  - After a reconnect, backfill the gap from Kite historical minute candles and record the source.
  - A tick stamped inside an already-closed minute is dropped and counted (stale-bar guard).
- **Flushing:**
  - Close minute *m* when a tick for *m+1* arrives, or when the **market clock** passes *m*+60 s + grace (2–3 s).
  - The market clock is the latest exchange_timestamp seen across all instruments, which makes tick-log replays deterministic.
  - Use the wall clock only to detect a dead feed.
- **Pre-open:** ticks from 09:00–09:15 are not part of the 09:15 candle. Store the pre-open equilibrium price and volume as a separate "pre-open print", and set the volume baseline at 09:15. Whether Kite's own 09:15 candle includes auction volume must be checked in Phase 2 so the two conventions match.
- **Close:**
  - Ignore exchange times at or after 15:30 for intraday candles, and finalize at 15:30 + grace.
  - Swing setups take daily candles from Kite's daily history, because the official close may differ from the last trade (unverified).
- **Debugging:** keep the raw tick log (JSONL or Parquet per day) so the aggregator itself can be replayed.

**D. Storage**
- **System of record:** SQLite through the standard-library `sqlite3`, in WAL mode, with one writer task in the recorder and readers in the TUI and CLI. Why:
  - The experiment shows a live DuckDB writer would lock the TUI and scoreboard processes out.
  - SQLite needs no dependency.
  - Volume is small: 50 symbols × 375 minutes × about 250 days is about 4.7M one-minute rows a year.
- Tables, all append-only:

  | Table | Columns |
  |---|---|
  | `candles_1m` | symbol, ts_start_ist, OHLCV, source live/hist/backfill |
  | `flags` | ULID, setup_id, setup_version, symbol, candle size, flag_ts (candle close), direction, levels, context JSON, mode live/replay/backfill, run_id |
  | `verdicts` | flag_id, role primary/shadow, model requested/reported, prompt hash, started/finished, status ok/timeout/error/no_structured_output, take/skip, reasons, passage ref, raw JSON, cost estimate |
  | `final_calls` | flag_id, take/skip/expired, verdict_shown_at, called_at, note |
  | `paper_events` | trade_id, flag_id, open/exit, ts, price, qty, reason, costs |
  | `runs` | code version, config hash |

- Enforce append-only with `BEFORE UPDATE/DELETE … RAISE(ABORT)` triggers, and record corrections as new rows.
- Back up nightly with the sqlite backup API.
- DuckDB 2.0, Polars or pandas are for offline analysis of a copied database or Parquet exports only.

**E. Paper-trade engine** (identical in replay and live; only 1-minute candles)
- **Entry:** the open of the first 1-minute candle after the flag candle closes, plus N ticks of slippage. It is the same for every scoreboard line, so the lines differ only in which flags they include. The trader's real fills, if any, are logged separately.
- **Sizing:** qty = floor(₹200 / |entry − stop|), capped by capital × allowed leverage. Record the actual risk. When qty < 1, record an "unfillable" outcome rather than dropping the flag.
- **Exits:**
  - If stop and target are both touched in the same 1-minute candle, assume the stop was hit first (conservative).
  - If the price gaps through the stop, fill at the open.
  - Intraday setups have a time exit (e.g. 15:15), safely before the broker's MIS auto square-off; the cut-off time is unverified (see Gaps).
  - Swing setups hold overnight, apply gap rules at the next open, and respect a maximum holding period from the setup card.
- **Costs:** a versioned table per product (brokerage, STT, exchange transaction charges, SEBI fee, stamp duty, GST, DP charges) applied per leg. The rates come from Zerodha's charges page, which couldn't be fetched; see the sibling cost notes.
- **Result:** R = ((exit − entry) × qty × direction − costs) / ₹200.
- **Restarts:** events are appended, and open positions are rebuilt from events plus candles after a restart.

**F. Scoreboard**
- **Lines:** all flags; verdict take and skip; final call take, skip and expired; overrides (took against a skip, skipped against a take); shadow Haiku take; plus Opus–Haiku and Opus–trader agreement.
- **Metrics:**
  - n
  - win rate (R > 0 after costs)
  - average win and average loss in R
  - **expectancy** = mean R
  - **profit factor** = ΣR⁺ / |ΣR⁻|, shown as "∞" when there are no losses
  - **max drawdown in R**, on cumulative realized R ordered by exit time
  - total R, longest losing streak
  - a bootstrap confidence interval for expectancy
- **Status:** pass-mark status per setup, and a trial-stop tracker (cumulative-R drawdown against 10R) on the final-call line.

**G. Verdict runner**
- **The call:**
  - Spawn with `asyncio.create_subprocess_exec("claude","-p","--model","opus","--output-format","json","--json-schema",SCHEMA,"--no-session-persistence","--permission-mode","dontAsk", cwd=EMPTY_DIR)`.
  - Send on stdin: setup card, passage IDs and text, candle context, levels and headlines.
  - Parse `structured_output` and treat its absence as a status. Record latency, the cost estimate and the per-model breakdown.
- **Shadow verdict:** run the identical call with `--model haiku` in parallel. Hide it until after the final call.
- **Settings to avoid:**
  - **Avoid `--bare`.** It needs an API key, not the Pro subscription, and the docs say it will become the default for `-p`. Pin the CLI version and test the authentication path.
  - Run in an empty working directory so non-bare `-p` loads no project hooks, MCP servers or CLAUDE.md.
  - Avoid `--fallback-model` for the primary verdict, because it would silently break "Opus decides".
- **Deadline:** a fraction of one candle. 60–90 s is plausible for 5-minute setups; a 1-minute candle leaves too little time for a verdict plus a human decision, so prefer 5- or 15-minute candles for setups that need verdicts.

**H. TUI with a one-candle decision timer**
- **Layout:** Textual panes for the flag queue (`DataTable`), the flag detail (card summary, levels, verdict reasons, book passage, headlines), a `ProgressBar` counting down to the end of the next candle (driven by `set_interval(1)`), the scoreboard, and logs.
- **Keys and flow:**
  - T/S/N, disabled until the verdict is displayed.
  - When the timer expires, write `expired`.
  - Alert with `notify()`, `bell()` and a macOS notification.
- **Processes and tests:** keep the TUI separate from the headless recorder, so a UI crash never stops recording. Test with `run_test()` and `Pilot`.

**I. Notifications**
- desktop-notifier needs a signed Python (python.org builds are signed; Homebrew's are not; uv-managed builds are unknown).
- Fallbacks are `osascript … display notification` (not verified in-session) and Textual's `bell`/`notify`.

**J. Daily Kite login**
- `tradingtool login` opens `login_url()`.
- A standard-library HTTP catcher on 127.0.0.1, registered as the app's redirect URL, receives `request_token`.
- `generate_session` returns the access token, stored with its date in the macOS Keychain or a gitignored `.env`.
- The recorder refuses to start on a token issued before 06:00 IST today.
- Do not automate the password or TOTP entry.

**K. Scheduling**
- Drive an event table from the market clock in the recorder:

  | Time (IST) | Event |
  |---|---|
  | 08:45 | holiday check (XNSE) and token check |
  | 09:00–09:15 | pre-open capture |
  | 09:15 | candles start |
  | per setup card | setup windows |
  | 15:15 | intraday time exits |
  | 15:30 | finalize candles |
  | about 15:35 | fetch historical candles, reconcile and write the parity report |
  | end of day | scoreboard |

- Start it by hand or from a launchd LaunchAgent, and keep the Mac awake during the session. Neither detail was verified in-session.
- APScheduler is optional; plain asyncio tasks are enough.

### Gaps
- **Kite docs were unreachable**, so the following are unverified (to be checked at kite.trade/docs/connect/v3/websocket/, /historical/ and /user/; the host must be allowed in the session's network settings):
  - WebSocket instrument and connection limits (recalled from prior knowledge: about 3,000 instruments per connection and 3 connections per API key).
  - Tick cadence: snapshots rather than every trade.
  - Whether `volume_traded` is the day's cumulative volume.
  - Historical per-request day limits and rate limits (recalled: about 60 days per minute request, about 3 requests a second).
  - Whether today's minute candles are available intraday.
  - Candle timestamp convention (start time, +0530).
  - Kite Connect pricing and data/historical entitlements.
- **Zerodha facts:** the MIS auto square-off times and the charges schedule are unverified (zerodha.com was blocked).
- **NSE facts:** the official closing-price method and the current tick-size table are unverified.
- **Claude facts:** Claude Pro usage limits for `claude -p` with Opus and Haiku, and typical verdict latency, are not in the fetched page.
- **Platform facts:** whether uv-managed Python is code-signed (affects desktop-notifier), and whether Kite accepts `http://127.0.0.1` redirect URLs.
- **DuckDB:** its documentation was not fetched (duckdb.org blocked); the conclusion rests on the in-session experiment.

---

## 4. Python libraries and open-source NSE/Kite projects maintained in 2026: use vs small custom code

### Takeaway
Use the official **kiteconnect** library (5.2.2, released 15 Sep 2026) for login, history and the WebSocket. It installed and imported on Python 3.13.18 in-session despite pinning **autobahn 19.11.2**, a release whose files date from January 2020. Keep a fallback plan: a small custom client on `websockets` using the binary format documented in its `ticker.py`. Use **Textual/Rich** for the TUI, the standard-library **sqlite3** for storage, and **pandas_market_calendars** (or a checked holiday table) for NSE sessions. Keep the aggregator, candle series, setups, paper engine, scoreboard and verdict runner as small custom code adapted from edge-scanner. No backtesting framework keeps the single live/replay code path, and several carry restrictive licences.

### Cited Findings
PyPI metadata queried on 31 Oct 2026; links to each project page.

| Package | Latest (upload date) | Python / licence | Notes |
|---|---|---|---|
| [kiteconnect](https://pypi.org/project/kiteconnect/5.2.2/) | 5.2.2 (2026-09-15) | `requires_python` unset; classifiers stop at 3.7; MIT | Official Zerodha client, 62 releases since 2016. Pins `autobahn[twisted]==19.11.2`; also needs service_identity, requests, six, pyOpenSSL, python-dateutil |
| [autobahn](https://pypi.org/project/autobahn/19.11.2/) | pinned 19.11.2 (files uploaded 2020-01-09); latest 26.10.2 (2026-10-21) | py2.py3 wheel | — |
| [twisted](https://pypi.org/project/Twisted/) | 26.10.0 (2026-10-30) | ≥3.10, classifiers to 3.14 | — |
| [textual](https://pypi.org/project/textual/8.2.8/) | 8.2.8 (2026-06-30) | ≥3.9,<4; MIT | needs rich ≥14.2 |
| [rich](https://pypi.org/project/rich/) | 15.0.0 (2026-04-12) | MIT | — |
| [duckdb](https://pypi.org/project/duckdb/2.0.0/) | 2.0.0 (2026-10-21) | ≥3.11 | — |
| [polars](https://pypi.org/project/polars/) / [pandas](https://pypi.org/project/pandas/) / [pyarrow](https://pypi.org/project/pyarrow/) | 2.1.0 (2026-10-25) / 3.1.0 (2026-10-22) / 26.0.0 (2026-10-09) | ≥3.11 | analysis only |
| [pandas-market-calendars](https://pypi.org/project/pandas-market-calendars/5.5.0/) | 5.5.0 (2026-10-05) | ≥3.10; MIT | calendars BSE, XBOM, NSE, XNSE, XBSE |
| [exchange-calendars](https://pypi.org/project/exchange-calendars/4.13.2/) | 4.13.2 (2026-03-10) | ≥3.10 | XBOM only (no XNSE); `last_session` 2026-12-31 |
| [APScheduler](https://pypi.org/project/APScheduler/) | 3.11.3 (2026-06-28) | MIT | — |
| [desktop-notifier](https://pypi.org/project/desktop-notifier/) | 6.2.0 (2025-08-08) | ≥3.9 | macOS needs a signed Python |
| [pync](https://pypi.org/project/pync/) | 2.0.3 (2018-05-04) | MIT | stale |
| [backtesting](https://pypi.org/project/backtesting/) (backtesting.py) | 0.6.6 (2026-07-22) | **AGPL-3.0** | — |
| [vectorbt](https://pypi.org/project/vectorbt/) | 1.2.0 (2026-10-19) | 3.11–3.14; *"fair-code … Apache 2.0 with Commons Clause"* | needs numba, pandas ≥3.0.3 |
| [nautilus_trader](https://pypi.org/project/nautilus_trader/) | 1.231.0 (2026-08-02) | 3.12–3.14; **LGPL-3.0** | — |
| [backtrader](https://pypi.org/project/backtrader/) | 1.9.78.123 (2023-04-19) | GPLv3+, classifiers to 3.7 | stale |
| [jugaad-data](https://pypi.org/project/jugaad-data/) | 0.37.0 (2026-10-22) | licence field "YOLO" | *"download historical/live stock, index … data from NSE and RBI website"*, with built-in caching *"to play nice with NSE"* |
| [nsepython](https://pypi.org/project/nsepython/) / [nselib](https://pypi.org/project/nselib/) | 2.101 (2026-10-07) / 2.5.1 (2026-05-01) | "GNU" / unset | NSE website scrapers |
| [openalgo](https://pypi.org/project/openalgo/) | 2.0.5 (2026-09-11) | ≥3.12; MIT | *"Python library for OpenAlgo's trading APIs and WebSocket feeds"*; examples centre on `placeorder` |
| [websockets](https://pypi.org/project/websockets/) / [pydantic](https://pypi.org/project/pydantic/) / [feedparser](https://pypi.org/project/feedparser/) / [httpx](https://pypi.org/project/httpx/) / [pyotp](https://pypi.org/project/pyotp/) | 17.4 (2026-10-30) / 2.14.2 (2026-10-29) / 6.0.14 (2026-07-30) / 0.28.1 (**2024-12-06**) / 2.10.0 (2026-06-14) | — | — |

- **Python 3.13 compatibility experiment:** `uv pip install kiteconnect==5.2.2` into a Python 3.13.18 environment resolved autobahn 19.11.2, twisted 26.10.0, txaio 26.6.1, cryptography 50.0.2 and pyopenssl 26.4.0. `from kiteconnect import KiteConnect, KiteTicker` succeeded, a `KiteTicker` was constructed, and `login_url()` worked. A live WebSocket session was not tested (no credentials; the Kite hosts were unreachable) — [experiment; kiteconnect 5.2.2](https://pypi.org/project/kiteconnect/5.2.2/)
- Official clients also exist for Node (npm `kiteconnect` 5.3.0, MIT) and Go (`gokiteconnect` v4.4.3) — [npm kiteconnect](https://www.npmjs.com/package/kiteconnect), [pkg.go.dev gokiteconnect](https://pkg.go.dev/github.com/zerodha/gokiteconnect/v4)

### Inferences
**Use**
- kiteconnect, pinned in `uv.lock`, with a CI smoke test that imports `KiteTicker` on 3.13.
- textual (which brings rich).
- standard-library `sqlite3`, `zoneinfo` and `urllib` (news.py already uses urllib; `requests` arrives with kiteconnect anyway).
- pandas_market_calendars `XNSE`. It pulls in pandas, so an alternative is a small yearly holiday table cross-checked against XBOM and NSE's circular.

**Optional (dev or analysis group)**
- duckdb, polars or pandas for offline scoreboard research.
- pydantic, to generate and validate the verdict JSON schema.
- desktop-notifier, if the Python build is signed.

**Avoid**
- backtrader, pync and httpx-only stacks, all stale.
- OpenAlgo. It adds a self-hosted server and order-routing layer, against "the tool never places orders".
- External backtesters as the replay engine. They impose their own bar and strategy semantics, which breaks the "same per-candle function live and in replay" rule. vectorbt can serve throwaway exploration (its Commons Clause licence is fine for personal use); backtesting.py's AGPL matters only if the code is distributed.
- NSE scrapers as primary data. jugaad-data and nselib are reasonable secondary sources for bhavcopies, F&O lists and corporate actions.

**Fallback if Twisted becomes a problem** (for example, conflicts or a future Python): about 150 lines on `websockets` 17.x implementing the binary parse logic visible in `ticker.py`, which is short and fully documented in code.

**Write ourselves:** tick aggregator, candle series, setup latches, paper engine, costs, scoreboard, verdict runner, and the login catcher. Each is small, and edge-scanner already provides tested patterns for the first three.

### Gaps
- GitHub last-commit dates and issue trackers could not be read (API limited to the configured repos), so PyPI release dates stand in as the maintenance signal.
- No maintained, reputable Kite tick-to-candle library was identified, because searching was blocked. Custom code is recommended either way.
- Not verified whether nautilus_trader or any other framework has an Indian-broker or Kite adapter.

---

## 5. Phased build order that produces evidence as early as possible

### Takeaway
Keep the trader's order, but move a minimal **paper-trade engine plus an "all flags" scoreboard line into the replay milestone**. That makes raw setup expectancy in R, after costs and over months of history, the first evidence, before any live plumbing. Then come:
1. live flags, recorded only and checked for parity;
2. live paper trading, which starts the forward trial;
3. verdicts and final calls;
4. the full scoreboard with pass mark and trial stop;
5. screen, in-play test and more setups.

### Cited Findings
- Replay measures setups alone, and verdicts can only be scored forward on paper — [ADR 0001](/home/user/tradingtool/docs/adr/0001-setups-are-code-model-judges-trader-decides.md)
- Setup cards are signed off before coding, and the pass mark is fixed before a trial — [CONTEXT.md](/home/user/tradingtool/CONTEXT.md)
- Existing tests are pytest with inline, deterministic fixtures — [test_news.py](/home/user/tradingtool/tests/test_news.py). edge-scanner injects a fake clock in [test_quote_bars.py](/home/user/edge-scanner/tests/test_quote_bars.py), and its tests include test_triggers, test_custom_setups, test_live_scanner, test_alert_sink and test_recent_activity — [edge-scanner tests/](/home/user/edge-scanner/tests)
- Textual's `run_test()` and `Pilot.press` exist for UI tests — [textual 8.2.8](https://pypi.org/project/textual/8.2.8/)
- `claude -p` exit codes and `structured_output` presence semantics are as documented — [Claude Code headless](https://code.claude.com/docs/en/headless)
- Tokens expire at 6 AM the next day — [npm kiteconnect typings](https://www.npmjs.com/package/kiteconnect)
- edge-scanner's acceptance style is *"Ready when every overlap is >= 97%"* — [check_schwab_match.py](/home/user/edge-scanner/scripts/check_schwab_match.py)

### Inferences
**M0 — Decisions and skeleton**
- *Work:*
  - Glossary additions: Shadow verdict, Flag time, Candle size, Entry price, Backfill flag, Expired call, 1R and Trial stop.
  - ADRs: 0002 market clock and candles; 0003 append-only SQLite; 0004 Kite and daily login; 0005 verdict runner.
  - Modules: `clock`, `calendar`, `kite_auth`, `history`, `candles`, `aggregator`, `setups/`, `engine`, `paper`, `costs`, `store`, `verdicts`, `news`, `tui/`, `scoreboard`.
- *DoD:* `uv sync` with pinned dependencies, `uv run pytest` green, and a smoke import of `KiteTicker` on 3.13.

**M1 — Setup card #1 → historical data → replay → paper engine → "all flags" line (first evidence)**
- *Work:*
  - Login CLI and instruments dump.
  - A chunked, cached minute-history fetcher and the candle store.
  - The engine and setup #1, coded from its signed card.
  - The paper engine with costs, and a replay CLI with a report.
- *DoD:* a per-flag trade table with R after costs across the watchlist, over as many months as Kite minute history allows, plus n, win rate, expectancy, profit factor and max drawdown. Then a go/no-go on starting a trial, and the pass mark written down before the trial starts.
- *Tests:*
  - 1→5/15-minute derivation: 09:15 anchor, 25 fifteen-minute candles per day, final candle closes at 15:30.
  - Setup fires and non-fires, once/edge latches, priming.
  - **No look-ahead:** flags on truncated history equal the prefix of flags on full history.
  - Paper engine: next-open entry, stop first on ambiguity, gap through stop, 15:15 time exit, sizing and leverage cap, cost legs, R arithmetic.
  - 2026 holiday sessions.
  - A golden replay-day snapshot.

**M2 — Live flags (record only)**
- *Work:* ticker in a thread in full mode, raw tick log, aggregator, the same engine, flag rows, a minimal Textual list plus notification, reconnect handling, late-start backfill.
- *DoD:* 3–5 full sessions recorded, with a nightly parity report:
  - ≥97% of 1-minute candles match Kite historical within one tick on O/H/L/C, with volume within a set tolerance;
  - re-running the engine on stored live candles reproduces live flags 100%;
  - differences between live flags and flags replayed on Kite historical candles are listed and explained.
- *Tests:*
  - Aggregator: cumulative-volume baseline, reset and correction; exchange-time bucketing; naive-to-IST conversion; late-tick drop; flush by market clock plus grace; no trade means no candle; pre-open exclusion; 15:30 finalization; reconnect gap and backfill.
  - Tick-log replay determinism.

**M3 — Live paper trading (starts the forward trial)**
- *Work:* every live or backfill flag becomes a paper trade through the M1 engine; event log; restart recovery; daily "all flags" scoreboard; trial clock.
- *DoD:* N sessions where flags = trades + unfillables (count reconciliation), and a mid-session restart test passes.
- *Tests:* event-sourced rebuild, idempotent writes, and append-only triggers rejecting UPDATE and DELETE.
- *Note:* start M3 as early as possible. Forward sample size is the longest lead time; at 2 flags a day, 100 trades take about 50 sessions.

**M4 — Verdicts and final calls**
- *Work:*
  - News context (news.py plus Firecrawl, capped and with timeouts).
  - Prompt builder (card, passages, levels, headlines).
  - Runner: Opus primary plus Haiku shadow, with JSON schema.
  - TUI decision timer and final-call capture.
- *DoD:* every flag has exactly one primary verdict row (ok, timeout, error or no structured output), one shadow row and one final-call row (take, skip or expired). The verdict-latency distribution is reported, and the UI refuses a final call before the verdict is shown.
- *Tests:*
  - A fake `claude` executable on PATH that returns canned JSON, omits `structured_output`, exits non-zero, or hangs (timeout).
  - Schema validation.
  - Pilot tests: keys disabled until the verdict arrives; expiry writes `expired`; T writes take.

**M5 — Full scoreboard**
- *Work:*
  - Lines and per-setup metrics, a bootstrap confidence interval, pass-mark status and the trial stop.
  - A Rich-table CLI and a TUI tab.
  - Parquet export for DuckDB.
- *DoD:* the scoreboard can be rebuilt from the database alone and matches hand-computed fixtures.
- *Tests:*
  - Expectancy, win rate, profit factor with zero losses, max-drawdown ordering by exit time, a seeded bootstrap.
  - Line membership: a missing verdict excludes a flag from verdict lines but keeps it in "all flags".

**M6 — Screen, In play, more setups and other horizons**
- *Work:*
  - The screen over daily candles with rupee thresholds and "first failed filter" diagnostics.
  - In-play morning tests.
  - Further setup cards.
  - Swing (CNC, overnight gaps, multi-day holds), then F&O (lot sizes and expiries from the instruments dump), only once their costs are modelled.
  - The near-miss log.

### Gaps
- How far back Kite minute history goes, which sets how deep M1 replays can be, is unverified.
- Flag frequency per setup is unknown until M1, so the time to reach a meaningful sample is unknown.
- Claude Pro usage limits may cap verdicts per day (2 calls per flag); these were not verified.
- Kite pricing and data entitlements, the Zerodha square-off times and charges, and the NSE pre-open and closing-session details all need verifying before M1 and M3 numbers are trusted. The hosts were blocked and the search budget was exhausted in this session.
