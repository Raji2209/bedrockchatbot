import os
import boto3
from langchain.chains import ConversationChain
from langchain_community.llms import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate



def bedrock_chain():
    os.environ["AWS_PROFILE"] = 'my_profile'
    os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-2'
    profile = os.environ["AWS_PROFILE"]

    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="ap-southeast-2",
    )

    titan_llm = Bedrock(
        model_id="amazon.titan-text-express-v1", client=bedrock_runtime, credentials_profile_name=profile
    )
    titan_llm.model_kwargs = {"temperature": 0.5, "maxTokenCount": 700}

    prompt_template = """System: The following is a friendly conversation between a knowledgeable helpful assistant and a customer.
    The assistant is talkative and provides lots of specific details from it's context.

    Current conversation:
    {history}

    User: {input}
    Bot:"""
    PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=prompt_template
    )

    memory = ConversationBufferMemory(human_prefix="User", ai_prefix="Bot")
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=titan_llm,
        verbose=True,
        memory=memory,
    )

    return conversation

def run_chain(chain, prompt):
    num_tokens = chain.llm.get_num_tokens(prompt)
    return chain({"input": prompt}), num_tokens


def clear_memory(chain):
    return chain.memory.clear()

def getAnswers(questions):
    
    bedrockClient = boto3.client('bedrock-agent-runtime', 'ap-southeast-2')
    
    knowledgeBaseResponse  = bedrockClient.retrieve_and_generate(
        input={'text': questions},
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'S8ZZNVP6NH',
                'modelArn': 'arn:aws:bedrock:ap-southeast-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )
    return knowledgeBaseResponse
