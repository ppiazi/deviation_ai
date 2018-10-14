# -*- coding: utf-8 -*-
"""
Copyright 2015 Joohyun Lee(ppiazi@gmail.com)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
import sourcereader

class test_sourcereader(unittest.TestCase):
    testTarget = None
    
    def setUp(self):
        self.sr = sourcereader.SourceReader()    

    def tearDown(self):
        pass

    def test_find_local_variable(self):
        wi = self.sr.parse("test/target.cpp", "testfunc", "param_var1", 31)
        var_info = wi.get_var_info()
        assert(var_info["name"] == "param_var1")
        assert(var_info["scope"] == sourcereader.E_VALUE_SCOPE_LC)
        assert(var_info["def_loc"].line == 21)
        

    def test_find_local_variable_2(self):
        wi = self.sr.parse("test/target.cpp", "testfunc", "lc_var", 23)
        var_info = wi.get_var_info()
        assert(var_info["name"] == "lc_var")
        assert(var_info["scope"] == sourcereader.E_VALUE_SCOPE_LC)

    def test_find_local_variable_3(self):
        wi = self.sr.parse("test/target.cpp", "testfunc", "arr", 27)
        var_info = wi.get_var_info()
        assert(var_info["name"] == "arr")
        assert(var_info["scope"] == sourcereader.E_VALUE_SCOPE_LC)

    def test_find_nonexist_variable(self):
        wi = self.sr.parse("test/target.cpp", "test", "non_exist_var", 1)
        assert( wi == None )

    def test_find_global_variable1(self):
        wi = self.sr.parse("test/target.cpp", "testfunc", "g_avalue1", 23)
        var_info = wi.get_var_info()
        assert(var_info["name"] == "g_avalue1")
        assert(var_info["scope"] == sourcereader.E_VALUE_SCOPE_GB)

    def test_find_global_variable_with_namespace(self):
        pass
        #wi = self.sr.parse("test/target.cpp", "mymethod", "g_avalue2", 14)
        #var_info = wi.get_var_info()
        #assert(var_info["name"] == "g_avalue2")
        #assert(var_info["scope"] == sourcereader.E_VALUE_SCOPE_GB)


if __name__ == "__main__":
    unittest.main()
