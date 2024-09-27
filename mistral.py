from mistralai import Mistral

api_key = 'X8ahOMkLJytSfLPPuEkPDg8CMSqFOWiE'
model = "mistral-large-latest"
safe_prompt = """Always assist with care, respect, and truth. 
Respond with utmost utility yet securely. Avoid harmful, 
unethical, prejudiced, or negative content. 
Ensure replies promote fairness and positivity.
Speak russian.
"""

class MistralClient:
    saved_messages_len = 10

    def __init__(self, api_key):
        self.context = [{"role": "system", "content": safe_prompt}]
        self.connection = Mistral(api_key=api_key)

    async def chat_ai(self, text):
        self.context.append({"role": "user", "content": text})

        reply = await self.connection.chat.stream_async(
            model=model,
            messages=self.context,
        )
        full_answer = ''
        async for chunk in reply:
            msg = chunk.data.choices[0].delta.content
            yield msg
            full_answer += msg

        self.context.append({"role": "assistant", "content": full_answer})

        if len(self.context) > self.saved_messages_len:
            self.context = [{"role": "system", "content": safe_prompt}] + self.context[-self.saved_messages_len:]


async def get_mistral_client():
    return MistralClient(api_key=api_key)

