import gradio as gr
from chatbot1 import ChatBot, extractSymptoms, extractReminders,SpeechToText
from util import *
import datetime

bot=ChatBot()
symptoms = ""
persona_keys = [
    "name", "age", "race", "height",
    "weight", "gender", "occupation", "phone",
    "birth", "symptoms", "detail", "log"
]
tones = get_tones()
try:
    persona = json.load(open("persona.json", "rb"))
except:
    persona = {key: "" for key in persona_keys}
with gr.Blocks() as demo:
    with gr.Tab("Chatbot"):
        with gr.Column(scale=0):
            with gr.Row():
                tone_select=gr.Dropdown(label="Tone",choices=tones.keys(),scale=2,value=sorted(tones.keys())[0],interactive=True)
                tone_button=gr.Button("Set Tone")
                tone_button.click(fn=bot.updatePrompt,inputs=[tone_select],outputs=[])
            chatbot=gr.Chatbot()
            Input = gr.Textbox(label="Your input goes here")
            save_check = gr.Checkbox(label="Save Conversation",value=True,interactive=True)
            examples=gr.Examples(examples=["I feel so bad, I have a headache and I feel like I am going to die",
                                            "I am a 22 years old male graduate student"],inputs=[Input])
            
            FinishButton = gr.Button("Finish Conversation")
            
            def respond(message, chat_history):
                response=bot.sendMessage(message)
                chat_history.append((message, response))
                return "", chat_history
            results=gr.Textbox(label="Results")
            Input.submit(respond, [Input, chatbot], [Input, chatbot])
            
    with gr.Tab("Persona"):
        with gr.Row():
            name=gr.Textbox(label="Name",value=persona["name"],interactive=True)
            age=gr.Textbox(label="Age",value=persona["age"],interactive=True)
            race=gr.Textbox(label="Race",value=persona["race"],interactive=True)
        with gr.Row():
            height=gr.Textbox(label="Height",value=persona["height"],interactive=True)
            weight=gr.Textbox(label="Weight",value=persona["weight"],interactive=True)
            gender=gr.Textbox(label="Gender",value=persona["gender"],interactive=True)
        with gr.Row():
            occupation=gr.Textbox(label="Occupation",value=persona["occupation"],interactive=True)
            phone=gr.Textbox(label="phone number",value=persona["phone"],interactive=True)
            birth=gr.Textbox(label="Date of Birth",value=persona["birth"],interactive=True)
        symptoms=gr.Textbox(label="Current Symptoms",value=list_to_string(persona["symptoms"]),interactive=True)
        detail=gr.Textbox(label="Other details",value=persona["detail"],interactive=True)
        clearButton=gr.Button("Clear Persona")
        

        def persona_update():
            return {name: gr.update(value=persona["name"],interactive=True),
                        age: gr.update(value=persona["age"]),
                        race: gr.update(value=persona["race"]),
                        height: gr.update(value=persona["height"]),
                        weight: gr.update(value=persona["weight"]),
                        gender: gr.update(value=persona["gender"]),
                        occupation: gr.update(value=persona["occupation"]),
                        phone: gr.update(value=persona["phone"]),
                        birth: gr.update(value=persona["birth"]),
                        symptoms: gr.update(value=list_to_string(persona["symptoms"])),
                        detail: gr.update(value=persona["detail"])}
        def clearPersona():
            global persona
            persona = {key: "" for key in persona_keys}
            #delete local person.json
            try:
                os.remove("persona.json")
            except:
                pass
            return persona_update()
        clearButton.click(fn=clearPersona,inputs=[],outputs=[name,age,race,height,weight,gender,occupation,
                                                                        phone,birth,symptoms,detail])
        def extractSymptoms_helper(save=False):
                user_input = bot.exportUserInputs()
                result=''
                try:
                    out=extractSymptoms(user_input)
                    result=format_json(json.loads(out),persona=persona)
                    print(persona)
                except:
                    pass
                
                #save person to json
                json.dump(persona, open("persona.json", "w"))
                #save conversation log to txt
                if save:
                    conversation = bot.exportConversation()
                    now = datetime.datetime.now()
                    with open("./conversations/conversation"+now.strftime("%Y-%m-%d-%H-%M-%S")+".txt", "w") as f:
                        f.write(conversation)

                return {results: gr.update(value=result),
                        name: gr.update(value=persona["name"],interactive=True),
                        age: gr.update(value=persona["age"]),
                        race: gr.update(value=persona["race"]),
                        height: gr.update(value=persona["height"]),
                        weight: gr.update(value=persona["weight"]),
                        gender: gr.update(value=persona["gender"]),
                        occupation: gr.update(value=persona["occupation"]),
                        phone: gr.update(value=persona["phone"]),
                        birth: gr.update(value=persona["birth"]),
                        symptoms: gr.update(value=list_to_string(persona["symptoms"])),
                        detail: gr.update(value=persona["detail"])}
                # return result
        
        FinishButton.click(fn=extractSymptoms_helper, inputs=[save_check], outputs=[results,name,age,race,height,weight,gender,occupation,
                                                                        phone,birth,symptoms,detail])
    with gr.Tab("Speech-to-Text"):
        audio = gr.Audio(type="filepath",format="mp3")
        text = gr.Textbox()
        transcript_button = gr.Button("Transcribe")
        
        summary = gr.Textbox(label="Summary")
        summary_button = gr.Button("Summarize")
        transcript_button.click(fn=SpeechToText, inputs=[audio], outputs=[text])
        summary_button.click(fn=extractReminders, inputs=[text], outputs=[summary])
                
if __name__ == "__main__":
    try:
        persona = json.load(open("persona.json", "rb"))
    except:
        persona = {key: "" for key in persona_keys}
    demo.launch()