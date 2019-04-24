# Cyber-investigation Analysis Standard Expression (CASE)

_Read the [CASE Wiki tab](https://github.com/ucoProject/CASE/wiki) to learn **everything** you need to know about the Cyber-investigation Analysis Standard Expression (CASE) ontology._
_For learning about the Unified Cyber Ontology, CASE's parent, see [UCO](https://github.com/ucoProject/UCO)._

# RDFDiff
Author: [jstroud-mitre](https://github.com/jstroud-mitre)
An RDF and ontology trouble shooter for CASE/UCO.

### What it does
RDFDiff takes output of a tool (JSON/JSON-LD/XML/etc...)
and attempts to validate it against a RDF based ontology (OWL/N3/ttl).
Any entry in the tool's output that is NOT in the Ontology (specified via CLI)
will display an error. CLI arugments can be added to cause a debugger to start
so you may explore the graph to view where things went wrong.


### How it works
rdfdiff.py will read in an RDF vocabulary defined via ``` -g``` (glossary) to
check a custom tool's output against via ```-i```. The Python library rdflib 
is used to turn the RDF schema into tripples which are then broken into three
lists; 
subject, predicate and object. Finally, each element of the tools ouput within
the tool's subject and predicate are checked againast the glossary's subject 
and predicate to confirm the existence of these RDF elements. If an element is 
found or not found it is displayed to the user. BNodes are skipped  as they
have no appropriate label in RDF and should not be used to verify an ontology.


### Why not SPARQL?
In order to facilitate a broad range of ontologies and custom tool outputs,
SPARQL queries are not used for verification. CASE/UCO allow for robust
flexibility and this tool  aims to compliment this approach.


### Installation
```
sudo pip install -r requirements.txt 
```

### Unit Tests
The ontology validator
is heavily reliant on 3rd pary libraries, primarily RDFlib.
RDFLib is under heavy development. To ensure compatability with new releases
unit tests have been written to check for consistency.

Run unit tests:
```
cd tests;
python test_verifier.py;
```

### CLI Usage

* ``` -g ```: Define the RDF schema (aka glossary) in use for your ontology.
* ``` -gf ```: Define the format the schema is in. By default validator.py
will try to auto-guess based on extension. However, if additional plugins are
installed it is best practice to manually specify it.

* ``` -i ```: The external tool's output you want to verify the ontology 
against.

* ```-if```: Define RDF schema for tool data that's being injested.
* ```--debug```: Break on errors that occur within ```--verify```.
* ```-tg```: Print subject, predicate, object for each graph within tool schema.
* ```-gg```: Print subject, predicate, object for each graph within glossary
* schema.


### CLI Example


* Check for inconsistencies between graphs:

```
rdfdiff.py -g case.ttl -gf turtle -i output.json-ld -if json-ld --verify=1
```

* Check for inconsistencies between graphs with color output:
```
rdfdiff.py -g case.ttl -gf turtle -i output.json-ld -if json-ld --verify=1
--color=1
```

* Enter debug mode. This will cause a PDB session to open when an inconsistency
* is met. This can be useful for manually navigating the RDF graph in Python.:
```
rdfdiff.py -g case.ttl -gf turtle -i output.json-ld -if json-ld --verify=1
--debug=1

```

* Print all graphs for tool's schema.

```
rdfdiff.py -g case.ttl -gf turtle -i output.json-ld -if json-ld -tg=1
```

* Print all graphs for ontology's schema.

```
rdfdiff.py -g case.ttl -gf turtle -i output.json-ld -if json-ld -gg=1
```

### Submitting an Issue
If/when you run into an issue with a given RDF schema format or the verifier.py
script, please open an issue with the error
and as much technical detail as you can provide.
