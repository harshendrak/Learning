# Chain of Thought prompting
from ollama import Client
import json

client = Client(
   host="http://localhost:11434",
)
# zeroshot prompting= Directly giving the instruction to the model

SYSTEM_PROMPT=""" You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START,PLAN,OUTPUT steps.
You need to first PLAN and what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly Follow the given JSON format
- Only run one step at a time.
-The sequence of steps is START (where user gives an input), PLAN(That can be multiple
times) and finally OUTPUT (which is going to be displayed to the user.)


Output JSON Format:
{"steps":"START"|"PLAN"|"OUTPUT","content":"string"}

Example:
START: Hey, can you solve 2+3*5/10
PLAN:{"step":"PLAN":"content":"Seems like the user is intrested in
 maths problem"}
PLAN:{"step":"PLAN":"content":"Looking at the problem, 
we should solve this using BODMAS method."}
PLAN:{"step":"PLAN":"content":"Yes, the BODMAS is the correct 
thing to be done here."}
PLAN:{"step":"PLAN":"first we should multiply 3*5 which is 15 "}
PLAN:{"step":"PLAN":"Now the equation is 2 + 15/10"}
PLAN:{"step":"PLAN":"we must perform divide that is 15/10 which is 1.5"}
PLAN:{"step":"PLAN":"now the equation is 2+1.5"}
PLAN:{"step":"PLAN":"now finaaly perform the addition which is 3.5"}
PLAN:{"step":"PLAN":"Great! we've solved the problem and left with the answer which is 
3.5"}
PLAN:{"step":"OUTPUT":"3.5"}


"""

response = client.chat(
    model="gemma2:2b",
    format="json",
    # response_format={"type":"json_object"}, only for openai, for ollama we need to manually format the response in json format
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT},
        {   "role": "user",
            "content": input("I can assist you with everything. Just ask :) \n")},
            # Manually keep on adding messeges to history
        { "role": "assistant",
            "content": json.dumps({    
             "steps":"START",
             "content":"Hey, can you write a code to add n numbers in js"}  )
        },
        { "role": "assistant",
            "content": json.dumps({
             "steps": "PLAN", 
            "content": "The user wants a JavaScript function to add 'n' numbers."}  )
        },
        { "role": "assistant",
            "content": json.dumps({
            "steps": "PLAN",
            "content": "I need to define a JavaScript function that can accept a variable number of arguments (n numbers)."
        })
        },
        { "role": "assistant",
            "content": json.dumps(
                {"steps": "PLAN",
                  "content": "I will use the rest parameter (...) to collect all passed arguments into an array."}
            )
        },
        { "role": "assistant",
            "content": json.dumps(
                {"steps": "PLAN", 
                 "content": "Inside the function, I will iterate over the array of numbers and sum them up."}
                
            )
        },
        { "role": "assistant",
            "content": json.dumps(
                {"steps": "PLAN", 
                 "content": "Alternatively, I can use array methods like `reduce` for a more concise solution."}
                
                
            )
        },
        { "role": "assistant",
            "content": json.dumps({
                "steps": "PLAN", 
                "content": "I will provide the JavaScript code for the function, including an example of how to use it."}
                
                
                
            )
        }
    ]
)

print(response.message.content)



