# LLM verdict layer: evidence, failure modes, evaluation design, and running Claude via `claude -p` on Pro vs the Claude API

Scope note: notes compiled 31 Oct 2026. Anthropic facts come from official pages fetched today: platform.claude.com pricing, models overview and citations pages; code.claude.com CLI reference, headless, model-config, legal and Agent SDK pages; support.claude.com; and anthropic.com legal pages. arXiv full texts could not be fetched in this session (the host was blocked), so findings from academic papers rest on abstracts, search-result summaries and secondary write-ups. Each such finding is labelled. INR figures use an **assumed** rate of about ₹88 per USD (not verified) and exclude any GST.

---

## 1. What do rigorous or out-of-sample studies show about LLMs predicting returns, picking stocks, filtering trades or trading as agents? Are there evaluations strictly after training cutoffs, or Indian-market evidence?

### Takeaway
The positive evidence is narrow. LLM scores of news headlines and GPT-4 stock ratings predicted short-horizon US returns, but the effect is concentrated in small stocks and negative news, and it decays as LLM use spreads. Tests that are contamination-free or live (StockBench, AI-Trader, LiveTradeBench, the Alpha Arena real-money contests) mostly show LLM agents failing to beat buy-and-hold consistently, struggling in down markets, or losing money. I found no study of the trader's exact design (an LLM giving take/skip verdicts on rule-based intraday setups), no published trading evaluation of Claude Opus 5.5, and no rigorous Indian-market evidence.

### Cited Findings
**Return forecasting from news and ratings**
- Lopez-Lira & Tang, "Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models" (arXiv 2304.07619). First appeared on arXiv on 15 Apr 2023, after an SSRN posting; latest revision is v6, 28 Oct 2025. The search found no journal publication, so it appears to remain a working paper. — [arXiv v6](https://arxiv.org/abs/2304.07619v6); [EconPapers listing](https://econpapers.repec.org/paper/arxpapers/2304.07619.htm)
- v5/v6 abstract (via search summary): ChatGPT scores of news headlines predict out-of-sample daily stock returns and outperform traditional methods. Predictability is stronger for smaller stocks and after negative news. — [arXiv v6](https://arxiv.org/abs/2304.07619v6)
- GPT-1, GPT-2 and BERT did not forecast returns reliably, while GPT-4 had the most predictive power. The authors call return predictability "an emerging capacity of more complex language models." The v1 abstract was more cautious. — [arXiv v6](https://arxiv.org/abs/2304.07619v6); [arXiv v1](https://arxiv.org/abs/2304.07619v1)
- v6 reports that strategy returns fall as LLM adoption rises, which the authors link to improved price efficiency. A theory section argues that some predictability persists in equilibrium. — [arXiv v6](https://arxiv.org/abs/2304.07619v6)
- Pelster & Val, "Can ChatGPT assist in picking stocks?", *Finance Research Letters* 59 (2024). A **live** test of GPT-4 investment advice during the Q2-2023 earnings season. It found a positive correlation between GPT-4 "attractiveness" ratings and subsequent earnings surprises and stock returns, and a positive return from a strategy built on the ratings. Ratings updated after news, accuracy varied over time, and the authors say LLMs should be "assistants," not the final judgment. — [IDEAS/RePEc record](https://ideas.repec.org/a/eee/finlet/v59y2024ics1544612323011583.html); [Alpha Architect summary](https://alphaarchitect.com/chatgpt/)
- A 2026 arXiv paper that tests ChatGPT, Gemini, DeepSeek and Perplexity stock predictions under several prompting strategies describes earlier work by the same authors as finding ChatGPT recommendations inconsistent and sensitive to prompting (snippet only). — [arXiv 2603.19944](https://arxiv.org/pdf/2603.19944v1)

**Benchmarks and agent studies**
- StockBench (Chen et al., arXiv 2510.02209, Oct 2025, revised Mar 2026) calls itself a "contamination-free" benchmark. Agents make daily buy/sell/hold decisions on large Dow Jones stocks using prices, fundamentals and news, over a recent multi-month window. Sources disagree on the window (Mar–Jun, Mar–Jul or May–Aug 2025) and on the number of stocks. Results:
  - Buy-and-hold returned about 0.4% with a −15.2% maximum drawdown.
  - Most agents beat buy-and-hold on return and risk, but **none consistently outperformed it**.
  - Agents failed to beat the passive baseline in a downturn (Jan–Apr 2025).
  - Trading costs, slippage and liquidity were not modelled.

  — [arXiv](https://arxiv.org/abs/2510.02209v1); [alphaXiv](https://alphaxiv.org/abs/2510.02209)
- FINSABER (Li, Kim, Cucuringu & Ma, arXiv 2505.07078, May 2025) is a backtesting framework with longer periods and a wider universe that tries to correct survivorship, look-ahead and data-snooping biases. Findings (via summaries):
  - Previously reported LLM advantages "deteriorate significantly" under the broader, longer evaluation.
  - LLM strategies were "overly conservative in bull markets" (underperforming passive benchmarks) and "overly aggressive in bear markets" (heavy losses).
  - Simpler risk-aware rule-based approaches did better across regimes.
  - The authors concede that pretrained LLMs may still carry look-ahead bias.

  — [arXiv](https://arxiv.org/html/2505.07078v3)
- AI-Trader (arXiv 2512.10971, Dec 2025) bills itself as the "first fully-automated, live, and data-uncontaminated" benchmark for LLM agents in finance. It tested six LLMs on US stocks, China A-shares and crypto. Findings:
  - "General intelligence does not automatically translate to effective trading capability."
  - Most agents showed poor returns and weak risk management.
  - Risk control determined robustness across markets.

  — [arXiv](https://arxiv.org/abs/2512.10971v1); [IDEAS](https://ideas.repec.org/p/arx/papers/2512.10971.html)
- LiveTradeBench (arXiv 2511.03628) ran 50-day **live** evaluations of 21 LLMs on US stocks and Polymarket prediction markets. I did not retrieve its results. — [arXiv](https://arxiv.org/html/2511.03628v1)
- InvestorBench (arXiv 2412.18174, Dec 2024) evaluated 13 LLM backbones in historical environments for single stocks, crypto and ETFs. Proprietary models generally beat open-source ones, and domain fine-tuning gave mixed results. Because it is a historical backtest, it is exposed to the lookahead problem in Section 2. — [arXiv](https://arxiv.org/abs/2412.18174); [project page](https://suchow.io/investorbench/)

**Live real-money competitions (press and secondary sources; anecdotal, roughly one run per model)**
- Alpha Arena Season 1 (nof1, ended about 3 Nov 2025; sources differ on the date) gave six LLMs $10,000 of real money each to trade crypto perpetuals on Hyperliquid, with identical data and no human intervention. Results:
  - Qwen3-Max won with +22.32% (equity $12,232).
  - Only two of the six models made a profit, both Chinese.
  - GPT-5 reportedly lost 62.7%.
  - nof1 warned that the short duration, modest capital and absence of statistical controls mean the results are not a definitive ranking. Its founder said, "It's not yet feasible to directly hand over money to an LLM and let it trade on its own."

  — [Forklog](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/); [KuCoin News](https://www.kucoin.com/news/flash/ai-trading-models-struggle-in-live-market-tests-majority-of-systems-report-losses)
- Alpha Arena Season 1.5 moved to US equities, running from about 19 Nov to early Dec 2025. Models included Qwen3, DeepSeek, Claude Sonnet, Gemini, Grok, GPT-5, Kimi and an undisclosed model. The undisclosed Grok 4.20 ("Grok 4.2") reportedly won; reported returns conflict, about 12.1% in one write-up and "10.12" in another headline. I found no accessible official per-model archive and could not confirm Claude's placing. — [Forklog](https://forklog.com/en/ai-model-grok-4-2-triumphs-in-trading-tournament/amp); [AIgazine](https://aigazine.com/markets/grok-420-takes-alpha-arena-season-15-with-1012-returns-in-live-stock-trading--a)

**Indian-market evidence**
- A *Journal of Data and Information Management* paper tests whether ChatGPT can forecast stock-price growth from Indian (bank) news headlines; its scale and out-of-sample design were not verified. — [dline.info](https://www.dline.info/ojs/index.php/jdim/article/view/316)
- A CHRIST University book chapter examines ChatGPT-4 for Indian stock analysis. It says the model "exhibits promise" despite limitations such as handling large datasets. — [IRMA/IGI chapter](https://www.irma-international.org/chapter/ai-chatbots-and-market-dynamics/380882/)
- "News-Driven Stock Price Forecasting in Indian Markets" (arXiv 2411.05788) uses VAE and diffusion deep-learning models, not an LLM acting as a judge. — [arXiv](https://arxiv.org/abs/2411.05788v1)

### Inferences
- No study tests the trader's architecture: rule-based book setups, then an LLM take/skip verdict with reasons, then a human decision. The nearest evidence covers LLM-as-signal (headline sentiment, ratings), which is positive but decaying, and LLM-as-autonomous-agent, which is mostly negative or fragile out of sample. The trader's own forward test will be the main evidence.
- The Lopez-Lira & Tang mechanism (news diffusing slowly into small, less-followed stocks at daily horizons) does not obviously transfer to intraday trading of a liquid 15–20 stock NSE watchlist.
- The regime finding (FINSABER's too-conservative-in-bull and too-aggressive-in-bear pattern, and StockBench's weakness in downturns) means a filter's measured value can depend on which regime the trial runs in. Results should be segmented by market regime (for example Nifty trend or volatility state).
- A more plausible source of value is consistent rule-compliance checking against the books (catching earnings days, gaps, circuit limits, news shocks or rule violations) rather than return forecasting. This is a hypothesis to test, not an established finding.
- Live competitions show that frontier models given discretion can lose large amounts quickly. The trader's human gate, 1R stops and paper trading every flag contain that risk.

### Gaps
- FinRL contest results (including tasks involving LLM-generated signals) were not researched.
- LiveTradeBench's results and any 2026 updates to StockBench or AI-Trader were not retrieved.
- I could not open the Lopez-Lira & Tang full text to confirm whether its sample sits after each model's training cutoff. My recollection, which is **unverified**, is that the original sample began in Oct 2021, after GPT-3.5's cutoff.
- Pelster & Val's exact sample size and whether GPT-4 had web access were not verified.
- No published trading evaluation of any Claude 5.x model was found.
- No rigorous, post-cutoff, out-of-sample study of LLMs on NSE stocks was found.

---

## 2. Lookahead bias and memorisation: why historical replay of LLM verdicts is invalid, and how to forward-test

### Takeaway
Pretrained LLMs leak post-period knowledge into "historical" analyses. Telling the model to ignore later information, or masking names and dates, does not reliably stop this. Opus, Sonnet and Haiku 5.5 all have a **June 2026 training-data cutoff**, so replaying their verdicts on NSE candles and news from before about July 2026 cannot validate the LLM layer. Valid evidence must come from a forward test that freezes inputs at flag time, or from a short post-cutoff replay with a pinned model snapshot and no web access.

### Cited Findings
- Glasserman & Lin (arXiv 2309.17322, Sep 2023) separate two biases:
  - look-ahead bias: the model knows what returns followed a news item;
  - a "distraction effect": general knowledge of the company interferes with judging sentiment.

  Using GPT-3.5 on original versus anonymised headlines, the anonymised headlines did better in-sample, so distraction mattered more than look-ahead. The effect was strongest for large companies, and the authors link it to a kind of overconfidence. They argue anonymisation is useful both for de-biased backtests and out of sample. — [arXiv](https://arxiv.org/abs/2309.17322); [Columbia poster](https://datascience.columbia.edu/wp-content/uploads/2024/01/P021_FB_PosterSession_Fall2023.pdf)
- Sarkar & Vafa, "Lookahead Bias in Pretrained Language Models" (2024; ICML 2025 workshop poster), build tests on events that are unpredictable from a prespecified information set, so a model that predicts them is leaking. They find lookahead in forecasting corporate risk factors from earnings calls and in predicting US House election winners from candidate biographies. **Prompting the model to ignore later information does not remove the bias.** — [NBER conference paper](https://conference.nber.org/conf_papers/f205530/f205530.pdf); [ICML 2025 poster](https://icml.cc/virtual/2025/48685); [CXO Advisory summary](https://www.cxoadvisory.com/investing-expertise/lookahead-bias-in-large-language-model-training-data)
- Lopez-Lira, Tang & Zhu, "The Memorization Problem: Can We Trust LLMs' Economic Forecasts?" (arXiv 2504.14765 / SSRN 5217505, Apr 2025, revised):
  - GPT-4o recalls S&P 500 levels, unemployment rates and quarterly GDP from before its Oct 2023 cutoff, and shows no recall after it.
  - With black-box access, forecasting skill and memorisation cannot be told apart inside the training window ("non-identification").
  - Instructions to ignore history did not stop the recall. Masking company names and dates did not help either, because the model reconstructed them from minimal clues. Memorisation also appears in embeddings.
  - Post-cutoff evaluation is the trustworthy test.
  - The authors propose converting identifiable text into anonymised "economic logic."

  — [arXiv v2](https://arxiv.org/html/2504.14765v2); [SSRN](https://papers.ssrn.com/abstract=5217505); [Quantpedia summary](https://quantpedia.com/the-memorization-problem-can-we-trust-llms-forecasts/)
- One proposed fix is point-in-time models. DatedGPT (2026) trains models on data with annual cutoffs to prevent lookahead bias. — [arXiv 2603.11838](https://arxiv.org/pdf/2603.11838); [alphaXiv](https://www.alphaxiv.org/abs/2603.11838.md)
- Official cutoffs: Claude Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 all list "Reliable knowledge cutoff: Jun 2026" and "Training data cutoff: Jun 2026". "Every Claude model ID is a pinned snapshot, including the dateless IDs." — [Anthropic models overview](https://platform.claude.com/docs/en/models/overview)

### Inferences
- **What historical replay can and cannot do.** Replaying Opus or Haiku 5.5 on 2020–mid-2026 NSE data mixes judgement with recall of what happened next (big moves, results surprises, index paths). Masking the ticker does not fix it. Such a replay can test plumbing (schema parsing, latency, citation checks), not the edge.
- The rule-based flag layer contains no LLM, so it can and should be backtested historically on its own.
- **Short post-cutoff replay.** Data from Jul–Oct 2026 (about 80 NSE sessions) is post-cutoff for the 5.5 snapshots, so it can be replayed with pinned IDs (`claude-opus-5-5`, `claude-haiku-5-5`) as long as:
  - there is no web search or fetch;
  - the news inputs are the time-stamped text available at the time, not articles edited later.

  This window is too short for strong conclusions and is useless for any future model whose cutoff is later.
- **Forward-test protocol:**
  - At each flag, assemble the exact payload (candles up to the flag bar, rule checks, news with timestamps, passage IDs) and hash and store it before calling the model.
  - Record the verdict before the outcome exists, and never re-ask once the outcome is known.
  - Let the paper engine compute outcomes mechanically from later candles with fixed stop and target rules.
  - Keep the model snapshot, effort level and prompt version fixed within an evaluation block. A change starts a new block.
- Frozen post-cutoff payloads stay valid test data for the *same* snapshot. They can later be re-run, for example to measure non-determinism, without leakage, because the model's training data predates them and it has no tools.
- **Disable web tools in verdict calls.** This is not about lookahead (the live future is not online yet). Web tools would bring in unlogged information and break auditability.
- **Optional anonymisation arm.** Glasserman & Lin's distraction effect suggests running the shadow model, or an occasional duplicate call, with the ticker and company name masked. Memorisation is not a concern live, but brand halo is.

### Gaps
- There is no evidence on how strongly Claude 5.5 models memorise NSE intraday price paths. It is likely weaker for 5-minute bars than for headline events, but that is unverified.
- I found no published Indian-market lookahead study.
- The 2026 point-in-time model papers (DatedGPT, Look-Ahead-Bench) were seen only as abstracts or snippets.

---

## 3. Other failure modes (non-determinism, overconfidence, anchoring on the presented setup, hallucinated citations) and prompt and output design for auditable verdicts

### Takeaway
Each failure mode is documented. Identical prompts can produce different outputs even at temperature 0, verbalised confidence is systematically overconfident, models shift toward a user's stated framing (more so for smaller models), and fabricated citations are common without grounding. Current Claude models cannot be made deterministic: sampling parameters are fixed at defaults, and on Opus 5.5 thinking is always on. Auditability must therefore come from pinned model IDs, a fixed effort level, versioned prompts, JSON schemas, full logging, measured run-to-run variance and probability scoring, not from "temperature 0".

### Cited Findings
**Non-determinism and sampling controls**
- On API version `2026-10-21`, a Messages request that sends `temperature`, `top_p` or `top_k` "returns a 400 error on every model - even at its default value." Claude 4.7 and later already accept only the default sampling values. — [Anthropic API migration guide 2026-10-21](https://platform.claude.com/docs/en/api/migration-2026-10-21) (read via Anthropic's bundled claude-api reference, cached Oct 2026; live page not fetched)
- Thinking and effort: Opus 5.5 thinking is "Adaptive (always on)" with default effort `medium`. Sonnet 5.5 is adaptive with default `high`; Haiku 5.5 is adaptive with default `medium`. — [Models overview](https://platform.claude.com/docs/en/models/overview)
- Claude Code exposes an `--effort` flag (`low`, `medium`, `high`, `xhigh`, `max`). In Claude Code, Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to `medium`. That differs from the API's `high` default for Sonnet 5.5, so effort should be set explicitly. — [CLI reference](https://code.claude.com/docs/en/cli-reference); [Claude Code model config](https://code.claude.com/docs/en/model-config)
- Temperature 0 is not deterministic. Thinking Machines Lab (Sep 2025) reported 1,000 runs of one prompt at T=0 on Qwen3-235B producing 80 distinct completions. The cause is batch-size-dependent numerics in inference kernels, the fix is batch-invariant kernels, and hosted APIs generally do not expose such controls (via secondary write-ups). — [Morph summary](https://www.morphllm.com/defeating-nondeterminism-llm-inference); [Spheron summary](https://www.spheron.network/blog/vllm-batch-invariance-why-temperature-0-isnt-deterministic/)
- A TMLR 2026 paper introduces "background temperature" to characterise the residual randomness at nominal T=0. — [Messina & Scotta, TMLR 2026](https://mlanthology.org/tmlr/2026/messina2026tmlr-introducing)

**Overconfidence and calibration**
- Xiong et al. (ICLR 2024): verbalised confidence "exhibits significant overconfidence" with poor failure prediction.
  - Calibration improves with scale but stays "far from ideal."
  - Consistency across sampled responses often beat verbalised confidence, and hybrid methods did best.
  - All methods struggled on professional-knowledge tasks.

  — [arXiv](https://arxiv.org/abs/2306.13063v2); [ICLR 2024 poster](https://iclr.cc/virtual/2024/poster/18135)
- Hager et al. (2025) argue that current LLMs' error rates are inconsistent with the confidence they communicate, and propose fine-tuning for calibrated verbal confidence. — [arXiv 2503.14749](https://arxiv.org/pdf/2503.14749v2)

**Anchoring and sycophancy toward the framing presented**
- UK AI Security Institute, "Ask Don't Tell" (Dubois et al., Feb 2026):
  - Sycophancy was substantially higher for statements than for questions.
  - Rewriting statements as questions reduced sycophancy more than an explicit "don't be sycophantic" instruction.
  - Stronger professed certainty and first-person framing ("I believe…") increased agreement.

  — [arXiv 2602.23971](https://arxiv.org/abs/2602.23971); [AISI blog](https://www.aisi.gov.uk/blog/ask-dont-tell-reducing-sycophancy-in-large-language-models-2)
- "Check My Work?" (Arvin, 2025): models switched answers to match options the user suggested, about 30% of the time for GPT-4.1-nano versus about 8% for GPT-4o. Smaller models were more susceptible. — [arXiv 2506.10297](https://arxiv.org/html/2506.10297v1)
- Li et al. (2025): simple opinion statements reliably induce sycophancy, which the authors trace to a late-layer shift in output preference. — [arXiv 2508.02087](https://arxiv.org/abs/2508.02087v1)

**Hallucinated citations**
- Walters & Wilder, *Scientific Reports* 13:14045 (2023), studied 636 citations across 84 generated literature reviews.
  - 55% of GPT-3.5 citations and 18% of GPT-4 citations were fabricated.
  - Of the real citations, 43% (GPT-3.5) and 24% (GPT-4) contained substantive errors.

  — [Nature/Sci Rep PDF](https://www.nature.com/articles/s41598-023-41032-5.pdf)
- A 2025 *JMIR Mental Health* study found 35 of 176 GPT-4o citations (19.9%) fabricated. — [JMIR 2025](https://mental.jmir.org/2025/1/e80371)
- Anthropic's own consumer terms say: "Outputs may not always be accurate and may contain material inaccuracies even if they appear accurate because of their level of detail or specificity," and "You should not rely on any Outputs or Actions without independently confirming their accuracy." — [Consumer Terms §4](https://www.anthropic.com/legal/consumer-terms)

**Tooling for structured, logged output**
- `claude -p --output-format json --json-schema '<schema>'` returns metadata (session ID, usage) with the schema-validated result in a `structured_output` field.
  - If a run ends without valid structured output (for example, Claude declined), the field is absent, so check for it.
  - An invalid schema makes `claude` exit with an error.
  - The `format` keyword is treated as an annotation and not enforced.

  — [Headless docs](https://code.claude.com/docs/en/headless); [CLI reference](https://code.claude.com/docs/en/cli-reference)
- JSON output includes `total_cost_usd` and a per-model cost breakdown. Both are client-side estimates that can differ from the bill. — [Headless docs](https://code.claude.com/docs/en/headless)
- Claude Code exits 0 on success and non-zero on failure. A failure inside the run, such as missing authentication, is printed as the result on stdout. — [Headless docs](https://code.claude.com/docs/en/headless)
- On the API, structured outputs (`output_config.format`) cannot be combined with Citations. Enabling citations together with `output_config.format` returns a 400. — [Citations docs](https://platform.claude.com/docs/en/build-with-claude/citations)

### Inferences
Suggested design rules, synthesised from the findings above:
1. **Version everything.**
   - Keep prompt templates and the JSON schema in git with a version number and a SHA-256 hash in every log row.
   - Pin full model IDs (`claude-opus-5-5`, `claude-haiku-5-5`), not aliases. Claude Code's `opus` and `haiku` aliases track the latest model, per the [model config page](https://code.claude.com/docs/en/model-config).
   - Set `--effort` explicitly (`low` or `medium`), and record the `claude --version` output.
2. **Treat non-determinism as a quantity to measure.**
   - Temperature cannot be set, so periodically re-run a random 10–20% of frozen flag payloads 3–5 times and report the take/skip flip rate.
   - Disagreement across runs is itself a confidence signal: Xiong et al. found consistency-based confidence better than verbal confidence.
   - A majority-of-3 live verdict is affordable on Haiku but triples Opus cost.
3. **Elicit probabilities, then score them.**
   - Ask for P(target hit before stop) or P(R > 0) as a number. Score with the Brier score and a reliability table, and do not trust the raw number until about 100 or more outcomes exist.
   - Never let a "high confidence" label change position size during the trial.
4. **De-anchor the prompt.**
   - Phrase the task as a question ("Should this flagged setup be taken or skipped?"), not as an assertion that it is an "A+ setup".
   - Require reasons to skip before reasons to take, and a rule-by-rule pass/fail with evidence taken from the candles.
   - Offer an explicit `abstain` / "insufficient information" verdict.
   - Give the setup's historical base rate from the rule backtest, so the model anchors on base rates rather than the narrative.
   - Expect the smaller Haiku shadow to be more suggestible, and track its take rate.
5. **Keep the model as verifier, not calculator.** Python computes indicators and rule checks (VWAP, opening range, relative volume, levels). The model receives those values plus raw candles (IST timestamps, compact CSV) and checks consistency and context.
6. **Proposed output schema.**
   - Fields: `verdict` (take / skip / abstain); `setup_id`; `rule_checks[]` (`rule_id`, `pass`, `evidence`); `reasons_against[]` (minimum length 1); `reasons_for[]`; `p_target_before_stop` (0–1); `key_risks[]`; `news_considered[]` (`news_id`, effect); `citations[]` (`passage_id`, verbatim `quote`); `data_issues[]`.
   - Use `additionalProperties: false`.
7. **Log everything, append-only (JSONL or SQLite).**
   - Inputs and versions: the full prompt text, payload hash, model ID, effort, prompt and schema versions, CLI version.
   - Raw output: stdout, parsed JSON, exit code, wall-clock latency, `total_cost_usd`.
   - Decision and outcome: the trader's decision and timestamp, the Haiku verdict, and outcome fields filled later by the paper engine.
8. **Fail safe.**
   - Set a hard timeout. A timeout, an error or a missing `structured_output` is logged as "no verdict" and never defaults to "take".
   - The trader decides on the rules alone when there is no verdict.
   - Each flag gets a fresh, independent call (no `--continue`), so earlier verdicts cannot anchor later ones.

### Gaps
- How many thinking tokens Opus 5.5 and Haiku 5.5 generate per verdict at `low` versus `medium` effort is unknown. This affects cost and latency, so it should be measured.
- I did not test whether `--json-schema` works with `--tools ""` and `--max-turns 1` (the schema mechanism may need an internal turn).
- No LLM-anchoring study specific to finance or trading was found; the evidence comes from general sycophancy research.

---

## 4. How to give the model book passages so its citations are checkable

### Takeaway
On the API, Anthropic's Citations feature returns the exact `cited_text` with machine-checkable locations, and the docs say citations are "guaranteed to contain valid pointers to the provided documents." It cannot be combined with JSON structured outputs. Through `claude -p` there is no documented Citations interface, so the reliable pattern is to give passages with IDs, require verbatim quotes tied to those IDs, and verify them locally by string matching, rejecting anything that fails.

### Cited Findings
- **Document types and chunking.** Citations work on plain-text, PDF and custom-content documents.
  - Plain text and PDFs are chunked into sentences.
  - Custom-content blocks "are used as-is and no further chunking is done."
  - Locations come back as character indices (plain text, 0-indexed), page numbers (PDF, 1-indexed) or content-block indices (custom content).

  — [Citations docs](https://platform.claude.com/docs/en/build-with-claude/citations)
- **Reliability and cost.** Because the API parses citations and extracts `cited_text` itself, "citations are guaranteed to contain valid pointers to the provided documents."
  - `cited_text` "does not count toward output tokens," and is not counted as input when passed back.
  - Enabling citations adds slightly to input tokens.
  - Citations work with prompt caching (cache the document blocks) and with batch processing.

  — [Citations docs](https://platform.claude.com/docs/en/build-with-claude/citations)
- **Limits.**
  - Citations and structured outputs are incompatible: `output_config.format` together with citation-enabled documents returns an error.
  - The docs add: "Check that each field has a value and at least one citation. The API doesn't guarantee either."
  - Scanned PDFs without extractable text are not citable.

  — [Citations docs](https://platform.claude.com/docs/en/build-with-claude/citations)
- Supported models include `claude-opus-5-5`, `claude-sonnet-5-5` and `claude-haiku-5-5`. — [Citations docs](https://platform.claude.com/docs/en/build-with-claude/citations)
- On API version `2026-10-21`, sending a `text` block with a non-empty `citations` array inside a `user` message returns a 400, so citation blocks should not be echoed back as user content. — [API migration guide 2026-10-21](https://platform.claude.com/docs/en/api/migration-2026-10-21) (via Anthropic's bundled claude-api reference)
- Without grounding, fabricated citations are common: 18% for GPT-4 in 2023, and 19.9% for GPT-4o in a 2025 study. — [Walters & Wilder](https://www.nature.com/articles/s41598-023-41032-5.pdf); [JMIR 2025](https://mental.jmir.org/2025/1/e80371)
- Models can reconstruct memorised content from minimal clues. — [Memorization Problem](https://arxiv.org/html/2504.14765v2)

### Inferences
- **Corpus design.**
  - For each coded setup, the trader hand-picks 3–8 short passages (about 100–300 words each) from Gujral & Vaidya and from Aziz: entry, stop, target, filters and "when not to take it".
  - Each passage gets a stable ID (for example `AZ-ORB-03`) with book, edition, chapter and page.
  - Eight passages of about 250 words is roughly 2,500–3,000 tokens per verdict.
  - A deterministic map from `setup_id` to passage IDs is the most auditable retrieval. An optional BM25 or embedding search over the same corpus can add context-specific passages (for example, gap days or news days); log the retrieved IDs.
- **API route (strongest checkability).**
  - Send passages as one custom-content document per setup (one content block per passage, with the ID in the text or title) and enable citations.
  - Because citations exclude JSON schemas, either:
    - (a) parse a fixed first line (`VERDICT: TAKE|SKIP|ABSTAIN; P=0.xx`) from the cited answer; or
    - (b) make a second cheap Haiku call that converts the cited answer into the JSON schema, keeping the original citations in the log.
- **`claude -p` route (Pro).**
  - Wrap passages as `<passage id="AZ-ORB-03" book="Aziz…" page="…">…</passage>`.
  - Instruct: "Cite only passage IDs provided; each citation must include a verbatim quote of 40 words or fewer from that passage; if no passage supports a reason, say so; never cite any book, page or passage not provided."
  - Python then checks `normalize(quote) in normalize(passages[id])` (whitespace and Unicode normalisation).
  - A failed check marks the verdict `citation_invalid`; the rate of these is a tracked quality metric.
- Popular trading books (Aziz's especially) may be partly memorised. Expect occasional plausible "quotes" that are not in the supplied text; local verification catches them.

### Gaps
- I found no documented way to use the API Citations feature (document blocks) through `claude -p`.
- I did not verify whether citations combine with strict tool use as an alternative way to get JSON.

---

## 5. How should a scoreboard judge "model picks vs all flags" with small samples, and is a cheaper "shadow" model useful?

### Takeaway
Because every flag is paper-traded, outcomes are seen for both taken and skipped flags. The core metric is E[R | model take] − E[R | model skip]: lift over "all flags" equals (1 − take rate) × that difference. With realistic per-trade R volatility, detecting a 0.5R difference needs roughly 60–110 flags per group, and a 0.25R difference roughly 250–420 per group. A 10R drawdown stop will often trigger before then, and API or subscription costs are a material fraction of 1R per month. A Haiku shadow is cheap and useful as a baseline and as an uncertainty flag, best compared on the flags where the two models disagree, using McNemar-style paired tests.

### Cited Findings
- Dietterich (1998, *Neural Computation* 10(7)): McNemar's test has low Type I error, and for algorithms that can be run only once on a single test set it is the only test of those reviewed with acceptable Type I error. Its main drawback is that it gives no measure of training-set or model variability. — [Dietterich 1998 PDF](https://web.engr.oregonstate.edu/~tgd/publications/dietterich-approximate-statistical-tests-nc1998.pdf)
- LLM strategy performance is regime-dependent: too conservative in bull markets and too aggressive in bear markets (FINSABER), and failing in downturns (StockBench). — [FINSABER](https://arxiv.org/html/2505.07078v3); [StockBench](https://alphaxiv.org/abs/2510.02209)
- Short live contests without statistical controls cannot rank models; nof1 said so explicitly. — [Forklog](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/)
- Consistency across samples is a better confidence signal than verbalised confidence. — [Xiong et al.](https://arxiv.org/abs/2306.13063v2)
- Smaller models defer more to suggested answers (about 30% versus 8% in one GPT study), which is relevant to a Haiku shadow's take rate. — [Arvin 2025](https://arxiv.org/html/2506.10297v1)
- LLM-news predictability decays as adoption grows, so expect non-stationarity. — [Lopez-Lira & Tang v6](https://arxiv.org/abs/2304.07619v6)

### Inferences
**Metrics, in priority order:**
1. **Primary:** ΔR = mean R of Opus-take flags − mean R of Opus-skip flags. Use disjoint groups; comparing picks against all flags double-counts the picks. Report net R after estimated costs.
2. **Supporting metrics:**
   - take rate and abstain rate;
   - win rate and profit factor per group;
   - per-setup and per-regime breakdowns;
   - Brier score and a reliability table for `p_target_before_stop`;
   - citation-validity rate, timeout and error rate, latency;
   - flip rate on re-runs.
3. **Uncertainty:**
   - Bootstrap confidence intervals, resampling *days* rather than flags, because flags on one day share market moves.
   - A within-day permutation test: shuffle take/skip labels across flags on the same day to build the null distribution of ΔR.
4. **Baselines:**
   - "take all";
   - random selection with the same take rate (Monte Carlo);
   - a simple rule-quality score threshold computed in Python;
   - the Haiku shadow;
   - the trader's own decisions. Ideally the trader logs a pre-verdict lean (take/skip) before seeing Opus, to separate human skill from model influence.

**Small-sample arithmetic** (standard normal approximations; two-sided α = 0.05, 80% power, n per group ≈ 15.7·σ²/δ²):

| Per-trade σ of R | δ = 0.25R | δ = 0.5R | δ = 1.0R |
|---|---|---|---|
| 1.0R | ~251 per group | ~63 | ~16 |
| 1.3R | ~424 per group | ~106 | ~27 |

- Win-rate precision: a 95% interval half-width at p ≈ 0.5 is about ±14 percentage points at n = 50, ±9.8 at n = 100 and ±6.9 at n = 200. Differences under about 10–15 points are noise at trial scale.
- **Paired model comparison (Opus vs Haiku on the same flags):**
  - Build the 2×2 agreement table and report the agreement rate and Cohen's kappa.
  - Use McNemar's test on the discordant flags for take-rate differences.
  - Value is decided on the **discordant flags** (Opus-take/Haiku-skip versus Haiku-take/Opus-skip). Compare their mean R with a paired bootstrap or sign test. If Haiku performs as well as Opus, the cheaper model wins.
- **Drawdown stop versus evidence.** For a zero-edge random walk, the expected maximum drawdown is about 1.25·σ·√N: about 10.6R after 50 trades and 15R after 100 trades at σ = 1.2R (standard Brownian-motion result, Magdon-Ismail et al. 2004; my calculation).
  - A 10R stop is therefore likely to end a no-edge trial within about 50 trades, before ΔR can be measured.
  - The trial should state which equity curve the 10R stop applies to (trader-taken trades or model-picks). It should keep paper-tracking *all* flags regardless, so filter evidence keeps accumulating after live risk stops.
- **Pre-registration.** Write down the hypotheses, the primary metric, the minimum sample (for example 150 flags or 3 months), the segmentation and the stopping rules before starting. If results will be checked repeatedly, use a sequential test (SPRT or always-valid intervals) rather than repeated fixed-sample p-values.
- **Count costs in R.** At an assumed ₹88/USD, ₹200 = 1R.
  - Opus via API at about 10 flags/day costs roughly ₹950–1,500 a month (about 4.8–7.6R). Pro at $20 is about ₹1,760 (about 8.8R) before any GST. See Section 6.
  - For the layer to pay its way, if about 100 trades a month are taken, ΔR-driven gains must exceed roughly 0.05–0.09R per taken trade.
- **Is the Haiku shadow useful?** Yes:
  - Cost: under $0.003 per verdict on the API.
  - Value: it is a cheap-model baseline, its disagreements with Opus mark uncertain flags, and it is a fallback.

  Caveats:
  - It needs the same sample sizes as Opus.
  - It may be more suggestible (watch whether its take rate is higher).
  - It must use the identical payload and prompt version.
  - It must run in parallel so it adds no latency.
  - Its verdict must stay hidden from the trader, as planned.

### Gaps
- No source gives the typical standard deviation of R for Aziz or Gujral-style intraday setups with fixed stops and targets; the 1.0–1.3R range is an assumption to replace with the trader's backtest.
- I found no published methodology specific to evaluating LLM trade filters.
- Indian intraday cost per trade in R (brokerage, STT, slippage) is outside this note's scope.

---

## 6. Is it feasible to get these verdicts through Claude Code headless mode (`claude -p`) on Claude Pro, and how does that compare with the Claude API on flags, latency, models, limits, terms, cost per verdict and verdicts per day?

### Takeaway
Technically yes: Opus 5.5 is the default model for Pro in Claude Code as of Oct 2026, and `claude -p` supports JSON-schema output, model and effort selection, and tool lockdown. But there are four problems:
- Pro limits are unpublished and shared with all other Claude use.
- The fast scripted `--bare` mode does not work with subscription login, and Anthropic says bare will become the default for `-p`.
- Pro is governed by the Consumer Terms, which **prohibit relying on the Services to buy or sell securities**. The API's Commercial Terms have no such clause, but the new Usage Policy (effective 12 Nov 2026) treats personalised buy/sell recommendations as "high-risk" and requires qualified human review.
- Per-call latency is not documented.

On the API, a verdict costs about $0.03–0.10 on Opus 5.5 and under $0.003 on Haiku 5.5, which is about ₹900–1,500 a month at roughly 10 flags/day, comparable to Pro's $20.

### Cited Findings
**CLI flags relevant to scripted verdicts** (all from the [CLI reference](https://code.claude.com/docs/en/cli-reference) unless noted)
- `-p/--print` runs non-interactively. `--output-format text|json|stream-json`. `--json-schema` gives "validated JSON output matching a JSON Schema" (print mode only). `--input-format text|stream-json`.
- `--model` takes an alias (`sonnet`, `opus`, `haiku`, `fable`) "or a model's full name." `--effort low|medium|high|xhigh|max`.
- `--system-prompt` / `--system-prompt-file` "Replace the entire system prompt"; `--append-system-prompt[-file]` appends to it.
- `--tools ""` disables all built-in tools; the flag does not affect MCP tools, so use `--disallowedTools "mcp__*"`. Also: `--strict-mcp-config`, `--disable-slash-commands`, `--setting-sources user,project,local`.
- `--max-turns` (print mode) limits agentic turns. `--max-budget-usd` (print mode) caps estimated spend using a client-side estimate. `--no-session-persistence` (print mode).
- `--fallback-model` switches on overload or unavailability only. "Authentication, billing, rate-limit, request-size, and transport errors … never trigger a switch." — [model config](https://code.claude.com/docs/en/model-config)
- **Bare mode** skips hooks, skills, plugins, MCP servers, auto memory and CLAUDE.md "so scripted calls start faster." It is "the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release." However, "In bare mode, Claude Code never reads OAuth credentials or the system keychain," and it needs `ANTHROPIC_API_KEY` or an `apiKeyHelper`, because "bare mode doesn't use your subscription login." — [Headless docs](https://code.claude.com/docs/en/headless)
- Without `--bare`, a `-p` session runs hooks from a project's `.claude/settings.json` and connects servers in its `.mcp.json`, "even in a folder you've never trusted," with no trust dialog. Piped stdin is capped at 10 MB. — [Headless docs](https://code.claude.com/docs/en/headless)
- `claude -p` is the Agent SDK's CLI form ("Use the Agent SDK to run Claude Code programmatically from the CLI"). Other languages can drive it as a subprocess with `-p --output-format json`. — [Headless docs](https://code.claude.com/docs/en/headless); [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)

**Models available on Pro in Claude Code (Oct 2026)**
- On the Anthropic API path, aliases resolve to `opus` → Opus 5.5, `sonnet` → Sonnet 5.5 and `haiku` → Haiku 5.5. The `default` model for "Pro, Max, Ultra, Team, Enterprise, and Anthropic API" is **Opus 5.5**. "Neither Fable model is the account-type default." — [Claude Code model config](https://code.claude.com/docs/en/model-config)
- The pricing page lists Pro as $20/month billed monthly, or $17/month on annual billing ($200 up front). It includes Claude Code and Opus ("Yes"), with "Fable, paid with usage credits," and "More usage than Free, every 5 hours and every week." Max is $100 for "5x Pro usage"; Ultra is $200 for "10x Pro usage every week" with "No 5-hour limit" for verified accounts. No INR pricing is shown. — [claude.com/pricing](https://claude.com/pricing)
- In `-p` mode, "When a Fable request there would bill to usage credits, Claude Code bills it without asking." — [model config](https://code.claude.com/docs/en/model-config)
- Third-party 2025–26 guides conflict: some say Pro was Sonnet-only in Claude Code. The official pages above supersede them. Old help-centre estimates (for example, "40–80 hours of Sonnet 4" a week on Pro) are outdated. — [Portkey guide](https://portkey.ai/blog/claude-code-limits); [Morph guide](https://www.morphllm.com/claude-code-pro)

**Usage limits**
- Pro and Max have "a five-hour session limit and a weekly limit." Claude and Claude Code share them. The current help article gives **no numeric** prompt or hour estimates.
- When Pro hits a limit, the options are to enable usage credits, switch to a Console account with API credits, upgrade to Max, or wait for the reset.
- A small "wrapping up" allowance lets an in-progress step finish.

  — [Help Center: Using Claude Code with Pro or Max](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- "Advertised usage limits for Pro, Max, and Ultra plans assume ordinary, individual usage of Claude Code and the Agent SDK." — [Claude Code legal & compliance](https://code.claude.com/docs/en/legal-and-compliance)

**Terms**
- Claude Code on Free, Pro, Max and Ultra is governed by the Consumer Terms; Team, Enterprise and API use by the Commercial Terms. — [Legal & compliance](https://code.claude.com/docs/en/legal-and-compliance)
- OAuth (subscription) authentication "is designed to support ordinary use of Claude Code and other native Anthropic applications." Developers building products should use API keys. This "does not … prevent an end user from signing in to the unmodified Claude Code binary with their own Claude subscription." Anthropic "may [enforce] without prior notice." — [Legal & compliance](https://code.claude.com/docs/en/legal-and-compliance)
- The Agent SDK overview says: "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK." — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- Consumer Terms (effective 8 Oct 2025), §3 prohibited uses. The lead-in is "You may not access or use … our Services in the following ways:".
  - Item 7: "Except when you are accessing our Services via an Anthropic API Key or where we otherwise explicitly permit it, to access the Services through automated or non-human means, whether through a bot, script, or otherwise."
  - Item 9: "To rely upon the Services, the Materials, or the Actions to buy or sell securities or to provide or receive advice about securities, commodities, derivatives, or other financial products or services," noting that Anthropic is not a registered broker-dealer or investment adviser.

  — [Consumer Terms](https://www.anthropic.com/legal/consumer-terms)
- The Commercial Terms (Jun 17, 2025) contain no securities or investment-advice restriction. They say "It is Customer's responsibility to evaluate whether Outputs are appropriate for Customer's use case," and that factual assertions should not be relied on without independent checking. — [Commercial Terms](https://www.anthropic.com/legal/commercial-terms)
- The Usage Policy shown today, with effective date **12 Nov 2026** (12 days from now), lists Finance as a "High-risk Area" covering "a personalized recommendation to buy, sell, hold, or allocate among specific investment products such as securities, funds, digital assets, or annuities."
  - Requirements: a "qualified person must meaningfully review a High-risk AI Recommendation" before it is used, that person remains responsible, and AI use must be disclosed.
  - "These requirements apply to anyone who uses our products to make a High-risk AI Recommendation."
  - A qualified person is "someone with the training or experience to evaluate the output in that field."
  - There is no explicit carve-out for individuals deciding for themselves.

  — [Usage Policy](https://www.anthropic.com/legal/aup)

**Latency (no official figures; community reports only)**
- Opus 5.5 is labelled "Moderate" latency and Haiku 5.5 "Fastest," relative to the current lineup. Actual latency depends on prompt length, output length and thinking effort. — [Models overview](https://platform.claude.com/docs/en/models/overview)
- The bare binary starts in about 0.1 s (median for `--version`). Initialisation of tools, MCP servers and skills dominates: one write-up reports about 75 s per call with everything loaded versus about 9 s with tools disabled. Default context overhead is estimated at about 16K tokens without MCP. Reported regressions include a constant ~405 s stall in v2.1.220/221 and indefinite startup hangs. I did not verify which page holds which figure. — [claudeissues #87652](https://claudeissues.com/issue/87652-bug-headless-first-stream-latency-regresses-between-2-1-197-and-2-1-200-on-linux); [claudeissues #83859](https://claudeissues.com/issue/83859-headless-claude-p-runs-stall-for-a-constant-405s-early-in-every-session-9-9-sinc); [claudeissues #75613](https://claudeissues.com/issue/75613-headless-claude-p-hangs-indefinitely-at-startup-no-transcript-no-output-suspecte); [community write-up](https://claude-cli-mastery.pages.dev/going-to-production/saas-patterns); [community skill notes](https://www.skills.lc/mcevoyinit/agentic-skills/mcevoyinit-agentic-skills-skills-productivity-claude-batch-ai-skill-md)

**API pricing (official, per million tokens)** — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing); [claude.com/pricing](https://claude.com/pricing)

| Model (API ID) | Input | 5-min cache write | 1-h cache write | Cache hit | Output | Batch in/out |
|---|---|---|---|---|---|---|
| Opus 5.5 (`claude-opus-5-5`) | $4 | $5 | $8 | $0.20 | $20 | $2 / $10 |
| Sonnet 5.5 (`claude-sonnet-5-5`) | $2 | $2.50 | $4 | $0.10 | $10 | $1 / $5 |
| Haiku 5.5 (`claude-haiku-5-5`), prompts ≤100K tokens | $0.10 | $0.125 | $0.20 | $0.01 | $0.50 | $0.05 / $0.25 |
| Haiku 5.5, prompts >100K tokens | $0.50 | $0.625 | $1 | $0.05 | $2.50 | $0.25 / $1.25 |
| Fable 5.1 (`claude-fable-5-1`) | $10 | $12.50 | $20 | $0.25 | $50 | $5 / $25 |

- The Batch API takes 50% off both input and output tokens and runs asynchronously. Caching "pays off after one cache read for the 5-minute duration … or after two cache reads for the 1-hour duration." `inference_geo: "us"` costs 1.1x. Fast mode on Opus 5.5 costs $8/$40. Models from 4.6 onward (except Haiku 5.5) get the 1M context window at standard pricing. — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Note: Anthropic's bundled API skill listed a $0.20 cache read for Sonnet 5.5, but the official pricing page fetched today says **$0.10**. Use the official figure.

### Inferences
**Per-verdict API cost** (standard rates, no caching; "2,000 out" means about 500 visible tokens plus about 1,500 thinking tokens; thinking is always on for Opus 5.5, and actual thinking length is unmeasured):

| Model | 5k in + 500 out | 15k in + 500 out | 15k in + 2,000 out |
|---|---|---|---|
| Opus 5.5 | $0.030 | $0.070 | $0.100 |
| Sonnet 5.5 | $0.015 | $0.035 | $0.050 |
| Haiku 5.5 | $0.00075 | $0.00175 | $0.0025 |
| Fable 5.1 (for reference) | $0.075 | $0.175 | $0.250 |

- **Caching.** If about 5k tokens (system prompt, setup rules, passages) form a stable prefix, an Opus cache hit costs $0.001 instead of $0.02, saving about $0.019 per verdict. A 1-hour cache write costs $0.04, so it pays after two hits within the hour. Flags are sparse, so the 1-hour TTL suits better than 5 minutes. Batch pricing does not suit live verdicts (asynchronous) but suits offline re-runs and evaluations.
- **Monthly API cost** for Opus plus a Haiku shadow over 21 sessions, at 10k input and 500–2,000 output tokens per verdict:

  | Flags per day | USD per month | INR per month (assumed ₹88/USD) |
  |---|---|---|
  | 5 | ≈ $5.4–8.6 | — |
  | 10 | ≈ $10.8–17.2 | ≈ ₹950–1,515 (≈ 4.8–7.6R) |
  | 20 | ≈ $21.6–34.4 | — |

  Pro is $20 (≈ ₹1,760, about 8.8R) or $17 a month on annual billing, plus any GST. If the trader already pays for Pro for other reasons, the marginal cost of the Pro route is zero.
- **Realistic verdicts per day.**
  - API: effectively unconstrained at this scale (tens per day). Cost is the binding factor; tier rate limits were not checked but are unlikely to bind below about 100 calls a day.
  - Pro: unknown, because the limits are unpublished and pooled with chat and coding use. A 5–15k-token verdict is small next to coding sessions, so tens per day *probably* fit, but this is **unverified**. Measure with `/usage` after a day of real flags.
  - The NSE session (6 h 15 m) spans at least two 5-hour windows, and the weekly cap can bite in weeks with heavy other use.
  - `--fallback-model` does not rescue usage-limit errors.
- **Recommended Pro invocation** (each flag is documented; the combination is untested). Run from an empty directory with no `CLAUDE.md`, `.mcp.json` or `.claude/` folder:
  `claude -p --model claude-opus-5-5 --effort low --system-prompt-file verdict_v1.txt --tools "" --disallowedTools "mcp__*" --strict-mcp-config --disable-slash-commands --no-session-persistence --max-turns 2 --output-format json --json-schema "$(cat verdict_schema_v1.json)" < payload.txt`
  - Run the identical command with `--model claude-haiku-5-5` in parallel for the shadow.
  - Treat a non-zero exit, a missing `structured_output` or a timeout as "no verdict".
  - Never use `--model fable` or `best` on Pro: in `-p` mode Fable silently bills usage credits.
- **Latency.** Expect several seconds to a few tens of seconds per Opus call: CLI initialisation, about 10k input tokens, adaptive thinking, and about 500 output tokens. Measure wall-clock time in Python. A 60–90 s timeout fits a 5-minute candle and longer fits a 15-minute candle. Haiku should return faster.
- **Forward risk.** If `--bare` becomes the default for `-p` as announced, and bare never reads subscription credentials, subscription-based `claude -p` scripts may break or need an opt-out flag. Plan for an API-key fallback.
- **Terms risk (not legal advice).**
  - Automation: `claude -p` is a documented feature of Anthropic's own unmodified binary, and Anthropic's limits language contemplates "individual usage of Claude Code and the Agent SDK." So scripted personal use looks within contemplated use, though item 7 is not explicitly waived for it.
  - Securities: item 9 is the more serious issue. Using Claude's take/skip verdicts to place real trades under a Pro plan plausibly falls within "rely upon the Services … to buy or sell securities." Paper trading plus a human decision softens this but does not clearly cure it.
  - API route: avoids the Consumer Terms clause, but from 12 Nov 2026 a per-stock take/skip verdict looks like "a personalized recommendation to buy, sell, hold." That brings in a qualified-person review requirement, and whether a self-directed retail trader qualifies is unclear.
  - Practical framing: treat verdicts as a logged research input reviewed by the trader, and prefer the API, under the Commercial Terms, for any live use. Flag this prominently in the report.
- **Overall comparison.** The API (Python `anthropic` SDK, pinned model IDs, explicit effort, structured outputs or Citations, per-call `usage`, no CLI start-up cost) is simpler to audit and costs about the same as Pro at 5–20 flags/day. `claude -p` with an API key and `--bare` is a middle path: same CLI, API billing, Commercial Terms.

### Gaps
- Numeric Pro limits (verdicts per 5-hour window or per week, and whether Opus draws the allowance faster than Sonnet or Haiku) are not published.
- There is no official latency figure for `claude -p` or the models.
- Thinking-token counts per verdict at `low` versus `medium` effort are unknown.
- API tier rate limits were not fetched.
- I did not verify whether a replaced system prompt still loads `~/.claude/CLAUDE.md` memory or user hooks in non-bare mode, or whether `--json-schema` works with `--tools ""` and `--max-turns 1`.
- How Claude Code behaves in `-p` mode when the Pro limit is hit (error versus prompt to use credits) was not verified.
- GST on Pro in India and INR pricing were not verified.
- The prior (currently effective) Usage Policy version was not retrieved.
- The legal interpretation of Consumer Terms item 9 and the high-risk rules for self-directed personal trading needs a lawyer or confirmation from Anthropic.

---

## 7. Copyright considerations of storing purchased book text locally for personal retrieval (brief)

### Takeaway
Indian law's fair-dealing exception for private or personal use, including research (s.52(1)(a)), likely covers keeping short, page-referenced excerpts from books the trader owns in a private local store for his own analysis. Circumventing e-book DRM may engage s.65A (anti-circumvention), where the interaction with fair dealing is legally unsettled. Sharing or publishing the corpus, for example in a public repository, would fall outside private use.

### Cited Findings
- Commentary describes s.52(1)(a) of the Copyright Act, 1957 as a fair-dealing provision covering "private or personal use, including research," criticism or review, and reporting current events. — [BananaIP](https://bananaip.com/?p=39294); [Maheshwari & Co.](https://www.maheshwariandco.com/blog/fair-use-doctrine/)
- s.65A makes circumventing an effective technological measure "with the intention of infringing" punishable by up to two years' imprisonment and a fine. s.65A(2) says nothing prevents acts "for a purpose not expressly prohibited by this Act." Commentators say courts have not definitively resolved the collision between s.65A and s.52, and some sources discuss 2010 Bill text rather than the consolidated statute. — [Bar & Bench](https://www.barandbench.com/columns/piracy-of-the-public-domain-a-right-without-a-remedy-in-indian-law); [BananaIP on TPMs](https://www.bananaip.com/intellepedia/?p=31448); [FSCI wiki](https://wiki.fsci.in/r/h9)
- The Consumer Terms prohibit using the Services "To infringe, misappropriate, or violate intellectual property or other legal rights." — [Consumer Terms](https://www.anthropic.com/legal/consumer-terms)

### Inferences
- Lower-risk practice:
  - store short excerpts (passages of a few hundred words), not whole books;
  - enter them from the physical copy or from the e-reader's own highlight or export features rather than by stripping DRM;
  - keep them out of any shared or public git remote (add the corpus folder to `.gitignore`);
  - prefer the trader's own paraphrased rule notes with page references, plus short verbatim quotes for citation checks.
- Sending excerpts to Anthropic transmits them to a third-party service. Minimal excerpts per call keep this proportionate. The trader should also check Claude's data-use and training settings for the account. Not legal advice.

### Gaps
- The consolidated current text of s.52(1)(a) and s.65A was not checked against India Code.
- The relevant e-book licence terms (Kindle or others) were not reviewed.
- I found no Indian case law on whether sending excerpts to a cloud LLM is still "private use".
- Anthropic's consumer data-training settings were not verified.
