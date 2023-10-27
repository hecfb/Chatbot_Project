import openai
import gradio

openai.api_key = "APIKEY"

messages = [{"role": "system", "content": "You are a health experts that specializes in longevity and use the knowledge from Andrew Huberman and Peter Atia"}]


def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply


demo = gradio.Interface(fn=CustomChatGPT, inputs="text",
                        outputs="text", title="Your Title")

demo.launch(share=True)
