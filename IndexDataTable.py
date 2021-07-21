import requests
import json
import pandas as pd
import streamlit as st

response = requests.get("https://indexapi.aws.merqurian.com/index?type=test%2Cprod")
data = json.loads(response.text)
url = ''
dataList = []
dataList2 = []
for result in data['results']:
    id = result['id']
    name = result['name']
    title = result['title']
    url = requests.get("https://indexapi.aws.merqurian.com/index/" + result['id'] + "/metrics/price_return/data")
    data3 = json.loads(url.text)
    result2 = data3['results']
    newLength = len(result2) - 1
    lastObject = result2[newLength]
    last_date = lastObject['id']
    metrics = lastObject['metrics']
    priceObject = metrics[0]
    last_level = priceObject['value']
    productionTable = {}
    nonProductionTable = {}
    if result['stage'] == "prod":
        for variable in ["name", "title", "last_date", "last_level"]:
            productionTable[variable] = eval(variable)
        dataList.append(productionTable)
    else:
        for variable in ["name", "title", "last_date", "last_level"]:
            nonProductionTable[variable] = eval(variable)
        dataList2.append(nonProductionTable)

dataset = st.beta_container()

with dataset:
    st.header("Production Table")
    st.write(pd.DataFrame(dataList))
    st.subheader("Non-Production Table")
    st.write(pd.DataFrame(dataList2))







