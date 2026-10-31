# Validation methodology: separating real edge from luck for a small NSE retail trader (1R = ₹200, trial stop ₹2,000 = 10R)

**How these notes were sourced (read first):**

- **No web pages were read for this topic.** The shared web-search budget was already used up when this task started. Direct fetches of the primary-source PDFs (davidhbailey.com, ams.org) also failed, because those hosts are outside the session's network allowlist.
- **"Sim" citations** point to my own seeded Monte Carlo simulations and closed-form calculations (Python 3.13, standard library only). Each drawdown scenario uses 40,000 paths; the sequential-test scenarios use 20,000–30,000. The scripts and raw outputs are saved beside this file in `validation_sims/`: `validation_sims.py` → `sims_output.txt` (sections §1–§11), `validation_sims2.py` → `sims2_output.txt` (sections §A–§E), and `verification_checks.py` → `verification_checks_output.txt` (MinBTL check, the K_max heuristic, SPRT lines in R and ₹, infinite-horizon ruin). They are reproducible bit-for-bit. Monte Carlo standard error is ≤ 0.25 percentage points (pp) for 40k paths and ≤ 0.35 pp for 20k paths.
- **References marked †** come from background knowledge and are cited by stable DOI or SSRN links. They were **not re-read in this session.** Where possible I checked them by computation. For example, the Bailey et al. MinBTL formula gives exactly 5.00 years for 45 trials, which matches their "45 configurations / 5 years" example.
- **NSE and Zerodha microstructure facts and charges could not be verified.** They appear under Gaps, marked "verify".
- **Notation:** E = expectancy (mean net R per trade); σ or SD = standard deviation of R per trade; n or T = number of trades; K = number of setups or parameter variants tried; "payoff A/B/C" = binary outcomes of +2R / +1.2R / +3R wins against −1R losses.
- **The user's two examples correspond to specific edges.** "40% winners at 2R" has E = +0.20R and SD 1.47R. "50% winners at 1.2R" has E = +0.10R and SD 1.10R. If those payoffs are before costs, 0.1R of costs makes them +0.10R and 0.00R net.

---

## Q1. How many trades are needed for 95% confidence that mean R > 0 (with 80% power) for edges of +0.05R, +0.1R, +0.2R and +0.3R, and what does a sample of 100 trades actually establish?

### Takeaway
With per-trade SD of 1.0–1.5R, a one-sided 95% test with 80% power needs roughly:

- **+0.3R edge:** 70–160 trades
- **+0.2R edge:** 155–350 trades
- **+0.1R edge:** 620–1,400 trades
- **+0.05R edge:** 2,500–5,600 trades

A 100-trade sample has a standard error of 0.10–0.15R. It only "proves" an edge if the observed mean is at least about +0.16 to +0.25R. Its power is just 16–26% for a true +0.1R edge and 38–64% for +0.2R. So 100 trades work as an execution, cost and kill check, not as proof of an edge.

### Cited Findings
- **Sample-size formula used:** n = ((z₁₋α + z₁₋β)·σ/δ)², plus a small-sample t-correction of z₁₋α²/2 (Guenther). Here δ is the true edge in R, z₀.₉₅ = 1.645 and z₀.₈₀ = 0.842. In short: **n ≈ 6.18·(σ/δ)² + 1.4** — [Sim §1](validation_sims/sims_output.txt)

- **Trades needed, one-sided α = 0.05, power 80%** — [Sim §1](validation_sims/sims_output.txt)

  | SD of R | +0.05R | +0.10R | +0.20R | +0.30R |
  |---|---|---|---|---|
  | 1.00R | 2,475 | 620 | 156 | 71 |
  | 1.25R | 3,866 | 968 | 243 | 109 |
  | 1.50R | 5,566 | 1,393 | 350 | 156 |

- **Stricter versions of the same test (SD 1.25R)** — [Sim §1](validation_sims/sims_output.txt)

  | Test | +0.05R | +0.10R | +0.20R | +0.30R |
  |---|---|---|---|---|
  | Two-sided α = 0.05, power 80% | 4,908 | 1,229 | 309 | 139 |
  | One-sided, power 90% | 5,354 | 1,340 | 336 | 151 |
  | Bonferroni α = 0.005 (10 variants tried) | 7,303 | 1,829 | 460 | 207 |
  | Harvey-Liu-Zhu t ≥ 3.0 hurdle | 9,229 | 2,311 | 581 | 261 |

- **Binary-payoff SDs.** SD = (W+1)·√(p(1−p)). A 1R target gives SD ≈ 0.95–1.0R. A 1.2R target gives ≈ 1.08–1.10R. A 2R target gives ≈ 1.41–1.49R. A 3R target gives ≈ 1.73–1.87R. Higher targets mean higher variance, which means more trades are needed for the same edge — [Sim §1](validation_sims/sims_output.txt)

- **What n = 100 shows (normal approximation)** — [Sim §2](validation_sims/sims_output.txt)

  | SD | SE of mean R | 95% CI half-width | Observed mean needed for one-sided p < 0.05 | Minimum detectable edge (80% power) | Power at +0.1 / +0.2 / +0.3R | P(true edge shows a losing 100-trade sample) at +0.1 / +0.2R |
  |---|---|---|---|---|---|---|
  | 1.00R | 0.100R | ±0.196R | +0.164R | 0.249R | 26% / 64% / 91% | 16% / 2% |
  | 1.25R | 0.125R | ±0.245R | +0.206R | 0.311R | 20% / 48% / 77% | 21% / 5% |
  | 1.50R | 0.150R | ±0.294R | +0.247R | 0.373R | 16% / 38% / 64% | 25% / 9% |

- **Larger samples (SD 1.25R)** — [Sim §2](validation_sims/sims_output.txt)
  - n = 200: SE 0.088R; minimum detectable edge 0.22R; power 30% at +0.1R and 73% at +0.2R.
  - n = 300: SE 0.072R; minimum detectable edge 0.18R; power 40% at +0.1R and 87% at +0.2R.
  - n = 500: minimum detectable edge 0.14R; power 56% at +0.1R and 97% at +0.2R.

- **Probabilistic Sharpe Ratio (PSR) and Minimum Track Record Length (MinTRL).** Bailey & López de Prado define the per-trade PSR as Φ((SR̂ − SR*)·√(T−1) / √(1 − γ₃·SR̂ + ((γ₄−1)/4)·SR̂²)), where γ₃ is skewness and γ₄ is (non-excess) kurtosis. They define MinTRL = 1 + (1 − γ₃·SR̂ + ((γ₄−1)/4)·SR̂²)·(z_α/(SR̂ − SR*))² — [Bailey & López de Prado 2012, "The Sharpe Ratio Efficient Frontier"†](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1821643)
  - For a 2R-target payoff, MinTRL at 95% is 545 / 244 / 139 / 64 trades for an observed +0.10 / +0.15 / +0.20 / +0.30R — [Sim §6](validation_sims/sims_output.txt)
  - MinTRL is the length at which an *observed* edge becomes significant. It gives no power guarantee.

- **Standard error of a Sharpe ratio.** Under IID normal returns the SE is about √((1 + SR²/2)/T). This underlies the per-trade calculations above — [Lo 2002†](https://doi.org/10.2469/faj.v58.n4.2453)

- **Flags that cluster on the same day shrink the effective sample.** The design effect is 1 + (m−1)·ρ, where m = flags per day and ρ = their correlation within a day — [Sim2 §E](validation_sims/sims2_output.txt)
  - 3 flags/day with ρ = 0.2 makes 100 trades worth about 71 independent trades.
  - 5 flags/day with ρ = 0.3 makes them worth about 45.

### Inferences
- **What 100 trades can establish:**
  - **A clearly bad setup.** If the observed mean is −0.25R or worse with SD 1.25R, the one-sided 95% upper bound is below 0, so the setup is very likely negative after costs.
  - **Whether forward fills, costs and slippage match the replay assumptions.**
  - **Only very large edges (≥ +0.3R).** These are detected with 64–91% power.
- **What 100 trades cannot establish:**
  - They cannot separate +0.1R from 0R, or +0.1R from +0.2R.
  - A genuine +0.1R edge loses money over 100 trades about 1 time in 5.
  - A "profitable after 100 trades" result is roughly as likely for a zero-net-edge setup (about 48–50%) as a coin flip (see Q2).
- **The "≥ 3 months" condition is not statistical.** About 62 NSE sessions sample roughly one market regime. Regime diversity should come mainly from the multi-year Stage-1 replay.
- **Van Tharp's SQN equals the one-sample t-statistic.** SQN (√N × mean R / SD R) is algebraically the t-statistic for mean R > 0 when N is the actual trade count. So "SQN ≥ 1.65 over all trades" is the same as one-sided p < 0.05. (This is background knowledge. Tharp is often described as capping N at 100, in which case SQN is no longer a t-statistic.)
- **Use net R and compute SE by day.** All tests should use **net R** after the replay's fee and slippage model. When several flags can fire on the same day, the app should compute SE on day-clustered data:
  - x̄ = ΣR / Σm_d (total R over total trades)
  - SE_cluster = √( D/(D−1) · Σ_d (R_d − x̄·m_d)² ) / Σm_d
  - Here R_d = total R on day d, m_d = trades on day d, and D = number of days.

### Gaps
- **Real R distributions are not binary.** They include time exits, the EOD square-off at intermediate R, partial exits, and slippage or gaps beyond −1R. The SD (and the skew and kurtosis used by PSR, DSR and MinTRL) must be estimated from the setup's own replay trade list. Required n scales with SD².
- **The within-day correlation ρ of NSE flags is unknown.** It must be estimated from replay data, for example by comparing day-clustered and naive SEs.

---

## Q2. Risk of ruin and drawdown: probability that a real edge trips a 10R drawdown stop in 100/200 trades, and probability that a zero-edge setup "passes" (profitable after costs)

### Takeaway
How the ₹2,000 (10R) stop is defined dominates the outcome.

- **Peak-to-trough definition:**
  - A genuine +0.2R edge trips it in **52%** of 100-trade runs and **80%** of 200-trade runs with a 2R target (SD ≈ 1.47R).
  - It trips it in **16% / 32%** with a 1.2R target.
- **Loss-from-starting-balance definition:** the same edges trip it only **12–14%** (2R target) and **3%** (1.2R target) of the time.
- **Zero-gross-edge setups still look profitable after 100 trades fairly often:**
  - 32–36% of the time at 0.05R costs
  - 16–28% at 0.10R
  - 4–11% at 0.20R
  - Zero-*net*-edge setups (gross edge just covering costs) look profitable about 45–50% of the time.

The current pass mark therefore throws out many real high-payoff edges. It also passes noise with high probability once several setups or scoreboard lines are tracked: 45–79% for 10 zero-edge setups.

### Cited Findings
- **P(10R drawdown) within 100 / 200 trades, with costs folded into the net payoff** — [Sim §3](validation_sims/sims_output.txt)

  | Payoff (SD) | True net E | P(peak-to-trough DD ≥ 10R), 100 / 200 trades | P(down 10R from start), 100 / 200 trades | Median / 90th-pct max DD in 100 trades | Median / 90th-pct longest losing streak in 100 trades |
  |---|---|---|---|---|---|
  | A: +2R (1.41–1.49) | 0 | 85.0% / 98.4% | 48.2% / 61.7% | 15R / 26R | 9 / 13 |
  | A | +0.10R | 70.4% / 92.5% | 26.5% / 32.4% | 12R / 20R | 8 / 12 |
  | A (= 40% winners @ 2R) | +0.20R | **51.9% / 79.7%** | **12.4% / 13.8%** | 10R / 16R | 7 / 11 |
  | A | +0.30R | 34.5% / 59.5% | 5.1% / 5.3% | 8R / 13R | 7 / 10 |
  | B: +1.2R (≈1.10) | 0 | 64.2% / 89.8% | 34.4% / 50.4% | 11.6R / 20.4R | 6 / 9 |
  | B (= 50% winners @ 1.2R) | +0.10R | **36.4% / 63.8%** | **12.1% / 15.7%** | 8.6R / 14.8R | 6 / 8 |
  | B | +0.20R | 15.8% / 31.5% | 2.9% / 3.2% | 6.8R / 11.0R | 5 / 7 |
  | B | +0.30R | 5.1% / 11.1% | 0.6% / 0.6% | 5.6R / 8.6R | 4 / 7 |
  | C: +3R (1.73–1.87) | 0 | 94.3% / 99.8% | 56.0% / 68.2% | 18R / 31R | 12 / 18 |
  | C | +0.10R | 88.4% / 98.8% | 38.2% / 45.2% | 15R / 26R | 11 / 16 |
  | C | +0.20R | 78.8% / 96.2% | 24.2% / 26.8% | 13R / 22R | 10 / 15 |

- **Drawdowns keep growing with the horizon.** Over 500 trades, P(peak DD ≥ 10R) is 98.3% for A at +0.2R, 64% for B at +0.2R and 26.6% for B at +0.3R. Any fixed peak-to-trough stop is eventually hit even by real edges — [Sim §3](validation_sims/sims_output.txt)

- **Same ₹2,000 limit at smaller risk per trade.** ₹150 risk makes ₹2,000 = 13.3R; ₹100 risk makes it 20R — [Sim2 §B](validation_sims/sims2_output.txt)
  - A at +0.2R: P(peak DD ≥ 13.3R) = 20.6% / 40.7% (100 / 200 trades); P(peak DD ≥ 20R) = 4.2% / 11.2%.
  - A at +0.1R: P(peak DD ≥ 20R) = 11.9% / 30.1%.
  - B at +0.2R: P(peak DD ≥ 13.3R) = 4.3% / 10.0%; P(peak DD ≥ 20R) = 0.3% / 1.0%.
  - B at +0.1R: P(peak DD ≥ 20R) = 2.2% / 7.7%.
  - B at zero edge: P(peak DD ≥ 20R) = 11.3% / 35.0%.

- **Closed form for "down D from the start within n trades".** This uses Brownian motion with drift μ (E per trade) and volatility σ — [Sim §11](validation_sims/sims_output.txt)
  - **P ≈ Φ((−D − μn)/(σ√n)) + exp(−2μD/σ²)·Φ((−D + μn)/(σ√n))**
  - For μ = 0 this becomes 2·Φ(−D/(σ√n)). Over an infinite horizon (μ > 0) it becomes exp(−2μD/σ²).
  - It matched the simulation within about 1–2 pp and errs slightly on the conservative side (overstates risk). Examples: A at +0.2R, n = 100: 0.139 vs simulated 0.124. B at +0.1R, n = 200: 0.169 vs 0.157. A at 0R, n = 100: 0.480 vs 0.482. C at +0.1R, n = 100: 0.399 vs 0.382.
  - Infinite-horizon probability of ever being down 10R from the start: 0.157 for +0.2R at σ 1.47; 0.191 for +0.1R at σ 1.1; 0.037 for +0.2R at σ 1.1 — [verification run](validation_sims/verification_checks_output.txt)
  - The 0.5826σ discrete-monitoring correction worsened the fit for −1R-lattice losses — [Broadie, Glasserman & Kou 1997†](https://doi.org/10.1111/1467-9965.00035)

- **Peak-to-trough drawdown has no simple closed form.** Its distribution for Brownian motion with drift is derived by [Magdon-Ismail et al. 2004†](https://doi.org/10.1239/jap/1077134674); the app should simulate or bootstrap it instead.

- **Zero gross edge plus costs** (every trade shifted down by c): chance of ending "profitable after costs" over 100 trades — [Sim §4](validation_sims/sims_output.txt)

  | Cost per trade | A: P(final > 0) | B: P(final > 0) | C: P(final > 0) | A / B / C: P(pass current rule = final > 0 and peak DD never ≥ 10R) |
  |---|---|---|---|---|
  | 0.00R (zero net edge) | 48.3% | 49.3% | 44.7% | 14.2% / 32.0% / 5.5% |
  | 0.05R | 32.0% | 33.7% | 36.4% | 10.0% / 19.8% / 4.3% |
  | 0.10R | 24.8% | 15.6% | 27.9% | 5.7% / 10.3% / 2.4% |
  | 0.15R | 13.8% | 7.7% | 20.8% | 2.9% / 4.2% / 1.3% |
  | 0.20R | 6.6% | 3.6% | 10.6% | 1.3% / 1.8% / 0.6% |
  | 0.25R | 4.5% | 1.4% | 6.9% | 0.6% / 0.7% / 0.3% |

  The normal approximation Φ(−c·√n/σ) is within about 1–4 pp of these figures.

- **How often the current rule passes (100 trades, peak-based 10R stop)** — [Sim §3](validation_sims/sims_output.txt)
  - Payoff A: 29% at +0.1R, 48% at +0.2R, 66% at +0.3R.
  - Payoff B: 62% at +0.1R, 84% at +0.2R, 95% at +0.3R.
  - Payoff C: 12% at +0.1R, 21% at +0.2R, 33% at +0.3R.
  - With a start-based stop the pass rates for real edges rise (A 66% / 84% / 94%; B 79% / 95% / 99%). But zero-net-edge setups then pass 41% (A), 47% (B) and 35% (C) of the time.

- **P(at least one of K independent zero-edge setups passes the current rule)** — [Sim §5](validation_sims/sims_output.txt)

  | K setups | A, zero net edge | A, zero gross edge + 0.1R cost | B, zero gross edge + 0.1R cost |
  |---|---|---|---|
  | 3 | 37% | 16% | 28% |
  | 5 | 54% | 26% | 42% |
  | 10 | 79% | 45% | 67% |
  | 20 | 96% | 69% | 89% |

### Inferences
- **Use a loss-from-start stop, not peak-to-trough.** Define the ₹2,000 limit as a loss from the stage's starting balance (equity falls to ₹18,000). Alternatively, keep a peak-to-trough limit but cut risk to ₹100/trade so the limit is 20R. Otherwise a genuine 2R-target edge is more likely than not to be "stopped out" within 100 trades.
- **During paper trading the stop protects no capital.** The drawdown rule there is purely a decision rule. It should be replaced by a statistically calibrated FAIL boundary (the SPRT in Q6), which already behaves like a "−₹1,900 to −₹2,400 floor rising ₹20 per trade". Keep the ₹2,000 rule for real money.
- **The current pass mark ("≥ 100 trades, profitable after costs, within ₹2,000") is not a test.**
  - Its false-positive rate depends mostly on payoff shape and costs (single setup: 0.3–32%) rather than a chosen α.
  - Its power against real edges swings from 12% to 95% depending on payoff shape.
  - Tracking several setups or lines inflates false passes towards 50–90%.
- **Expectations the app should show before a trial starts.** For example: "For a +0.2R, 2R-target setup, the median worst drawdown over 100 trades is 10R (90th percentile 16R), and the median longest losing streak is 7 (90th percentile 11)."
- **Which setup shapes fit ₹20,000 capital.** Setups with high win rates and lower payoffs (SD ≈ 1.1R) are much more compatible with a ₹2,000 budget than 2R–3R-target setups (SD 1.45–1.85R), at the same expectancy.

### Gaps
- **Costs in R depend on stop width and the current rate card** (see Q4).
- **Fat left tails are not modelled.** Gaps through stops, circuit-locked exits and freak prints make the drawdown probabilities above optimistic for setups prone to them. The app should bootstrap the actual replay trade list (10,000 resampled sequences of n trades) to estimate P(DD ≥ 10R) for each setup.

---

## Q3. Replay protocol best practice and multiple testing (IS/OOS, walk-forward, freezing, pre-registration, Deflated Sharpe Ratio, Probability of Backtest Overfitting, White's Reality Check, Hansen's SPA, Harvey-Liu-Zhu haircuts), and how many setups or parameter sets can be tried

### Takeaway
Treat replay as a confirmatory test:

1. Pre-register and freeze the rule.
2. Count every variant ever tried (K).
3. Test once on a chronologically held-out period.
4. Deflate for selection.

Luck from trying many variants is large at this sample size. With SD 1.25R and 300 trades per variant, the best of 10 zero-edge variants is *expected* to show +0.11R, and the best of 20 +0.135R. With 1,000 trades, about 107 variants produce an expected +0.10R by luck alone.

Practical hurdles:

- **Bonferroni/Holm t-thresholds:** K = 10 → t ≥ 2.58; K = 20 → 2.81; K = 50 → 3.09. Harvey-Liu-Zhu use t ≥ 3.0.
- **DSR ≥ 0.95.**
- **K ≤ exp(T·δ²/(8σ²))** keeps expected luck below half the target edge δ.

### Cited Findings
- **White's Reality Check.** A bootstrap p-value for whether the *best* of a universe of models beats a benchmark, accounting for the full specification search — [White 2000†](https://doi.org/10.1111/1468-0262.00152)
- **Sullivan, Timmermann & White applied it to technical rules.** They tested 7,846 rules on about 100 years of DJIA data. The best rule's apparent outperformance survived the data-snooping adjustment in-sample but did not hold in the later out-of-sample decade (1987–1996) — [Sullivan, Timmermann & White 1999†](https://doi.org/10.1111/0022-1082.00163)
- **Hansen's SPA test** studentizes each model's performance and uses a sample-dependent null. That makes it more powerful than the Reality Check and less sensitive to including poor or irrelevant alternatives, which inflate the Reality Check p-value — [Hansen 2005†](https://doi.org/10.1198/073500105000000063)
- **Romano-Wolf StepM** identifies *which* of many strategies beat the benchmark while controlling the familywise error rate — [Romano & Wolf 2005†](https://doi.org/10.1111/j.1468-0262.2005.00615.x)
- **Holm step-down.** Sort p-values ascending and reject p₍ᵢ₎ while p₍ᵢ₎ ≤ α/(K−i+1) — [Holm 1979†](https://www.jstor.org/stable/4615733)
- **Benjamini-Hochberg false discovery rate (FDR).** Find the largest i with p₍ᵢ₎ ≤ i·q/K and reject 1..i — [Benjamini & Hochberg 1995†](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)
- **FDR applied to the same 7,846-rule universe.** Bajgrowicz & Scaillet found that apparent technical-rule profits on the DJIA do not survive realistic transaction costs or persist out of sample — [Bajgrowicz & Scaillet 2012†](https://doi.org/10.1016/j.jfineco.2012.06.001)
- **Survey of technical-analysis studies.** Most of the 95 modern studies reviewed reported profits, but many suffered from data snooping, ex-post rule selection and cost/risk-measurement problems — [Park & Irwin 2007†](https://doi.org/10.1111/j.1467-6419.2007.00519.x)
- **Aronson's large-scale test.** He tested 6,402 binary technical rules on the S&P 500 (1980–2005) with White's Reality Check and Monte Carlo permutation. None was significant after correcting for data-mining bias — [Aronson 2006, Evidence-Based Technical Analysis†](https://www.wiley.com/en-us/Evidence+Based+Technical+Analysis%3A+Applying+the+Scientific+Method+and+Statistical+Inference+to+Trading+Signals-p-9780470008744)
- **Harvey-Liu-Zhu hurdle.** After 316 published factors, a newly discovered factor should clear t > 3.0 rather than 2.0 — [Harvey, Liu & Zhu 2016†](https://doi.org/10.1093/rfs/hhv059)
- **Harvey-Liu Sharpe ratio haircut.** Convert the Sharpe ratio to a p-value, adjust it for the number of tests, and convert back. The haircut is nonlinear: strong results are penalized little and marginal ones heavily, so a flat "50% haircut" rule is wrong — [Harvey & Liu 2015, "Backtesting"†](https://doi.org/10.3905/jpm.2015.42.1.013)
  - My Bonferroni version of this haircut — [Sim2 §D](validation_sims/sims2_output.txt):
    - Observed +0.20R over 400 trades (SD 1.45, t = 2.76) falls to +0.158R for K = 5 (21% cut), +0.137R for K = 10 (31%), +0.114R for K = 20 (43%), +0.077R for K = 50 (62%) and +0.040R for K = 100 (80%).
    - Observed +0.15R over 400 trades falls to +0.063R at K = 10 and +0.021R at K = 20.
- **Deflated Sharpe Ratio (DSR)** — [Bailey & López de Prado 2014†](https://doi.org/10.3905/jpm.2014.40.5.094)
  - The DSR is the PSR evaluated against SR₀, the expected maximum Sharpe ratio of N unskilled trials.
  - SR₀ = √V[SR̂ₙ]·((1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e))), where γ ≈ 0.5772 is the Euler-Mascheroni constant and V[SR̂ₙ] is the variance of the trial Sharpe ratios.
  - Their recommendation: record every trial and report N.
- **DSR examples** (2R payoff, per-trade Sharpe = mean/SD, V[SR̂] ≈ 1/T as the null proxy) — [Sim §6](validation_sims/sims_output.txt)
  - Observed +0.20R over T = 400: PSR = 0.997, but DSR = 0.94 / 0.88 / 0.80 / 0.68 / 0.58 for N = 5 / 10 / 20 / 50 / 100 trials. Over T = 1,000, DSR is 0.966 even at N = 100.
  - Observed +0.15R over T = 400: DSR = 0.69 (N = 10) and 0.56 (N = 20).
  - Observed +0.10R over T = 1,000: PSR 0.987 but DSR 0.73 at N = 10.
- **Minimum backtest length (MinBTL)** — [Bailey, Borwein, López de Prado & Zhu 2014†](https://doi.org/10.1090/noti1105) (PDF: [ams.org](https://www.ams.org/notices/201405/rnoti-p458.pdf))
  - MinBTL ≈ ((1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(Ne)))² / E[max SR]², with an upper bound of 2·ln N / E[max SR]².
  - Their example: with 5 years of data, no more than about 45 independent configurations should be tried, or an annualized in-sample Sharpe of 1 is expected from pure noise.
  - Check: the formula gives 5.00 years for N = 45, 3.61 for N = 20, 6.40 for N = 100 and 10.6 for N = 1,000 — [own calculation](validation_sims/verification_checks_output.txt)
- **Probability of Backtest Overfitting (PBO) via combinatorially symmetric cross-validation (CSCV)** — [Bailey, Borwein, López de Prado & Zhu 2017†](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)
  - Split the T × N matrix of per-period results (N configurations) into S even blocks.
  - For every choice of S/2 blocks as in-sample (12,870 choices for S = 16), pick the best in-sample configuration and find its relative out-of-sample rank ω.
  - Compute λ = ln(ω/(1−ω)). PBO is the share of choices with λ ≤ 0, i.e. where the in-sample winner lands at or below the out-of-sample median.
- **Purged and embargoed cross-validation.** Purge training observations whose labels overlap test periods and add an embargo after test folds. Combinatorial purged CV produces many backtest paths — [López de Prado 2018, Advances in Financial Machine Learning†](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
- **Luck from multiple variants (SD 1.25R)** — [Sim §5](validation_sims/sims_output.txt)
  - E[max of K standard normals] = 1.16 / 1.54 / 1.87 / 2.25 / 2.51 / 3.26 for K = 5 / 10 / 20 / 50 / 100 / 1,000.
  - So the best zero-edge variant's mean R by luck is (σ/√T)·E[max]:

    | Trades per variant | K = 5 | K = 10 | K = 20 | K = 50 | K = 100 |
    |---|---|---|---|---|---|
    | 100 | +0.145R | +0.19R | +0.23R | +0.28R | +0.31R |
    | 300 | +0.084R | +0.111R | +0.135R | +0.162R | +0.181R |
    | 1,000 | +0.046R | +0.061R | +0.074R | +0.089R | +0.099R |

- **Variants needed before luck alone is *expected* to reach +m** (SD 1.25R) — [Sim §5](validation_sims/sims_output.txt)

  | Trades per variant | m = +0.05R | m = +0.10R | m = +0.15R | m = +0.20R |
  |---|---|---|---|---|
  | 100 | 2 | 3 | 6 | 12 |
  | 200 | 3 | 5 | 14 | 52 |
  | 300 | 3 | 8 | 33 | 205 |
  | 500 | 4 | 17 | 166 | ≈3,300 |
  | 1,000 | 6 | 107 | ≈7,800 | ≈2.7 million |
  | 2,000 | 17 | ≈3,300 | > 10 million | > 10 million |

- **Bonferroni thresholds and the trades they require** — [Sim §5](validation_sims/sims_output.txt)
  - One-sided z for K variants: 1.645 (K = 1), 2.128 (3), 2.326 (5), 2.576 (10), 2.807 (20), 3.090 (50), 3.291 (100).
  - Trades needed for 80% power at that threshold (SD 1.25R) for a +0.2R edge: 243 (K = 1), 347 (3), 460 (10), 524 (20), 673 (100).
  - For a +0.1R edge: 968 (K = 1), 1,829 (10), 2,674 (100).
- **Peeking inflates false positives.** Re-running a one-sided t-test (t ≥ 1.645) as trades accumulate, on a zero-net-edge setup — [Sim §7](validation_sims/sims_output.txt)
  - One look at n = 100: 4.3–5.3% false passes.
  - A look every 25 trades up to 300: 16–18%.
  - A look after every trade from 30 to 100: 15–17%.
  - A look after every trade from 20 to 300: 25–27%.
  - "Always-valid" sequential methods exist precisely to fix this — [Johari, Pekelis & Walsh 2017†](https://doi.org/10.1145/3097983.3097992)

### Inferences
- **Replay protocol for this trader:**
  - **(a) Pre-registration record in the app.** Store the setup rules, parameters, universe, timeframe, entry/exit/fill/slippage/cost model, data range, primary metric (mean net R per trade), decision thresholds, and a code hash or setup-version id. Store it *before* the run.
  - **(b) Trial counter.** Increment K for every variant evaluated on any data, including ones discarded. K feeds the Bonferroni threshold, the DSR (N) and the haircut automatically.
  - **(c) Chronological split.** Use at least 3 years (ideally 4–5) of 1-minute data. Take the earliest ~2/3 for development (in-sample, IS) and hold out the most recent ~1/3 (at least 12 months and ideally at least 200 trades) as out-of-sample (OOS), opened once. Walk-forward or rolling re-optimization is allowed inside the IS block only.
  - **(d) Purge and embargo swing trades.** Trades that span days near the split boundary should be purged and embargoed, per López de Prado.
  - **(e) Limit candidates.** Carry one pre-registered candidate (or at most 2–3) into OOS. A single untouched OOS test of a single candidate keeps α = 5% honest. With 3 candidates, use t ≥ 2.13.
  - **(f) Treat OOS as burned.** If the OOS result is used to tweak the rule, it becomes in-sample. A fresh holdout is then the forward paper period (Stage 2).
- **Heuristic for the number of variants: K_max ≈ exp(T·δ²/(8σ²)).** This keeps the expected best-of-K luck at or below half the target edge δ. The bound is conservative: actual luck at K_max was 0.074–0.087R against a 0.10R bound.
  - With δ = 0.2R and σ = 1.25R: T = 500 → K ≤ 5; T = 750 → K ≤ 11; T = 1,000 → K ≤ 24; T = 1,500 → K ≤ 121; T = 2,000 → K ≤ 600.
  - Chasing a 0.1R edge allows almost no search at T ≤ 1,000 (K ≤ 2).
  - Rule of thumb for an NSE trader with about 1 flag per day per setup over 3–4 years (T ≈ 750–1,000): **keep total setups × parameter variants at roughly 10–25**, and demand t ≥ the Bonferroni threshold for that K, or DSR ≥ 0.95, in IS.
- **When the scoreboard compares several setups,** run a Reality Check, SPA or StepM on day-level R series against the 0R benchmark, or against the "all flags" line when testing filters. Use a stationary bootstrap with an average block of about 5–10 days, as in [Politis & Romano 1994†](https://doi.org/10.1080/01621459.1994.10476870). Use this instead of eyeballing the best line.
- **Book-coded setups have a hidden K.** Setups coded from trading books were often chosen by their authors because they "worked" on past charts, so treat them as already partly mined. This argues for the stricter thresholds (t ≥ 2.5–3) rather than 1.645 when many book setups are screened.
- **Count every variant shown on a scoreboard.** Every additional setup, parameter variant or scoreboard line counts toward K, whether or not it is ever "selected".

### Gaps
- **Walk-forward efficiency thresholds unverified.** Robert Pardo's walk-forward efficiency (OOS / IS annualized return, with commonly quoted acceptability around ≥ 50–60%) could not be checked in-session. Treat it as a practitioner heuristic.
- **PBO thresholds.** Primary papers give no fixed PBO pass threshold. A requirement such as "PBO ≤ 0.1–0.2" would be my judgment, not a literature standard.
- **Ernest Chan's backtesting-pitfall material** was not consulted in-session.

---

## Q4. Pitfalls specific to replaying NSE 1-minute data, and how to avoid them

### Takeaway
For a manual NSE trader, most replay inflation comes from timing and fills, not from statistics:

- acting on an unfinished candle
- filling at the signal price or the auction-set 09:15 open
- ignoring manual-entry delay and the broker's intraday square-off
- using today's index lists
- unadjusted corporate actions
- bad prints and circuit-locked stocks

Costs are just as decisive. At ₹200 risk, round-trip intraday costs run roughly **0.1–0.4R** depending on stop width (**cost_R = round-trip cost % ÷ stop distance %**). Bought options carry at least 0.2R in brokerage alone. Every one of these items needs an explicit rule in the replay engine, and the same fill and slippage model must be applied to forward paper trades.

### Cited Findings
- **Round-trip cost in R, on an *assumed* Zerodha-style rate card** (rates listed under Gaps; verify against the [Zerodha charges page†](https://zerodha.com/charges)) — [Sim2 §A](validation_sims/sims2_output.txt)
  - **Intraday equity (notional = ₹200 ÷ stop %):**

    | Stop distance | Notional | Fees alone | With 2 bps/side slippage | With 5 bps/side slippage |
    |---|---|---|---|---|
    | 0.3% | ₹66,667 | 0.35R | 0.49R | 0.69R |
    | 0.5% | ₹40,000 | 0.21R | 0.29R | 0.41R |
    | 0.75% | — | 0.14R | 0.20R | 0.28R |
    | 1.0% | ₹20,000 | 0.11R | 0.15R | 0.21R |
    | 2.0% | — | 0.05R | 0.07R | 0.10R |

  - **Delivery/swing (CNC):** a 3% stop costs about 0.15R, 5% about 0.12R and 8% about 0.10R. The fixed DP charge dominates.
  - **Bought options at ₹20 per order:** about 0.25–0.33R for ₹2,000–10,000 premium per side; brokerage alone is 0.20R.
- **Overview of standard backtest biases.** These include look-ahead, survivorship, data snooping, transaction costs and outliers, the "seven sins" catalogued by Luo et al. (2014) — [López de Prado 2018, Ch. 11†](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
- **Kite Connect's historical-candles API** is the natural source of 1-minute data for a Zerodha user — [Kite Connect historical API docs†](https://kite.trade/docs/connect/v3/historical/). Its candle conventions are listed under Gaps.

### Inferences
These are pitfall-to-rule mappings for the replay engine, based on practitioner knowledge rather than in-session sources.

1. **Look-ahead and candle timing.**
   - Evaluate signals only on *closed* bars.
   - If a bar is stamped with its start time (verify for Kite), a 10:05 bar is known only at 10:06:00.
   - The earliest realistic entry is the open of the bar after the signal bar, plus manual delay.
   - Never use the day's high, low, close, volume or "today's range" before it is complete. For example, a 09:15–09:30 opening range is usable only after 09:30.
   - Never use indicators computed on full-day or adjusted data that include future bars.
2. **Manual-entry delay (Kite by hand).**
   - Model at least one extra bar of delay: fill at the open of signal bar + 2, or at the worse of next-bar open and next-bar VWAP.
   - In Stage 2, log the flag time, decision time and (hypothetical) order time to measure the real delay, then feed it back into the replay.
   - Report replay results both with zero delay and with 1–2 minutes of delay. Edge that vanishes with 1 minute of delay is not usable by a manual trader.
3. **Fill model.**
   - Market entries: next tradable price plus slippage of at least 1 tick or a bps model scaled to spread and liquidity. Stress-test at 2× slippage.
   - Stop exits: the stop price minus slippage. If the next bar gaps beyond the stop, fill at that bar's open.
   - Limit or target exits: fill only if price trades *through* the limit, not merely touches it.
   - If one bar touches both stop and target, assume the stop was hit first.
4. **Auction prices.**
   - Do not fill at the 09:15 first-bar open. It is set by the pre-open call auction, which a manual trader can only get by participating in the auction.
   - Avoid entries in the first 1–5 minutes, or model wide slippage there.
   - Do not use the official closing price as an intraday exit. On NSE it is a 30-minute VWAP, not a traded price available at a moment in time.
5. **End-of-day square-off.**
   - Force intraday (MIS) exits by the broker's auto square-off time (verify; about 15:20 for equity), at the bar price minus slippage.
   - Better still, exit by a self-imposed time such as 15:10–15:15 to avoid broker square-off charges.
6. **Circuit-locked and illiquid stocks.**
   - Skip a fill when the bar is flat (O = H = L = C) at the price-band limit on the side you need, or has zero volume.
   - Cap position size at a small share of 1-minute traded value (e.g., ≤ 1–5%).
   - Exclude stocks in price bands of 2%/5% if the setup needs room.
   - Treat a stop that cannot fill because of a lock as a gap loss beyond −1R. Do not treat it as −1R.
7. **Corporate actions.**
   - Adjust prices for splits and bonuses (ratio-adjust) *point-in-time* before computing multi-day levels (20-day high, ATR, moving averages).
   - Check ex-dates for dividend gaps on swing trades.
   - Verify that rupee stop distances and tick sizes stay consistent after adjustment.
8. **Survivorship.**
   - Build universes from point-in-time index membership and F&O-eligibility lists, not today's lists.
   - Include delisted and merged names. For example, HDFC Ltd. was merged into HDFC Bank in 2023 (verify dates).
9. **Bad ticks, halts and outages.**
   - Filter isolated spikes (e.g., a bar deviating more than X ATR from both neighbours and reverting), zero-volume bars and duplicated timestamps.
   - Flag known incident days for exclusion or a separate check, such as the 5 Oct 2012 erroneous-order crash in Nifty and the 24 Feb 2021 NSE trading outage (verify).
10. **Holidays and special sessions.** Exclude Muhurat or special sessions and half days from intraday statistics.
11. **Sizing realism.**
    - Quantity = floor(₹200 ÷ (entry − stop)). Expensive stocks may need fewer shares than ₹200 of risk implies, and quantity can even be zero.
    - Check MIS leverage limits against ₹20,000.
    - Record R against the *planned* ₹200 so R stays additive with the rupee stop.
12. **Costs.**
    - Compute fees per trade from the actual notional and the current rate card. Shortcut: cost_R = round-trip cost % / stop %.
    - Keep only setups whose *gross* edge clearly exceeds about 2× cost_R. A 0.5%-stop intraday setup needs roughly +0.3–0.4R gross just to clear about 0.2R of costs comfortably.
    - Options buying at ₹200 risk starts about 0.25–0.33R in the hole per trade. That is a structural reason to avoid F&O at this capital and risk size.
13. **Paper-trade parity.** Forward paper trades must use the same fill, slippage, delay and cost model as replay. Otherwise the Stage-1 vs Stage-2 comparison is meaningless.

### Gaps
None of the following could be verified in-session. Treat them as facts to confirm before the report states them.

- **Assumed rate card (Zerodha, as recalled from the Oct-2024 revision):**
  - Intraday equity: brokerage the lower of 0.03% and ₹20 per order; STT 0.025% on sell; NSE transaction charge 0.00297%; SEBI fee ₹10/crore; stamp duty 0.003% on buy; GST 18% on brokerage, transaction and SEBI charges.
  - Delivery: no brokerage; STT 0.1% on both sides; stamp duty 0.015% on buy; DP charge about ₹15.34 per scrip per sell day.
  - Options: ₹20 per order; STT 0.1% of sell premium; transaction charge 0.03503% of premium.
  - It is unknown whether **Union Budget 2026-27** changed F&O STT (I have an unverified recollection of an increase). Check the current Zerodha charges page or a contract note.
- **NSE session structure:**
  - Pre-open call auction 09:00–09:15, with order entry until about 09:08 and random closure.
  - Continuous trading 09:15–15:30.
  - Closing price = VWAP of 15:00–15:30.
  - Post-close session 15:40–16:00.
  - Whether a closing-auction session proposed by SEBI/NSE has been introduced by Oct 2026.
- **Zerodha MIS auto square-off times** (about 15:20 equity and about 15:25 F&O?) and the auto-square-off charge (about ₹50 + GST per order?).
- **NSE price-band and market rules:** price bands (2/5/10/20% for non-F&O stocks; dynamic bands for F&O stocks), market-wide circuit breakers (10/15/20%), and any 2025 tick-size revisions.
- **Kite historical-data conventions:** candle timestamp convention, corporate-action adjustment, per-request limits on minute data, and current pricing.
- **SEBI loss studies.** Headline figures from SEBI's 2024 studies (about 70% of individual intraday equity traders and about 93% of individual F&O traders lost money) are relevant base rates but were not verified.

---

## Q5. Comparing filtered subsets fairly: does the model's take/skip filter or the trader's final call beat all flags?

### Takeaway
The three scoreboard lines are nested subsets of the same flags, so testing "model picks vs all flags" with an ordinary two-sample test is invalid. Instead:

- **For the model's filter:** test taken vs skipped. Uplift over all flags = (1 − take rate) × (taken − skipped).
- **For model vs trader:** test only the flags where they disagree, as a paired comparison.

The sample sizes needed are large. With SD 1.25R and a 50% take rate, detecting a 0.3R taken-vs-skipped gap needs about 430 flags (0.5R: about 155; 0.2R: about 970). A 30-trade "trader picks" line has a ±0.45R 95% CI. After 100 flags the scoreboard can reveal only very large filter effects.

### Cited Findings
- **Total flags needed to detect a taken-minus-skipped gap D** (one-sided α = 0.05, 80% power, SD 1.25R). Formula: n_total = (z₁₋α + z₁₋β)²·σ²·(1/f + 1/(1−f)) / D², where f is the take rate — [Sim §10](validation_sims/sims_output.txt)

  | Take rate f | D = 0.1R | D = 0.2R | D = 0.3R | D = 0.5R |
  |---|---|---|---|---|
  | 0.2 | 6,038 | 1,510 | 671 | 242 |
  | 0.3 or 0.7 | 4,601 | 1,151 | 512 | 185 |
  | 0.5 | 3,865 | 967 | 430 | 155 |

- **Model vs trader, paired on disagreements only.** Number of disagreement flags needed for a mean advantage dd per disagreement (SD 1.25R) — [Sim §10](validation_sims/sims_output.txt)

  | Advantage dd | Disagreement flags | Total flags if they disagree on 20% / 40% |
  |---|---|---|
  | 0.1R | 968 | 4,840 / 2,420 |
  | 0.2R | 243 | 1,215 / 608 |
  | 0.3R | 109 | 545 / 273 |
  | 0.5R | 40 | 200 / 100 |

- **Precision of a single scoreboard line (SD 1.25R)** — [Sim §10](validation_sims/sims_output.txt)

  | Trades in the line | SE | 95% CI |
  |---|---|---|
  | 100 | 0.125R | ±0.25R |
  | 50 | 0.177R | ±0.35R |
  | 30 | 0.228R | ±0.45R |
  | 20 | 0.280R | ±0.55R |

- **Benchmark-relative "best of many" tests apply here** with the "all flags" line as benchmark — [White 2000†](https://doi.org/10.1111/1468-0262.00152); [Hansen 2005†](https://doi.org/10.1198/073500105000000063)
- **Block bootstrap for serially dependent (day-clustered) data** — [Politis & Romano 1994†](https://doi.org/10.1080/01621459.1994.10476870)

### Inferences
- **Formulas the app can compute (per setup):**
  - **Filter effect:** D̂ = x̄_taken − x̄_skipped; SE = √(s_T²/n_T + s_S²/n_S); z = D̂/SE; 95% CI = D̂ ± 1.96·SE.
  - **Uplift over all flags:** U = x̄_taken − x̄_all = (1 − f)·D̂, with CI = (1 − f) × the CI of D̂.
  - **Permutation p-value (exact, no normality needed):**
    1. Keep n_T fixed.
    2. Randomly reassign the "taken" labels among all flags, B = 10,000 times.
    3. p = (1 + #{D_perm ≥ D̂}) / (B + 1).
    4. To respect day clustering, permute labels *within days* (stratified permutation), or use a day-block bootstrap for the CI.
  - **Model vs trader (paired):**
    1. For each flag, d_i = (T_i − M_i)·R_i, where T_i and M_i are 1 if the trader or model took the flag.
    2. Only the disagreement cells (trader-only, model-only) contribute.
    3. Statistic = Σd_i, the difference in total R between the two lines.
    4. Test with t = mean(d)/(sd(d)/√n_disagree), or a sign-flip permutation over disagreement flags.
    5. Also show the 2×2 table (model take/skip × trader take/skip) with mean R in each cell.
  - **Shrinkage for display.** Use Bayesian shrinkage of each line's mean toward the all-flags mean, e.g. a normal prior with n₀ phantom trades as in Q6, so small lines do not show extreme numbers.
- **Blinding.** Record the trader's take/skip **before** revealing the model's verdict. Otherwise the "trader" line measures model plus anchoring, and the trader's independent value cannot be estimated. If blinding is not wanted, record both a pre-verdict and a final call.
- **Pre-specify one primary comparison** (e.g., model taken vs skipped, pooled over setups). Treat every other cut (per setup, per time of day, per regime) as exploratory with Holm/BH correction. Otherwise 3 lines × N setups × several metrics recreates the multiple-testing problem from Q3.
- **Version the model.** Record the model version and prompt version with each verdict. A change in either starts a new evaluation series, just as a parameter change does.
- **Practical timeline.**
  - Required flags ÷ (flags per session × about 21 sessions per month) gives the months needed.
  - At 5 flags/day, 430 flags take about 4 months. At 2 flags/day they take about 10 months.
  - The "all flags" line therefore reaches decision-grade sample sizes long before the model-filter and trader-filter lines.
- **Other useful filter metrics:** "R saved" (sum of R of skipped losers) vs "R forgone" (sum of R of skipped winners). Also the filter's hit rate on outcome direction, with a binomial CI. These are more intuitive for a trader but carry the same sample-size limits.

### Gaps
- **Disagreement rate and correlation.** How often the model and trader disagree, and how correlated the model's verdicts are with simple features (time of day, trend), are unknown. Power for the paired test depends directly on the disagreement rate.
- **No empirical estimates of LLM take/skip effect sizes on trading flags** were reviewed in-session.

---

## Q6. Recommended two-stage pass-mark design, with formulas the app can compute and concrete numbers for this trader

### Takeaway
- **Stage 1 (replay, setups only).** Pre-register and freeze the rule. Use at least 3 years of point-in-time NSE 1-minute data with a chronological ~2/3 in-sample and ~1/3 out-of-sample split (OOS at least 12 months and ideally at least 200 trades), and count every variant tried.
  - Pass only if OOS net mean R > 0 with t ≥ the Bonferroni threshold for the candidates taken to OOS (1.645 for a single candidate).
  - In-sample DSR (N = all variants) must be ≥ 0.95.
  - The edge must survive a 1.5× cost stress test plus one extra minute of entry delay.
- **Stage 2 (forward paper trading, setups plus verdicts).** Run a Wald SPRT on per-trade net R of *all flags*: H0 μ = 0 vs H1 μ = +0.2R, α = 5%, β = 20%.
  - **PASS when ΣR ≥ (σ²/0.2)·2.773 + 0.1·n**, with at least 50 trades and at least 3 months.
  - **FAIL when ΣR ≤ (σ²/0.2)·(−1.558) + 0.1·n**.
  - Stop at 300 trades as "not proven".
  - For σ = 1.25R in rupees: PASS line ₹4,332 + ₹20·n; FAIL line −₹2,435 + ₹20·n. This FAIL line replaces the peak-to-trough ₹2,000 stop.
- **Model and trader filters** are graded separately on taken-vs-skipped confidence intervals and are never declared "better" on fewer than about 400 flags.

### Cited Findings
- **SPRT boundaries.** Wald's sequential probability ratio test uses A = ln((1−β)/α) and B = ln(β/(1−α)). The expected sample sizes are E[N|H1] ≈ ((1−β)A + βB)/(δ²/2σ²) and E[N|H0] ≈ (αA + (1−α)B)/(−δ²/2σ²) — [Wald 1945†](https://doi.org/10.1214/aoms/1177731118)
  - For normal-approximated R, these give **PASS: ΣR ≥ (σ²/δ₁)·A + n·δ₁/2** and **FAIL: ΣR ≤ (σ²/δ₁)·B + n·δ₁/2**. With α = 0.05 and β = 0.20, A = 2.773 and B = −1.558 — [Sim §8](validation_sims/sims_output.txt)
- **SPRT boundaries for δ₁ = 0.2R, with the mean R a pass or fail implies at n = 100 / 200 / 300** — [verification run](validation_sims/verification_checks_output.txt)

  | σ | PASS line | FAIL line | Mean needed to pass at n = 100 / 200 / 300 | Mean that fails at n = 100 / 200 / 300 |
  |---|---|---|---|---|
  | 1.0R | 13.86 + 0.1n | −7.79 + 0.1n | 0.239 / 0.169 / 0.146R | ≤ 0.022 / 0.061 / 0.074R |
  | 1.1R | 16.77 + 0.1n | −9.43 + 0.1n | 0.268 / 0.184 / 0.156R | — |
  | 1.25R | 21.66 + 0.1n | −12.17 + 0.1n | 0.317 / 0.208 / 0.172R | ≤ −0.022 / 0.039 / 0.059R |
  | 1.47R | 29.96 + 0.1n | −16.83 + 0.1n | 0.400 / 0.250 / 0.200R | — |

  - Untruncated Wald expected trades for σ = 1.25 are about 149 under H1 and about 105 under H0, against 243 for the fixed-sample test.
- **Simulated SPRT performance** (δ₁ = 0.2R, min 50 and max 300 trades, no capital stop) — [Sim2 §C](validation_sims/sims2_output.txt)

  | Payoff (σ) | True E | PASS | FAIL | Undecided at 300 | Average trades |
  |---|---|---|---|---|---|
  | B (1.10) | 0 | 4.3% | 93.2% | 2.5% | 85 |
  | B | +0.1R | 30.3% | 58.8% | — | 131 |
  | B | +0.2R | 76.9% | 18.3% | — | 122 |
  | B | +0.3R | 96.3% | — | — | 86 |
  | A (1.47) | 0 | 3.1% | 85.0% | 11.9% | 136 |
  | A | +0.1R | 21.2% | — | — | — |
  | A | +0.2R | 61.5% | 16.6% | 21.9% | 185 |
  | A | +0.3R | 91.0% | — | — | 141 |

  - Realized α is about 3–4%, below the nominal 5%. Power at +0.2R is about 62–77%, below the nominal 80% because of truncation.
- **The same SPRT under different capital stops** — [Sim2 §C](validation_sims/sims2_output.txt)
  - **10R stop measured from the start:**
    - Payoff B: results are identical to no stop, because the SPRT FAIL line (−9.35 to −9.43R + 0.1n) always sits above −10R.
    - Payoff A: at +0.2R, PASS 58.8% and stopped out 11.5%. At 0R, PASS 3.0%.
  - **10R peak-to-trough stop:**
    - Payoff A at +0.2R: PASS only 30.9%, stopped out 68.6%.
    - Payoff B at +0.2R: PASS 69.8%, stopped out 17.4%.
  - **20R peak-to-trough stop (₹100 risk per trade):** PASS 60.5% (A) and 77.2% (B) at +0.2R.
  - With the 10R peak stop and δ₁ = 0.15R, payoff A at +0.2R passed only 24% (stopped out 75.5%) — [Sim §8](validation_sims/sims_output.txt)
- **Bayesian alternative — skeptical normal prior N(m₀, τ²) as "phantom trades".**
  - The prior is equivalent to adding n₀ = σ²/τ² phantom trades at R = m₀:
    - **P(μ > θ | data) = Φ( ((n₀·m₀ + ΣR)/(n₀ + n) − θ) · √(n₀ + n)/σ )**
    - With m₀ = θ = 0 this simplifies to **Φ( ΣR / (σ·√(n + n₀)) )** — [Sim §9](validation_sims/sims_output.txt)
  - Posterior P(μ > 0) at SD 1.25R — [Sim §9](validation_sims/sims_output.txt):

    | Prior | n = 100, observed mean +0.2R | n = 300, +0.2R | n = 300, +0.1R | n = 500, +0.1R |
    |---|---|---|---|---|
    | Flat (same as one-sided p) | 0.945 | — | — | — |
    | N(0, 0.1²), n₀ = 156 | 0.841 | 0.988 | 0.869 | 0.941 |

- **Sequential Bayesian rule performance.** Check after every trade from n = 50; PASS at P ≥ 0.95, FAIL at ≤ 0.10; 10R peak stop; max 300 trades — [Sim §9](validation_sims/sims_output.txt)

  | Payoff | Prior | False pass at 0R | PASS at +0.1R | PASS at +0.2R |
  |---|---|---|---|---|
  | B | Flat | 17.3% | — | 84.5% |
  | B | τ = 0.15 | 10.1% | — | 81.0% |
  | B | τ = 0.10 | 5.7% | 34.7% | 76.5% |
  | A | Flat | 12.3% | — | 54.1% |
  | A | τ = 0.10 | 1.2% | — | 28.7% (the peak stop dominates) |

- **Fixed-sample equivalents.** The fixed-n test with 80% power at +0.2R needs 187 trades (σ 1.1), 243 (σ 1.25) and 336 (σ 1.47). The SPRT needs fewer on average — [Sim §8](validation_sims/sims_output.txt)

### Inferences
**Stage 0 — Pre-registration (in-app form, locked before any run):**

- Setup id and version hash, universe definition (point-in-time), timeframe, entry trigger, stop, target/exit, time stop, and the square-off rule.
- Fill model (next-bar open plus manual-delay bars), slippage model, cost model.
- Primary metric: mean net R per trade, day-clustered SE.
- K counter, the thresholds below, and the minimum edge worth trading δ₁ (default +0.2R).

**Stage 1 — Historical replay (setups only; verdicts cannot be replayed):**

- **Data:** at least 3 years (prefer 4–5) of NSE 1-minute data, point-in-time universe, corporate-action adjusted, cleaned per Q4.
- **Split:** earliest ~2/3 in-sample (IS: design and any walk-forward tuning); latest ~1/3, and at least 12 months, as OOS, opened once.
- **Gates (all required):**
  - **S1. Sample size.** n_OOS ≥ 200 trades (power ≈ 73% for +0.2R at σ 1.25; 300 trades gives ≈ 87%). If fewer, extend history or pool similar instruments. Otherwise mark the result "insufficient sample" rather than pass.
  - **S2. OOS significance.** OOS net mean R > 0 with day-clustered t ≥ z₁₋₀.₀₅/K_OOS: 1.645 for one candidate, 1.96 for two, 2.13 for three.
  - **S3. In-sample selection deflated.** DSR ≥ 0.95 with N = K_IS (all variants tried). Equivalently, IS t ≥ the Bonferroni z for K_IS (2.58 at K = 10; 2.81 at K = 20), and/or a Harvey-Liu-style haircut mean R > 0.
  - **S4. Robustness (practitioner heuristics, my judgment).** OOS mean R must stay > 0 with costs × 1.5 and with one extra minute of entry delay. It must be ≥ 50% of the IS mean. No single month or stock may contribute more than about 30% of total R. At least 60% of calendar quarters must be positive. The parameter-neighbourhood average (±20% on each parameter) must be > 0.
  - **S5. Budget fit.** Bootstrap the OOS trade list to estimate P(down 10R from start within 200 trades). If it is above about 20%, reduce risk per trade (e.g., ₹100) before Stage 2.
- **Outputs carried forward:** μ̂_OOS, σ̂, skew and kurtosis, and the cost and delay assumptions. σ̂ sets the Stage-2 SPRT lines; μ̂_OOS sets the consistency check.

**Stage 2 — Forward paper trading (setups plus model verdicts plus trader calls; paper-trade every flag):**

- **Primary endpoint:** net R per trade of **all flags** of the frozen setup, with the same fill, slippage, delay and cost model as Stage 1.
- **Decision rule:** SPRT with δ₁ = +0.2R, α = 0.05, β = 0.20, σ = σ̂ from Stage 1:
  - **PASS** if ΣR ≥ 13.86·σ̂² + 0.1·n, **and** n ≥ 50, **and** at least 3 calendar months elapsed. (13.86 = 2.773/0.2.)
  - **FAIL** if ΣR ≤ −7.79·σ̂² + 0.1·n. (−7.79 = −1.558/0.2.)
  - **NOT PROVEN** at n = 300 (or 12 months) if neither line is crossed. Either return to Stage 1 or continue at reduced risk with a new pre-registration.
  - **For σ̂ = 1.25R in rupees (1R = ₹200):** PASS when cumulative P&L ≥ ₹4,332 + ₹20 × trades; FAIL when cumulative P&L ≤ −₹2,435 + ₹20 × trades.
  - This FAIL line *is* the "₹2,000 drawdown" idea, made statistically consistent: a rising floor starting near −₹1,900 to −₹2,400 for σ̂ = 1.1–1.25R.
  - For 2R-target setups (σ̂ ≈ 1.47R) the floor starts lower, at −₹3,367. If the trader insists on a hard ₹2,000-from-start limit as well, it binds first for roughly the first 68 trades. The cost in power is small: pass rate at +0.2R falls from 61.5% to 58.8% (Sim2 §C).
  - Drop the peak-to-trough 10R stop in paper trading. It kills 52–80% of real +0.2R edges with 2R targets.
- **Optional Bayesian display alongside the SPRT** (not a second decision rule): P(edge > 0) = Φ(ΣR / (σ̂·√(n + n₀))) with n₀ = σ̂²/0.1² (about 120–220 phantom zero-R trades). Label it "skeptical prior: most setups have no edge".
- **Replay-vs-paper consistency check:** z_gap = (x̄_paper − μ̂_OOS) / √(σ̂²/n_paper + σ̂²/n_OOS). If z_gap < −2, the replay was probably optimistic (fills, look-ahead or costs). Fix the replay engine before trusting any Stage-1 pass.
- **Secondary endpoints:** model picks and trader picks. Report the taken-vs-skipped difference D̂ with CI, the uplift (1−f)·D̂, the permutation p, and the paired disagreement test.
  - Declare a filter "adds value" only if the lower 95% bound of the uplift is > 0, with at least about 400 flags (SD 1.25R, 50% take rate, D ≈ 0.3R).
  - Until then, show "insufficient evidence", not a ranking.
- **Multiplicity in Stage 2.** If several setups run Stage 2 at once, apply Holm across setups to the final PASS decisions, or use α/K in the SPRT A boundary: A = ln((1−β)/(α/K)). For K = 3 that is ln(48) = 3.87, so the PASS intercept rises by about 40%.

**Stage 3 — Small live trading (recommended, beyond the question):** run live at ₹100–200 risk with the same SPRT lines, recomputed from live fills, and the ₹2,000 limit measured from the starting balance. Scale up only after live expectancy is consistent with paper (z_gap > −2).

**Formula sheet for the app (R = net R per trade; n = trades; D = days):**

1. **Expectancy and uncertainty:** x̄ = ΣR/n; s = SD(R); SE = s/√n (or the day-clustered SE from Q1); t = x̄/SE; 95% CI = x̄ ± t₀.₉₇₅,ₙ₋₁·SE.
2. **Trades still needed for an edge δ:** n_req = ((z₁₋α/K + z₁₋β)·s/δ)² + z²/2.
3. **PSR:** PSR(SR*) = Φ((SR̂ − SR*)·√(n−1)/√(1 − γ₃SR̂ + ((γ₄−1)/4)SR̂²)), with SR̂ = x̄/s.
4. **DSR:** DSR = PSR(SR₀), with SR₀ = √(1/n)·((1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(Ne))).
5. **MinTRL:** 1 + (1 − γ₃SR̂ + ((γ₄−1)/4)SR̂²)·(z_α/(SR̂ − SR*))².
6. **Expected luck from K variants:** (s/√n)·((1−γ)Φ⁻¹(1−1/K) + γΦ⁻¹(1−1/(Ke))). Variant budget: K_max ≈ exp(n·δ²/(8s²)).
7. **Haircut:** p = 1 − Φ(t); p_adj = min(1, K·p) (or Holm/BH); t_adj = Φ⁻¹(1 − p_adj); haircut mean = t_adj·s/√n.
8. **SPRT lines:** PASS ΣR ≥ (s²/δ₁)·ln((1−β)/α) + nδ₁/2; FAIL ΣR ≤ (s²/δ₁)·ln(β/(1−α)) + nδ₁/2.
9. **Bayesian:** P(μ > 0) = Φ((n₀m₀ + ΣR)/(s·√(n₀ + n))), with n₀ = s²/τ².
10. **Ruin from start within n trades:** Φ((−Dᵣ − x̄n)/(s√n)) + exp(−2x̄Dᵣ/s²)·Φ((−Dᵣ + x̄n)/(s√n)), with Dᵣ = 10R. For peak-to-trough drawdown, use a 10,000-path bootstrap of the trade list.
11. **Filter tests:** D̂ = x̄_T − x̄_S with SE √(s_T²/n_T + s_S²/n_S); uplift (1−f)·D̂; permutation p = (1 + #{D_perm ≥ D̂})/(B+1); paired d_i = (T_i − M_i)·R_i over disagreements.
12. **Costs:** cost_R = round-trip cost % / stop %. Require gross x̄ − cost_R > 0 under 1.5× costs.

**Why this replaces "100 trades / 3 months / profitable / within ₹2,000":**

- The SPRT controls false passes at about 3–5% for one setup. The current rule's false-pass rate floats between 0.3% and 47% depending on payoff shape, cost level and stop definition.
- The SPRT reaches decisions in about 85–185 trades on average.
- It keeps the ₹2,000 loss budget, but as a rising floor that does not kill real edges.
- It forces the multiple-testing accounting (K) that makes a scoreboard of many setups and lines interpretable.

### Gaps
- **The choice of δ₁ = +0.2R is a judgment.** It is roughly the smallest edge that survives about 0.1–0.2R of costs with margin at this risk size. A trader content with +0.1R edges faces about 4× larger samples (about 620–1,400 trades), which is infeasible to verify within months.
- **Untested refinements.** Truncated or group-sequential designs (O'Brien-Fleming boundaries, mixture SPRTs or always-valid p-values) could improve power at the 300-trade cap. They were not simulated here.
- **The Stage-1 thresholds in S4** (≥ 50% of IS, ≤ 30% concentration, ≥ 60% positive quarters, ±20% neighbourhood) are practitioner heuristics, not literature standards.
- **Non-stationarity is not modelled.** Edges decay and regimes shift. A setup that passes can still fail later, so monitoring with the same SPRT lines should continue in live trading.
