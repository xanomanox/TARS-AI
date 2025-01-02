
import socket
import numpy as np
import asyncio
import pyaudio

async def listen_to_voice(text, server_ip='localhost', server_port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    async def play_audio_stream():
        buffer = b''
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=24000,  # Ensure this matches the server's sampling rate
                        output=True,
                        frames_per_buffer=2048)

        try:
            while True:
                chunk = await asyncio.get_event_loop().run_in_executor(None, client_socket.recv, 1024)
                if not chunk:  # End of stream
                    break
                if b"END_OF_AUDIO" in chunk:
                    buffer += chunk.replace(b"END_OF_AUDIO", b"")
                    if buffer:
                        audio_array = np.frombuffer(buffer, dtype=np.float32).copy()  # Make a writable copy
                        stream.write(audio_array.tobytes())
                    break
                buffer += chunk
                if len(buffer) >= 4096:
                    audio_array = np.frombuffer(buffer[:4096], dtype=np.float32).copy()  # Make a writable copy
                    stream.write(audio_array.tobytes())
                    buffer = buffer[4096:]
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    try:
        # Send only the text to the server
        await asyncio.get_event_loop().run_in_executor(None, client_socket.sendall, text.encode('utf-8'))
        await play_audio_stream()
        print("Audio playback finished.")

    except Exception as e:
        print(f"Error in listen_to_voice: {e}")

    finally:
        client_socket.close()

# Example usage: Replace this with your actual server IP and port
async def main():
    await listen_to_voice("my name is jenny..", server_ip='localhost', server_port=9998)

# Run the main async function
asyncio.run(main())