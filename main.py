import json, requests, csv, pandas

api_url = "https://prices.runescape.wiki/api/v1/osrs"
headers = {'user-agent': 'elidevo-osrs-price-aggregator-python'}

class price_data:
    def __init__(self):
        self.__data = {}

    def pull_data(self):
        item_mappings = {}

        res_mapping = requests.get(f"{api_url}/mapping", headers=headers)
        jdata_mapping = json.loads(res_mapping.text)

        res_latest = requests.get(f"{api_url}/latest", headers=headers)
        jdata_latest = json.loads(res_latest.text)

        res_volumes = requests.get(f"{api_url}/volumes", headers=headers)
        jdata_volumes = json.loads(res_volumes.text)

        for idict in jdata_mapping:
            try:
                idict["volume"] = jdata_volumes["data"][str(idict["id"])]
            except:
                print("Problem finding volume data for itemId {}".format(idict["id"]))

            try:
                idata = jdata_latest["data"][str(idict["id"])]

                idict["high"] = idata["high"] # price item is being bought for
                idict["highTime"] = idata["highTime"] # time in unix millis when high price was gathered
                idict["low"] = idata["low"] # price item is being sold for
                idict["lowTime"] = idata["lowTime"] # time in unix millis when low price was gathered

                idict["margin"] = idict["high"] - idict["low"] # margin between high and low prices (PROFIT MARGIN)
            except:
                print("Problem finding latest data for itemId {}, popping?...".format(idict["id"]))
                #item_mappings.pop(key)

        self.__data = pandas.DataFrame.from_dict(jdata_mapping)

    def get_data(self):
        return self.__data

pdata = price_data()
pdata.pull_data()

pdata.get_data().to_excel("data_output.xlsx")
