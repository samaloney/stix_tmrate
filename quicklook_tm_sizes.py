"""
Quick look (QL) TM packet size information:

* Light Curve
* Background
* Spectra
* Variance
* Flare flag and location
* Energy Calibration (spectra)
* TM Management status and flare list.

References
----------
STIX TMTC ICD [1]_ contains all the relevant information.


.. [1] STIX Flight Software TM/TC Interface Control Document (ICD), 
   STIX-ICD-0812-ESC, I4R1, 17/09/2019
"""


def light_curve(num_energies, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL light 
    curves
    
    Parameters
    ----------
    num_energies : int
        Number of energies
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                    1*8    # SSID
                    + 4*8  # SCET Coarse time
                    + 2*8  # SCET Fine time
                    + 2*8  # Integration time
                    + 4*8  # Detector mask
                    + 4    # spare
                    + 12   # Pixel mask
                    + 1    # spare
                    + 1    # Comp Schema light curve S
                    + 3    # Comp Schema light curve K
                    + 3    # Comp Schema light curve M
                    + 1    # Comp Schema trigger S
                    + 3    # Comp Schema trigger K
                    + 3    # Comp Schema trigger M
                    + 1    # Energy bin mask upper boundary
                    + 4*8  # Energy bin mask lower boundray
                    + 1*8  # Number of energies
                    + num_energies*2*8 # Number data points
                    + 2*8  # Number of data points
                    + 2*8  # Number of data point
                   )

    variable = (
                + num_energies*num_samples*8  # Compressed light curves
                + num_samples*8               # Compressed triggers
                + num_samples*8               # RCR
               )

    return fixed_header, variable


def background(num_energies, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL background
    
    Parameters
    ----------
    num_energies : int
        Number of energies
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                1*8    # SSID
                + 4*8  # SCET Coarse time
                + 2*8  # SCET Fine time
                + 2*8  # Integration time
                + 1    # Comp Schema background S
                + 3    # Comp Schema background K
                + 3    # Comp Schema background M
                + 1    # Comp Schema trigger S
                + 3    # Comp Schema trigger K
                + 3    # Comp Schema trigger M
                + 1    # Energy bin mask upper boundary
                + 4*8  # Energy bin mask lower boundary
                + 1.   # Spare
                + 1*8  # Number of energies
                + num_energies*2*8  # Number data points
                + 2*8  # Number of data points
               )

    variable = (
            num_energies*num_samples*8  # Compressed background
            + num_samples*8               # Compressed triggers
           )

    return fixed_header, variable

def variance(num_energies, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL variance
    
    Parameters
    ----------
    num_energies : int
        Number of energies
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                1*8    # SSID
                + 4*8  # SCET Coarse time
                + 2*8  # SCET Fine time
                + 2*8  # Integration time
                + 1*8  # Samples per variance
                + 4*8  # Detector mask
                + 4*8  # Energy mask
                + 4    # Spare
                + 12   # Pixel mask
                + 1    # Spare
                + 1    # Comp Schema variance S
                + 3    # Comp Schema variance K
                + 3    # Comp Schema variance M
                + 2*8  # Number of data points
               )

    variable = (
            num_samples*1*8. # Number data points
           )

    return fixed_header, variable

def spectra(num_energies, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL spectra
    
    Parameters
    ----------
    num_energies : int
        Number of energies
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                1*8    # SSID
                + 4*8  # SCET Coarse time
                + 2*8  # SCET Fine time
                + 2*8  # Integration time
                + 1    # Spare
                + 1    # Comp Schema spectra S
                + 3    # Comp Schema spectra k
                + 3    # Comp Schema spectra M
                + 1    # Spare
                + 1    # Comp Schema trigger S
                + 3    # Comp Schema trigger S
                + 3    # Comp Schema trigger S
                + 4    # Spare
                + 12   # Pixel mask
                + 2*8  # Number of data samples
        )

    variable = (
            num_samples * (
                    1*8     # Detector index
                    + 32*8  # Spectrum x 32
                    + 1*8   # Trigger
                    + 1*8   # Number of integrations
                )
        )

    return fixed_header, variable

def flare_flag_location(num_energies, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL flare 
    flag and location.
    
    Parameters
    ----------
    num_energies : int
        Number of energies
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                1*8    # SSID
                + 4*8  # SCET Coarse time
                + 2*8  # SCET Fine time
                + 2*8  # Integration time
                + 2*8  # Number of data samples
        )

    variable = (
            num_samples * (
                    1*8   # Flare
                    + 1*8 # Flare location z (arcmin)
                    + 1*8 # Flare locatoin y (arcmin)
                )
        )

    return fixed_header, variable

def flarelist_tm_mgmt(_, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL TM 
    Management and flare list
    
    Parameters
    ----------
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                1*8   # SSID
                + 4*8 # UBSD counter
                + 4*8 # PALD counter
                + 2*8 # Number of flares
        )

    variable = (
            num_samples * (
                    4*8   # Start time 
                    + 4*8 # End time
                    + 1*8 # highest flare flag
                    + 4*8 # TM byte volume
                    + 1*8 # Avg z location
                    + 1*8 # Avg Y location
                    + 1*8 # Processing status 
                )
        )

    return fixed_header, variable

def calibration_spectra(num_energies, num_samples):
    """
    Return the fixed overhead and variable data structure size for QL
    energy calibration spectra
    
    Parameters
    ----------
    num_energies : int
        Number of energies
    num_samples : int
        Number of data samples
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed_header = (
                1*8    # SSID
                + 4*8  # SCET Coarse time
                + 4*8  # Duration
                + 2*8  # Quiet time
                + 4*4  # Live time
                + 2*8  # Avg Temperature
                + 1    # Spare
                + 1    # Comp Schema accum S
                + 3    # Comp Schema accum K
                + 3    # Comp Schema accum M
                + 4*8  # Detector mask
                + 4    # Spare
                + 12   # Pixel mask
                + 1*8  # Sub spectrum mask
                + 2    # Spare
                + 8*( # 8 x 
                        2     # Spare
                        + 10  # Number of spectral points
                        + 10  # Number of summed channels in spectral point
                        + 10  # Lowest channel in sub spectrum 
                    )
                + 2*8 # Number of structure in packet
        )

    variable = (
            num_samples * (
                        4     # Spare
                        + 5   # Detector ID
                        + 4   # Pixel ID
                        + 3   # Sub spec ID
                        + 16  # Number of compressed spectral points
                        + num_energies*1*8 # Compressed spectral point

                )
        )

    return fixed_header, variable
