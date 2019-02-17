import rdflib

class Property:
    def __init__(self, value, role, subject):
        self.value = value
        self.role = role
        self.subject = subject

class Definition:
    def __init__(self, wn_sense, properties):
        self.wn_sense = wn_sense
        self.properties = properties

definition_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?definition
WHERE{
    ?definition rdf:type ?property .
    FILTER(?property != rdf:Statement)
}"""

property_template = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?value ?role ?subject
WHERE{{
<{}>      rdf:type      ?property .
?property rdf:object    ?value .
?property rdf:predicate ?role .
?property rdf:subject   ?subject
}}"""

reified_property_template = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?role ?subject ?subValue ?subRole ?subSubject
WHERE {{
<{}>             rdf:type    ?property .
?property        rdf:object    ?subProperty .
?property        rdf:predicate ?role .
?property        rdf:subject   ?subject .
?subProperty     rdf:object    ?subValue .
?subProperty     rdf:predicate ?subRole .
?subProperty     rdf:subject   ?subSubject
}}"""

wn_graph = rdflib.Graph()
wn_graph.parse("WN_DSR_model_XML.rdf")

definitions = wn_graph.query(definition_query)

print(definitions[0][0])
