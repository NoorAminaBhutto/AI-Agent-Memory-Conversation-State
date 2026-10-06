# AI Agent Memory & Conversation State

A practical Generative AI application demonstrating short-term conversation memory and selected long-term user memory.

## Features

- Short-term conversation memory
- Long-term user memory
- Memory storage using JSON
- Memory recall
- Individual memory deletion
- Clear conversation
- Clear long-term memory
- User-controlled memory
- No API key required
- Streamlit interface

## How It Works

The application uses two memory layers.

### Short-Term Memory

The current conversation is maintained during the active session.

### Long-Term Memory

Selected user information is stored in `memory.json` so it can be recalled later.

## Demo

1. Send:

Hello

2. Send:

I am working on an AI project.

3. Ask:

What did I say earlier?

4. Save:

Category: goal

Value: Build practical AI applications

5. Ask:

What do you remember about me?

6. Delete the saved memory to demonstrate user control.

## Technologies

- Python
- Streamlit
- JSON
- Session State

## Assignment Concepts

- AI Agent Memory
- Conversation State
- Short-Term Memory
- Long-Term Memory
- Memory Retrieval
- User Memory Control

## Architecture

User
↓
Chat Interface
↓
Conversation State
↓
Assistant Response

Selected User Information
↓
Long-Term Memory
↓
memory.json
↓
Future Responses
