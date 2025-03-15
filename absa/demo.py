import json

import chainlit as cl

from absa.utils.functions import initialize_openai, process_absa

client = initialize_openai()


@cl.on_chat_start
async def start():
    await cl.Message("Hello, I'm the ABSA bot. Please provide a review.").send()


@cl.on_message
async def main(message):
    absa_result = process_absa(client, message.content)
    await cl.Message(f"\n```json\n{json.dumps(absa_result, indent=2)}\n```\n").send()
