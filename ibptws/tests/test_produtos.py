# -*- coding: utf-8 -*-
#
# ibptws/tests/test_produtos.py
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

from decimal import Decimal

import pytest

import requests

from ibptws.excecoes import ErroProdutoNaoEncontrado
from ibptws.excecoes import ErroIdentificacao
from ibptws.produtos import get_produto


def test_consulta_sucesso(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.instancia_resp_sucesso_produto
    monkeypatch.setattr(requests, 'get', mockreturn)
    p = get_produto('12340101')
    assert p.codigo == '12340101'
    assert p.ex == 0
    assert p.aliquota_nacional == Decimal(str(p.nacional))
    assert p.aliquota_estadual == Decimal(str(p.estadual))
    assert p.aliquota_importado == Decimal(str(p.importado))


def test_produto_nao_encontrado(monkeypatch):
    def mockreturn(endpoint, params=()):
        return pytest.ResponseMockup({}, requests.codes.not_found)
    monkeypatch.setattr(requests, 'get', mockreturn)
    with pytest.raises(ErroProdutoNaoEncontrado):
        p = get_produto('12340101')
        

def test_erro_identificacao(monkeypatch):
    def mockreturn(endpoint, params=()):
        return pytest.ResponseMockup({}, requests.codes.forbidden)
    monkeypatch.setattr(requests, 'get', mockreturn)
    with pytest.raises(ErroIdentificacao):
        p = get_produto('12340101')
        

def test_erro_inesperado(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.ResponseMockup({}, requests.codes.teapot)
    monkeypatch.setattr(requests, 'get', mockreturn)
    with pytest.raises(requests.HTTPError):
        p = get_produto('12340101')
