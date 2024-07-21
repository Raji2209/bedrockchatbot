import boto3
import streamlit as st
import bedrock
from bedrock import bedrock_chain, run_chain, clear_memory, getAnswers

st.subheader('Acts, Rules, and Regulations of Mining industries', divider='rainbow')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

questions = st.chat_input('Enter your questions here...')

if questions:
    with st.chat_message('user'):
        st.markdown(questions)
    st.session_state.chat_history.append({"role": 'user', "text": questions})

    response = getAnswers(questions)
    print(response)

    if 'error' in response:
        with st.chat_message('assistant'):
            st.markdown(f"Error: {response['error']}")
        st.session_state.chat_history.append({"role": 'assistant', "text": f"Error: {response['error']}"})
    else:
        try:
            answer = response['output']['text']
            
            with st.chat_message('assistant'):
                st.markdown(answer)
            st.session_state.chat_history.append({"role": 'assistant', "text": answer})

            # Check if 'citations' exists and is non-empty
            if 'citations' in response and response['citations']:
                # Check if 'retrievedReferences' exists and is non-empty
                if 'retrievedReferences' in response['citations'][0] and response['citations'][0]['retrievedReferences']:
                    context = response['citations'][0]['retrievedReferences'][0]['content']['text']
                    doc_url = response['citations'][0]['retrievedReferences'][0]['location']['s3Location']['uri']

                    # Below lines are used to show the context and the document source for the latest Question Answer
                    st.markdown(f"<span style='color:#FFDA33'>Context used: </span>{context}", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#FFDA33'>Source Document: </span>{doc_url}", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color:red'>No Context</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:red'>No Citations</span>", unsafe_allow_html=True)
                
        except KeyError as e:
            st.markdown(f"Response structure error: {str(e)}")
          
