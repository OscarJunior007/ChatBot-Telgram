import telebot
from openai import OpenAI
import urllib.request
import subprocess
import uuid
from pathlib import Path
from pytube import YouTube


TOKEN = "6837535719:AAE1h-2BZwvqDBHG4W2GInGqN5_dXs-_roc"
client = OpenAI(api_key="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")

bot = telebot.TeleBot(TOKEN)

d = dict()

@bot.message_handler(commands=['descargar_youtube'])
def descargar_video(message):
  global d
  d[message.chat.id] = 'DESCARGAR'
  bot.reply_to(message, 'Ingresa el link: ')

@bot.message_handler(commands=['resumen_youtube'])
def resumen_video(message):
  global d
  d[message.chat.id] = 'RESUMEN'
  bot.reply_to(message, 'Ingresa el link: ')

def descargar(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    id = yt.title
    try:
        video.download(output_path="youtube", filename=f"{id}.mp3" )
        return f"{id}.mp3"
    except:
        None

@bot.message_handler(commands=['generar_audio'])
def texto_speech(message):
    global d
    d[message.chat.id] = 'AUDIO'
    bot.reply_to(message, "Hazme tu pregunta y la respondere con un audio, puedo tardarme un poco. ")

def ask_audio(input:str):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input= input
    )
    response.stream_to_file(speech_file_path)

def run_command(command):
    """Run a command, given an array of the command and arguments"""
    proc = subprocess.Popen(command)
    ret = proc.wait()

@bot.message_handler(commands=['generar_imagen'])
def image(message):
    global d
    d[message.chat.id]="IMAGE"
    bot.reply_to(message, "Dime que imagen deseas que cree, puedo tardarme un poco.")

@bot.message_handler(commands=['generar_texto'])
def text(message):

    print(message.text)
    global d
    d[message.chat.id]="TEXT"
    bot.reply_to(message, "¿Que quieres saber el dia de hoy?")

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    id=str(uuid.uuid4())
    commands = ["ffmpeg", "-i", "new_file.ogg" ,"-acodec" ,"libmp3lame", f"{id}.mp3"]
    run_command(commands)

    with open(f"{id}.mp3", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file
        )
        print(transcription.text)
        #bot.reply_to(message,transcription.text)
        bot.reply_to(message, ask_texto(transcription.text))


@bot.message_handler()
def send(message):

    valor=d.get(message.chat.id)

    if valor is None:
        bot.reply_to(message,"Debe escoger un comando, da click al boton 'menu que aparece abajo a la izquierda")
    elif valor == "TEXT":
        bot.reply_to(message,ask_texto(message.text))
    elif valor == "AUDIO":
        respuesta_chat_gpt=ask_texto(message.text)#Aca se pregunta a chatgpt texto a texto, respuesta_chat_gpt contendra la respuesta de chatgpt
        ask_audio(respuesta_chat_gpt) # aca paso la respuesta de testo a audio
        with open('speech.mp3', 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)
    elif valor == "IMAGE":
        url = ask_image(message.text)
        urllib.request.urlretrieve(url, 'photo.png')
        with open('photo.png','rb') as f:
            bot.send_photo(message.chat.id, f)
    elif valor == 'DESCARGAR':
        filename = descargar(message.text)
        with open(f"youtube/{filename}", "rb") as audio_file:
            bot.send_audio(message.chat.id, audio_file)
        bot.reply_to(message, "Done")
    elif valor == 'RESUMEN':
        bot.reply_to(message,' Esto puede tardar hasta 2 minutos por favor espera.')
        filename = descargar(message.text)
        with open(f"youtube/{filename}", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            print(transcription.text)
            # bot.reply_to(message,transcription.text)
            bot.reply_to(message, ask_resumen(transcription.text))
def ask_texto(text:str):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      max_tokens=1000,
      messages=[
        {"role": "system", "content": "Oscar "},
        {"role": "user", "content":text}
      ]
    )

    return completion.choices[0].message.content
def ask_resumen(text:str):
    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      max_tokens=1000,
      messages=[
        {"role": "system", "content": "Maestro en resumenes"},
        {"role": "user", "content":'apartir de ahora te comportaras como un experto en hacer resumenes, resume los siguientes textos que envie '},
        {"role": "user", "content": text}
      ]
    )

    return completion.choices[0].message.content

def ask_image(prompt:str):
    response = client.images.generate(
        model="dall-e-3",
        prompt= prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

bot.set_my_commands([
    telebot.types.BotCommand("/generar_texto", "Responde preguntas"),
    telebot.types.BotCommand("/generar_imagen", "Genera imagenes apartir de texto"),
    telebot.types.BotCommand("/generar_audio", "Responde tus preguntas con un audio"),
    telebot.types.BotCommand("/descargar_youtube", "Descargo Audios"),
    telebot.types.BotCommand("/resumen_youtube", "Hago resumenes de videos que me envies")
])



bot.infinity_polling()
