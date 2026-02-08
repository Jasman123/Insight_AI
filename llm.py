from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


def create_chat(provider: str):
    provider = provider.lower()

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    elif provider == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",   # or gpt-4o / gpt-3.5-turbo
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    elif provider == "claude":
        return ChatAnthropic(
            model="claude-3-5-sonnet-20240620",  # or haiku / opus
            temperature=0,
            max_tokens=4096,
            timeout=None,
            max_retries=2,
        )

    else:
        raise ValueError("Unsupported provider. Choose: gemini, openai, claude")
