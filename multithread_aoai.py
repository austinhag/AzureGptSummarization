from openai import AzureOpenAI
import concurrent.futures
import pandas as pd

from env import api_key, azure_endpoint, deployment_name

# Set calling API version
api_version = "2023-05-15"

# Set max number of threads to create
max_workers = 5

# Set core instructions for GPT
instructions = {"role":"system",
                 "content":'''You are charged with reviewing calls for a banking service center. Please review the call log below and provide the following three elements: 
                     #1 - Summarize the call in one sentence, 
                     #2 - Categorize the call using a category of your choosing,
                     #3 - Indicate whether the caller's issue was resolved or not. Use Resolved or Unresolved to indicate the same.
                     Provide this information in separate lines with clear field names.'''}

# Import call logs from CSV
df_logs = pd.read_csv("sample_logs.csv")
                     
# This is the worker function for multithreading. It calls GPT for an individual call log and returns results
def call_api(call_log):
    print(f"New thread created for log #: {call_log[0]}")
    client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version
            )

    # Call Azure OpenAI and have it process the sample call log
    response = client.chat.completions.create(
      model = deployment_name,
      messages = [instructions,{"role":"user","content":call_log[1]}],
      temperature = 0
      )
    text_result = response.choices[0].message.content
    print(f"Thread completed for log #: {call_log[0]}")
    
    # Return results    
    return([call_log[0],call_log[1], text_result])

# Main function. Runs and manages multithreading and coordination of results
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(call_api, [row['Log #'],row['Log Text']]) for index, row in df_logs.iterrows()]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")
    
    # Compile results in Pandas dataframe
    results = []
    for f in futures:
        results.append(f.result())
    df_results = pd.DataFrame(results,columns=['Log #','Log Text','Summary'])

    # Save results to CSV
    df_results.to_csv("results.csv",index=False)
    print("Processing completed and results saved.")
                    
if __name__ == "__main__":
    main()    
