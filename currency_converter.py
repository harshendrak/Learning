
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import requests
from dotenv import load_dotenv
load_dotenv()

# tools creation
@tool
def multiply(a:int, b:int) -> int:
    """ multiply given two numbers """
    return a*b

# tool binding
llm=ChatGoogleGenerativeAI(model="gemma-4-31b-it")
llm_with_tools=llm.bind_tools([multiply])

llm_with_tools.invoke('Hi how are you')

query=HumanMessage('Can you multiply 5 and 3')

messages=[query]


result=llm_with_tools.invoke(messages)

messages.append(result)#type:ignore



tool_result=multiply.invoke(result.tool_calls[0])

messages.append(tool_result)

llm_with_tools.invoke(messages).content

"""tool creation"""

from langchain_core.tools import InjectedToolArg
from typing import Annotated
@tool
def get_conversion_factor(base_currency:str,target_currency:str)->float:
  """This function fethches the  currency conversion factor
  between a given base currency and a target currecy"""
  url=f"https://v6.exchangerate-api.com/v6/2c1af2eacac4b1280ca84f60/pair/{base_currency}/{target_currency}"

  response=requests.get(url)
  return response.json()

@tool
def convert(base_currency_value:int,conversion_rate:Annotated[float,InjectedToolArg])->float:
  """given a currency conversion rate this function calculates the target currency value from a given base currency value."""
  return base_currency_value*conversion_rate

get_conversion_factor.invoke({'base_currency':'USD','target_currency':'INR'})

convert.invoke({'base_currency_value':19,'conversion_rate':95.3548})

# tool binding
llm=ChatGoogleGenerativeAI(model="gemma-4-31b-it")

llm_with_tools=llm.bind_tools([get_conversion_factor,convert])

messages=[HumanMessage("What is the conversion factor between USD and INR, and how much is 50 USD in INR?")]

ai_message=llm_with_tools.invoke(messages)
messages.append(ai_message)#type:ignore

import json
for tool_call in ai_message.tool_calls:
  if tool_call['name']=='get_conversion_factor':
    tool_message1=get_conversion_factor.invoke(tool_call)
    conversion_rate=json.loads(tool_message1.content)['conversion_rate']
    messages.append(tool_message1)

  if tool_call['name']=='convert':
    # fetch the current arguments
    tool_call['args']['conversion_rate']=conversion_rate
    tool_message2=convert.invoke(tool_call)
    messages.append(tool_message2)

# 1. Send the updated history back to the LLM
ai_message_2 = llm_with_tools.invoke(messages)
messages.append(ai_message_2)#type:ignore

# 2. Check if it wants to call the 'convert' tool now
for tool_call in ai_message_2.tool_calls:
    if tool_call['name'] == 'convert':
        tool_call['args']['conversion_rate'] = conversion_rate
        tool_message2 = convert.invoke(tool_call)
        messages.append(tool_message2)

# 3. Get the final text summary
final_response = llm_with_tools.invoke(messages)
print(final_response.content)