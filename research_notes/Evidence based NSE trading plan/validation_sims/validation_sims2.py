#!/usr/bin/env python3
"""Second batch: costs in R, drawdown-stop definitions, SPRT under stop variants, haircuts. Stdlib only."""
import math, random, time
from statistics import NormalDist

ND = NormalDist()
PHI, PHI_INV = ND.cdf, ND.inv_cdf
Z95, Z80 = PHI_INV(0.95), PHI_INV(0.80)
T0 = time.time()


def hdr(s):
    print("\n" + "=" * 100 + f"\n{s}   [t={time.time()-T0:.0f}s]\n" + "=" * 100, flush=True)


def p_for(W, E):
    return (1.0 + E) / (W + 1.0)


def sd_bin(W, p):
    return math.sqrt(p * (1 - p)) * (W + 1.0)


# ------------------------------------------------------------ A. costs in R
hdr("A. ROUND-TRIP COST IN R (1R = Rs200). Rate card ASSUMED (Zerodha, as recalled; verify on zerodha.com/charges)")
GST = 0.18
SEBI = 10 / 1e7  # Rs10 per crore


def eq_intraday_cost(notional):
    brok = 2 * min(0.0003 * notional, 20.0)
    stt = 0.00025 * notional            # sell side
    txn = 0.0000297 * 2 * notional      # NSE both sides
    sebi = SEBI * 2 * notional
    stamp = 0.00003 * notional          # buy side
    gst = GST * (brok + txn + sebi)
    return brok + stt + txn + sebi + stamp + gst


def eq_delivery_cost(notional, dp=15.34):
    stt = 0.001 * 2 * notional
    txn = 0.0000297 * 2 * notional
    sebi = SEBI * 2 * notional
    stamp = 0.00015 * notional
    gst = GST * (txn + sebi)
    return stt + txn + sebi + stamp + gst + dp


def option_cost(premium_turnover_per_side):
    v = premium_turnover_per_side
    brok = 40.0
    stt = 0.001 * v                      # sell side premium
    txn = 0.0003503 * 2 * v
    sebi = SEBI * 2 * v
    stamp = 0.00003 * v
    gst = GST * (brok + txn + sebi)
    return brok + stt + txn + sebi + stamp + gst


print("Equity intraday (MIS): notional = Rs200 / stop%  | statutory+brokerage cost | + slippage 0.02%/side | + slippage 0.05%/side")
for stop in (0.003, 0.005, 0.0075, 0.01, 0.015, 0.02):
    N_ = 200 / stop
    c = eq_intraday_cost(N_)
    s2 = 2 * 0.0002 * N_
    s5 = 2 * 0.0005 * N_
    print(f"   stop {stop*100:.2f}% -> notional Rs{N_:,.0f} (lev {N_/20000:.1f}x on Rs20k): fees Rs{c:.1f} = {c/200:.3f}R | "
          f"+slip2bp {(c+s2)/200:.3f}R | +slip5bp {(c+s5)/200:.3f}R")
print("Equity delivery/swing (CNC): notional = Rs200 / stop% | fees incl. ~Rs15.34 DP charge | + slippage 0.05%/side")
for stop in (0.02, 0.03, 0.05, 0.08, 0.10):
    N_ = 200 / stop
    c = eq_delivery_cost(N_)
    s5 = 2 * 0.0005 * N_
    print(f"   stop {stop*100:.0f}% -> notional Rs{N_:,.0f}: fees Rs{c:.1f} = {c/200:.3f}R | +slip5bp {(c+s5)/200:.3f}R")
print("Index/stock options bought (flat Rs20/order): premium turnover per side")
for v in (2000, 5000, 7500, 10000, 20000):
    c = option_cost(v)
    print(f"   premium Rs{v:,} per side: fees Rs{c:.1f} = {c/200:.3f}R (brokerage alone 0.200R)")
print("General formula: cost_R = round_trip_cost_% / stop_distance_%  (e.g. 0.10% round trip / 0.5% stop = 0.2R)")

# ------------------------------------------------------------ B. stop definitions & risk size


def mc_dd(p, win, loss, n_trades, n_sims, dd_lims, seed):
    rr = random.Random(seed).random
    hit_peak = {d: 0 for d in dd_lims}
    hit_start = {d: 0 for d in dd_lims}
    for _ in range(n_sims):
        eq = peak = mdd = mn = 0.0
        for _t in range(n_trades):
            if rr() < p:
                eq += win
                if eq > peak:
                    peak = eq
            else:
                eq += loss
                if peak - eq > mdd:
                    mdd = peak - eq
                if eq < mn:
                    mn = eq
        for d in dd_lims:
            hit_peak[d] += mdd >= d - 1e-9
            hit_start[d] += mn <= -d + 1e-9
    return ({d: v / n_sims for d, v in hit_peak.items()}, {d: v / n_sims for d, v in hit_start.items()})


hdr("B. P(stop is tripped) by stop definition and size (Rs2,000 = 10R at Rs200 risk; = 20R at Rs100 risk; = 13.3R at Rs150)")
seed = 500
for W in (2.0, 1.2):
    for E in (0.0, 0.10, 0.20, 0.30):
        for n in (100, 200):
            seed += 1
            pk, stt = mc_dd(p_for(W, E), W, -1.0, n, 30000, (10, 13.33, 15, 20), seed)
            print(f"W={W} E={E:+.2f} n={n}: peak-to-trough DD>= 10R {pk[10]:.3f} 13.3R {pk[13.33]:.3f} 15R {pk[15]:.3f} 20R {pk[20]:.3f} | "
                  f"loss-from-start>= 10R {stt[10]:.3f} 13.3R {stt[13.33]:.3f} 15R {stt[15]:.3f} 20R {stt[20]:.3f}", flush=True)

# ------------------------------------------------------------ C. SPRT under stop variants


def sprt_sim(p, win, loss, sigma, d1, stop_mode, dd_lim, n_min=50, n_max=300, n_sims=20000, seed=11, alpha=0.05, beta=0.2):
    A = math.log((1 - beta) / alpha)
    B = math.log(beta / (1 - alpha))
    up, lo, slope = sigma * sigma / d1 * A, sigma * sigma / d1 * B, d1 / 2
    rr = random.Random(seed).random
    res = dict(h1=0, h0=0, dd=0, und=0)
    totn = 0
    for _ in range(n_sims):
        S = peak = 0.0
        n = 0
        while True:
            n += 1
            if rr() < p:
                S += win
                if S > peak:
                    peak = S
            else:
                S += loss
                if stop_mode == 'peak' and peak - S >= dd_lim - 1e-9:
                    res['dd'] += 1
                    break
                if stop_mode == 'start' and S <= -dd_lim + 1e-9:
                    res['dd'] += 1
                    break
            dr = slope * n
            if S <= lo + dr:
                res['h0'] += 1
                break
            if n >= n_min and S >= up + dr:
                res['h1'] += 1
                break
            if n >= n_max:
                res['und'] += 1
                break
        totn += n
    return {k: v / n_sims for k, v in res.items()}, totn / n_sims


hdr("C. SPRT H0 mu=0 vs H1 mu=+0.2R (alpha .05, beta .20, n_min 50, n_max 300) under different capital-stop rules")
for W in (2.0, 1.2):
    sig = sd_bin(W, p_for(W, 0.2))
    for mode, lim in (('none', 0), ('start', 10), ('peak', 10), ('peak', 20)):
        print(f"W={W} sigma={sig:.2f} stop={mode}{'' if mode == 'none' else f' {lim}R'}")
        for E in (0.0, 0.10, 0.20, 0.30):
            seed += 1
            r, asn = sprt_sim(p_for(W, E), W, -1.0, sig, 0.2, mode, lim, seed=seed)
            print(f"   E={E:+.2f}: PASS={r['h1']:.3f} FAIL={r['h0']:.3f} STOP={r['dd']:.3f} UNDECIDED={r['und']:.3f} avg n={asn:.0f}", flush=True)

# ------------------------------------------------------------ D. Haircuts (Harvey-Liu style, Bonferroni/Holm-type)
hdr("D. Harvey-Liu style haircut of an observed mean R for K tested variants (Bonferroni p-adjust), and BH/Holm thresholds")
for T, mean, sd in ((400, 0.20, 1.45), (400, 0.15, 1.45), (1000, 0.10, 1.25), (200, 0.25, 1.25)):
    t = mean * math.sqrt(T) / sd
    p = 1 - PHI(t)
    row = []
    for K in (1, 5, 10, 20, 50, 100):
        padj = min(1.0, K * p)
        z = PHI_INV(1 - padj) if padj < 1 else 0.0
        hm = max(0.0, z) * sd / math.sqrt(T)
        row.append(f"K={K}: p_adj={padj:.4f} haircut mean={hm:.3f}R ({(1 - hm / mean) * 100:.0f}% cut)")
    print(f"T={T} obs mean={mean}R SD={sd} t={t:.2f} p={p:.4f} :: " + " | ".join(row))
print("Holm step-down: sort p ascending; reject p_(i) while p_(i) <= alpha/(K-i+1). BH (FDR q): largest i with p_(i) <= i*q/K; reject 1..i.")

# ------------------------------------------------------------ E. Day-clustering design effect
hdr("E. Effective sample size when flags cluster on the same day (design effect 1+(m-1)*rho)")
for m in (1, 2, 3, 5):
    for rho in (0.0, 0.1, 0.2, 0.3):
        deff = 1 + (m - 1) * rho
        print(f"   avg flags/day m={m} intra-day correlation rho={rho}: design effect={deff:.2f} -> 100 trades worth {100/deff:.0f} independent trades")

print(f"\nDONE in {time.time()-T0:.0f}s")
