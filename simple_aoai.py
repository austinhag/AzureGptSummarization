from openai import AzureOpenAI
from env import api_key, azure_endpoint, api_version, deployment_name

# Documentation on the API: https://learn.microsoft.com/en-us/azure/ai-services/openai/

# Create Azure OpenAI object
client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version
    )
deployment_name = deployment_name

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
                   "content":"Please summarize the following call log and categorize it as resolved or unresolved."},
               {"role":"user",
                    "content":call_logs[0]}]
  )
text_result = response.choices[0].message.content

print(text_result)
