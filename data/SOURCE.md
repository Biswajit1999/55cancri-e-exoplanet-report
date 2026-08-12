# Data source

`spitzer_occultation_depths.csv` holds the two season-averaged
occultation depths reported in Demory et al. (2016), *Variability in
the super-Earth 55 Cnc e*, MNRAS 455, 2018-2027 (arXiv:1505.00269).

The paper's underlying dataset is eight individual Spitzer/IRAC
4.5-micron secondary eclipses observed between 2011 and 2013. Their
Table 4 reports two fits: a single depth fit to all eight eclipses
combined (83 ± 14 ppm), and a season-split fit that assigns one depth
to the four 2012 eclipses and another to the four 2013 eclipses:

- 2012: 47 ± 21 ppm
- 2013: 176 ± 28 ppm

Section 2.3.5 of the paper states that a constant-depth model fits
those eight eclipses poorly (reduced chi-squared 13.6), rejecting a
non-varying occultation depth at the 3.7-sigma level, and reports the
corresponding season brightness temperatures directly: 1365 K
(+219/-257) for 2012 and 2528 K (+224/-229) for 2013.

An earlier version of this repository queried the NASA Exoplanet
Archive's `pl_occdep` column and paired the combined 83 ± 14 ppm figure
with a 154 ± 23 ppm value from a separate paper, treating the two as
independent epochs. That pairing conflated two different quantities —
the archive result is a combined fit across all eight eclipses, not one
epoch, and the second number comes from unrelated later work. This
version replaces both with the two season depths as reported directly
in Demory et al. (2016)'s own Table 4.
