import asyncio
import os
from openai import OpenAI
from bot.config_data.config import load_config
config = load_config()

async def connect_client():
    client = OpenAI(
        organization=config.open_ai.organization_id,
        api_key=config.open_ai.api_key
    )
    print(f"Подключились к клиенту: {client}")
    return client


async def create_assistant():
    assistant = config.open_ai.assistant_id
    print(f"Подключили ассистента: {assistant}")
    return assistant


async def create_thread(client):
    thread = client.beta.threads.create()
    print(f"Создали тред: {thread.id}")
    return thread


async def user_input():
    request = input("Ваш запрос: ")
    return request


async def add_message_to_thread(client, thread, content):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )


async def run_assistant(client, thread, assistant):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant
    )
    print(f"Run ассистент: {run}")
    return run


async def retrieve_run(client, thread, run):
    run_info = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(run_info)
    return run_info.status


async def wait_run_assistant(client, thread, run):
    status = run.status  # начальный статус
    while status != 'completed':
        # Ожидание 3 секунды перед следующей попыткой
        await asyncio.sleep(3)
        status = await retrieve_run(client, thread, run)
    return status


async def response_gpt(client, thread):
    return client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value


async def clear_context(client, thread):
    client.beta.threads.delete(thread.id)






