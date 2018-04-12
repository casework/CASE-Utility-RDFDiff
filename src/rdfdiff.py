# 'Approved for Public Release; Distribution Unlimited. Case Number 18-0399'.

# NOTICE
# 
# This software was produced for the U.S. Government under
# contract SB-1341-14-CQ-0010, and is subject to the Rights
# in Data-General Clause 52.227-14, Alt. IV (DEC 2007)
#
# (c) 2018 The MITRE Corporation. All Rights Reserved.


#!/usr/bin/python2.7
import sys
import argparse
import xml
import pdb

try:
    from colorama import Fore, init
    import rdflib_jsonld
    import rdflib
    from rdflib import Graph, Namespace, exceptions
    from rdflib import URIRef, RDFS, RDF, BNode, compare
except ImportError as import_err:
    print("[Error] Missing package %s" % import_err)
    sys.exit()

init(convert=True)  # Used for printing colorful text.


class Verifier:

    def __init__(self, custom_glossary, glossary_format, injest_format, tool_injest):

        """
        Name: __init__
        Description: Read in the initial glossary to perform queries against.
                     RDFLib's guess_format function is utilized to choice the
                     appropriate file type (rdf/turtle/rma/xml/etc...)
        Parameter: (str) ontology_glossary: user defined glossary via -g.
                   (str) format: Explicitly defined format.
        Return: N/A
        """

        self.custom_gloss = custom_glossary
        self.gloss_format = glossary_format

        self.tool_output = tool_injest
        self.tool_format = injest_format

        self.custom_gloss_subject = []
        self.custom_gloss_predicate = []
        self.custom_gloss_object = []

        self.tool_output_subject = []
        self.tool_output_predicate = []
        self.tool_output_object = []

    def __graph_parse__(self, rdf_graph_file, graph_format):
        """
        Description: Read in graph to parse.
        Parameter: (str) rdf_graph: user defined glossary via -g & -i.
        Return: RDF graph
        """

        # Required RDFLib graph for JSON-LD, there is an open Stackoverflow issue at this time.
        if graph_format.lower() == 'json-ld':
            # Required RDFLib graph for JSON-LD, there is an open Stackoverflow issue at this time.
            self.graph = rdflib.graph.ConjunctiveGraph()
#            self.graph.parse(rdf_graph_file, format="json-ld")
        else:
            self.graph = rdflib.Graph()

        try:
            if graph_format == "json-ld":
                #  graph_format, even when set to the stream "json-ld" will not properly
                # be processed by RDFLib's graph.parse format parameter, thus it is explicitly defined below.
                self.graph.parse(rdf_graph_file, format="json-ld")
            else:
                self.graph.parse(rdf_graph_file, format=graph_format)
            return self.graph

        except rdflib.plugin.PluginException as plug_err:
            print("[Error] Plugin does not exist %s.\nThis mostly means '%s' cannot be parsed or does not exist.\n"
                  % (plug_err, graph_format) + "Is there another name for the plugin you're trying to use?" +
                  "(Ex: 'turtle' vs 'ttl')")
            sys.exit(1)

        except rdflib.plugins.parsers.notation3.BadSyntax as rdfplug_err:
            print(Fore.RED + "[Parsing Error] %s.\nDid you specify the correct format?" % rdfplug_err)
            sys.exit(1)

        except IOError as io_err:
            print(Fore.RED + "[Error] %s.\nMost likely because %s does not exist.\n"  % (io_err, rdf_graph_file))
            sys.exit(1)

        except ValueError as val_err:
            print(Fore.RED + "[Parsing Error] %s." % val_err)
            sys.exit(1)

        except xml.sax._exceptions.SAXException as xml_err:
            print(Fore.RED + "[XMLError] %s." % xml_err)
            sys.exit(1)

    def __populate_lists__(self, rdf_graph, graph_format, subject_list, predicate_list, object_list,
                           ignore_bnodes=True):
        """
        Name: __populate_lists__
        Description: Iterate through RDF graphs and populate subject, predicate, object lists.
        Parameters:
                    rdf_graph:  RDF graph to parse.
                    graph_format: XML/JSON-LD/TTL/N3
                    subject_list: List for subject portion of RDF triples.
                    predicate_list: List for predicate portion of RDF triples.
                    object_list: List for object portion of RDF triples.
                    ignore_bnodes: Skipping Blank Nodes in RDF graphs.
        Return: None
        """
        graph = self.__graph_parse__(rdf_graph, graph_format)

        try:
            for subject, predicate, rdf_object in graph:
                if ignore_bnodes is True:
                    if isinstance(subject, rdflib.term.BNode) or isinstance(predicate, rdflib.term.BNode) or \
                            isinstance(object, rdflib.term.BNode):
                        pass
                    else:
                        subject_list.append(subject)
                        predicate_list.append(predicate)
                        object_list.append(rdf_object)
                else:
                    subject_list.append(subject)
                    predicate_list.append(predicate)
                    object_list.append(rdf_object)

        except AttributeError as attr_err:
            print("[iter] Error parsing graph: %s" % str(attr_err))

    def compare_graphs(self):
        """
        Name: compare_graphs
        Description: Iterate through RDF graphs and populate subject, predicate, object lists.
        Parameters: None.
        Return: None.
        """
        print("Loading graphs for comparison...")
        graph = self.__graph_parse__(self.custom_gloss, self.gloss_format)
        graph_tool = self.__graph_parse__(self.tool_output, self.tool_format)
        in_both , in_graph, in_graph_tool = compare.graph_diff(graph, graph_tool)

    def populate_graphs(self):
        """
        Name: compare_graphs
        Description: Iterate through graphs
        Return: None.
        """

        self.__populate_lists__(self.custom_gloss, self.gloss_format, self.custom_gloss_subject,
                                self.custom_gloss_predicate, self.custom_gloss_object, True)

        self.__populate_lists__(self.tool_output, self.tool_format, self.tool_output_subject,
                                self.tool_output_predicate, self.tool_output_object, True)

    def print_tools_graph(self, color):
        """
        Name: print_tools_graph
        Description: Printing RDF graphs.
        Parameter: None.
        Return: N/A.
        """
        if color is not None:
            color= Fore.GREEN
        else:
            color = Fore.WHITE

        print(color + "\n[Tool Subject]\n")
        for element in self.tool_output_subject:
            print(color + "\t"+element)

        print(color + "\n[Tool Predicate]\n")
        for element in self.tool_output_predicate:
            print(color + "\t"+element)

        print(color + "\n[Tool Object]\n")
        for element in self.tool_output_object:
            print(color + "\t"+element)


    def print_glossary_graph(self, color):
        """
        Name: print_glossary_graph
        Description: Printing RDF graphs.
        Parameter: None.
        Return: N/A.
        """
        if color is not None:
            color= Fore.GREEN
        else:
            color = Fore.WHITE

        print(color + "[Custom Gloss Predicate]\n")
        print("custom_output_predicate")
        for element in self.custom_gloss_predicate:
            print(color + "\t" + element)

        print(color + "[Custom Gloss Subject]\n")
        for element in self.custom_gloss_subject:
            print(color + "\t" + element)

        print(color + "[Custom Gloss Object]\n")
        for element in self.custom_gloss_object:
            print(color + "\t" + element)


    def print_graphs(self):
        """
        Name: print_graphs
        Description: Printing RDF graphs.
        Parameter: None.
        Return: N/A.
        """

        print(Fore.GREEN + "[Tool Predicate]\n")
        for element in self.tool_output_predicate:
            print(Fore.GREEN + "\t"+element)

        print(Fore.GREEN + "\n[Tool Subject]\n")
        for element in self.tool_output_subject:
            print(Fore.GREEN + "\t"+element)

        print(Fore.GREEN + "\n[Tool Object]\n")
        for element in self.tool_output_object:
            print(Fore.GREEN + "\t"+element)

        print(Fore.GREEN + "[Custom Gloss Predicate]\n")
        print("custom_output_predicate")
        for element in self.custom_gloss_predicate:
            print(Fore.GREEN + "\t" + element)

        print(Fore.GREEN + "[Custom Gloss Subject]\n")
        for element in self.custom_gloss_subject:
            print(Fore.GREEN + "\t" + element)

        print(Fore.GREEN + "[Custom Gloss Object]\n")
        for element in self.custom_gloss_object:
            print(Fore.GREEN + "\t" + element)

    def verify_object_existance(self, debug, color):
        """
        Name: verify_object_existence
        Description: Iterate through custom tool structure and
                     checking its existence within the glossary structure.
        Parameter: None
        Return: N/A
        """

        for predicate in self.tool_output_predicate:
            if (predicate in self.custom_gloss_predicate) \
                    or (predicate in self.custom_gloss_subject) \
                    or (predicate in self.custom_gloss_object):
                if color is not None:
                    print(Fore.GREEN + "[+] Match!\n\t%s in %s and %s\n" % (predicate, self.custom_gloss, self.tool_output))
                else:
                    print("[+] Match!\n\t%s in %s and %s\n" % (predicate, self.custom_gloss, self.tool_output))
            else:
                if color is not None:
                    print(Fore.RED + "[!] %s not in %s, but it is in %s\n" % (predicate, self.custom_gloss,
                                                                          self.tool_output))
                else:
                    print("[!] %s not in %s, but it is in %s\n" % (predicate, self.custom_gloss,
                                                                              self.tool_output))

                if debug is not None:
                    print(Fore.WHITE + "="*10+"[ Entering Debug Mode ]" + "="*10+"\n")
                    pdb.set_trace()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    try:

        parser.add_argument("-g", "--glossary", required=True, help="Specify glossary to base ontology upon.")
        parser.add_argument("-i", "--ingest", required=True, help="Specify external tool output to ingest.")

        # RDFLib has an auto-guessing format utility. You do not HAVE to explicitly specify the format.
        # However RDFLib does have issues guessing formats that are plugins, IE: JSON-LD.
        # It is recommend to explicitly specify the format to avoid issues, thus required is set to True.
        parser.add_argument("-gf", "--glossaryFormat", required=True,
                            help="Specify RDF format of ontology (turtle,n3,xml,json-ld)")

        parser.add_argument("-if", "--ingestFormat", required=True,
                            help="Specify external tool format (turtle,n3,xml,json-ld).")

        parser.add_argument("-pdb", "--debug", required=False, help="Break on errors within --verify.")
        parser.add_argument("-v", "--verify", required=False, help="Iterate over RDFgraphs between tool output and a" +
                            "given RDFSchema. Differences and similaries (ignoring BNodes) will be displayed.")

        parser.add_argument("-tg", "--toolgraph", required=False, help="Print all graphs from tool schema.")
        parser.add_argument("-gg", "--glossarygraph", required=False, help="Print all graphs from glossary schema.")

        parser.add_argument("--color", required=False, help="Utilize color output.")

    except argparse.ArgumentError as err:
        print ("[Error] %s is required." % err)

    finally:
        parser.parse_args()
        args = parser.parse_args()

    vobj = Verifier(args.glossary, args.glossaryFormat, args.ingestFormat, args.ingest)
    vobj.populate_graphs()

    if args.verify:
        vobj.verify_object_existance(args.debug, args.color)
    elif args.toolgraph:
        vobj.print_tools_graph(args.color)
    elif args.glossarygraph:
        vobj.print_glossary_graph(args.color)
    else:
        parser.print_help()
