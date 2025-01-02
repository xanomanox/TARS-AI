import asyncio
import socket
import numpy as np
import pyaudio
import struct
import time

# Configuration Constants
SERVER_IP = '192.168.168.57'      # Replace with your server's IP address
TTS_SERVER_PORT = 9999           # Replace with your f5-tts server's port
CHUNK = 1024                     # Audio chunk size
FORMAT = pyaudio.paInt16         # Audio format (16-bit int)
CHANNELS = 1                     # Mono audio
RATE = 24000                     # Sampling rate (ensure it matches the server's rate)
VAD_THRESHOLD = 500              # Threshold for voice activity detection
SILENCE_DURATION = 1.0           # Duration (in seconds) to consider as silence

# Placeholder STT function
def stt_inference(audio_data: bytes) -> str:
    """
    Placeholder function for Speech-to-Text (STT) processing.
    Replace this function with your actual STT implementation.

    :param audio_data: Raw audio bytes captured from the microphone.
    :return: Transcribed text.
    """
    # TODO: Integrate with actual STT service
    print("STT Inference Placeholder: Received audio data.")
    return "This is a placeholder response."

async def send_text_to_tts(text: str, server_ip: str, server_port: int) -> bytes:
    """
    Sends text to the TTS server and receives synthesized speech audio.

    :param text: The text to synthesize.
    :param server_ip: IP address of the TTS server.
    :param server_port: Port number of the TTS server.
    :return: Synthesized audio in bytes.
    """
    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        print(f"Connected to TTS server at {server_ip}:{server_port}")

        # Send the text to the server
        writer.write(text.encode('utf-8'))
        await writer.drain()
        print(f"Sent text to TTS server: {text}")

        # Receive the audio data
        audio_data = b''
        while True:
            data = await reader.read(4096)
            if not data:
                break
            if b"END_OF_AUDIO" in data:
                audio_data += data.replace(b"END_OF_AUDIO", b"")
                break
            audio_data += data

        print("Received audio data from TTS server.")
        writer.close()
        await writer.wait_closed()
        return audio_data

    except Exception as e:
        print(f"Error communicating with TTS server: {e}")
        return b''

async def play_audio(audio_data: bytes):
    """
    Plays the given audio data through the speaker.

    :param audio_data: Audio data in bytes.
    """
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        # Convert bytes to numpy float32 array
        audio_array = np.frombuffer(audio_data, dtype=np.float32)
        stream.write(audio_array.tobytes())

        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Audio playback finished.")

    except Exception as e:
        print(f"Error during audio playback: {e}")

def is_speech(audio_chunk: bytes) -> bool:
    """
    Simple energy-based voice activity detection (VAD).

    :param audio_chunk: Audio data chunk in bytes.
    :return: True if speech is detected, False otherwise.
    """
    # Unpack the byte data to integers
    fmt = "<" + ("h" * (len(audio_chunk) // 2))
    audio_int = struct.unpack(fmt, audio_chunk)
    # Compute the energy of the audio chunk
    energy = sum([abs(sample) for sample in audio_int]) / len(audio_int)
    return energy > VAD_THRESHOLD

async def capture_and_process_audio():
    """
    Captures audio from the microphone, detects voice activity,
    sends audio to STT, sends text to TTS, and plays back the audio.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening for speech...")

    audio_buffer = b''
    is_recording = False
    silence_start = None

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)

            if is_speech(data):
                if not is_recording:
                    print("Speech detected. Start recording.")
                    is_recording = True
                audio_buffer += data
                silence_start = None
            else:
                if is_recording:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > SILENCE_DURATION:
                        print("Silence detected. Stop recording.")
                        is_recording = False
                        # Process the buffered audio
                        if audio_buffer:
                            # Placeholder STT processing
                            transcribed_text = stt_inference(audio_buffer)
                            print(f"Transcribed Text: {transcribed_text}")

                            # Send text to TTS server and receive audio
                            if transcribed_text.strip():
                                audio_response = await send_text_to_tts(transcribed_text, SERVER_IP, TTS_SERVER_PORT)
                                if audio_response:
                                    await play_audio(audio_response)
                            audio_buffer = b''
                # If not recording, continue listening
                pass

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Audio stream closed.")

async def main():
    await capture_and_process_audio()

if __name__ == "__main__":
    asyncio.run(main())
