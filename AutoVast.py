#!/usr/bin/env python3

from vast.api import VastAPI
from pprint import pprint as pp

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

def find_best_bid(lstOfferDicts, dictBids={}):
    for dictOffer in lstOfferDicts:
        dictBids[dictOffer['id']] = dictOffer['dlperf'] / dictOffer['min_bid']
    return max(dictBids, key=dictBids.get)

strBestBid = find_best_bid(lstOfferDicts)

## Uncomment to print all information returned by the vast.ai API on the most economical instance.
#pp(next(item for item in lstOfferDicts if item["id"] == strBestBid))