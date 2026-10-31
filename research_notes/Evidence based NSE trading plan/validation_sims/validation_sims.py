#!/usr/bin/env python3
"""
Validation-methodology simulations for a small NSE retail trader (1R = Rs200, stop at 10R drawdown).
Standard library only. Seeded for reproducibility.
"""
import math, random, time
from statistics import NormalDist

ND = NormalDist()
PHI, PHI_INV, PDF = ND.cdf, ND.inv_cdf, ND.pdf
GAMMA = 0.5772156649015329
Z95, Z80 = PHI_INV(0.95), PHI_INV(0.80)
T0 = time.time()


def hdr(s):
    print("\n" + "=" * 100 + f"\n{s}   [t={time.time()-T0:.0f}s]\n" + "=" * 100, flush=True)


def ceil(x):
    return int(math.ceil(x))


def n_fixed(delta, sigma, alpha=0.05, power=0.80, sides=1, guenther=True):
    za = PHI_INV(1 - alpha / sides)
    zb = PHI_INV(power)
    n = ((za + zb) * sigma / delta) ** 2
    return n + (za * za / 2 if guenther else 0.0)


def p_for(W, E):
    return (1.0 + E) / (W + 1.0)


def sd_bin(W, p):
    return math.sqrt(p * (1 - p)) * (W + 1.0)


def skew_bin(p):
    return (1 - 2 * p) / math.sqrt(p * (1 - p))


def kurt_bin(p):  # non-excess kurtosis
    return (1 - 6 * p * (1 - p)) / (p * (1 - p)) + 3.0


def pct(xs, q):
    ys = sorted(xs)
    k = (len(ys) - 1) * q
    f = int(math.floor(k))
    c = min(f + 1, len(ys) - 1)
    return ys[f] + (ys[c] - ys[f]) * (k - f)


# ---------------------------------------------------------------- 1
hdr("1. TRADES NEEDED to show mean R > 0 (one-sample z test + Guenther t-correction za^2/2)")
EDGES = (0.05, 0.10, 0.20, 0.30)
for label, alpha, power, sides in (
    ("alpha=0.05 one-sided, power=80%", 0.05, 0.80, 1),
    ("alpha=0.05 two-sided, power=80%", 0.05, 0.80, 2),
    ("alpha=0.05 one-sided, power=90%", 0.05, 0.90, 1),
    ("alpha=0.005 one-sided (Bonferroni for 10 variants), power=80%", 0.005, 0.80, 1),
    ("t>=3.0 (HLZ) i.e. alpha=0.00135 one-sided, power=80%", 0.00135, 0.80, 1),
):
    print(f"-- {label}")
    for sigma in (1.0, 1.25, 1.5):
        print(f"   SD={sigma:4.2f}R: " + "  ".join(
            f"{d:+.2f}R -> {ceil(n_fixed(d, sigma, alpha, power, sides)):6d}" for d in EDGES))
print("Binary-payoff SDs (SD = sqrt(p(1-p))*(W+1)):")
for W in (1.0, 1.2, 2.0, 3.0):
    print(f"   W={W}: " + "  ".join(
        f"E={E:+.2f}: p={p_for(W, E):.3f} SD={sd_bin(W, p_for(W, E)):.3f}" for E in (0.0, 0.1, 0.2, 0.3)))

# ---------------------------------------------------------------- 2
hdr("2. WHAT n TRADES CAN SHOW (analytic, normal approx)")
for n in (50, 100, 200, 300, 500):
    for sigma in (1.0, 1.25, 1.5):
        se = sigma / math.sqrt(n)
        crit = Z95 * se
        mde = (Z95 + Z80) * se
        pw = [1 - PHI(Z95 - d / se) for d in EDGES]
        pneg = [PHI(-d / se) for d in EDGES]
        print(f"n={n:3d} SD={sigma:4.2f}: SE={se:.3f} 95%CI=+/-{1.96*se:.3f} sig.threshold(mean)={crit:.3f} MDE80={mde:.3f} | power "
              + " ".join(f"{d:+.2f}:{x:.2f}" for d, x in zip(EDGES, pw)) + " | P(obs mean<0) "
              + " ".join(f"{d:+.2f}:{x:.2f}" for d, x in zip(EDGES, pneg)))


# ---------------------------------------------------------------- 3
def mc(p, win, loss, n_trades, n_sims, cps, dd_lim=10.0, seed=1):
    rr = random.Random(seed).random
    st = {cp: dict(dd=0, ruin=0, pos=0, pas=0, pas_start=0, mdd=[], stk=[]) for cp in cps}
    eps = 1e-9
    for _ in range(n_sims):
        eq = peak = mdd = mn = 0.0
        streak = maxstreak = 0
        ci = 0
        nxt = cps[0]
        for t in range(1, n_trades + 1):
            if rr() < p:
                eq += win
                streak = 0
                if eq > peak:
                    peak = eq
            else:
                eq += loss
                streak += 1
                if streak > maxstreak:
                    maxstreak = streak
                if peak - eq > mdd:
                    mdd = peak - eq
                if eq < mn:
                    mn = eq
            if t == nxt:
                s = st[nxt]
                hit = mdd >= dd_lim - eps
                ruin = mn <= -dd_lim + eps
                s['dd'] += hit
                s['ruin'] += ruin
                if eq > eps:
                    s['pos'] += 1
                    if not hit:
                        s['pas'] += 1
                    if not ruin:
                        s['pas_start'] += 1
                s['mdd'].append(mdd)
                s['stk'].append(maxstreak)
                ci += 1
                nxt = cps[ci] if ci < len(cps) else -1
    for cp in cps:
        s = st[cp]
        for k in ('dd', 'ruin', 'pos', 'pas', 'pas_start'):
            s[k] /= n_sims
    return st


hdr("3. MONTE CARLO: 10R drawdown & current pass-mark (binary payoffs; costs folded into net payoff); 40k paths")
NS = 40000
PAYOFFS = (("A (~33-40% winners @ +2R)", 2.0), ("B (~45-55% winners @ +1.2R)", 1.2), ("C (~25-33% winners @ +3R)", 3.0))
NET = (-0.10, 0.0, 0.05, 0.10, 0.20, 0.30)
RES3 = {}
seed = 100
for name, W in PAYOFFS:
    print(f"\n--- Payoff {name}: win +{W}R, loss -1R ---")
    for E in NET:
        p = p_for(W, E)
        seed += 1
        st = mc(p, W, -1.0, 500, NS, (100, 200, 500), seed=seed)
        RES3[(W, E)] = st
        a, b, c = st[100], st[200], st[500]
        print(f"E={E:+.2f} p={p:.3f} SD={sd_bin(W, p):.2f} | N=100: P(peakDD>=10R)={a['dd']:.3f} P(down 10R from start)={a['ruin']:.3f} "
              f"P(final>0)={a['pos']:.3f} PASS(final>0 & DD<10R)={a['pas']:.3f} PASS(start-based stop)={a['pas_start']:.3f} "
              f"medDD={pct(a['mdd'], .5):.1f} p90DD={pct(a['mdd'], .9):.1f} medMaxLossStreak={pct(a['stk'], .5):.0f} p90Streak={pct(a['stk'], .9):.0f} "
              f"| N=200: P(DD>=10R)={b['dd']:.3f} startRuin={b['ruin']:.3f} P(final>0)={b['pos']:.3f} PASS={b['pas']:.3f} medDD={pct(b['mdd'], .5):.1f} p90DD={pct(b['mdd'], .9):.1f} "
              f"| N=500: P(DD>=10R)={c['dd']:.3f} startRuin={c['ruin']:.3f} medDD={pct(c['mdd'], .5):.1f}", flush=True)

# ---------------------------------------------------------------- 4
hdr("4. ZERO GROSS EDGE + COSTS (every trade shifted by -c): chance of 'profitable after costs' over 100 trades")
PASS_COST = {}
for name, W in PAYOFFS:
    p0 = 1.0 / (W + 1.0)
    sd0 = sd_bin(W, p0)
    for c in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25):
        seed += 1
        st = mc(p0, W - c, -1.0 - c, 100, NS, (100,), seed=seed)[100]
        approx = PHI(-c * 10 / sd0)
        print(f"W={W} cost={c:.2f}R/trade: P(final>0)={st['pos']:.3f} (normal approx {approx:.3f}) "
              f"PASS(final>0 & peakDD<10R)={st['pas']:.3f} P(peakDD>=10R)={st['dd']:.3f} P(down10R from start)={st['ruin']:.3f}", flush=True)
        PASS_COST[(W, c)] = st['pas']

# ---------------------------------------------------------------- 5
hdr("5. MULTIPLE TESTING")


def emax_numeric(K, h=0.002):
    if K == 1:
        return 0.0
    s, x = 0.0, -9.0
    while x < 9.0:
        s += x * K * PDF(x) * PHI(x) ** (K - 1)
        x += h
    return s * h


def emax_approx(K):
    if K <= 1:
        return 0.0
    return (1 - GAMMA) * PHI_INV(1 - 1.0 / K) + GAMMA * PHI_INV(1 - 1.0 / (K * math.e))


EMAX = [0.0, 0.0] + [emax_numeric(k) for k in range(2, 201)]


def emax(K):
    return EMAX[K] if K <= 200 else emax_approx(K)


print("K | E[max of K N(0,1)] numeric, BLdP approx | Bonferroni z(0.05/K) | luck: best-of-K zero-edge mean R (SD1.25) at n=100/300/1000 "
      "| n for 80% power at 0.05/K for +0.1/+0.2/+0.3R (SD1.25) | P(>=1 of K indep zero-edge setups passes current rule): net-zero A, zero-gross+0.1R cost A, zero-gross+0.1R cost B")
for K in (1, 2, 3, 5, 10, 20, 50, 100, 200, 1000):
    em = emax(K)
    ea = emax_approx(K)
    zb = PHI_INV(1 - 0.05 / K)
    luck = [em * 1.25 / math.sqrt(n) for n in (100, 300, 1000)]
    nn = [ceil(n_fixed(d, 1.25, 0.05 / K, 0.8, 1)) for d in (0.1, 0.2, 0.3)]
    pa = RES3[(2.0, 0.0)][100]['pas']
    pk = [1 - (1 - pa) ** K, 1 - (1 - PASS_COST[(2.0, 0.10)]) ** K, 1 - (1 - PASS_COST[(1.2, 0.10)]) ** K]
    print(f"K={K:5d}: Emax={em:.3f}/{ea:.3f}  zBonf={zb:.3f}  luck={luck[0]:.3f}/{luck[1]:.3f}/{luck[2]:.3f}R  n80={nn}  P(any passes)={pk[0]:.3f}/{pk[1]:.3f}/{pk[2]:.3f}")

print("\nNumber of independent variants K at which the BEST zero-edge variant is EXPECTED to show mean >= m (SD 1.25R), by trades per variant T:")
for T in (100, 200, 300, 500, 1000, 2000, 5000):
    row = []
    for m in (0.05, 0.10, 0.15, 0.20):
        target = m * math.sqrt(T) / 1.25
        K = 2
        while emax(K) < target and K < 10 ** 9:
            K = K + 1 if K < 200 else int(K * 1.02) + 1
        row.append(K)
    print(f"   T={T:5d}: m=+0.05R -> K={row[0]}, m=+0.10R -> K={row[1]}, m=+0.15R -> K={row[2]}, m=+0.20R -> K={row[3]}")

# ---------------------------------------------------------------- 6
hdr("6. PSR / DSR / MinTRL examples (per-trade Sharpe SR = mean R / SD R), payoff A; DSR uses V[SR]=1/T null proxy")
W = 2.0
for E in (0.10, 0.15, 0.20, 0.30):
    p = p_for(W, E)
    sd = sd_bin(W, p)
    sr = E / sd
    sk = skew_bin(p)
    ku = kurt_bin(p)
    denom = math.sqrt(1 - sk * sr + (ku - 1) / 4 * sr * sr)
    mtrl = 1 + (1 - sk * sr + (ku - 1) / 4 * sr * sr) * (Z95 / sr) ** 2
    print(f"Payoff A observed E={E:+.2f}: SR/trade={sr:.3f} skew={sk:.2f} kurt={ku:.2f} MinTRL(95%, SR*=0)={mtrl:.0f} trades")
    for T in (100, 200, 400, 1000):
        ps = PHI(sr * math.sqrt(T - 1) / denom)
        dsr = []
        for N in (1, 5, 10, 20, 50, 100):
            sr0 = 0.0 if N == 1 else math.sqrt(1.0 / T) * emax_approx(N)
            dsr.append(PHI((sr - sr0) * math.sqrt(T - 1) / denom))
        print(f"   T={T}: PSR(0)={ps:.3f}  DSR for N trials 1/5/10/20/50/100 = " + " ".join(f"{x:.3f}" for x in dsr))


# ---------------------------------------------------------------- 7
hdr("7. PEEKING: naive repeated one-sided t-test (t>=1.645) under ZERO net edge (false-positive rate)")


def peek(W, n_min, n_max, every, n_sims=20000, seed=9):
    p = 1 / (W + 1)
    rr = random.Random(seed).random
    hits = 0
    for _ in range(n_sims):
        n = 0
        mean = 0.0
        m2 = 0.0
        for t in range(1, n_max + 1):
            x = W if rr() < p else -1.0
            n += 1
            d = x - mean
            mean += d / n
            m2 += d * (x - mean)
            if t >= n_min and (t - n_min) % every == 0:
                sd = math.sqrt(m2 / (n - 1))
                if sd > 0 and mean / (sd / math.sqrt(n)) >= Z95:
                    hits += 1
                    break
    return hits / n_sims


for W in (2.0, 1.2):
    print(f"W={W}: one look at n=100: {peek(W, 100, 100, 1):.3f} | look every 25 trades (25..300): {peek(W, 25, 300, 25):.3f} | "
          f"every trade 30..100: {peek(W, 30, 100, 1):.3f} | every trade 20..300: {peek(W, 20, 300, 1):.3f}", flush=True)


# ---------------------------------------------------------------- 8
hdr("8. SPRT (Wald) on per-trade net R: H0 mu=0 vs H1 mu=d1; alpha=0.05, beta=0.20; min n=50, max n=300; 10R peak DD stop")


def sprt_bounds(sigma, d1, alpha=0.05, beta=0.20):
    A = math.log((1 - beta) / alpha)
    B = math.log(beta / (1 - alpha))
    return sigma * sigma / d1 * A, sigma * sigma / d1 * B, d1 / 2


def sprt_sim(p, win, loss, sigma, d1, n_min=50, n_max=300, dd_lim=10.0, n_sims=20000, seed=11):
    up, lo, slope = sprt_bounds(sigma, d1)
    rr = random.Random(seed).random
    res = dict(h1=0, h0=0, dd=0, und=0)
    totn = 0
    for _ in range(n_sims):
        S = 0.0
        peak = 0.0
        n = 0
        while True:
            n += 1
            if rr() < p:
                S += win
                if S > peak:
                    peak = S
            else:
                S += loss
                if peak - S >= dd_lim - 1e-9:
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


A_ = math.log(0.8 / 0.05)
B_ = math.log(0.2 / 0.95)
for name, W in PAYOFFS[:2]:
    for d1 in (0.15, 0.20):
        sig = sd_bin(W, p_for(W, d1))
        up, lo, sl = sprt_bounds(sig, d1)
        k1 = d1 * d1 / (2 * sig * sig)
        print(f"\nPayoff {name}, d1={d1}, sigma={sig:.3f}: PASS when cumR >= {up:.2f} + {sl:.3f}*n (n>=50); FAIL when cumR <= {lo:.2f} + {sl:.3f}*n; "
              f"Wald ASN (untruncated) H1={(0.8*A_+0.2*B_)/k1:.0f}, H0={(0.05*A_+0.95*B_)/(-k1):.0f}; fixed-n equivalent={ceil(n_fixed(d1, sig))}")
        for E in (-0.10, 0.0, 0.05, 0.10, 0.15, 0.20, 0.30):
            seed += 1
            r, asn = sprt_sim(p_for(W, E), W, -1.0, sig, d1, seed=seed)
            print(f"   true E={E:+.2f}: PASS={r['h1']:.3f} FAIL(H0)={r['h0']:.3f} DDstop={r['dd']:.3f} undecided@300={r['und']:.3f} avg trades={asn:.0f}", flush=True)

# ---------------------------------------------------------------- 9
hdr("9. BAYESIAN posterior P(edge>0) with prior N(m0, tau^2) == adding n0 = sigma^2/tau^2 phantom trades at m0")
sigma = 1.25
for tau in (None, 0.2, 0.15, 0.1):
    n0 = 0.0 if tau is None else sigma * sigma / tau / tau
    print("-- prior: " + ("flat" if tau is None else f"N(0,{tau}^2) -> n0={n0:.0f} phantom zero-R trades") + f"  (SD {sigma}R)")
    for n in (50, 100, 200, 300, 500):
        row = [PHI(xbar * n / (sigma * math.sqrt(n + n0))) for xbar in (0.1, 0.2, 0.3)]
        print(f"   n={n}: observed mean +0.1/+0.2/+0.3R -> P(mu>0|data)= " + " ".join(f"{x:.3f}" for x in row))


def bayes_seq(p, win, loss, sigma, n0, m0=0.0, pass_p=0.95, fail_p=0.10, n_min=50, n_max=300, dd_lim=10.0, n_sims=20000, seed=13):
    rr = random.Random(seed).random
    zp = PHI_INV(pass_p)
    zf = PHI_INV(fail_p)
    res = dict(pas=0, fail=0, dd=0, und=0)
    totn = 0
    for _ in range(n_sims):
        S = 0.0
        peak = 0.0
        n = 0
        while True:
            n += 1
            if rr() < p:
                S += win
                if S > peak:
                    peak = S
            else:
                S += loss
                if peak - S >= dd_lim - 1e-9:
                    res['dd'] += 1
                    break
            if n >= n_min:
                z = (n0 * m0 + S) / (sigma * math.sqrt(n0 + n))
                if z >= zp:
                    res['pas'] += 1
                    break
                if z <= zf:
                    res['fail'] += 1
                    break
            if n >= n_max:
                res['und'] += 1
                break
        totn += n
    return {k: v / n_sims for k, v in res.items()}, totn / n_sims


print("\nSequential Bayesian rule: check after every trade from n=50; PASS if P(mu>0)>=0.95, FAIL if <=0.10, 10R DD stop, max 300 trades")
for name, W in PAYOFFS[:2]:
    sig = sd_bin(W, p_for(W, 0.2))
    for tau in (None, 0.15, 0.10):
        n0 = 0.0 if tau is None else sig * sig / tau / tau
        print(f"Payoff {name} sigma={sig:.2f} prior={'flat' if tau is None else f'N(0,{tau}^2), n0={n0:.0f}'}")
        for E in (-0.10, 0.0, 0.10, 0.20, 0.30):
            seed += 1
            r, asn = bayes_seq(p_for(W, E), W, -1.0, sig, n0, seed=seed)
            print(f"   true E={E:+.2f}: PASS={r['pas']:.3f} FAIL={r['fail']:.3f} DDstop={r['dd']:.3f} undecided@300={r['und']:.3f} avg trades={asn:.0f}", flush=True)

# ---------------------------------------------------------------- 10
hdr("10. FILTER COMPARISONS (taken vs skipped; model vs trader) - analytic")
sigma = 1.25
print("Total flags so that 'taken minus skipped' difference D is detected (one-sided 0.05, 80% power), SD 1.25R; uplift vs ALL flags = (1-f)*D")
for f in (0.2, 0.3, 0.5, 0.7):
    print(f"   take-rate f={f}: " + "  ".join(
        f"D={D:.1f}R -> {ceil((Z95 + Z80) ** 2 * sigma ** 2 * (1 / f + 1 / (1 - f)) / D ** 2)}" for D in (0.1, 0.2, 0.3, 0.5)))
print("Paired model-vs-trader: discordant flags needed for mean advantage dd per discordant flag (SD 1.25R)")
for dd in (0.1, 0.2, 0.3, 0.5):
    nd = ceil(n_fixed(dd, sigma))
    print(f"   dd={dd}: {nd} discordant flags -> total flags if they disagree on 20%/40% of flags: {ceil(nd / 0.2)} / {ceil(nd / 0.4)}")
print("Precision of a scoreboard line with n trades (SD 1.25R):")
for n in (100, 60, 50, 30, 20):
    print(f"   n={n}: SE={sigma / math.sqrt(n):.3f}R, 95% CI half-width={1.96 * sigma / math.sqrt(n):.2f}R")

# ---------------------------------------------------------------- 11
hdr("11. Closed form: P(cum R hits -D within n) for Brownian motion with drift (with/without 0.5826*sigma discreteness correction) vs MC")


def fp(mu, sigma, D, n, corr=True):
    if corr:
        D = D + 0.5826 * sigma
    s = sigma * math.sqrt(n)
    if abs(mu) < 1e-12:
        return 2 * PHI(-D / s)
    return PHI((-D - mu * n) / s) + math.exp(-2 * mu * D / sigma ** 2) * PHI((-D + mu * n) / s)


for name, W in PAYOFFS:
    for E in (0.0, 0.10, 0.20):
        sig = sd_bin(W, p_for(W, E))
        for n in (100, 200, 500):
            print(f"W={W} E={E:+.2f} n={n}: closed form raw={fp(E, sig, 10, n, False):.3f} corrected={fp(E, sig, 10, n, True):.3f} MC={RES3[(W, E)][n]['ruin']:.3f}"
                  + (f" | infinite-horizon exp(-2*mu*D'/s^2)={math.exp(-2 * E * (10 + 0.5826 * sig) / sig ** 2):.3f}" if E > 0 and n == 500 else ""))

print(f"\nDONE in {time.time() - T0:.0f}s")
