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
import clang.cindex
import warninginfo

E_VALUE_SCOPE_GB = 0x1
E_VALUE_SCOPE_FM = 0x2
E_VALUE_SCOPE_LC = 0x3
E_VALUE_SCOPE_UK = 0x4
E_VALUE_SCOPE_ERR = 0xFF

NODE_SCOPE_GB = 0x1
NODE_SCOPE_LC = 0x2
NODE_SCOPE_UK = 0x3

class SourceReader:
    def __init__(self):
        self.__index = clang.cindex.Index.create()

    def parse(self, tfile, tfunc, tvalue, tline):
        self.__tfile = tfile
        self.__tfunc = tfunc
        self.__tvalue = tvalue
        self.__tline = tline
        main_cursor = self.__index.parse(tfile, ['-x', 'c++']).cursor
        
        wi = warninginfo.WarningPointInfo()
        (ret_code, ret_node) = self.find_func_info(main_cursor)
        if ret_code == 0:
            print("Function %s Not Found" % (self.__tfunc))
            return None
        else:
            wi.set_func_info(ret_node)

        start_node = main_cursor         

        (ret_scope, ret_node) = self.find_value_info(start_node)
        if ret_scope == E_VALUE_SCOPE_ERR:
            print("Variable %s Not Found at %d" % (self.__tvalue, self.__tline))
            return None
        else:
            wi.set_var_info(ret_scope, ret_node)

        return wi

    def find_value_info(self, node):
        ## find variable in function first and get id        
        (ret_code, ret_node) = self.__find_value_hash(node)
        if ret_code == 0:
            return (E_VALUE_SCOPE_ERR, None)

        variable_def_hash = ret_node.referenced.hash
        (ret_scope, ret_node) = self.__find_value_decl(node, variable_def_hash, NODE_SCOPE_GB)
        if ret_scope == E_VALUE_SCOPE_UK:
            return (E_VALUE_SCOPE_ERR, None)
        else:
            return (ret_scope, ret_node)

    def __find_value_hash(self, node):
        if node.location.line == self.__tline and node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
            if self.__tvalue == node.spelling:
                self.__print_variable_info(node)
                return (1, node)

        for tnode in node.get_children():
            (ret_code, ret_node) = self.__find_value_hash(tnode)

            if ret_code != 0:
                return (ret_code, ret_node)
       
        return (0, None)

    def __find_value_decl(self, node, variable_def_hash, node_scope):
        if node.hash == variable_def_hash:
            self.__print_variable_info(node)
            if node.kind == clang.cindex.CursorKind.PARM_DECL:
                ret_scope = E_VALUE_SCOPE_LC
            elif node.kind == clang.cindex.CursorKind.FIELD_DECL:
                ret_scope = E_VALUE_SCOPE_FM
            elif node.kind == clang.cindex.CursorKind.VAR_DECL:
                if node_scope == NODE_SCOPE_GB:
                    ret_scope = E_VALUE_SCOPE_GB
                else:
                    ret_scope = E_VALUE_SCOPE_LC                
            return (ret_scope, node)

        for tnode in node.get_children():
            if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                (ret_scope, ret_node) = self.__find_value_decl(tnode, variable_def_hash, NODE_SCOPE_LC)
            else:
                (ret_scope, ret_node) = self.__find_value_decl(tnode, variable_def_hash, node_scope)

            if ret_scope != E_VALUE_SCOPE_UK:
                return (ret_scope, ret_node)
       
        return (E_VALUE_SCOPE_UK, None)

    def find_func_info(self, node):
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL or node.kind == clang.cindex.CursorKind.CXX_METHOD:
            if self.__tfunc == node.spelling:                
                print("Found at (%s)(%s) %s:%d:%d" % (node.spelling, node.type.spelling, node.extent.start.file, node.location.line, node.location.column))
                return (1, node)

        for tnode in node.get_children():
            (ret_code, ret_node) = self.find_func_info(tnode)
            if ret_code == 0:
                continue
            else:
                return (ret_code, ret_node)
        
        return (0, None)

    def __print_variable_info(self, node):
        def_node = node.referenced
        print("Found at (%s)(%s)(%s -> %s) %s:%d:%d" % (node.spelling, node.type.spelling, 
                                                        hex(node.hash), hex(def_node.hash),
                                                        node.extent.start.file, node.location.line, node.location.column))

if __name__ == "__main__":
    t = SourceReader()
    #t.parse("test/target.cpp", "testfunc", "g_avalue1", 23)
    t.parse("test/target.cpp", "testfunc", "param_var1", 31)
