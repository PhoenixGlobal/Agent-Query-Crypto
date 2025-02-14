from flask import Flask, flash, request, redirect, url_for, jsonify, make_response, session
import os
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from datetime import date
import os
from pydantic import BaseModel, Field
import datetime
from tools import *
import typing
import re

#add your own openai key
openai_api_key = ""

import os
os.environ["OPENAI_API_KEY"] = openai_api_key
gpt_4o_mini = ChatOpenAI(model="gpt-4o-mini")


app = Flask(__name__)

#set tools 
def fetch_date(query):
    """return current date"""
    curr_date = "today's date is:" + str(date.today())
    prompt = ChatPromptTemplate.from_messages(
        [("system",curr_date),
        ("system","return the corresponding date in the same format based on user query"),
        ("user","{query}")]
    )
    datechain = prompt | gpt_4o_mini
    return datechain.invoke(query).content

#customer parser
class coin_search(BaseModel):
    """If user input ralated to crpyto,use this tool to extract the key words from the user input"""
    
    coin_name: str = Field(description="the name of the crypto coin(BTC , ETH, SOLANA,etc) mentioned in the query")
    coin_feature :str = Field(description="the current price / market cap / supply info / order book / historical price of the crypto coin mentioned in the query")    
    time_interested: str = Field(description="time mentioned in query")



#bind tools with the model
tools = [coin_search]
gpt_with_tools = gpt_4o_mini.bind_tools([coin_search])

def fetch_related_data(params:dict,timestamp):
    feature = params["coin_feature"]
    coin_name = params["coin_name"]
    if feature == "current price":
        ts = timestamp
        return fetch_coin_price(coin_name,ts)
    if feature == "market cap":
        return fetch_coin_marketcap(coin_name)
    if feature == "supply info":
        return fetch_coin_supply_info(coin_name)
    if feature == "order book":
        return fetch_coin_orderbook(coin_name)
    if feature == "historical price":
        try:
            tw = re.search(r'\d+', params["time_interested"])
            return fetch_coin_historical_price(coin_name,tw)
        except Exception as e:
            print(f"call failed : {e}")
    return None 
        
        

def general_response(request_result,query):
    prompt = ChatPromptTemplate([
    ("system","reply the user query based on the info provided"),
    ("system","{request_res}"),
    ("user","{input}")]
)   

    chain = prompt | gpt_4o_mini
    return chain.invoke({"request_res": request_result,"input": query}).content

@app.route('/response', methods=["GET","POST"])
def response():
    """
    current request body:
    {
        "user_input" : "..."
    }
    """
    chat_model = ChatOpenAI(model="gpt-4o-mini")
    data = request.get_json()
    query = data.get("user_input")
    
    tool_call_info = gpt_with_tools.invoke(query).tool_calls
    if tool_call_info:
        curr_timestamp = int(datetime.datetime.now().timestamp())*1000
        print(curr_timestamp)
        params = tool_call_info[0]["args"]
        res = fetch_related_data(params,curr_timestamp)
        print(res)
        resp = general_response(res,query)
        res_completion = {}
        res_completion["query"] = query
        res_completion["text"] = resp
        res_completion["created"] = curr_timestamp
        return res_completion
        
    else:
        resp = chat_model.invoke(query).content
        res_completion = {}
        res_completion["query"] = query
        # consider change the resp text
        res_completion["text"] = resp
        res_completion["created"] = datetime.datetime.now().timestamp()
        return res_completion



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010)