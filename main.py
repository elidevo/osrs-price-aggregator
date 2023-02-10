import json, requests, csv

api_url = "https://prices.runescape.wiki/api/v1/osrs"
headers = {'user-agent': 'elidevo-osrs-price-aggregator-python'}

class price_data:
    def __init__(self):
        self.data = {}

    def pull_data(self):
        item_mappings = {}

        res_mapping = requests.get(f"{api_url}/mapping", headers=headers)
        jdata_mapping = json.loads(res_mapping.text)

        res_latest = requests.get(f"{api_url}/latest", headers=headers)
        jdata_latest = json.loads(res_latest.text)

        res_volumes = requests.get(f"{api_url}/volumes", headers=headers)
        jdata_volumes = json.loads(res_volumes.text)

        for item in jdata_mapping:
            item_mappings[item["id"]] = item
            # if not in latest or volumes dont add?? idk

        for id, idict in item_mappings.items():
            try:
                idict["volume"] = jdata_volumes["data"][str(id)]
            except:
                print(f"Problem finding volume data for itemId {str(id)}")

            try:
                idata = jdata_latest["data"][str(id)]

                idict["high"] = idata["high"] # price item is being bought for
                idict["highTime"] = idata["highTime"] # time in unix millis when high price was gathered
                idict["low"] = idata["low"] # price item is being sold for
                idict["lowTime"] = idata["lowTime"] # time in unix millis when low price was gathered

                idict["margin"] = idict["high"] - idict["low"] # margin between high and low prices (PROFIT MARGIN)
            except:
                print(f"Problem finding latest data for itemId {str(id)}, popping?...")
                #item_mappings.pop(key)

        self.data = item_mappings

pdata = price_data()
pdata.pull_data()