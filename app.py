from openai import AzureOpenAI  
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os  
import base64
import json


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})   # allow all origins on /api/*

@app.route("/api/messages", methods=["POST"])
def messages():
    print(f'request...{request}')
    incoming_message = request.json["text"]
    print(f'incoming_message...{incoming_message}')
    
    # Call your Azure OpenAI endpoint
    
    endpoint = "https://ai-s2248968285899ai935042442247.openai.azure.com/"
    deployment ="gpt-4.1"
    subscription_key = "Afqb9cEa2IWbJugldnIBELsknbAOztPr8mnMnA31rbFevlv5VfMdJQQJ99BDACHYHv6XJ3w3AAAAACOGBuoS"
   
    
    # Initialize Azure OpenAI Service client with key-based authentication    
    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2025-01-01-preview",
    )
 
    #Prepare the chat prompt 
    chat_prompt = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{incoming_message}"
                }
            ]
        }
    ] 
    
    # Include speech result if speech is enabled  
    messages = chat_prompt  

    # Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,
        messages=messages,
        max_tokens=800,  
        temperature=1,  
        top_p=1,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )
    
    print(f"completion.json() type: {type(completion.json())}") 
    
    
    resp_dict = json.loads(completion.json())
    response = json.dumps(resp_dict)
    print(f"Response type: {type(response)}") 
    
    data = json.loads(response)
    print(f"data type: {type(data)}") 
    print(data["choices"][0]["message"]["content"])
      
    if 'choices' in data:
        reply = data["choices"][0]["message"]["content"]
    else:
        reply = "No data"
        
    print(f'reply...{reply}')
        
    return jsonify({"text": reply})


@app.route("/", methods=["GET", "POST"])
def root():
    return jsonify({
        "error": "This is the bot endpoint. POST your JSON to /api/messages."
    }), 404

if __name__ == "__main__":
    app.run(port=3978)
