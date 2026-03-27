"""
DSPy ReAct agent for text-to-SPARQL over the keyboards knowledge graph.

The agent is given three tools and reasons step by step until it can
answer the question using data from the graph.
"""

import os

import dspy
from dotenv import load_dotenv

from tools import lookup_item, lookup_property, run_sparql

load_dotenv(os.path.expanduser("~/.env"))
load_dotenv()


def _configure_lm():
    """Set up the DSPy language model using CampusAI credentials."""
    lm = dspy.LM(
        model="openai/" + os.getenv("CAMPUSAI_MODEL", "Gemma 3 (Chat)"),
        api_key=os.getenv("CAMPUSAI_API_KEY"),
        api_base=os.getenv("CAMPUSAI_API_URL", "https://chat.campusai.compute.dtu.dk/api/v1"),
        temperature=0,
        max_tokens=1024,
    )
    dspy.configure(lm=lm)


_configure_lm()


class AnswerQuestion(dspy.Signature):
    """
    Answer questions about keyboards using a knowledge graph.

    Use lookup_item to find the graph ID (kb:Q...) for a keyboard or brand.
    Use lookup_property to find the property ID (kbt:P...) for a property like width or weight.
    Use run_sparql to execute a SPARQL query and retrieve the answer.
    The SPARQL query should use prefixed forms (kb:Q1, kbt:P2) without PREFIX declarations.
    """

    question: str = dspy.InputField(desc="A natural language question about keyboards")
    answer: str = dspy.OutputField(desc="The answer based on the knowledge graph results")


agent = dspy.ReAct(AnswerQuestion, tools=[lookup_item, lookup_property, run_sparql])


def react(question: str) -> dict:
    """
    Run the DSPy ReAct agent for a natural language question.

    Returns a dict with answer, sparql, results, and trace.
    """
    prediction = agent(question=question)
    trajectory = prediction.trajectory  # flat dict: thought_0, tool_name_0, tool_args_0, ...

    # Extract SPARQL query and results from the trajectory steps
    sparql_query = None
    sparql_results = None
    i = 0
    while f"tool_name_{i}" in trajectory:
        if trajectory[f"tool_name_{i}"] == "run_sparql":
            sparql_query = trajectory[f"tool_args_{i}"].get("query")
            sparql_results = trajectory[f"observation_{i}"]
        i += 1

    return {
        "answer": prediction.answer,
        "sparql": sparql_query,
        "results": sparql_results,
        "trace": trajectory,
    }
