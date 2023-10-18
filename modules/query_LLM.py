from dotenv import load_dotenv
import openai
import os

load_dotenv('.env')

subscription_key = os.environ.get('SPEECH_KEY')
service_region = os.environ.get('SPEECH_REGION')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Initialize the OpenAI API client
openai.api_key = OPENAI_API_KEY

def get_LLM_response(conversation, question):

    prompt_text = f"""
            You are an expert in Telecom domain with focus on Indian market, you will be asked questions related to that, you have respond in a short 2-3 para response
            here's your question

            Past Conversations: {conversation}

            Question: {question}
            Answer:"""
    
        # Generate text completion using OpenAI's GPT-3 model
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # You can choose a different engine if needed
        prompt=prompt_text,
        max_tokens=200,  # Adjust the number of tokens you want in the completion
        temperature=0.1
    )

    completion_text = response.choices[0].text

    return completion_text