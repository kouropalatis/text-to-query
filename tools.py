"""
SPARQL tools for the keyboards knowledge graph.

Three functions usable in the ReAct loop:
  run_sparql(query)       -- execute any SPARQL query against QLever
  lookup_item(label)      -- find kb:Q... for a named entity
  lookup_property(label)  -- find kbt:P... for a property name
"""

import requests

QLEVER_ENDPOINT = "http://localhost:7070/api/sparql"

PREFIXES = """
PREFIX kb:   <https://keyboards.wikibase.cloud/entity/>
PREFIX kbt:  <https://keyboards.wikibase.cloud/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX wikibase: <http://wikiba.se/ontology#>
"""


def run_sparql(query: str) -> list[dict]:
    """
    Execute a SPARQL query against the local QLever instance.
    Returns a list of result bindings (each binding is a dict of variable -> value).
    """
    full_query = PREFIXES + "\n" + query
    response = requests.get(
        QLEVER_ENDPOINT,
        params={"query": full_query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=10,
    )
    response.raise_for_status()
    bindings = response.json()["results"]["bindings"]
    return [{k: v["value"] for k, v in row.items()} for row in bindings]


def lookup_item(label: str) -> str:
    """
    Find the knowledge graph ID (kb:Q...) for an item by its English label.
    Returns a prefixed URI string like 'kb:Q1', or None if not found.
    """
    query = f"""
SELECT ?item {{
  ?item rdfs:label | skos:altLabel "{label}"@en .
}}
LIMIT 1
"""
    results = run_sparql(query)
    if not results:
        return None
    uri = results[0]["item"]
    # Convert full URI to prefixed form: https://keyboards.wikibase.cloud/entity/Q1 → kb:Q1
    return "kb:" + uri.split("/entity/")[-1]


def lookup_property(label: str) -> str:
    """
    Find the property ID (kbt:P...) for a property by its English label.
    Returns a prefixed URI string like 'kbt:P2', or None if not found.
    """
    query = f"""
SELECT ?property {{
  ?property_item rdfs:label | skos:altLabel "{label}"@en ;
                wikibase:directClaim ?property .
}}
LIMIT 1
"""
    results = run_sparql(query)
    if not results:
        return None
    uri = results[0]["property"]
    # Convert full URI to prefixed form: https://keyboards.wikibase.cloud/prop/direct/P2 → kbt:P2
    return "kbt:" + uri.split("/prop/direct/")[-1]
