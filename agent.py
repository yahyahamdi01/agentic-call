import asyncio
import requests
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, silero 

load_dotenv()

class AssistantFunctions(llm.FunctionContext):
    def __init__(self, context: JobContext):
        super().__init__()
        self.context = context

    @llm.ai_callable(description="Call this function ONLY when the user provides a clear appointment date. Pass the date as the argument.")
    async def save_appointment(self, date: str):
        print(f"Date extracted: {date}")
        print("Waiting 5...")
        
        await asyncio.sleep(5)
        
        try:
            response = requests.post(
                "http://127.0.0.1:5000/end-of-call",
                json={"appointment_date": date},
                timeout=5
            )
            print(f"API Status Code: {response.status_code}")
        except Exception as error:
            print(f"Failed to contact the API: {error}")

        print("Disconnecting...")
        await self.context.room.disconnect()
        
        return "Appointment saved successfully."

async def run_agent(context: JobContext):
    await context.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    functions = AssistantFunctions(context)

    # Agent Init 
    agent = VoicePipelineAgent(
        vad=silero.VAD.load(), 
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        fnc_ctx=functions,
    )

    system_prompt = (
        "You are a receptionist for the Bee2link garage. "
        "Your ONLY job is to ask the client what date they want for their appointment. "
        "Keep your answers very short. "
        "When the client gives you a date, thank them, say goodbye, and IMMEDIATELY use the save_appointment function."
    )
    
    agent.chat_ctx.append(role="system", text=system_prompt)

    agent.start(context.room)
    await agent.say("Bonjour, bienvenue chez Bee2link. À quelle date souhaitez-vous prendre rendez-vous ?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=run_agent))