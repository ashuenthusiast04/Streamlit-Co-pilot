
from dotenv import load_dotenv
import openai
import pickle
from pathlib import Path
import time
# from create_assistant import createassis
import streamlit as st
import streamlit_authenticator as stauth 


st.set_page_config(page_title="CPQ Co Pilot", page_icon="👨🏻‍💻")
# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


    names = ["Ashutosh Singh", "Shobhit Gupta","Himanshu Srivastava"]
usernames = ["ash_02", "shobhit@04","himanshu@06"]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "CPQ_COPILOT", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")



if authentication_status:

    load_dotenv()

    client = openai.OpenAI()

    model = "gpt-4o"  


    if "ak" not in st.session_state:
        st.session_state.ak="asst_GytA23ODMbhKmpQnU0OD94lP"
    if "file_id_list" not in st.session_state:
        st.session_state.file_id_list = []

    if "start_chat" not in st.session_state:
        st.session_state.start_chat = False

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None


        


   

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")


    
    if st.sidebar.button("Start Chatting..."):
        # if st.session_state.file_id_list:
            st.session_state.start_chat = True

            # Create a new thread for this chat session
            chat_thread = client.beta.threads.create()
            st.session_state.thread_id = chat_thread.id
            st.write("Thread ID:", chat_thread.id)
        # else:
        #     st.sidebar.warning(
        #         "No files found. Please upload at least one file to get started."
        #     )


    # Define the function to process messages with citations
    def process_message_with_citations(message):
        """Extract content and annotations from the message and format citations as footnotes."""
        try:
            message_content = message.content[0].text
            annotations = (
                message_content.annotations if hasattr(message_content, "annotations") else []
            )

            # Add footnotes to the end of the message content
            full_response = message_content.value 
            return full_response
        
        except openai.APIConnectionError as e:
            return f"Error: {str(e)} - The message object may not have the expected attributes."
        except openai.RateLimitError  as e:
            return f"Error: {str(e)} - The message object may not have the expected structure or may be empty."
        except openai.APIError as e:
            return f"An unexpected error occurred: {str(e)}"



    # the main interface ...
    st.title("CPQ CO PILOT ")
    st.write("Your own assistant")


    # Check sessions
    if st.session_state.start_chat:
        if "openai_model" not in st.session_state:
            st.session_state.openai_model = "gpt-4o"
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Show existing messages if any...
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # chat input for the user
        if prompt := st.chat_input("What's new?"):
            # Add user message to the state and display on the screen
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # add the user's message to the existing thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id, role="user", content=prompt
            )

            # Create a run with additioal instructions
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=st.session_state.ak,
                instructions="""You are an assistant named rowan.
    You are interacting with the a user.

    Remember very important !!! 
    #Base Data csv has file id "file-X1AR8GJ6UgEFIoUhfyEUt0ZQ"
    #Tickets csv has file id "file-A3EMdMN4ZxOMFkGtbuxALr02"
    #Licensing csv has file id "file-KOFGR8f6NJlAcVS9VlQDLxIV"
    #Product usage  data csv has file id "file-od7CeARSzlQTtjbQbauHCyue"
    #Norfolk consulting pdf is stored in vector store with id 
    'vs_nAymwvuhEZbYrHLS0YCbzWrg'
    Base Data csv : This file includes columns for details of company and company's representative with details about contract of company such as name, Company, Primary Contact, ARR, Existing Contract Start Date, Existing Contract End Date, Renewal Date, Renewal ARR, Renewal Stage, Renewal Rep, Renewals Geo.

    Tickets  csv: This file encompasses columns related to tickets or issue raised by company, including Date Creaated,Ticket ID,SubjectTicket Status,Ticket Severity,Module,company name.

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
    Trigger Objective 4 if user queries " Explain the commercial agreements that we have with Norfolk Consulting"

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

    #Objective 4-To answer query 'Explain the commercial agreements that we have with Norfolk Consulting '
    steps to take for objective 3:
    1)understand the users question
    2)**Read the Document:**
    - Access the file `Norfolk Consulting.pdf` stored in the vector store with id - 'vs_nAymwvuhEZbYrHLS0YCbzWrg'.
    - Locate and read the sections related to the commercial agreements

    3) **Extract Relevant Information:**
    4)Follow this template to answer question
    1. Subscription Services and Fees:
    Platform Fee:
    Base Transaction Fee:
    Support Fees:
    Total Fees:
    2. Support Services:
    Silver Support Program: Year 1, 24x7, $0
    Gold Support Program: Year 2, 24x7, $15,000
    Platinum Support Program: Year 3, 24x7, $20,000
    3. Implementation Fee:
    4. Change Requests:

    5. Additional Transactions Fee:
    6. Subscription Term:
    7. Invoicing and Payment:

    8. Taxes:
    9. Penalties for Late/Non-Payment:
    """,
            )

        
            with st.spinner("Wait... Generating response..."):
                while run.status != "completed":
                    time.sleep(1)
                    run = client.beta.threads.runs.retrieve(
                        thread_id=st.session_state.thread_id, run_id=run.id
                    )
                # Retrieve messages added by the assistant
                messages = client.beta.threads.messages.list(
                    thread_id=st.session_state.thread_id
                )
                # Process and display assistant messages
                assistant_messages_for_run = [
                    message
                    for message in messages
                    if message.run_id == run.id and message.role == "assistant"
                ]

                for message in assistant_messages_for_run:
                    full_response = process_message_with_citations(message=message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_response}
                    )
                    with st.chat_message("assistant"):
                        st.markdown(full_response, unsafe_allow_html=True)

  
