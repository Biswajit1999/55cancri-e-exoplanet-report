"""Convert the two season-averaged Spitzer 4.5-micron occultation depths
for 55 Cancri e into dayside brightness temperatures via the Planck
function, and compare against the season temperatures Demory et al.
(2016) report directly in their own paper.

Data source: Demory et al. (2016), Variability in the super-Earth 55
Cnc e, MNRAS 455, 2018-2027 (arXiv:1505.00269), Table 4 -- the
season-split fit to eight individual Spitzer/IRAC eclipses observed in
2012 and 2013, reproduced in data/spitzer_occultation_depths.csv. See
data/SOURCE.md for why this replaces an earlier, incorrectly paired
pair of archive values.

This script's own Planck inversion is an independent computation from
the same two season depths; it is reported next to the temperatures
the paper itself quotes (from their own MCMC posterior, not a simple
inversion), rather than presented as a reproduction of them.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401 (registers 'science' style)
import numpy as np
from scipy.optimize import brentq

plt.style.use(["science", "no-latex"])

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR = Path(__file__).resolve().parents[1] / "figures"

H = 6.62607015e-34
C = 2.99792458e8
KB = 1.380649e-23

# 55 Cancri system parameters (NASA Exoplanet Archive, pscomppars)
RP_REARTH = 1.875
RS_RSUN = 0.943
TEFF_STAR_K = 5172.0
WAVELENGTH_UM = 4.5  # Spitzer/IRAC channel 2

REARTH_M = 6.371e6
RSUN_M = 6.957e8

# Season brightness temperatures as quoted directly in Demory et al.
# (2016), Section 2.3.5 -- from their own MCMC posterior, not from this
# script's Planck inversion.
PAPER_TEMPS_K = {"2012": (1365, 257, 219), "2013": (2528, 229, 224)}
PAPER_SIGNIFICANCE = 3.7  # paper's own stated rejection of a constant-depth model


def planck(wavelength_m: np.ndarray, temperature_k: float) -> np.ndarray:
    return (2 * H * C**2 / wavelength_m**5) / (
        np.expm1(H * C / (wavelength_m * KB * temperature_k))
    )


def brightness_temperature(eclipse_depth: float) -> float:
    wavelength_m = WAVELENGTH_UM * 1e-6
    rp_over_rs = (RP_REARTH * REARTH_M) / (RS_RSUN * RSUN_M)

    def residual(t_planet: float) -> float:
        predicted = rp_over_rs**2 * planck(wavelength_m, t_planet) / planck(wavelength_m, TEFF_STAR_K)
        return predicted - eclipse_depth

    return brentq(residual, 50, 6000)


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True)
    rows = []
    with (DATA_DIR / "spitzer_occultation_depths.csv").open() as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(row)

    results = []
    for row in rows:
        depth = float(row["occultation_depth_ppm"]) * 1e-6
        depth_err = float(row["occultation_depth_err_ppm"]) * 1e-6
        t_best = brightness_temperature(depth)
        t_hi = brightness_temperature(depth + depth_err)
        t_lo = brightness_temperature(max(depth - depth_err, 1e-9))
        results.append(
            {
                "season": row["season"],
                "depth_ppm": depth * 1e6,
                "depth_err_ppm": depth_err * 1e6,
                "t_day_k": t_best,
                "t_day_err_k": (t_hi - t_lo) / 2,
            }
        )

    depth_diff_ppm = results[1]["depth_ppm"] - results[0]["depth_ppm"]
    depth_diff_err_ppm = np.sqrt(results[0]["depth_err_ppm"] ** 2 + results[1]["depth_err_ppm"] ** 2)
    depth_diff_sigma = depth_diff_ppm / depth_diff_err_ppm

    temp_diff = results[1]["t_day_k"] - results[0]["t_day_k"]
    temp_diff_err = np.sqrt(results[0]["t_day_err_k"] ** 2 + results[1]["t_day_err_k"] ** 2)

    summary_path = FIG_DIR / "summary_statistics.csv"
    with summary_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["quantity", "value", "unit"])
        for r in results:
            writer.writerow([f"t_day_{r['season']}_this_script", f"{r['t_day_k']:.0f} +/- {r['t_day_err_k']:.0f}", "K"])
            paper_t, paper_lo, paper_hi = PAPER_TEMPS_K[r["season"]]
            writer.writerow([f"t_day_{r['season']}_paper", f"{paper_t} (+{paper_hi}/-{paper_lo})", "K"])
        writer.writerow(["season_to_season_temp_difference_this_script", f"{temp_diff:.0f} +/- {temp_diff_err:.0f}", "K"])
        writer.writerow(["season_to_season_depth_difference_sigma_this_script", f"{depth_diff_sigma:.1f}", "sigma (two-point comparison)"])
        writer.writerow(["paper_significance", f"{PAPER_SIGNIFICANCE}", "sigma (constant-depth model rejected, all 8 eclipses)"])

    fig, ax = plt.subplots(figsize=(7, 5.5))
    x = np.arange(len(results))
    ax.errorbar(
        x, [r["t_day_k"] for r in results], yerr=[r["t_day_err_k"] for r in results],
        fmt="o", ms=10, color="#c0562a", capsize=4, label="This script's Planck inversion",
    )
    paper_y = [PAPER_TEMPS_K[r["season"]][0] for r in results]
    paper_yerr = [[PAPER_TEMPS_K[r["season"]][1] for r in results], [PAPER_TEMPS_K[r["season"]][2] for r in results]]
    ax.errorbar(x, paper_y, yerr=paper_yerr, fmt="s", ms=8, color="#1f4e79", capsize=4, label="Demory et al. (2016), quoted directly")
    ax.set_xticks(x)
    ax.set_xticklabels([r["season"] for r in results])
    ax.set_xlabel("Observing season")
    ax.set_ylabel("Dayside brightness temperature [K]")
    ax.set_title("55 Cancri e dayside temperature by season\n(Spitzer 4.5 um occultation depths, Demory et al. 2016)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "55cnce_dayside_variability.png", dpi=200)

    print(f"Wrote {summary_path}")
    print(f"Wrote {FIG_DIR / '55cnce_dayside_variability.png'}")
    for r in results:
        paper_t, paper_lo, paper_hi = PAPER_TEMPS_K[r["season"]]
        print(f"  {r['season']}: depth={r['depth_ppm']:.0f} ppm, T_day (this script) = {r['t_day_k']:.0f} +/- {r['t_day_err_k']:.0f} K, T_day (paper) = {paper_t} (+{paper_hi}/-{paper_lo}) K")
    print(f"Season-to-season depth difference: {depth_diff_sigma:.1f} sigma (this script's two-point comparison)")
    print(f"Paper's own significance for a varying depth across all 8 eclipses: {PAPER_SIGNIFICANCE} sigma")


if __name__ == "__main__":
    main()
