import os
import openai
import json
import textwrap
import chainlit as cl

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.groq.com/openai/v1"
OPENAI_LLM_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "Act as an ABSA model. When I send a message, return a JSON object "
    'that rates four aspects {"FOOD", "PRICE", "SERVICE", "ATMOSPHERE"}. '
    'Each aspect rate MUST be one of the following values: {"NEGATIVE", "NEUTRAL", "POSITIVE"}. '
    'Example output: {"FOOD": <rate>, "PRICE": <rate>, "SERVICE": <rate>, "ATMOSPHERE": <rate>}'
)

print(SYSTEM_PROMPT)
client = openai.OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)


def process_absa(review_message: str) -> dict:
    try:
        completion = client.chat.completions.create(
            model=OPENAI_LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": review_message},
            ],
            temperature=0.1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        """
        Price 4o-mini
        Input: $0.150 / 1M tokens
        Output: $0.600 / 1M tokens
        """
        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens

        input_price = 0.150 / 1000000
        output_price = 0.600 / 1000000
        total_cost = (input_tokens * input_price) + (output_tokens * output_price)

        print(f"REVIEW: {textwrap.fill(review_message, 120)}\n")
        print(
            f"Input Token: {input_tokens} tokens, Output Token: {output_tokens} tokens\n"
        )
        print(f"Price for 4o-mini: ${total_cost:.6f}\n")

        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


@cl.on_chat_start
async def start():
    await cl.Message("Hello, I'm the ABSA bot. Please provide a review.").send()


@cl.on_message
async def main(message):
    absa_result = process_absa(message.content)
    await cl.Message(
        "\n```json\n" f"{json.dumps(absa_result, indent=2)}" "\n```\n"
    ).send()
