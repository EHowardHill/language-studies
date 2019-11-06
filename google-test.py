from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()
voice = texttospeech.types.VoiceSelectionParams(
    language_code='ja-JP',
    name="ja-JP-Wavenet-C",
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

synthesis_input = texttospeech.types.SynthesisInput(text="こんにちは、皆さん！お元気ですか？")

# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(synthesis_input, voice, audio_config)

# The response's audio_content is binary.
with open('output.mp3', 'wb') as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')