"""Executable checks on the Planck inversion and a regression guard
that the pipeline still reproduces the documented headline numbers
(including the real 3.7-sigma season-to-season significance) when run
on the real season-split occultation depths."""

import csv

import numpy as np
import analyze_spectrum as spec


def test_planck_brightness_temperature_round_trip():
    t_true = 2000.0
    wavelength_m = spec.WAVELENGTH_UM * 1e-6
    rp_over_rs = (spec.RP_REARTH * spec.REARTH_M) / (spec.RS_RSUN * spec.RSUN_M)
    eclipse_depth = rp_over_rs**2 * spec.planck(wavelength_m, t_true) / spec.planck(wavelength_m, spec.TEFF_STAR_K)
    t_recovered = spec.brightness_temperature(eclipse_depth)
    assert abs(t_recovered - t_true) < 1e-3


def test_pipeline_reproduces_documented_headline_numbers():
    spec.FIG_DIR.mkdir(exist_ok=True)
    spec.main()
    rows = {}
    with (spec.FIG_DIR / "summary_statistics.csv").open() as f:
        for row in csv.DictReader(f):
            rows[row["quantity"]] = row["value"]
    depth_sigma = float(rows["season_to_season_depth_difference_sigma_this_script"])
    paper_sigma = float(rows["paper_significance"])
    # This repo's own independent two-point comparison should land close
    # to the paper's own full-eclipse-set significance -- confirming the
    # season-split values (47+/-21 and 176+/-28 ppm) were transcribed
    # correctly from Demory et al. (2016) Table 4.
    assert abs(depth_sigma - 3.7) < 0.1
    assert abs(paper_sigma - 3.7) < 0.1
