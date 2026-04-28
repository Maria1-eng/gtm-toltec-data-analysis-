# GTM TolTEC Data Analysis

Data analysis pipeline for evaluating flux recovery in millimeter-wave galaxy observations from the Gran Telescopio Milimétrico (GTM), using TolTEC camera simulations.

The pipeline compares simulated input flux against TolTEC's observed output across three wavelength bands (1.1 mm, 1.4 mm, 2.0 mm) to quantify instrument accuracy and derive calibration factors.

## Notebooks

All notebooks are located in the `TolTEC Galaxy Analysis/` folder.

### `01_leer_fits.ipynb` — How to read FITS files
Introductory guide to working with FITS files using `astropy.io.fits`. Covers:
- Opening a FITS file and inspecting its structure with `info()`
- Accessing image data (HDU arrays) and headers
- Displaying 2D images with `matplotlib`
- Reading binary table extensions (`.srl.FITS`) and accessing specific columns and rows

### `02_leer_flujo.ipynb` — Flux recovery pipeline
Step-by-step walkthrough of the full flux comparison workflow. Covers:
- Loading a TolTEC observation with `ToltecSignalFits` and applying a weight cut
- Reading simulated input sources from a `.csv` catalog with `SimuInputSources`
- Performing PSF photometry with `inphotPS` to compare input vs. observed flux
- Extracting PyBDSF source catalogs with `BdsfCat`
- Matching catalogs with `CatalogMatch` and plotting results

### `03_Una_fuente.ipynb` — Single source example
Minimal worked example using a single source catalog at 1.1 mm. Useful for understanding the photometry workflow before scaling up.

### `04_a1400.ipynb` — Flux calibration at 1.4 mm and 2.0 mm
Demonstrates that the input-to-observed flux relationship is not one-to-one and derives a calibration constant:
- Computes the ratio between input and observed flux across all sources
- Applies the mean ratio as a calibration factor
- Plots flux comparisons before and after calibration

### `05_nearby_galaxies.ipynb` — Full multi-wavelength galaxy analysis
Complete analysis pipeline applied to the galaxy NGC 3938 across all three TolTEC bands:
- Segments images with `photutils` to identify sources
- Reprojects the input model (MIPS 24 µm resolution) to TolTEC resolution using a Gaussian convolution kernel
- Performs aperture and PSF photometry
- Compares input vs. observed fluxes per band

## Stack

Python · NumPy · Astropy · Matplotlib · Photutils · Jupyter
