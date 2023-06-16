import openai
import os
import sys
import streamlit as st

st.title("Sales Calls Analysis WebApp.")
uploaded_file = st.file_uploader("Upload your call", type=["mp3", "wav"])

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
  
except KeyError:
    sys.stderr.write("""
    You haven't set up your API key yet.

    If you don't have an API key yet, visit:

    https://platform.openai.com/signup

    1. Make an account or sign in
    2. Click "View API Keys" from the top right menu.
    3. Click "Create new secret key"

    Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
    """)
    exit(1)
  
if uploaded_file is not None:
    # Process the uploaded audio file
    # You can access the file data using the 'uploaded_file' variable
    # Perform your desired operations on the audio file
    # ...
    st.text("Please wait a few minutes while the call is being processed.")
    transcript = openai.Audio.transcribe("whisper-1", uploaded_file)
    transcript_text = transcript["text"]
    delimiter = "####"
    sys_content = '''You will be given a transcript of a sales dialogue.     Complete the following steps: 
  Step 1. The transcript will be given as plain text, assign roles to the dialogue and rewrite the text, like this:
"Nicole: Hi, this is Nicole from McDonald's. How are you today?
Ann: Hi, good, how are you?
Nicole: Good, I'm just calling to tell you..."
Step 2. Analyze this call, answering the following questions: Was the contact an inbound lead or an outbound one? Was the contact lead from any of the campaigns, ads, referrals, affiliate partners, etc.? What were the topics discussed? What were the prospect’s objections? Was the seller able to effectively communicate the product’s USPs and offers? How did the seller respond to the prospect’s queries? What were the challenges faced by the sales in the call? What was the source of the contact? Was it an inbound lead or an outbound? Was it the decision-maker of that company? What were the key takeaways from the conversation? When is the next follow-up scheduled? How would you rate this call on a scale from 0 to 100? How would you rate the salesperson's performance? Is there anything that you would change in this call, if so, what? Was it successful or unsuccessful, and why? Please, be concise but keep all the valuable information. Respond in such format: 
"Call analysis:

Contact: Inbound lead from Google search.

Topics discussed: Previous property search, decision to pause due to work and pandemic, intention to find a property for parents in Johnston or Cranston, preferred price range.

Prospect's objections: Paused search due to work and pandemic uncertainties.

Effective communication of product's USPs: Seller (Nicole) establishes expertise by mentioning residency in Johnston.

Seller's response to queries: Confirms price range, understands preferred areas, ensures email correspondence, offers property listings, plans follow-up in a few weeks.

Challenges faced: Prospect's temporary halt in property search due to work and pandemic.

Contact source: Inbound lead from Google search.

Decision-maker: Elizabeth, seeking property for parents.

Key takeaways: Prospect's situation, future search plans, specific requirements for parents' property.

Next follow-up: Scheduled in a few weeks as agreed.

Performance: 85/100 - Good.

Reasons: Effective communication, trust-building, addressing objections, confirming preferences, offering support and follow-up, positive approach

Call Success: Yes."

For your output, use the following format:
Step 1:#### <call transcript with roles>
Step 2:#### <call analysis>

Make sure to include {delimiter} to separate every step.
'''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": sys_content},
            {"role": "user", "content": transcript_text},
        ]
    )
    analysis = response['choices'][0]['message']['content']
    try:
        final_response = analysis.split("Step 2:")[-1].strip('"')
        final_response = final_response.replace('"', '')
    except Exception as e:
        final_response = "Sorry, I'm having trouble right now, please try asking another question."
    
    print(final_response)

    st.success("Upload successful!")
    st.text(final_response)