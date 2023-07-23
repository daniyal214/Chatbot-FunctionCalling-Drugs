import streamlit as st
from streamlit_chat import message
from converstation import run_conversation_backup

st.set_page_config(page_title="DrugChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 DrugChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built used to answer questions related to drugs, medication and health.
    
    💡 Note: API key is required!
    ''')
    # add_vertical_space(5)

    api_key = st.text_input("Paste your API Key below and press ENTER", "", type="password")

# Generate empty lists for generated and past.
# generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm DrugChat, How may I help you?"]
# past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']


if 'obj' not in st.session_state:
    if api_key:
        st.session_state['api_key'] = api_key
    else:
        st.warning("Please enter the API key to initialize the chatbot.")
        st.stop()

# Layout of input/response containers
input_container = st.container()
response_container = st.container()


# User input
# Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Applying the user input box
with input_container:
    user_input = get_text()


# Response output
# Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt, api_key):
    chatbot, function_ran = run_conversation_backup(api_key, prompt)
    # chatbot = run_conversation(api_key, prompt)
    if function_ran:
        if chatbot:
            chatbot_response = chatbot['choices'][0]['message']['content']
            return chatbot_response
        else:
            return None
    else:
        return chatbot


# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input, api_key)
        if response:
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
