# Data source

`spitzer_occultation_depths.csv` is queried live from the NASA Exoplanet
Archive TAP service, `ps` table, column `pl_occdep` (unit: percent) for
`55 Cnc e`, retrieved 2026-08-11:

```
select pl_name, pl_occdep, pl_occdeperr1, pl_pubdate, pl_refname
from ps where pl_name='55 Cnc e' and pl_occdep is not null
```

Both real values trace back to Demory et al. (2016), based on Spitzer/IRAC
4.5-micron secondary-eclipse photometry. HTML reference-link markup from
the archive's raw response was stripped to plain text; no numeric values
were altered.

**Note on units:** `pl_occdep` is reported in percent by the archive. This
repo's analysis script divides by 100 again to convert to a fractional
depth before use in the Planck-ratio equation.
