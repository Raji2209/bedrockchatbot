# bedrockchatbot

Prerequisites :
1. Create an aws profile called "my_profile" in your local to test from local
2. Create a bed rock knowledge base of articles pointing to an s3 bucket that stores the pdf files

Steps:
1. lambda/start_ingestion.py

   Deploy the python file into lambda. Over and above the basic lambda policies, you would have to give it access to start_ingestion_job towards the bedrock knowledge base.
   Create the following environment variables in the lambda :
   
   DATASOURCEID 
   KNOWLEDGEBASEID
2. From the root, run the streamlit app through the command: 

   streamlit run app.py 
