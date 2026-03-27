# Text-to-Query

A web service that lets you ask questions about keyboards in plain English (or Danish) and get answers back from a local knowledge graph.

## What it does

You send a question like:

> "What is the width of a Yamaha P-150?"

And the service figures out the answer by:
1. Understanding what you're asking about (the keyboard model, the property)
2. Looking those up in a graph database of keyboard data
3. Running a database query automatically
4. Returning the answer as JSON

No need to know anything about databases or query languages — just ask naturally.

## How it works

The data comes from the [Keyboards Wikibase](https://keyboards.wikibase.cloud), a community knowledge base about keyboards. It's stored locally in a graph database called [QLever](https://github.com/ad-freiburg/qlever).

When you ask a question, an AI agent (using [DSPy ReAct](https://github.com/stanfordnlp/dspy)) reasons step by step — first identifying the keyboard and property you're asking about, then translating that into a database query, then fetching the result.

## Setup

**Requirements:** Python, Docker Desktop, a CampusAI API key.

1. Start the graph database:
```
cd C:\qlever\keyboards
qlever index
qlever start
```

2. Add your API key to a `.env` file:
```
CAMPUSAI_API_KEY=your-key-here
```

3. Start the service:
```
uvicorn main:app --reload --port 8001
```

## Usage

Send a POST request to `/v1/query`:

```json
{
  "text": "What is the width of a Yamaha P-150?"
}
```

Response:

```json
{
  "query": "What is the width of a Yamaha P-150?",
  "answer": "1385.0",
  "sparql": "SELECT ?width WHERE { kb:Q1 kbt:P2 ?width . }",
  "results": [{"width": "1385.0"}]
}
```

Interactive API docs available at `http://localhost:8001/docs`.

## Example questions

- "What is the width of a Yamaha P-150?"
- "What is the height of a Yamaha P-150?"
- "Hvad er bredden på Yamaha P-150?"

## Course

DTU NLP Special Course — Week 7: Text-to-Query (Graph-RAG style)
