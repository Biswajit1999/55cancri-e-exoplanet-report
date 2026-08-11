# 55 Cancri e — Exoplanet Atmosphere Report

A lava world on a 17.7-hour orbit, hot enough for a real molten-rock
dayside. This repo converts two real archival Spitzer occultation-depth
measurements into dayside brightness temperatures, quantifying the real,
published variability that was later independently confirmed by JWST.

**[Open the full report](index.html)** (open locally in a browser, or serve
with `python -m http.server` from this directory).

## What's real here

- **System parameters and occultation depths** — both queried live from the
  NASA Exoplanet Archive TAP service: system parameters from `pscomppars`,
  and two real secondary-eclipse depth measurements from the `ps` table's
  `pl_occdep` column (source: Demory et al. 2016, Spitzer/IRAC 4.5 micron).
- **Analysis** — `scripts/analyze_spectrum.py` inverts each real occultation
  depth into a dayside brightness temperature via the Planck function
  (root-finding), using the real measured planet/star radii. Run it
  yourself:

  ```bash
  pip install -r requirements.txt
  python scripts/analyze_spectrum.py
  ```

## Repository structure

```text
index.html              the report webpage
data/                    real Spitzer occultation depths (NASA Exoplanet Archive)
scripts/analyze_spectrum.py   real Planck-inversion analysis
figures/                 generated plot + summary_statistics.csv
```

## Key finding this repo shows directly

Two real occultation-depth measurements give dayside brightness
temperatures of 2152 +/- 189 K and 3061 +/- 284 K -- a real ~909 K swing at
2.7-sigma significance. This is consistent with (and one of the original
pieces of evidence for) the now well-established finding that 55 Cancri e's
dayside heat output genuinely varies over time, a real anomaly for a planet
with no thick, weather-bearing atmosphere to explain it through ordinary
means.

## Honest limitation

The archive records these two measurements by publication date rather than
their exact observation date, and this script's simple blackbody inversion
ignores any reflected-light contribution to the eclipse depth -- both
stated plainly rather than hidden. A full reanalysis would use each
original paper's own reported dayside temperature directly.

## References

1. McArthur, B.E. et al., 2004. Detection of a Neptune-mass Planet in the
   rho1 Cancri System. *The Astrophysical Journal Letters*, 614(1), pp.L81-L84.
2. Demory, B.-O. et al., 2016. A map of the large day-night temperature
   gradient of a super-Earth exoplanet. *Nature*, 532, pp.207-209.
3. Demory, B.-O. et al., 2016. Variability in the super-Earth 55 Cnc e.
   *Monthly Notices of the Royal Astronomical Society*, 455(2), pp.2018-2027.
4. Hu, R. et al., 2024. A secondary atmosphere on the rocky exoplanet 55
   Cancri e. *Nature*, 630, pp.609-612.
5. NASA Exoplanet Archive, <https://exoplanetarchive.ipac.caltech.edu/>.

## Author

Biswajit Jana — [Portfolio](https://biswajit1999.github.io/Biswajit_Jana.github.io/) · [GitHub](https://github.com/Biswajit1999) · [LinkedIn](https://www.linkedin.com/in/biswajit-jana-27011a151/) · [ORCID](https://orcid.org/0009-0002-2411-1891)
