import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

# System prompt requiring Question and Year to be extracted from the user
system_prompt = '''
You are a helpful Tax knowledge base assistant. You need to capture a Question and Year from each customer.
The Question is their query on Taxes, and the Year is the year of the applicable Tax season.
If they haven't provided the Year, ask them for it again.
Once you have the Year, say "searching for answers".

Example 1:

User: I'd like to know the deductions I am eligible for with an income of 100000 dollars , married and 2 kids

Assistant: Certainly, what year would you like this for?

User: 2023 please.

Assistant: Searching for answers.
'''

### CHATBOT APP

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

st.title('1040 Form Chatbot')
st.subheader("Help us help you learn about the 1040 Form")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input("What do you want to know: ","", key="input")

if st.button('Submit', key='generationSubmit'):

    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant()
        messages = []
        system_message = Message('system',system_prompt)
        messages.append(system_message.message())
    else:
        messages = []

    user_message = Message('user',prompt)
    messages.append(user_message.message())
    response = query(messages)
    # Debugging step to print the whole response
    #st.write(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['content'])

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

