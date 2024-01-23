from openai import AzureOpenAI
from env import api_key, azure_endpoint, deployment_name

# Documentation on the API: https://learn.microsoft.com/en-us/azure/ai-services/openai/

# Set calling API version
api_version = "2023-05-15"

# Create Azure OpenAI object
client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version
    )

# Sample call log - This sample was generated via ChatGPT. :-)
call_logs = [['''
             John Doe: "Good morning, thank you for calling ABC Bank. This is John speaking. How can I assist you today?"

            Caller: "Hi, I just wanted to check the balance on my savings account, please."
            
            John Doe: "Certainly! May I have your account number and the name on the account for verification?"
            
            Caller: "[Provides account information]"
            
            John Doe: "Thank you. I see your current balance is $3,250. There was a recent transaction of $150 on January 20th. Would you like more details on this?"
            
            Caller: "No, that's fine. I just wanted to make sure my paycheck was deposited. Thanks for your help!"
            
            John Doe: "You're welcome! Is there anything else I can assist you with?"
            
            Caller: "No, that's all for now."
            
            John Doe: "Great! Have a wonderful day. Thank you for calling ABC Bank.''',
             ]]

# Call Azure OPI and have it process the sample call log
response = client.chat.completions.create(
  model = deployment_name,
  messages = [{"role":"system",
                   "content":'''You are charged with reviewing calls for a banking service center. Please review the call log below and provide the following three elements: 
                       #1 - Summarize the call in one sentence, 
                       #2 - Categorize the call using a category of your choosing,
                       #3 - Indicate whether the callers issue was resolved or not. Use Resolved or Unresolved to indicate the same.
                       Provide this information in separate lines with clear field names.'''},
               {"role":"user",
                    "content":call_logs[0][0]}]
  )
text_result = response.choices[0].message.content

print(text_result)
