#!/usr/bin/env python3

from vast.api import VastAPI
from pprint import pprint as pp
from math import ceil

# VastAPI.set_api_key(KEY)
api = VastAPI()
dictQuery = {}
# 'reliability > 0.95  num_gpus=1 inet_down>40 inet_up>40 rentable=True verified=True total_flops>10 dlperf>9' -o 'dlperf_usd'

# Define minimum acceptable benchmarks here
dictQuery['reliability'] = '>0.95'
dictQuery['num_gpus'] = "=1"
dictQuery['cpu_cores_effective'] = '>=5.9'
dictQuery['total_flops'] = '>10'
dictQuery['inet_down'] = '>=40'
dictQuery['inet_up'] = '>=40'
dictQuery['dlperf'] = '>9'
dictQuery['disk_space'] = '>=20'
dictQuery['rentable'] = "=True"
# dictQuery['rented'] = False
dictQuery['verified'] = "=True"

# Generate query string
# strQuery = 'reliability > 0.95  num_gpus=1 inet_down>40 inet_up>40 rentable=True rented=False verified=True total_flops>10 dlperf>9 disk_space>20'
strQuery = str(' '.join(['%s%s' % (key, value) for (key, value) in dictQuery.items()]))

# Query the Vast.ai server for biddable instances which match the search filters
lstOfferDicts = api.search_offers(raw=True, max_rows=1000, order="dlperf_usd-", query_type="interruptible",
                                  query=str(strQuery))
# api.search_offers(max_rows=1000, order="dlperf_usd-", query_type="on-demand", query='reliability > 0.95  num_gpus=1 inet_down>40 inet_up>40 rentable=True rented=False verified=True total_flops>10 dlperf>9 disk_space>20')
#pp(lstOfferDicts)

def find_best_instance(lstOfferDicts, dictBids={}):
    for dictOffer in lstOfferDicts:
        dictBids[dictOffer['id']] = dictOffer['dlperf'] / dictOffer['min_bid']
    return max(dictBids, key=dictBids.get)

strBestInstance = find_best_instance(lstOfferDicts)

dictBestInstance = next(item for item in lstOfferDicts if item["id"] == strBestInstance)
## Uncomment to print all information returned by the vast.ai API on the most economical instance.
pp(dictBestInstance)
pp(dictBestInstance['min_bid'])

image = "rcko/deeplabcut-2.1_tensorflow-1.1.3-gpu"
floatBid = ceil(dictBestInstance['min_bid'] * 1000.0) / 1000

api.create_instance(id='352307', image=image, price=0.076, label=None, disk=20, create_from_id=None,
                        runtype='ssh', onstart=~/startup.sh, onstart_cmd=None,
                        use_jupyer_lab=False, jupyter_dir=None,
                        python_utf8=False, force=False,  extra=None)

# api.create_instance(strBestBid, rcko/deeplabcut-2.1_tensorflow-1.1.3-gpu,