# 55 Cancri e — Exoplanet Atmosphere Report

<p align="center">
  <img src="images/thumbnail.png" alt="Artist's concept of 55 Cancri e" width="360">
</p>

<p align="center"><em>AI-generated artist's concept — not a real photograph. See the report for actual Spitzer/IRAC data.</em></p>

A lava world on a 17.7-hour orbit, hot enough to keep its dayside
molten. This repo converts two Spitzer occultation-depth measurements,
split by observing season, into dayside brightness temperatures and
compares them against the temperatures Demory et al. (2016) report
directly.

**[Open the full report](https://biswajit1999.github.io/55cancri-e-exoplanet-report/)** — the live GitHub Pages version. You can also open `index.html` locally in a browser, or serve it with `python -m http.server` from this directory.

## Data sources

- **System parameters** — from the NASA Exoplanet Archive TAP service
  (`pscomppars`).
- **Occultation depths** — the season-split values from Demory et al.
  (2016), Table 4: 47 ± 21 ppm for 2012 and 176 ± 28 ppm for 2013,
  fit from eight individual Spitzer/IRAC 4.5-micron eclipses. See
  [data/SOURCE.md](data/SOURCE.md) for how these differ from a pair of
  values an earlier version of this repo pulled from the archive.
- **Analysis** — `scripts/analyze_spectrum.py` inverts each season's
  occultation depth into a dayside brightness temperature via the
  Planck function (root-finding), using the measured planet/star
  radii, and prints it next to the temperature the paper quotes for
  that season. Run it yourself:

  ```bash
  pip install -r requirements.txt
  python scripts/analyze_spectrum.py
  ```

## Repository structure

```text
index.html              the report webpage
data/                    season-split Spitzer occultation depths (Demory et al. 2016)
scripts/analyze_spectrum.py   Planck-inversion analysis, this script vs. the paper
figures/                 generated plot + summary_statistics.csv
tests/                   unit tests + a regression check against the real data
```

## Tests

`tests/test_analysis.py` checks the Planck-inversion round trip and
reruns the full pipeline on the real season-split occultation depths,
verifying this repo's own independent two-point significance still
lands close to the paper's own 3.7-sigma constant-depth rejection — a
consistency check that the season values were transcribed correctly.
Runs automatically on every push via GitHub Actions; run locally with:

```bash
pytest tests/ -v
```

## What the numbers show

The two season depths differ at 3.7σ — the same significance Demory et
al. (2016) report from fitting all eight individual eclipses and
rejecting a constant depth. This script's own blackbody inversion gives
1639 K (2012) and 3330 K (2013); the paper's own MCMC fit gives 1365 K
and 2528 K for the same seasons. The gap between the two methods has a
documented cause: Demory et al. derive their temperatures using an
observed infrared stellar spectrum of 55 Cancri A (Crossfield 2012)
and their own fitted mean planet radius (1.92 Earth radii), while this
script instead assumes the star radiates as a monochromatic blackbody
at its catalog effective temperature and uses the NASA Exoplanet
Archive's default planet radius (1.875 Earth radii) — a simpler
stellar and radius treatment, not a missing reflected-light term. The
season-to-season swing itself holds up either way.

## Limitations

The occultation depths here are Demory et al.'s season-split fit, not
per-eclipse values — a fuller version of this analysis would fit all
eight eclipses individually. This script's blackbody inversion is also
a simplification in two specific, documented ways relative to the
paper: it treats the Spitzer channel as a monochromatic point rather
than integrating over the real bandpass, and it uses a monochromatic
blackbody stellar spectrum at the catalog Teff rather than the
observed infrared stellar spectrum (Crossfield 2012) the paper uses,
along with a slightly different adopted planet radius — which is why
its temperatures run above the paper's own.

## References

1. McArthur, B.E. et al., 2004. Detection of a Neptune-mass Planet in the
   rho1 Cancri System. *The Astrophysical Journal Letters*, 614(1), pp.L81-L84.
2. Demory, B.-O. et al., 2016. A map of the large day-night temperature
   gradient of a super-Earth exoplanet. *Nature*, 532, pp.207-209.
3. Demory, B.-O. et al., 2016. Variability in the super-Earth 55 Cnc e.
   *Monthly Notices of the Royal Astronomical Society*, 455(2), pp.2018-2027
   (arXiv:1505.00269) — source of the occultation depths used here.
4. Hu, R. et al., 2024. A secondary atmosphere on the rocky exoplanet 55
   Cancri e. *Nature*, 630, pp.609-612.
5. Crossfield, I.J.M., 2012. ACME Stellar Spectra. I. Absolutely
   Calibrated, Mostly Empirical Flux Densities of 55 Cancri and its
   Transiting Planet 55 Cancri e. *Astronomy & Astrophysics*, 545, A97
   — the observed infrared stellar spectrum Demory et al. (2016) use to
   convert eclipse depth to brightness temperature.
6. NASA Exoplanet Archive, <https://exoplanetarchive.ipac.caltech.edu/>.

## Author

Biswajit Jana — [Portfolio](https://biswajit1999.github.io/Biswajit_Jana.github.io/) · [GitHub](https://github.com/Biswajit1999) · [LinkedIn](https://www.linkedin.com/in/biswajit-jana-27011a151/) · [ORCID](https://orcid.org/0009-0002-2411-1891)
