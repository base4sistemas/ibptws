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

#
# NOTA: Veja https://github.com/jamesls/fakeredis/issues/91
#       Por essa razão, não utilize sequências fora da faixa ASCII, caso
#       contrário, 'fakeredis' irá falhar ao converter um comando Redis.
#

RESPOSTA_SUCESSO_PRODUTO = {
        'codigo': '12340101',
        'uf': 'SP',
        'ex': 0,
        'descricao': 'Teste simples',
        'nacional': 0.1,
        'estadual': 0.2,
        'importado': 0.3,
    }

RESPOSTA_SUCESSO_SERVICO = {
        'codigo': '0123',
        'uf': 'SP',
        'descricao': u'Servico Simples', # veja NOTA acima
        'tipo': 'NBS',
        'nacional': 0.1,
        'estadual': 0.2,
        'municipal': 0.3,
        'importado': 0.4,
    }


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
    return {
            'ResponseMockup': ResponseMockup,
            'RESPOSTA_SUCESSO_PRODUTO': lambda: RESPOSTA_SUCESSO_PRODUTO,
            'RESPOSTA_SUCESSO_SERVICO': lambda: RESPOSTA_SUCESSO_SERVICO,
            'instancia_resp_sucesso_produto': ResponseMockup(
                    RESPOSTA_SUCESSO_PRODUTO,
                    requests.codes.ok),
            'instancia_resp_sucesso_servico': ResponseMockup(
                    RESPOSTA_SUCESSO_SERVICO,
                    requests.codes.ok),
        }
