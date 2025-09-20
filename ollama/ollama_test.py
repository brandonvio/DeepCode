from openai import OpenAI


def ollama_hello_world(host="nvda", port=30434, model="gpt-oss:20b"):
    """Send a hello world prompt to Ollama using OpenAI-compatible API."""

    # Create OpenAI client pointing to Ollama's OpenAI-compatible endpoint
    client = OpenAI(
        base_url=f"http://{host}:{port}/v1",
        api_key="ollama"  # Ollama doesn't require a real API key
    )

    try:
        # Use OpenAI's chat completions API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say hello world"}
            ],
            stream=False
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error connecting to Ollama: {e}"


# Example usage
if __name__ == "__main__":
    hello_message = ollama_hello_world()
    print(hello_message)