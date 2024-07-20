
from dotenv import load_dotenv
import openai
import time
import logging



# load_dotenv()

# client = openai.OpenAI()

# model = "gpt-4o"  
# file_codeinterpreter=[]
# filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Base_Data.csv"
# file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
# file_codeinterpreter.append(file_object.id)
# filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Licensing.csv"
# file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
# file_codeinterpreter.append(file_object.id)
# filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Product Usage Data.csv"
# file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
# file_codeinterpreter.append(file_object.id)
# filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Tickets.csv"
# file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
# file_codeinterpreter.append(file_object.id)

# # file_retrieve=[]
# # filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Base_Data.csv"
# # file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
# # file_retrieve.append(file_object.id)

# assistant = client.beta.assistants.create(
#     name="CPQ COPILOT",
#     instructions="""You are an assistant named rowan.
# You are interacting with the a user.

# Remember very important !!! 
# #Base Data csv has file id "file-X1AR8GJ6UgEFIoUhfyEUt0ZQ"
# #Tickets csv has file id "file-RzDgMaFytkTCDTE2KJKgIrTc"
# #Licensing csv has file id "file-KOFGR8f6NJlAcVS9VlQDLxIV"
# # Product usage  data csv has file id "file-od7CeARSzlQTtjbQbauHCyue"
# #Norfolk consulting pdf is stored in vector store with id 
# 'vs_nAymwvuhEZbYrHLS0YCbzWrg'
# Base Data csv : This file includes columns for details of company and company's representative with details about contract of company such as name, Company, Primary Contact, ARR, Existing Contract Start Date, Existing Contract End Date, Renewal Date, Renewal ARR, Renewal Stage, Renewal Rep, Renewals Geo.

#  Tickets  csv: This file encompasses columns related to tickets or issue raised by company, including Date Creaated, Ticket ID, SubjectTicket Status, Ticket Severity,Module, Company name.

# Licensing csv: This file contains columns detailing  of  Licenses a company can acquire for services as Licenses Types,Definition,Duration  .

# Product usage  data csv: This file provides details of columns regarding company usage of  service including Name,Primary Contact,Active Licenses, ARR, Health.
# Norfolk Consulting pdf: This file provides the detail 
# for quoting cost yearwise.

# you as rowan have multiple objectives

# Remember before anything you need to know which Objective to trigger.
# So select one of the objective according to user's query and follow the steps under the Objective.


# Trigger Objective 1 if user is asking any general queries regarding "renewal date approaching in three months" from Quoting Automation- Base Data csv.
# Trigger objective 2 if user queries "Summarise (Company name)".
# Trigger Objective 3 if user queries "Create a Quote for   "
 
# #Objective - 1 :  To answer queries of the users regarding which are Base Data


# Mostly use pandas library to give the answers from the csvs.

# steps to take for objective 1:
# 1) understand the users question
# 2) search each csv with file id "file-ImqWxmKEVbjEkgLq2gnJTKCz"
# 4) generate python code with pandas on the  csv  to answer the query of the user
# 5) see the results of the code , if the result is wrong then repeat the above steps
# 6)if the result seems right the tell the user.
# #Remember if user asks to give details about a company search relevant column and dont attempt to search all at once

# #Examples for objective 1
# #user: Give me details of renewal dates approaching in three months
# #steps: 
# #first start from one csv.
# #think about the relevant column or columns , here the relevant column is "Renewal Date"
# #search relevant column with the dates near in three months from today
# #Return the whole row of dates found relevant in the response


# #Objective - 2:  To answer query  Summary for company

# Mostly use pandas library to give the answers from the csvs.

# steps to take for objective 2:
# 1) understand the users question and understand the name of company and you will extract everything based on that company
# 2) search each csv with file name Quoting Automation - Base Data.csv, Quoting Automation - Product Usage Data (1).csv, Tickets.csv.
# 3) Compile Name,Primary Contact,ARR,Existing Contract Start Date,Existing Contract end date
# from Quoting Automation - Base Data.csv corresponding to company name
# 4)Compile Active Licenses,Usage Percentage YoY from Quoting Automation - Product Usage Data (1).csv
# corresponding to company name

# 5)Calculate the number of Tickets by specific company by calculating number of rows does the same company name repeated in Tickets.csv
# 6)Compile the above fields in a table described above in 3,4,5 points in a single table corresponding to company name
# 7) generate python code with pandas on the  csv  to answer the query of the user.

# 8) see the results of the code , if the result is wrong then repeat the above steps
# 9)if the result seems right the tell the user.
# 10) I want data compiled over a single row which also contains the number of Tickets
# #Remember if user asks to give details about a company search relevant column and dont attempt to search all at once
# #Examples for objective 2
# #user: Give me details of renewal dates approaching in three months
# #steps: 
# #first start from one csv.
# #think about the relevant column or columns , here the relevant columns are Name,Primary Contact,ARR,Existing Contract Start Date,Existing Contract end date,Active Licenses,Usage Percentage YoY,Number of Tickets
# #Get the values for theses column from the three csv files Quoting Automation - Base Data.csv, Quoting Automation - Product Usage Data (1).csv, Tickets.csv respectively

# #Return the whole row of data found relevant in the response

# #Objective 3-To answer query 'Create a Quote for Norfolk Consulting '

# Mostly use pandas library to give the answers from the
# Norfolk Consulting pdf.
# steps to take for objective 3:
# 1)understand the users question
# 2)**Read the Document:**
#    - Access the file `Norfolk Consulting.pdf` stored in the vector store with id - 'vs_nAymwvuhEZbYrHLS0YCbzWrg'.
#    - Locate and read the sections related to the subscription services and fees for Year 2.

# 3) **Extract Relevant Information:**
#    - Identify and extract the subscription service fees, including platform fees, base transaction fees, and support fees for Year 2.
#    - Ensure to include any additional fees mentioned for Year 2.

# 4)**Create the Quote:**
#    - Use the extracted information to create a detailed quote for Year 2.
#    - The quote should include the following:
#      - Platform Fee
#      - Base Transaction Fee
#      - Support Fees
#      - Any other applicable fees
# """,
   
#     model=model,
#      tools=[{"type": "code_interpreter"}],
#   tool_resources={
#     "code_interpreter": {
#       "file_ids": file_codeinterpreter
#     }
#   }
# )


# assis_id = assistant.id
# print(assis_id)

# message = "get me details regarding company's which renewable date is approaching"

# thread = client.beta.threads.create()
# thread_id = thread.id
# print(thread_id)

# message = client.beta.threads.messages.create(
#     thread_id=thread_id, role="user", content=message
# )

# # == Run the Assistant
# run = client.beta.threads.runs.create(
#     thread_id=thread_id,
#     assistant_id=assis_id,
#     instructions="You are rowan an ai assistant",
# )


# def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
#     """
#     Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
#     :param thread_id: The ID of the thread.
#     :param run_id: The ID of the run.
#     :param sleep_interval: Time in seconds to wait between checks.
#     """
#     while True:
#         try:
#             run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
#             if run.completed_at:
#                 elapsed_time = run.completed_at - run.created_at
#                 formatted_elapsed_time = time.strftime(
#                     "%H:%M:%S", time.gmtime(elapsed_time)
#                 )
#                 print(f"Run completed in {formatted_elapsed_time}")
#                 logging.info(f"Run completed in {formatted_elapsed_time}")
#                 messages = client.beta.threads.messages.list(thread_id=thread_id)
#                 last_message = messages.data[0]
#                 response = last_message.content[0].text.value
#                 print(f"Assistant Response: {response}")
#                 break
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving the run: {e}")
#             break
#         logging.info("Waiting for run to complete...")
#         time.sleep(sleep_interval)



# wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
# print(f"Run Steps --> {run_steps.data[0]}")
def createassis():
    
  load_dotenv()

  client = openai.OpenAI()

  model = "gpt-4o"  
  file_codeinterpreter=[]
  filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Base_Data.csv"
  file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
  file_codeinterpreter.append(file_object.id)
  filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Licening.csv"
  file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
  file_codeinterpreter.append(file_object.id)
  filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Product Usage Data.csv"
  file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
  file_codeinterpreter.append(file_object.id)
  filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Tickets.csv"
  file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
  file_codeinterpreter.append(file_object.id)

  # file_retrieve=[]
  # filepath ="F:/intern/streamlit 2/STREAMLIT_ASSISTANT/Base_Data.csv"
  # file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
  # file_retrieve.append(file_object.id)

  assistant = client.beta.assistants.create(
      name="CPQ COPILOT",
      instructions="""You are an assistant named rowan.
  You are interacting with the a user.

  Remember very important !!! 
  #Base Data csv has file id "file-X1AR8GJ6UgEFIoUhfyEUt0ZQ"
  #Tickets csv has file id "file-RzDgMaFytkTCDTE2KJKgIrTc"
  #Licensing csv has file id "file-KOFGR8f6NJlAcVS9VlQDLxIV"
  # Product usage  data csv has file id "file-od7CeARSzlQTtjbQbauHCyue"
  #Norfolk consulting pdf is stored in vector store with id 
  'vs_nAymwvuhEZbYrHLS0YCbzWrg'
  Base Data csv : This file includes columns for details of company and company's representative with details about contract of company such as name, Company, Primary Contact, ARR, Existing Contract Start Date, Existing Contract End Date, Renewal Date, Renewal ARR, Renewal Stage, Renewal Rep, Renewals Geo.

  Tickets  csv: This file encompasses columns related to tickets or issue raised by company, including Date Creaated, Ticket ID, SubjectTicket Status, Ticket Severity,Module, Company name.

  Licensing csv: This file contains columns detailing  of  Licenses a company can acquire for services as Licenses Types,Definition,Duration  .

  Product usage  data csv: This file provides details of columns regarding company usage of  service including Name,Primary Contact,Active Licenses, ARR, Health.
  Norfolk Consulting pdf: This file provides the detail 
  for quoting cost yearwise.

  you as rowan have multiple objectives

  Remember before anything you need to know which Objective to trigger.
  So select one of the objective according to user's query and follow the steps under the Objective.


  Trigger Objective 1 if user is asking any general queries regarding "renewal date approaching in three months" from Quoting Automation- Base Data csv.
  Trigger objective 2 if user queries "Summarise (Company name)".
  Trigger Objective 3 if user queries "Create a Quote for   "
  
  #Objective - 1 :  To answer queries of the users regarding which are Base Data


  Mostly use pandas library to give the answers from the csvs.

  steps to take for objective 1:
  1) understand the users question
  2) search each csv with file id "file-ImqWxmKEVbjEkgLq2gnJTKCz"
  4) generate python code with pandas on the  csv  to answer the query of the user
  5) see the results of the code , if the result is wrong then repeat the above steps
  6)if the result seems right the tell the user.
  #Remember if user asks to give details about a company search relevant column and dont attempt to search all at once

  #Examples for objective 1
  #user: Give me details of renewal dates approaching in three months
  #steps: 
  #first start from one csv.
  #think about the relevant column or columns , here the relevant column is "Renewal Date"
  #search relevant column with the dates near in three months from today
  #Return the whole row of dates found relevant in the response


  #Objective - 2:  To answer query  Summary for company

  Mostly use pandas library to give the answers from the csvs.

  steps to take for objective 2:
  1) understand the users question and understand the name of company and you will extract everything based on that company
  2) search each csv with file name Quoting Automation - Base Data.csv, Quoting Automation - Product Usage Data (1).csv, Tickets.csv.
  3) Compile Name,Primary Contact,ARR,Existing Contract Start Date,Existing Contract end date
  from Quoting Automation - Base Data.csv corresponding to company name
  4)Compile Active Licenses,Usage Percentage YoY from Quoting Automation - Product Usage Data (1).csv
  corresponding to company name

  5)Calculate the number of Tickets by specific company by calculating number of rows does the same company name repeated in Tickets.csv
  6)Compile the above fields in a table described above in 3,4,5 points in a single table corresponding to company name
  7) generate python code with pandas on the  csv  to answer the query of the user.

  8) see the results of the code , if the result is wrong then repeat the above steps
  9)if the result seems right the tell the user.
  10) I want data compiled over a single row which also contains the number of Tickets
  #Remember if user asks to give details about a company search relevant column and dont attempt to search all at once
  #Examples for objective 2
  #user: Give me details of renewal dates approaching in three months
  #steps: 
  #first start from one csv.
  #think about the relevant column or columns , here the relevant columns are Name,Primary Contact,ARR,Existing Contract Start Date,Existing Contract end date,Active Licenses,Usage Percentage YoY,Number of Tickets
  #Get the values for theses column from the three csv files Quoting Automation - Base Data.csv, Quoting Automation - Product Usage Data (1).csv, Tickets.csv respectively

  #Return the whole row of data found relevant in the response

  #Objective 3-To answer query 'Create a Quote for Norfolk Consulting '

  Mostly use pandas library to give the answers from the
  Norfolk Consulting pdf.
  steps to take for objective 3:
  1)understand the users question
  2)**Read the Document:**
    - Access the file `Norfolk Consulting.pdf` stored in the vector store with id - 'vs_nAymwvuhEZbYrHLS0YCbzWrg'.
    - Locate and read the sections related to the subscription services and fees for Year 2.

  3) **Extract Relevant Information:**
    - Identify and extract the subscription service fees, including platform fees, base transaction fees, and support fees for Year 2.
    - Ensure to include any additional fees mentioned for Year 2.

  4)**Create the Quote:**
    - Use the extracted information to create a detailed quote for Year 2.
    - The quote should include the following:
      - Platform Fee
      - Base Transaction Fee
      - Support Fees
      - Any other applicable fees
  """,
    
      model=model,
      tools=[{"type": "code_interpreter"}]
    #   tool_resources={
    #   "code_interpreter": {
    #     "file_ids": file_codeinterpreter
    #   }
    # }
  )


  assis_id = assistant.id
  print(assis_id)

  message = "get me details regarding company's which renewable date is approaching"

  thread = client.beta.threads.create()
  thread_id = thread.id
  print(thread_id)

  message = client.beta.threads.messages.create(
      thread_id=thread_id, role="user", content=message
  )

  # == Run the Assistant
  run = client.beta.threads.runs.create(
      thread_id=thread_id,
      assistant_id=assis_id,
      instructions="You are rowan an ai assistant",
  )


  def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
      """
      Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
      :param thread_id: The ID of the thread.
      :param run_id: The ID of the run.
      :param sleep_interval: Time in seconds to wait between checks.
      """
      while True:
          try:
              run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
              if run.completed_at:
                  elapsed_time = run.completed_at - run.created_at
                  formatted_elapsed_time = time.strftime(
                      "%H:%M:%S", time.gmtime(elapsed_time)
                  )
                  print(f"Run completed in {formatted_elapsed_time}")
                  logging.info(f"Run completed in {formatted_elapsed_time}")
                  messages = client.beta.threads.messages.list(thread_id=thread_id)
                  last_message = messages.data[0]
                  response = last_message.content[0].text.value
                  print(f"Assistant Response: {response}")
                  break
          except Exception as e:
              logging.error(f"An error occurred while retrieving the run: {e}")
              break
          logging.info("Waiting for run to complete...")
          time.sleep(sleep_interval)



  wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

  run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
  print(f"Run Steps --> {run_steps.data[0]}")
  return assis_id