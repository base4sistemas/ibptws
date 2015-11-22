# -*- coding: utf-8 -*-
#
# ibptws/tests/conftest.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests


class ResponseMockup(object):
    
    def __init__(self, response_data, status_code):
        self._response_data = response_data
        self._status_code = status_code
    
    @property
    def status_code(self):
        return self._status_code
        
    def json(self):
        return self._response_data
        
    def raise_for_status(self):
        raise requests.HTTPError(str(self.status_code))


def pytest_namespace():
    return {'ResponseMockup': ResponseMockup,}
