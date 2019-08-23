import requests
from datetime import datetime
import time
import os.path


def get_measurements(measurement_id, start, stop, probe_ids=[]):
    """Load RIPE NCC measurements.

    Keyword arguments:
    measurement_id -- id of the measurement
    start -- start date formated as 'DD/MM/YYYY',  e.g '01/12/2018'
    stop -- stop date formated as 'DD/MM/YYYY',  e.g '05/12/2018'
    probe_ids -- list of probe ids

    Returns: Required measurements in JSON format
    """
    def to_unix_time(d):
        return int(time.mktime(datetime.strptime(d, '%d/%m/%Y').timetuple()))

    start, stop = map(to_unix_time, [start, stop])
    probe_ids = ','.join(str(x)
                         for x in probe_ids) if len(probe_ids) > 0 else None
    url_base = 'https://atlas.ripe.net/api/v2/measurements/{}/results/?start={}&stop={}&probe_ids={}'
    url = url_base.format(measurement_id, start, stop, probe_ids)
    print('Fetching data from:\n' + url)
    r = requests.get(url)
    return r.json()


def get_probes(probes_id=[]):
    """Load RIPE NCC probes description.

    Keyword arguments:
    probe_ids -- list of probe ids

    Returns: Required probes description in JSON format
    """
    url_probe = 'https://atlas.ripe.net:443/api/v2/probes/?id__in=' + \
        str(probes_id)[1:-1] + '&page_size=500'

    r_probe = requests.get(url_probe)
    return r_probe.json()


def df_to_csv(df, prefix_name="dump", folder="data"):
    """Save dataframe to csv

    Keyword arguments:
    df -- dataframe to be saved
    prefix_name -- prefix name to be used in front of current date 
    folder -- base folder
    """
    base_filename = prefix_name + "-" + datetime.now().strftime('%Y-%m-%d')
    df.to_csv(os.path.join(folder, base_filename + '.csv'), index=False)
