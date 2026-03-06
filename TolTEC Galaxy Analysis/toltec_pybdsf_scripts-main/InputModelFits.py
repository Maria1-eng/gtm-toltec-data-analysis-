from astropy.io import fits
from reproject import reproject_interp
from astropy.convolution import Gaussian2DKernel, convolve
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.wcs import WCS
from photutils.segmentation import SourceCatalog
import numpy as np
from matplotlib import pyplot as plt
from astropy import units as u

plt.ion()

class InputModelFits:
    
    #Read the input, reproject it, convolve it, and estimate photometry in the segments
    
    def __init__(self, filename=None,array='a1100'):
        self.filename=filename
        self.hdulist=fits.open(self.filename)
        self.convolved=None
        self.reprojected=None
        self.repro_header=None
        #self.exts=[exti.header['EXTNAME'] for exti in self.hdulist]
        self.data=self.hdulist[array].data
        self.header=self.hdulist[array].header
        self.array=array
        #self.beam=
    def convolveInputToOutput(self,toltec_signal_out=None):
        hdr=toltec_signal_out.headers[1]
        #array_name=tfipj.array
        beam_fwhm=toltec_signal_out.beam*abs(hdr['CDELT1'])*3600.
        beam_fwhm=5.*u.arcsec
        sigma = beam_fwhm * gaussian_fwhm_to_sigma 
        sigma_pix=sigma/(abs(self.header['CDELT1'])*3600.)
        kernel=Gaussian2DKernel(sigma.value,mode='center')
        data=self.data
        data_conv=convolve(self.data,kernel=kernel)#,normalize_kernel=False)
        self.convolved=data_conv
        
        return fits.PrimaryHDU(self.convolved,header=self.header)
        
    def reprojectInputToOutput(self,toltec_signal_out):
        
        hdr=toltec_signal_out.headers[1]
        w = WCS(hdr)
        w=w.celestial
        
        reprodata, footprint = reproject_interp(self.convolveInputToOutput(toltec_signal_out), w,shape_out=(hdr['NAXIS2'],hdr['NAXIS1']))
        reprodata=reprodata#.transpose()
        self.reprojected=reprodata
        self.repro_header=hdr
        
        return fits.PrimaryHDU(reprodata,header=hdr)
    
    def writeReproject(self,toltec_signal_out):
        flux_fact=1.e9*abs(toltec_signal_out.headers[1]['CDELT1']*np.pi/180.)**2
        hdurepro=self.reprojectInputToOutput(toltec_signal_out)
        hdurepro.writeto(self.filename.split('.fits')[0]+'_conv_repro.fits',overwrite=True)
        hdu_ratio=fits.PrimaryHDU(hdurepro.data*flux_fact/(toltec_signal_out.getMap('signal_I')*flux_fact),header=toltec_signal_out.headers[1])
        hdu_ratio.writeto('ratio.fits',overwrite=True)
        
        
        
    def inPhot(self,segm_deblend):
      flux_fact=1.e9*abs(self.repro_header['CDELT1']*np.pi/180.)**2
      #flux_fact=tfipj.to_mJyPerBeam/(omega_B.value/abs(hdr['CDELT1'])**2)      
      #print(segm_deblend.shape,self.reprojected.shape)
      cat = SourceCatalog(self.reprojected*flux_fact, segm_deblend)
      
      tblin = cat.to_table()
      self.extPhotTab=tblin 
      return tblin
  
    def plotExtPhot(self,tblout):
        
        plt.figure()
        
        plt.plot(self.extPhotTab['segment_flux'],tblout['segment_flux'],'.',color='black')
        plt.plot(self.extPhotTab['segment_flux'],self.extPhotTab['segment_flux'],color='black')
