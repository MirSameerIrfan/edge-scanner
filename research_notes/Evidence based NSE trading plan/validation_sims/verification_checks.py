#!/usr/bin/env python3
"""Inline checks cited in validation_methodology.md: MinBTL (Bailey et al. 2014), K_max heuristic, SPRT lines, infinite-horizon ruin."""
import math
from statistics import NormalDist
N=NormalDist(); g=0.5772156649015329
def emax(K): return (1-g)*N.inv_cdf(1-1/K)+g*N.inv_cdf(1-1/(K*math.e))
for K in (10,20,45,100,1000):
    print(f"MinBTL (years) for E[maxSR]=1 annual, N={K}: {emax(K)**2:.2f}   (2lnN upper bound: {2*math.log(K):.2f})")
print("K_max ~ exp(T*d^2/(8*s^2)) keeps expected best-of-K luck <= d/2 (s=1.25R):")
for T in (300,500,750,1000,1500,2000):
    for d in (0.1,0.2):
        km=math.exp(T*d*d/(8*1.25**2)); K=max(2,int(km))
        print(f"  T={T} d={d}: Kmax~{km:.1f}; check luck at K={K}: {emax(K)*1.25/math.sqrt(T):.3f}R vs d/2={d/2}")
d=0.2; A=math.log(16); B=math.log(0.2/0.95)
for s in (1.0,1.1,1.25,1.47):
    up=s*s/d*A; lo=s*s/d*B
    print(f"SPRT sigma={s}: PASS cumR>={up:.2f}+0.1n (Rs{up*200:,.0f}+Rs20n); FAIL cumR<={lo:.2f}+0.1n (Rs{lo*200:,.0f}+Rs20n); at n=100/200/300 pass mean>={(up+10)/100:.3f}/{(up+20)/200:.3f}/{(up+30)/300:.3f}, fail mean<={(lo+10)/100:.3f}/{(lo+20)/200:.3f}/{(lo+30)/300:.3f}")
print("infinite-horizon P(down 10R from start) exp(-2muD/s^2):", [f"mu={m},s={v}: {math.exp(-2*m*10/v**2):.3f}" for m,v in ((0.1,1.1),(0.2,1.1),(0.1,1.45),(0.2,1.47),(0.3,1.49))])
