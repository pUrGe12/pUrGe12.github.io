#!/usr/bin/env python3
"""
Tank-level vs time plots (like Figs 1-3 of the old report) + transient metrics,
from the time-series logs exported by the DAQ / PI-controller software.

1) Export each run's log as CSV (or XLSX) with a time column and a level column
   (optionally an inlet-flow column).
2) Make a manifest CSV listing the runs:

       file,SP,Kc,tauI
       logs/sp10_kc4_ti1.csv,10,4,1
       logs/sp10_kc4_ti2.csv,10,4,2
       ...

3) Run:
       python plot_time_response.py runs.csv
       python plot_time_response.py runs.csv --time-col "Time" --level-col "Level" --level-scale 0.1   # log in mm
       python plot_time_response.py runs.csv --flow-col "Flow"                                        # also plot flow

Outputs (in --out): one PNG per run, one grid PNG per setpoint, metrics.csv and metrics.md
Metrics: rise time (10-90 %), % overshoot, settling time (±band of SP), steady-state error, IAE.
"""
import argparse
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.35,
                     "figure.dpi": 150, "savefig.bbox": "tight"})


def load_log(path, time_col, level_col, flow_col, level_scale, time_scale):
    path = pathlib.Path(path)
    df = pd.read_excel(path) if path.suffix.lower() in (".xlsx", ".xls") else pd.read_csv(path, sep=None, engine="python")
    df.columns = [str(c).strip() for c in df.columns]

    def pick(name, keyword, fallback_idx):
        if name:
            return name
        hits = [c for c in df.columns if keyword in c.lower()]
        return hits[0] if hits else df.select_dtypes("number").columns[fallback_idx]

    tc, lc = pick(time_col, "time", 0), pick(level_col, "level", 1)
    t = pd.to_numeric(df[tc], errors="coerce").to_numpy() * time_scale
    h = pd.to_numeric(df[lc], errors="coerce").to_numpy() * level_scale
    q = pd.to_numeric(df[flow_col], errors="coerce").to_numpy() if flow_col else None
    m = ~(np.isnan(t) | np.isnan(h))
    t, h = t[m] - t[m][0], h[m]
    return t, h, (q[m] if q is not None else None)


def metrics(t, h, sp, band, tail):
    h0 = h[0]
    step = sp - h0
    sgn = 1 if step >= 0 else -1
    frac = (h - h0) / step if step != 0 else np.zeros_like(h)

    def first_cross(level):
        idx = np.where(frac >= level)[0]
        return t[idx[0]] if idx.size else math.nan

    t10, t90 = first_cross(0.1), first_cross(0.9)
    peak = h.max() if sgn > 0 else h.min()
    overshoot = max(0.0, 100 * (peak - sp) / step) if step != 0 else math.nan

    n_tail = max(1, int(tail * len(h)))
    out_band = np.abs(h - sp) > band * sp
    if out_band[-n_tail:].any():
        ts = math.nan                                   # still leaving the band near the end of the log
    else:
        idx = np.where(out_band)[0]
        ts = t[idx[-1] + 1] if idx.size else 0.0

    h_ss = h[-n_tail:].mean()
    osc_amp = (h[-n_tail:].max() - h[-n_tail:].min()) / 2
    trapz = getattr(np, "trapezoid", None) or np.trapz      # numpy 2.x renamed trapz
    iae = trapz(np.abs(sp - h), t)
    return dict(h0=h0, rise_time=t90 - t10, peak=peak, overshoot_pct=overshoot,
                settling_time=ts, h_final=h_ss, e_ss=sp - h_ss, tail_osc_amp=osc_amp, IAE=iae)


def draw(ax, t, h, sp, title):
    ax.plot(t, h, "b-", lw=1.2, label="Tank Level")
    ax.axhline(sp, color="#1f9bde", ls="--", lw=1.2, label="Set Point")
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Tank Level (cm)")
    ax.set_title(title, fontweight="bold", fontsize=10)
    ax.legend(loc="best", fontsize=8.5)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", help="CSV with columns file,SP,Kc,tauI")
    ap.add_argument("--out", default="figures/time_response")
    ap.add_argument("--time-col"); ap.add_argument("--level-col"); ap.add_argument("--flow-col")
    ap.add_argument("--level-scale", type=float, default=1.0, help="multiply level by this (0.1 for mm -> cm)")
    ap.add_argument("--time-scale", type=float, default=1.0, help="multiply time by this (60 for min -> s)")
    ap.add_argument("--band", type=float, default=0.02, help="settling band as fraction of SP (default 2%%)")
    ap.add_argument("--tail", type=float, default=0.10, help="fraction of log at the end used for steady state")
    args = ap.parse_args()

    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    runs = pd.read_csv(args.manifest)
    base = pathlib.Path(args.manifest).parent
    rows, data = [], []

    for _, r in runs.iterrows():
        f = pathlib.Path(r.file); f = f if f.is_absolute() else base / f
        t, h, q = load_log(f, args.time_col, args.level_col, args.flow_col, args.level_scale, args.time_scale)
        title = f"Response for Set point = {r.SP:g} cm, $K_c$ = {r.Kc:g}, $\\tau_I$ = {r.tauI:g}"
        data.append((r, t, h, q, title))
        rows.append(dict(SP=r.SP, Kc=r.Kc, tauI=r.tauI, **metrics(t, h, r.SP, args.band, args.tail)))

        if q is None:
            fig, ax = plt.subplots(figsize=(6.5, 4))
            draw(ax, t, h, r.SP, title)
        else:
            fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.5, 6), sharex=True)
            draw(ax, t, h, r.SP, title)
            ax2.plot(t, q, "g-", lw=1.1); ax2.set_ylabel("Inlet flow (LPH)"); ax2.set_xlabel("Time (s)")
        stem = f"SP{r.SP:g}_Kc{r.Kc:g}_tauI{r.tauI:g}".replace(".", "p")
        fig.savefig(out / f"{stem}.png"); plt.close(fig)

    # one grid per setpoint, 2 columns, like the report
    for sp in sorted({d[0].SP for d in data}):
        sub = [d for d in data if d[0].SP == sp]
        n = len(sub); ncol = 2 if n > 1 else 1; nrow = math.ceil(n / ncol)
        fig, axes = plt.subplots(nrow, ncol, figsize=(6.2 * ncol, 4.2 * nrow), squeeze=False)
        for k, (ax, (r, t, h, q, title)) in enumerate(zip(axes.flat, sub)):
            draw(ax, t, h, r.SP, title)
            ax.text(0.5, -0.25, f"({chr(97 + k)}) $K_c$ = {r.Kc:g}, $\\tau_I$ = {r.tauI:g}",
                    transform=ax.transAxes, ha="center", color="navy")
        for ax in list(axes.flat)[n:]:
            ax.axis("off")
        fig.tight_layout(h_pad=3)
        fig.savefig(out / f"grid_SP{sp:g}.png"); plt.close(fig)

    m = pd.DataFrame(rows)
    m.to_csv(out / "metrics.csv", index=False)
    md = m.round(3).astype(object).where(m.notna(), "n.a.").to_markdown(index=False)
    (out / "metrics.md").write_text(md + "\n")
    print(md)
    print("n.a. settling time = level still leaves the ±band in the final part of the log (not settled)")
    print(f"\nWrote figures + metrics to {out.resolve()}")


if __name__ == "__main__":
    main()