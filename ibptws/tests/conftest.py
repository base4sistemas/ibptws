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
        'descricao': 'Produto Simples',
        'nacional': 4.2,
        'importado': 4.8,
        'estadual': 18.0,
    }

RESPOSTA_SUCESSO_PRODUTO_ALT_A = {
        'codigo': '12340202',
        'uf': 'SP',
        'ex': 0,
        'descricao': 'Produto Simples Alternativo (A)',
        'nacional': 4.2,
        'importado': 5.41,
        'estadual': 0.0,
    }
    
RESPOSTA_SUCESSO_PRODUTO_ALT_B = {
        'codigo': '12340303',
        'uf': 'SP',
        'ex': 0,
        'descricao': 'Produto Simples Alternativo (B)',
        'nacional': 4.2,
        'importado': 6.18,
        'estadual': 12.0,
    }

RESPOSTA_SUCESSO_SERVICO = {
        'codigo': '0123',
        'uf': 'SP',
        'descricao': u'Servico Simples', # veja NOTA acima
        'tipo': 'NBS',
        'nacional': 13.45,
        'importado': 14.05,
        'estadual': 0,
        'municipal': 4.33,
    }
    
RESPOSTA_SUCESSO_SERVICO_ALT_A = {
        'codigo': '0124',
        'uf': 'SP',
        'descricao': u'Servico Simples Alternativo (A)', # veja NOTA acima
        'tipo': 'NBS',
        'nacional': 13.45,
        'importado': 14.05,
        'estadual': 0,
        'municipal': 3.55,
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
            'instancia_resp_sucesso_produto_alt_a': ResponseMockup(
                    RESPOSTA_SUCESSO_PRODUTO_ALT_A,
                    requests.codes.ok),
            'instancia_resp_sucesso_produto_alt_b': ResponseMockup(
                    RESPOSTA_SUCESSO_PRODUTO_ALT_B,
                    requests.codes.ok),
            'instancia_resp_sucesso_servico': ResponseMockup(
                    RESPOSTA_SUCESSO_SERVICO,
                    requests.codes.ok),
            'instancia_resp_sucesso_servico_alt_a': ResponseMockup(
                    RESPOSTA_SUCESSO_SERVICO_ALT_A,
                    requests.codes.ok),
        }
