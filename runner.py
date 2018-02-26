import unittest
from select_results import SelectResults
from org_search import PythonOrgSearch

def suite():
    suite = unittest.TestSuite()
    suite.addTest(PythonOrgSearch('test_search_in_python_org'))
    suite.addTest(SelectResults('test_select'))
    unittest.TextTestRunner(verbosity=2).run(suite)


suite()
