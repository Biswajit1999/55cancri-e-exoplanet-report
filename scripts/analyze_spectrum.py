"""Analyze real Spitzer 4.5-micron secondary-eclipse depths for 55 Cancri e,
converting them into dayside brightness temperatures to quantify its real,
published dayside variability.

Data source: NASA Exoplanet Archive `ps` table, column `pl_occdep`
(occultation/secondary-eclipse depth), queried live via the TAP service for
55 Cnc e. Both real measurements come from Demory et al. (2016), based on
Spitzer/IRAC 4.5-micron photometry at different epochs -- reproduced
unmodified in data/spitzer_occultation_depths.csv.

This script inverts each real occultation depth into a dayside brightness
temperature via the Planck function (root-finding), using the real
measured planet and star radii. The real result is a large, genuine
epoch-to-epoch difference in dayside brightness temperature -- the original
discovery of 55 Cnc e's dayside variability, later independently confirmed
by JWST (Patel et al., 2024).
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

# Real 55 Cancri system parameters (NASA Exoplanet Archive, pscomppars)
RP_REARTH = 1.875
RS_RSUN = 0.943
TEFF_STAR_K = 5172.0
WAVELENGTH_UM = 4.5  # Spitzer/IRAC channel 2

REARTH_M = 6.371e6
RSUN_M = 6.957e8


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
        # NASA Exoplanet Archive pl_occdep column is in PERCENT, so divide by 100
        # again to get the fractional depth used in the Planck-ratio equation.
        depth = float(row["occultation_depth"]) / 100
        depth_err = float(row["occultation_depth_err"]) / 100
        t_best = brightness_temperature(depth)
        t_hi = brightness_temperature(depth + depth_err)
        t_lo = brightness_temperature(max(depth - depth_err, 1e-6))
        results.append(
            {
                "date": row["publication_date"],
                "depth_pct": depth * 100,
                "depth_err_pct": depth_err * 100,
                "t_day_k": t_best,
                "t_day_err_k": (t_hi - t_lo) / 2,
            }
        )

    temp_diff = results[1]["t_day_k"] - results[0]["t_day_k"]
    temp_diff_err = np.sqrt(results[0]["t_day_err_k"] ** 2 + results[1]["t_day_err_k"] ** 2)
    temp_diff_sigma = abs(temp_diff) / temp_diff_err

    summary_path = FIG_DIR / "summary_statistics.csv"
    with summary_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["quantity", "value", "unit"])
        for r in results:
            writer.writerow([f"t_day_{r['date']}", f"{r['t_day_k']:.0f} +/- {r['t_day_err_k']:.0f}", "K"])
        writer.writerow(["epoch_to_epoch_temp_difference", f"{temp_diff:.0f}", "K"])
        writer.writerow(["epoch_to_epoch_significance", f"{temp_diff_sigma:.1f}", "sigma"])

    fig, ax = plt.subplots(figsize=(7, 5.5))
    x = np.arange(len(results))
    ax.errorbar(
        x, [r["t_day_k"] for r in results], yerr=[r["t_day_err_k"] for r in results],
        fmt="o", ms=10, color="#c0562a", capsize=4,
    )
    ax.set_xticks(x)
    ax.set_xticklabels([r["date"] for r in results])
    ax.set_xlabel("Publication epoch (Demory et al. 2016)")
    ax.set_ylabel("Dayside brightness temperature [K]")
    ax.set_title("55 Cancri e real dayside temperature variability\n(from real Spitzer 4.5 um occultation depths)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "55cnce_dayside_variability.png", dpi=200)

    print(f"Wrote {summary_path}")
    print(f"Wrote {FIG_DIR / '55cnce_dayside_variability.png'}")
    for r in results:
        print(f"  {r['date']}: depth={r['depth_pct']:.2f}%, T_day = {r['t_day_k']:.0f} +/- {r['t_day_err_k']:.0f} K")
    print(f"Epoch-to-epoch difference = {temp_diff:.0f} K ({temp_diff_sigma:.1f} sigma)")


if __name__ == "__main__":
    main()
