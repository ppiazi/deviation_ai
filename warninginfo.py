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

import sourcereader

class WarningPointInfo:
    def __init__(self):
        self.__var = {}
        self.__var["scope"] = None
        self.__var["name"] = None
        self.__var["type"] = None
        self.__var["node"] = None

        self.__func = {}
        self.__func["name"] = None
        self.__func["ref"] = None

    def set_var_info(self, scope, node):
        self.__var["scope"] = scope
        self.__var["name"] = node.spelling
        self.__var["type"] = node.type.spelling
        self.__var["loc"] = node.location
        self.__var["def_loc"] = node.referenced.location
        self.__var["node"] = node
        self.__var["def_node"] = node.referenced

    def get_var_info(self):
        return self.__var

    def set_func_info(self, node):
        self.__func["name"] = node.spelling
        self.__func["node"] = node

    def get_func_info(self):
        return self.__func
