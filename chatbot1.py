import os
import openai

# Define your API key
api_key = "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"
# Initialize the OpenAI API client
openai.api_key = api_key    

default_prompt = """You are a doctor assistant, a patient will talk with you. Give the person some
confide and try to talk more about their symptoms and get their basic background information to let real doctor know them faster.
make sure you answer is not too long,within , and try to be more friendly."""
class ChatBot:
    def __init__(self,prompt = default_prompt,doctor_conversation=None):
        self.chat_history = []
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 500
        self.prompt = prompt
        if doctor_conversation is not None:
            self.prompt = "Please try to simulate the tone of the doctor, here is the past conversation:" + doctor_conversation
        self.chat_history.append({"role": "system", "content": self.prompt})
    def updatePrompt(self,prompt):
        self.prompt = prompt
        self.chat_history[0]["content"] = self.prompt
    
    def sendMessage(self,message):
        user_input = {
            "role": "user",
            "content": message
        }
        self.chat_history.append(user_input)
        #print(self.chat_history)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.chat_history,
            max_tokens=self.max_tokens
        )
        if len(response.choices) == 0:
            print("no response!!!!!!!!!!!!!!!!!")
        reply = response.choices[0].message.content
        chat_input = {
            "role": "assistant",
            "content": reply
        }
        self.chat_history.append(chat_input)
        return reply
    #first three without name tag
    def exportUserInputs(self):
        userInputs = ""
        for i in range(1,len(self.chat_history),2):
            userInputs+=self.chat_history[i]["content"]+"\n\n"
        return userInputs
    def exportBotOutputs(self):
        botOutputs = ""
        for i in range(2,len(self.chat_history),2):
            botOutputs+=self.chat_history[i]["content"]+"\n\n"
        return botOutputs
    def exportAll(self):
        output=""
        for i in range(len(self.chat_history)):
            output+=self.chat_history[i]["content"]+"\n\n"
        return output
    #export with name tag
    def exportConversation(self):
        output=""
        output += "prompt: "+self.prompt+"\n\n"
        for i in range(len(self.chat_history)//2):
            output+="User: "+self.chat_history[2*i+1]["content"]+"\n\n"
            output+="Doctor: "+self.chat_history[2*i+2]["content"]+"\n\n"
        return output
    

def extractSymptoms(message):
    prompt="""you are an entity extractor, you will extract the information two the following big categories: Symptoms, patient's characteristics and other details from the conversationchara, and output the result
    to a json data structure, do not add true/false for the result. I want symptoms to be a list of strings"""
    # print("extracting symptoms!!!!!!!!!!!!!!!q")
    # print(message)
    sym_bot=ChatBot(prompt)
    response=sym_bot.sendMessage(message)
    return response
def extractReminders(message):
    prompt="""I will give you conversation between doctor and patient, Please summary your output to three catagories: summary of the conversation, reminder for medicine, allergy, food and etc..., and explanation of medical terms. Formate should be numerical list and each item should be short and clear.  """
    rem_bot=ChatBot(prompt)
    response=rem_bot.sendMessage(message)
    return response
def SpeechToText(audio_file):
    print(audio_file)
    audio_file = open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]