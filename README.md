# GTM TolTEC Data Analysis

Python tools and Jupyter notebooks for analyzing TolTEC simulated FITS data and galaxy observations from the Gran Telescopio Milimétrico (GTM).

The goal of this project is to evaluate how accurately the TolTEC camera recovers flux from galaxy observations by comparing simulated input data with the camera's observed output.

## Notebooks

All notebooks are located in the `TolTEC Galaxy Analysis/` folder.

### `01_leer_fits.ipynb` — How to read FITS files
Introductory guide to working with FITS files using `astropy.io.fits`. Covers:
- Opening a FITS file and inspecting its structure with `info()`
- Accessing image data (HDU arrays) and headers
- Displaying 2D images with `matplotlib`
- Reading binary table extensions (`.srl.FITS`) and accessing specific columns and rows

**Start here if you are new to FITS files.**

### `02_leer_flujo.ipynb` — Flux recovery pipeline
Step-by-step manual for the full flux comparison workflow. Covers:
- Loading a TolTEC observation with `ToltecSignalFits` and applying a weight cut
- Reading simulated input sources from a `.csv` catalog with `SimuInputSources`
- Performing PSF photometry with `inphotPS` to compare input vs. observed flux
- Extracting PyBDSF source catalogs with `BdsfCat`
- Matching catalogs with `CatalogMatch` and plotting results

### `03_Una_fuente.ipynb` — Single source example
Minimal worked example using a single source catalog (`sources.csv`) at 1.1 mm (a1100). Useful for understanding the basic photometry workflow before scaling up.

### `04_a1400.ipynb` — Flux calibration at 1.4 mm and 2.0 mm
Demonstrates that the input-to-observed flux relationship is not one-to-one and shows how to derive a calibration constant:
- Loads `toltec_simu_a1400_filtered.fits` and `toltec_simu_a2000_filtered.fits`
- Computes the ratio between input and observed flux across all sources
- Applies the mean ratio as a calibration factor
- Plots flux comparisons before and after calibration

### `05_nearby_galaxies.ipynb` — Full multi-wavelength galaxy analysis
Complete analysis pipeline applied to the galaxy NGC 3938 across all three TolTEC bands (1.1 mm, 1.4 mm, 2.0 mm):
- Loads simulated TolTEC observations for each array
- Segments images with `photutils` to identify sources
- Reprojects the input model (MIPS 24 µm resolution) to TolTEC resolution using a Gaussian convolution kernel
- Performs aperture and PSF photometry
- Compares input vs. observed fluxes per band

## Repository Structure

```
TolTEC Galaxy Analysis/
├── 01_leer_fits.ipynb                       # How to read FITS files
├── 02_leer_flujo.ipynb                      # Flux recovery pipeline manual
├── 03_Una_fuente.ipynb                      # Single source example
├── 04_a1400.ipynb                           # Flux calibration at 1.4 mm and 2.0 mm
├── 05_nearby_galaxies.ipynb                 # Full multi-wavelength galaxy analysis
│
├── Toltec_simu_a1100_filtered.fits          # Simulated TolTEC observation at 1.1 mm
├── Toltec_simu_a1400_filtered.fits          # Simulated TolTEC observation at 1.4 mm
├── Toltec_simu_a2000_filtered.fits          # Simulated TolTEC observation at 2.0 mm
│
├── ngc3938_11mm_eqCalz_MJypersr_pixsize1.fits   # Input model: NGC 3938 (MIPS 24 µm)
├── Kernel_LowRes_MIPS_24_to_Gauss_07.0.fits.gz  # Convolution kernel for resolution matching
│
├── squareCat_0.01mJy.csv                    # Simulated source catalog (flux > 0.01 mJy)
├── sources.csv                              # Single-source catalog
├── sq0.01.pybdsm.srl.FITS                   # PyBDSF source extraction catalog
│
├── toltec.py                                # Helper utilities
└── toltec_pybdsf_scripts-main/              # Analysis library (ToltecSignalFits, InputModelFits, etc.)
```

## Dependencies

```
numpy
astropy
matplotlib
photutils
```

The `toltec_pybdsf_scripts-main/` folder must be present alongside the notebooks. It provides the core analysis classes:

| Class | Purpose |
|---|---|
| `ToltecSignalFits` | Load and display TolTEC FITS observations |
| `InputModelFits` | Load and reproject input galaxy models |
| `SimuInputSources` | Read simulated source catalogs and run PSF photometry |
| `BdsfCat` | Extract sources from PyBDSF `.srl.FITS` catalogs |
| `CatalogMatch` | Match sources between catalogs and compare photometry |
