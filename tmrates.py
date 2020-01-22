from math import ceil 

from quicklook_tm_sizes import light_curve, background, variance, spectra, \
    flare_flag_location, flarelist_tm_mgmt, calibration_spectra

# Packet size data in bis
PACKET_DEF = {
    'header': 6*8,
    'data-header': 10*8,
    'data': 4096*8
}

def calculate_tm_rate(product, num_energies, integration_time):
    fixed, variable = product(num_energies, 1)
    num_data = 24 * 60 * 60 / integration_time
    if not num_data.is_integer():
        raise ValueError('Integration time expected to be evenly divisible into'
                         'number of second in a day') 

    packet_space = PACKET_DEF['data'] - fixed

    # number of full data blocks to fit in available packet space 
    data_per_packet, rem = divmod(packet_space, variable)

    # Total number of packets (if not full sent next day)
    num_packets = num_data / data_per_packet
 
    total_size = num_packets * (fixed + data_per_packet*variable)

    print('''{}: Packet Size: {}, Fixed Header: {}, Remaining: {},
        Sample size {}, Samples per packet: {}, Free {},
        No. packets {}'''.format(product.__name__, PACKET_DEF['data'], fixed,
            packet_space, variable, data_per_packet, rem, num_packets))

    return total_size

def run():
    res = {
        'lc': calculate_tm_rate(light_curve, 5, 4)/(24*60*60),
        'bg': calculate_tm_rate(background, 5, 8)/(24*60*60),
        'sp': calculate_tm_rate(spectra, 32, 32)/(24*60*60),
        'var': calculate_tm_rate(variance, None, 4)/(24*60*60),
        'ff': calculate_tm_rate(flare_flag_location, None, 8)/(24*60*60),
        'ftm': calculate_tm_rate(flarelist_tm_mgmt, None,288)/(24*60*60),
        'cal': calculate_tm_rate(calibration_spectra, 64, 56.25)/(24*60*60)
        }

    for k, v in res.items():
        print(k, v)
    print(sum(res.values()))

if __name__ == "__main__":
    run()