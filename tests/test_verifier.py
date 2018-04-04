# 'Approved for Public Release; Distribution Unlimited. Case Number 18-0399'.

# NOTICE
# 
# This software was produced for the U.S. Government under
# contract SB-1341-14-CQ-0010, and is subject to the Rights
# in Data-General Clause 52.227-14, Alt. IV (DEC 2007)
#
# (c) 2018 The MITRE Corporation. All Rights Reserved.


#!/usr/bin/env python
import unittest

class TestRDFMethods(unittest.TestCase):

    def setUp(self):
        import rdflib
        self.rdfObj = rdflib

    def test_rdflib_has_methods(self):
        """
        Name: test_rdflib_methods
        Description: Test 3rd party library so that methods exist.
                     RDF is actively developed, this will identify
                     potential comparability errors.
        Parameters: None.
        Return: None.
        """
        self.assertTrue(hasattr(self.rdfObj, 'ConjunctiveGraph'))
        self.assertTrue(hasattr(self.rdfObj, 'Graph'))


class TestRDFFIleParsing(unittest.TestCase):

    def setUp(self):
        import rdflib
        self.graph = rdflib.Graph()
        self.rdfObj = rdflib

    def test_turtle_read(self):
        """
        Name: test_turtle_read
        Description: Reda in turtle (ttl) file, and create a graph.
        Parameters: None.
        Return: None.
        """
        try:
            isinstance(self.graph.parse("test_rdf/test.ttl", format="turtle"), self.rdfObj.graph.Graph)
        except IOError as io_err:
            print("Error, %s" % io_err)

    def test_jsonld_read(self):
        """
        Name: test_turtle_read
        Description: Reads in JSON-LD file, and create a Conjunctive graph.
        Parameters: None.
        Return: None.
        """
        try:
            isinstance(self.graph.parse("test_rdf/test.json-ld", format="json-ld"), self.rdfObj.graph.ConjunctiveGraph)
        except IOError as io_err:
            print("Error, %s" % io_err)



if __name__ == '__main__':
    unittest.main(verbosity=2)
