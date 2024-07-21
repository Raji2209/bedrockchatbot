# bedrockchatbot

1. lambda/start_ingestion.py

   Deploy the python file into lambda. Over and above the basic lambda policies, you would have to give it access to start_ingestion_job towards the bedrock knowledge base.
   Create the following environment variables in the lambda :
   
   DATASOURCEID 
   KNOWLEDGEBASEID 

2. 
