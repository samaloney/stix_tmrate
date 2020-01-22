"""
Bulk Science Data TM packet size information

* X-ray data
  * L0 data compression - no compression
  * L1 data compression - triggers and combined pixel counts compressed to 1 octet
  * L2 data compression - triggers and total pixels counts compress to 1 octet
  * L3 data compression - counts transformed to visibilities  
* Spectrum
* Aspect

References
----------
STIX TMTC ICD [1]_ contains all the relevant information


.. [1] STIX Flight Software TM/TC Interface Control Document (ICD), 
   STIX-ICD-0812-ESC, I4R1, 17/09/2019

Attributes
----------
COMMON_XRAY_USER : int
    Common header overhead for user defined xray data (L0,L1,L2,L3)

"""


# Common fixed header size for all user x-ray data
COMMON_XRAY_USER = (
        # 14      # Source sequence count
        # + 16    # Packet data field length -1
        # + 1     # spare
        # + 3     # PUS version (0)
        # + 4     # Spare
        # + 8     # Service Type (21) 
        # + 8     # Service Subtype (6)
        # + 8     # Destination ID (0)
        # + 32    # SCET Coarse time
        # + 16    # SCET Fine time
        + 8     # SSID (20, 21, 22, 23, 24)
        + 16    # Reference to user TC packet ID
        + 16    # Reference to user TC packet sequence control
        + 32    # Unique data request number
        + 1     # Spare
        + 1     # Compression Schema Accumulators S
        + 3     # Compression Schema Accumulators K
        + 3     # Compression Schema Accumulators M
        + 1     # Spare
        + 1     # Compression Schema Triggers S
        + 3     # Compression Schema Triggers K
        + 3     # Compression Schema Triggers M
        + 48    # SCET of first data sample
        + 16    # Number of samples N
    )


def xray_level0(num_samples):
    """
    Return the fixed overhead and variable data structure size for level 0 
    x-ray data.
    
    Parameters
    ----------
    num_samples : int
        Number of data samples
    
    References
    ----------
    
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    
    """
    fixed = (
        2*8     # Starting time
        + 1*8   # RCR
        + 2*8   # Integration time
        + 4     # Spare
        + 12    # Pixel mask
        + 32    # Detector mask
        + (
            15*8 # Trigger accumulators 
            )
        + 2*8 # Number of samples (M)
        )

    variable = (
        num_samples * (
            4       # Pixel ID
            + 5     # Detector Index
            + 5     # Energy ID
            + 2     # Continuation Bits
            + 2*8   # Assume worst case 2 bytes for counts
            )
        )

    return fixed, variable


def xray_level1(num_pixel_sets, num_energy_groups, num_detector_masks):
    """
    Return the fixed overhead and variable data structure size for level 0 
    x-ray data.
    
    Parameters
    ----------
    num_pixel_sets : int
        Number of pixels
    num_energy_groups : int
        Number of energies
    num_detector_masks : int
        Number of detector mask
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed = (
        2*8     # Starting time
        + 1*8   # RCR
        + 1*8   # Number of pixel sets P
        + num_pixel * (
            4       # Spare
            + 12    # Pixel mask for set P
            )
        + 32    # M detector masks
        + 2*8   # Integration time
        + (
            15*8    # Trigger Accumulators
            )
        + 1*8   # Number of Energies
        )

    variable = (
        num_energies * (
                3       # Spare
                + 5     # E1 low bound
                + 3     # Spare
                + 5     # E2 high bound
                + 16    # Number of data elements 
                + num_pixel_sets * num_detector_masks * 8 # Compressed counts
            )
        )

    return fixed, variable

def xray_level2(num_pixel_sets, num_energy_groups, num_detector_masks):
    """Summary
    Return the fixed overhead and variable data structure size for level 2 
    x-ray data.

    Level 1 and level 2 use the same data structure so just a wrapper around
    the level 1 structure
    
    Parameters
    ----------
    num_pixel_sets : int
        Number of pixels
    num_energy_groups : int
        Number of energies
    num_detector_masks : int
        Number of detector mask
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    return xray_level1(num_pixel_sets, num_energy_groups, num_detector_masks)


def xray_level3(num_pixel_sets, num_energy_groups, num_detector_masks):
    """
    Return the fixed overhead and variable data structure size for level 3 
    x-ray data.
    
    Parameters
    ----------
    num_pixel_sets : int
        Number of pixels
    num_energy_groups : int
        Number of energies
    num_detector_masks : int
        Number of detector mask
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    
    """
    fixed = (
        2*8     # Starting time
        + 1*8   # RCR
        + 1*8   # Duration
        + 4     # Spare
        + 12    # Pixel mask 1
        + 4     # Spare
        + 12    # Pixel mask 2
        + 4     # Spare
        + 12    # Pixel mask 3
        + 4     # Spare
        + 12    # Pixel mask 4
        + 4     # Spare
        + 12    # Pixel mask 5
        + 32    # Detector mask
        + (
            15*8    # Trigger Accumulators
            )
        + 1*8   # Number of energy groups
        )

    variable = (
        num_energies * (
                3       # Spare
                + 5     # E1 low bound
                + 3     # Spare
                + 5     # E2 high bound
                + 8     # Flux
                + 8     # Number of detectors N
                num_detector_masks * (
                    8   # Detector ID
                    + 8 # Real visibility component
                    + 8 # Imaginary visibility component
                    )
            )
        )

    return fixed, variable


def spectrogram(num_samples, num_energies):
    """
    Return the fixed overhead and variable data structure size for spectrogram 
    x-ray data.
    
    Parameters
    ----------
    num_samples : int
        Number of spectrogram sample of time
    num_energies : int
        Number of energies
    
    Returns
    -------
    tuple
        Fixed and variable size in bits
    """
    fixed = (
        4       # Spare
        + 12    # Pixel mask
        + 4*8   # Detectors mask
        + 1*8   # RCR
        + 1     # Spare
        + 5     # Emin
        + 5     # Emax
        + 5     # E unit
        + 2*8   # Number of samples N
        + 2*8   # Closing time offset
        )

    variable = (
        num_samples * (
            2*8     # Delta time
            + 1*8     # Compress combined trigger count
            + 1*8     # Number of energies M
            + num_energies * 8
            )
        )

    return fixed, variable


def aspect(num_samples):
    """
    Return the fixed overhead and variable data structure size for aspect data
    
    Parameters
    ----------
    num_samples : int
        Number of Samples 
    
    Returns
    -------
    TYPE
        Fixed and variable size in bits
    """
    fixed = (
        1*8     # SSID
        + 4*8     # SCET Coarse time
        + 2*8     # SCET Fine time
        + 1*8     # Summing value
        + 2*8     # Number of samples N
    )

    variable = (
        num_samples * (
            2*8     # ChA diode 0 voltage
            2*8     # ChA diode 1 voltage
            2*8     # ChB diode 0 voltage
            2*8     # ChB diode 1 voltage
            ) 
        )

    return fixed, variable
