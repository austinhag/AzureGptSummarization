from openai import AzureOpenAI
import concurrent.futures
import pandas as pd
import time

from env import api_key, azure_endpoint, deployment_name

# Set operating paramters
recover = False  # Recover from prior executions. Requires results.csv file to exist.
throttle = 0   # Set the number of seconds to wait before executing API call in each thread.

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

# Recover from prior execution
processed = {}
if recover:
    df_recover = pd.read_csv("results.csv")
    df_merge = df_logs.merge(df_recover[['Log #',"Summary"]], how="inner", on=['Log #'])
    processed = dict(df_merge[['Log #','Summary']].values)

# Instantiate client
client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version
        )
        
# This is the worker function for multithreading. It calls GPT for an individual call log and returns results
def call_api(call_log):
    logid = call_log[0]
    logtext = call_log[1]
    
    if logid in processed:
        print(f"Summary already processed for log #: {logid}. Using recovered value.")
        text_result = processed[logid]
        return logid, logtext, text_result
    
    print(f"New thread created for log #: {logid}")

    # Sleep if required
    time.sleep(throttle)

    # Call Azure OpenAI and have it process the sample call log
    try:
        response = client.chat.completions.create(
          model = deployment_name,
          messages = [instructions,{"role":"user","content":logtext}],
          temperature = 0
          )
        text_result = response.choices[0].message.content
        print(f"Thread completed for log #: {logid}")
    
        # Return results    
        return([logid, logtext, text_result])
    except:
        print(f"Error processing log #: {logid}")
        return([logid, logtext, "ERROR PROCESSING!"])

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
