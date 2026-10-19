#!/usr/bin/env python3
"""Draw the harmonic oscillator "quantum vs classical" figure.

Plots |psi_n(x)|^2 next to the classical probability density for the same
energy, for the ground state and one highly excited state, and writes the
result as a Zola shortcode:

    python3 scripts/make_qho_plot.py

Then use it in a note with {{ qho_classical_limit() }}.

Everything is in oscillator units: x in units of x0 = sqrt(hbar / m omega),
densities in units of 1 / x0. The classical turning point for level n is
A = x0 sqrt(2n + 1), from (1/2) m omega^2 A^2 = (n + 1/2) hbar omega.
"""

import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "templates" / "shortcodes" / "qho_classical_limit.html"

# One panel per level: (n, title, x range, y max, x ticks, y ticks, label spots)
PANELS = [
    {
        "n": 0,
        "title": "n = 0, the ground state",
        "x": (-3.0, 3.0),
        "ymax": 0.8,
        "xticks": [-3, -2, -1, 0, 1, 2, 3],
        "yticks": [0, 0.2, 0.4, 0.6, 0.8],
        # (x, y, anchor, text) for the direct labels
        "labels": [(1.15, 0.25, "start", "quantum"), (-1.1, 0.7, "end", "classical")],
        "samples": [0, 0.5, 0.9, 1.5, 2.5],
        "steps": 240,
    },
    {
        "n": 30,
        "title": "n = 30",
        "x": (-9.5, 9.5),
        "ymax": 0.3,
        "xticks": [-8, -4, 0, 4, 8],
        "yticks": [0, 0.1, 0.2, 0.3],
        "labels": [(0, 0.125, "middle", "quantum"), (-8.0, 0.27, "end", "classical")],
        "samples": [0, 2, 4, 6, 7.5, 8.5],
        "steps": 900,
    },
]

# viewBox geometry, shared by both panels
VW, VH = 320, 214
LEFT, RIGHT, TOP, BOTTOM = 34, 10, 20, 34
PW, PH = VW - LEFT - RIGHT, VH - TOP - BOTTOM
CLASSICAL_STEPS = 200


def psi2(n, x):
    """|psi_n(x)|^2 via the normalized Hermite-function recurrence."""
    p0 = math.pi ** -0.25 * math.exp(-x * x / 2)
    if n == 0:
        return p0 * p0
    p1 = math.sqrt(2) * x * p0
    for k in range(1, n):
        p0, p1 = p1, math.sqrt(2 / (k + 1)) * x * p1 - math.sqrt(k / (k + 1)) * p0
    return p1 * p1


def classical(n, x):
    """Classical density 1 / (pi sqrt(A^2 - x^2)) inside the turning points."""
    a2 = 2 * n + 1
    return 1 / (math.pi * math.sqrt(a2 - x * x)) if x * x < a2 else 0.0


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def panel_svg(p):
    n, (x0, x1), ymax = p["n"], p["x"], p["ymax"]
    sx = lambda x: LEFT + (x - x0) / (x1 - x0) * PW
    sy = lambda y: TOP + PH - min(y, ymax) / ymax * PH
    amp = math.sqrt(2 * n + 1)
    out = []
    # gridlines and y ticks
    for t in p["yticks"]:
        y = sy(t)
        out.append(f'<line class="qho-grid" x1="{LEFT}" x2="{LEFT + PW}" y1="{fmt(y)}" y2="{fmt(y)}"/>')
        out.append(f'<text class="qho-tick" x="{LEFT - 6}" y="{fmt(y + 3.5)}" text-anchor="end">{t:g}</text>')
    # x ticks
    for t in p["xticks"]:
        out.append(f'<text class="qho-tick" x="{fmt(sx(t))}" y="{TOP + PH + 14}" text-anchor="middle">{t:g}</text>')
    out.append(f'<text class="qho-tick" x="{LEFT + PW / 2}" y="{VH - 4}" text-anchor="middle">x / x₀</text>')
    # turning points
    for s, name in ((-1, "−A"), (1, "A")):
        x = fmt(sx(s * amp))
        out.append(f'<line class="qho-turn" x1="{x}" x2="{x}" y1="{TOP}" y2="{TOP + PH}"/>')
        out.append(f'<text class="qho-tick" x="{x}" y="{TOP - 6}" text-anchor="middle">{name}</text>')
    # quantum curve: area wash + line
    steps = p["steps"]
    xs = [x0 + (x1 - x0) * i / steps for i in range(steps + 1)]
    pts = " ".join(f"{fmt(sx(x))},{fmt(sy(psi2(n, x)))}" for x in xs)
    base = fmt(sy(0))
    out.append(f'<path class="qho-q-area" d="M{fmt(sx(x0))},{base} L{pts} L{fmt(sx(x1))},{base} Z"/>')
    out.append(f'<path class="qho-q" d="M{pts}"/>')
    # classical curve, only between the turning points, clipped at the top.
    # Sampled evenly in angle (x = A sin t) so the steep edges get more points.
    cxs = [amp * math.sin(-1.5705 + 3.141 * i / CLASSICAL_STEPS) for i in range(CLASSICAL_STEPS + 1)]
    cpts = " ".join(f"{fmt(sx(x))},{fmt(sy(classical(n, x)))}" for x in cxs if x0 <= x <= x1)
    out.append(f'<path class="qho-c" d="M{cpts}"/>')
    # baseline last so it sits on top of the fills
    out.append(f'<line class="qho-axis" x1="{LEFT}" x2="{LEFT + PW}" y1="{base}" y2="{base}"/>')
    # direct labels
    for lx, ly, anchor, text in p["labels"]:
        out.append(f'<text class="qho-label" x="{fmt(sx(lx))}" y="{fmt(sy(ly))}" text-anchor="{anchor}">{text}</text>')
    # hover layer (hidden until pointer or focus)
    out.append(f'<line class="qho-cross" x1="0" x2="0" y1="{TOP}" y2="{TOP + PH}" style="display:none"/>')
    out.append('<circle class="qho-dot-q" r="4" cx="0" cy="0" style="display:none"/>')
    out.append('<circle class="qho-dot-c" r="4" cx="0" cy="0" style="display:none"/>')
    out.append(f'<rect class="qho-hit" x="{LEFT}" y="{TOP}" width="{PW}" height="{PH}"/>')
    label = (f"Probability density for n = {n}: the quantum |ψ|² against the classical density, "
             f"with turning points at plus and minus {amp:.2f} x₀")
    svg = (f'<svg viewBox="0 0 {VW} {VH}" role="img" tabindex="0" aria-label="{label}" '
           f'data-n="{n}" data-xmin="{x0}" data-xmax="{x1}" data-ymax="{ymax}" '
           f'data-left="{LEFT}" data-top="{TOP}" data-w="{PW}" data-h="{PH}">'
           + "".join(out) + "</svg>")
    tip = ('<div class="qho-tip" style="display:none"><div class="qho-tip-x"></div>'
           '<div class="qho-row"><span class="qho-key qho-key-q"></span><b class="qho-tip-q"></b> quantum</div>'
           '<div class="qho-row"><span class="qho-key qho-key-c"></span><b class="qho-tip-c"></b> classical</div></div>')
    return f'<div class="qho-panel"><div class="qho-title">{p["title"]}</div>{svg}{tip}</div>'


def table():
    rows = []
    for p in PANELS:
        n = p["n"]
        for x in p["samples"]:
            c = classical(n, x)
            c_txt = f"{c:.3f}" if c else "0 (forbidden)"
            rows.append(f"<tr><td>{n}</td><td>{x:g}</td><td>{psi2(n, x):.3f}</td><td>{c_txt}</td></tr>")
    return ('<details class="qho-table"><summary>Table view</summary><table>'
            '<thead><tr><th>n</th><th>x / x₀</th><th>quantum |ψₙ|²</th><th>classical</th></tr></thead>'
            "<tbody>" + "".join(rows) + "</tbody></table></details>")


STYLE = """<style>
.qho-viz{--qho-s1:#2a78d6;--qho-s2:#eb6834;--qho-grid:#e1e0d9;--qho-axis:#c3c2b7;--qho-muted:#898781;--qho-ink2:#52514e;--qho-surface:#ffffff;--qho-ring:rgba(11,11,11,0.10);margin:1.5rem 0}
html.dark .qho-viz{--qho-s1:#3987e5;--qho-s2:#d95926;--qho-grid:#2c2c2a;--qho-axis:#383835;--qho-ink2:#c3c2b7;--qho-surface:#1c1917;--qho-ring:rgba(255,255,255,0.10)}
.qho-legend{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:0.85rem;color:var(--qho-ink2);margin-bottom:8px}
.qho-legend span{display:inline-flex;align-items:center;gap:6px}
.qho-key{display:inline-block;width:16px;height:0;border-top:2px solid}
.qho-key-q{border-color:var(--qho-s1)}
.qho-key-c{border-color:var(--qho-s2)}
.qho-panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.qho-panel{position:relative}
.qho-title{font-size:0.85rem;color:var(--qho-ink2);margin-bottom:2px}
.qho-panel svg{width:100%;height:auto;display:block;overflow:visible;font-family:inherit}
.qho-panel svg:focus{outline:none}
.qho-panel svg:focus-visible{outline:2px solid var(--qho-s1);outline-offset:2px;border-radius:4px}
.qho-grid{stroke:var(--qho-grid);stroke-width:1}
.qho-axis{stroke:var(--qho-axis);stroke-width:1}
.qho-turn{stroke:var(--qho-muted);stroke-width:1;opacity:0.6}
.qho-tick{fill:var(--qho-muted);font-size:10px}
.qho-label{fill:var(--qho-ink2);font-size:11px}
.qho-q{fill:none;stroke:var(--qho-s1);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.qho-q-area{fill:var(--qho-s1);opacity:0.1;stroke:none}
.qho-c{fill:none;stroke:var(--qho-s2);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.qho-cross{stroke:var(--qho-muted);stroke-width:1}
.qho-dot-q{fill:var(--qho-s1);stroke:var(--qho-surface);stroke-width:2}
.qho-dot-c{fill:var(--qho-s2);stroke:var(--qho-surface);stroke-width:2}
.qho-hit{fill:transparent;cursor:crosshair}
.qho-tip{position:absolute;pointer-events:none;background:var(--qho-surface);border:1px solid var(--qho-ring);border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.12);padding:6px 8px;font-size:12px;line-height:1.4;color:var(--qho-ink2);white-space:nowrap;z-index:5}
.qho-tip b{color:inherit;font-weight:600;font-variant-numeric:tabular-nums}
.qho-row{display:flex;align-items:center;gap:6px}
.qho-tip-x{color:var(--qho-muted)}
.qho-table{margin-top:10px;font-size:0.85rem}
.qho-table table{margin-top:6px;font-variant-numeric:tabular-nums}
</style>"""

SCRIPT = """<script>
(function () {
  function psi2(n, x) {
    var p0 = Math.pow(Math.PI, -0.25) * Math.exp(-x * x / 2);
    if (n === 0) return p0 * p0;
    var p1 = Math.SQRT2 * x * p0;
    for (var k = 1; k < n; k++) {
      var p2 = Math.sqrt(2 / (k + 1)) * x * p1 - Math.sqrt(k / (k + 1)) * p0;
      p0 = p1;
      p1 = p2;
    }
    return p1 * p1;
  }
  function classical(n, x) {
    var a2 = 2 * n + 1;
    return x * x < a2 ? 1 / (Math.PI * Math.sqrt(a2 - x * x)) : 0;
  }
  var panels = document.querySelectorAll('.qho-panel');
  Array.prototype.forEach.call(panels, function (panel) {
    var svg = panel.querySelector('svg');
    var d = svg.dataset;
    var n = +d.n, x0 = +d.xmin, x1 = +d.xmax, ymax = +d.ymax;
    var L = +d.left, T = +d.top, W = +d.w, H = +d.h;
    var cross = svg.querySelector('.qho-cross');
    var dq = svg.querySelector('.qho-dot-q');
    var dc = svg.querySelector('.qho-dot-c');
    var tip = panel.querySelector('.qho-tip');
    var tx = tip.querySelector('.qho-tip-x');
    var tq = tip.querySelector('.qho-tip-q');
    var tc = tip.querySelector('.qho-tip-c');
    var cur = 0;
    function sx(x) { return L + (x - x0) / (x1 - x0) * W; }
    function sy(y) { return T + H - Math.min(y, ymax) / ymax * H; }
    function show(x) {
      cur = Math.max(x0, Math.min(x1, x));
      var q = psi2(n, cur), c = classical(n, cur), X = sx(cur);
      cross.setAttribute('x1', X);
      cross.setAttribute('x2', X);
      cross.style.display = '';
      dq.setAttribute('cx', X);
      dq.setAttribute('cy', sy(q));
      dq.style.display = '';
      if (c > 0 && c <= ymax) {
        dc.setAttribute('cx', X);
        dc.setAttribute('cy', sy(c));
        dc.style.display = '';
      } else {
        dc.style.display = 'none';
      }
      tx.textContent = 'x = ' + cur.toFixed(2) + ' x₀';
      tq.textContent = q.toFixed(3);
      tc.textContent = c > 0 ? c.toFixed(3) : '0 (forbidden)';
      var r = svg.getBoundingClientRect(), pr = panel.getBoundingClientRect();
      var px = r.left - pr.left + X / svg.viewBox.baseVal.width * r.width;
      tip.style.display = 'block';
      var left = px + 12;
      if (left + tip.offsetWidth > pr.width) left = px - tip.offsetWidth - 12;
      tip.style.left = left + 'px';
      tip.style.top = (r.top - pr.top + 8) + 'px';
    }
    function hide() {
      cross.style.display = 'none';
      dq.style.display = 'none';
      dc.style.display = 'none';
      tip.style.display = 'none';
    }
    svg.addEventListener('pointermove', function (e) {
      var pt = svg.createSVGPoint();
      pt.x = e.clientX;
      pt.y = e.clientY;
      var p = pt.matrixTransform(svg.getScreenCTM().inverse());
      if (p.x < L || p.x > L + W) { hide(); return; }
      show(x0 + (p.x - L) / W * (x1 - x0));
    });
    svg.addEventListener('pointerleave', hide);
    svg.addEventListener('focus', function () { show(cur); });
    svg.addEventListener('blur', hide);
    svg.addEventListener('keydown', function (e) {
      var step = (x1 - x0) / 200;
      if (e.key === 'ArrowLeft') { show(cur - step); e.preventDefault(); }
      if (e.key === 'ArrowRight') { show(cur + step); e.preventDefault(); }
    });
  });
})();
</script>"""


def main():
    legend = ('<div class="qho-legend"><span><span class="qho-key qho-key-q"></span>quantum |ψₙ(x)|²</span>'
              '<span><span class="qho-key qho-key-c"></span>classical, same energy</span></div>')
    figure = ('<figure class="qho-viz not-prose">' + legend + '<div class="qho-panels">'
              + "".join(panel_svg(p) for p in PANELS) + "</div>" + table() + "</figure>")
    # No blank lines anywhere: markdown would end the HTML block at the first one.
    html = "\n".join([STYLE, figure, SCRIPT]) + "\n"
    assert "\n\n" not in html
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
