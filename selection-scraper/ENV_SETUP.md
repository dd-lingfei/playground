# Environment Variables Setup

This project requires certain environment variables to be set for the OpenAI client to function properly.

## Required Environment Variables

### PORTKEY_API_KEY (Required)
The Portkey API key for authentication.

### PORTKEY_VIRTUAL_KEY (Required)
The Portkey virtual key for routing requests.

### GATEWAY_URL (Optional)
The gateway URL for API requests.
- **Default:** `http://cybertron-service-gateway-offline-jobs.svc.ddnw.net:8080/v1`

## Setup Instructions

### Option 1: Using .env File (Recommended)

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add the following content to `.env`:
```bash
# OpenAI Client Configuration
PORTKEY_API_KEY=your_portkey_api_key_here
PORTKEY_VIRTUAL_KEY=your_virtual_key_here

# Optional: Override the default gateway URL
# GATEWAY_URL=http://your-custom-gateway-url.com
```

3. Install python-dotenv if not already installed:
```bash
pip install python-dotenv
```

4. Load the environment variables in your Python code:
```python
from dotenv import load_dotenv
load_dotenv()

from clients import OpenAIClient
client = OpenAIClient()
```

### Option 2: Export Environment Variables

Export the variables in your shell:

```bash
export PORTKEY_API_KEY="your_portkey_api_key_here"
export PORTKEY_VIRTUAL_KEY="your_virtual_key_here"
```

### Option 3: Pass Directly to Constructor

```python
from clients import OpenAIClient

client = OpenAIClient(
    portkey_api_key="your_portkey_api_key_here",
    portkey_virtual_key="your_virtual_key_here"
)
```

## Validation

The OpenAI client will raise a `ValueError` if required environment variables are not set:

- `PORTKEY_API_KEY is required. Please set it as an environment variable or pass it to the constructor.`
- `PORTKEY_VIRTUAL_KEY is required. Please set it as an environment variable or pass it to the constructor.`

## Security Notes

- **Never commit `.env` files to version control** - they are already added to `.gitignore`
- Keep your API keys secure and do not share them
- Rotate keys regularly for security best practices

