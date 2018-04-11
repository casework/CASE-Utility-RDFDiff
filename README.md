### Ontology-Verifier
A RDF Ontology verifier and ontology trouble shooter for CASE/UCO.

### What it does.
Ontology-Verifier takes output of a tool (JSON/JSON-LD/XML/etc...)
and attempts to verify it aligns with a RDF based ontology (OWL/N3/ttl).
Any entry in the tool's output that is NOT in the Ontology (specified via CLI)
will display an error. CLI arugments can be added to cause a debugger to start
so you may explore the graph to view where things went wrong.

### What it does not do.
This utility does not check ontology correctness. Due to CASE/UCO being flexible in implementation
, allowing for custom property bundles, and multiple ways of data representation there are multiple 
possibilities for what "correct" can be in a given scenario.



### How it works.
Verifier.py will read in an RDF vocabulary defined via ``` -g``` (glossary) to
check a custom tool's output against via ```-i```. The Python library [RDFLib](https://rdflib.readthedocs.io/en/stable/)
is used to turn the RDF schema into tripples which are then broken into three lists; 
subject, predicate and object. Finally, each element of the tools ouput within
the tool's subject and predicate are checked againast the glossary's subject 
and predicate to confirm the existence of these RDF elements. If an element is 
found or not found it is displayed to the user. BNodes are skipped  as they
have no appropriate label in RDF and should not be used to verify an ontology.


#### Why not SPARQL?
In order to facilitate a broad range of ontologies and custom tool outputs,
SPARQL queries are not used for verification. CASE/UCO allow for robust
flexibility and this tool  aims to compliment this approach.


### Installation.
```
sudo pip install -r requirements.txt 
```

### Unit Tests
The ontology verifier is heavily reliant on 3rd pary libraries, primarily RDFlib.
RDFLib is under heavy development. To ensure compatability with new releases
unit tests have been written to check for consistency.

#### Run Unit Tests
```
cd tests;
python test_verifier.py;
```

### Usage

#### CLI Usage
* ``` -g ```: Define the RDF schema (aka glossary) in use for your ontology.
* ``` -gf ```: Define the format the schema is in. By default verifier
will try to auto-guess based on extension. However, if additional plugins are
installed it is best practice to manually specify it.

* ``` -i ```: The external tool's output you want to verify the ontology 
against.

* ```-if```: Define RDF schema for tool data that's being injested.
* ```-tg```: Print subject, predicate, object for each graph within tool schema.
* ```-gg```: Print subject, predicate, object for each graph within glossary schema.
* ```-s```: Strict mode. Stop when first error is encountered.
* ```--debug```: Break on errors that occur within ```--verify```.
* ```--verbose```: View all matched and non-matched entries.
* ```--color```: Highlight successful and unsuccessful matches.


#### CLI Example


* Check for inconsistencies between graphs:

```
verify.py -g case.ttl -gf turtle -i output.json-ld -if json-ld --verify --strict
```
```
verify.py -g case.ttl -gf turtle -i output.json-ld -if json-ld -v -s
```

* Check for inconsistencies between graphs with color output:
```
verify.py -g case.ttl -gf turtle -i output.json-ld -if json-ld --verify --color
```

* Enter debug mode. This will cause a PDB session to open when an inconsistency is met. This can be useful for manually navigating the RDF graph in Python.:
```
verify.py -g case.ttl -gf turtle -i output.json-ld -if json-ld --verify --debug

```

* Print all graphs for tool's schema.

```
verify.py -g case.ttl -gf turtle -i output.json-ld -if json-ld -tg

```

* Print all graphs for ontology's schema.

```
verify.py -g case.ttl -gf turtle -i output.json-ld -if json-ld -gg

```

### Submitting an Issue
If/when you run into an issue with a given RDF schema format or the verifier.py script, please open an issue with the error
and as much technical detail as you can provide.
