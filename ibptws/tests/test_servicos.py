# -*- coding: utf-8 -*-
#
# ibptws/tests/test_servicoes.py
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

from ibptws.excecoes import ErroServicoNaoEncontrado
from ibptws.excecoes import ErroIdentificacao
from ibptws.servicos import get_servico


RESPOSTA_SUCESSO = {
        'codigo': '0123',
        'uf': 'SP',
        'descricao': u'Serviço Simples',
        'tipo': 'NBS',
        'nacional': 0.1,
        'estadual': 0.2,
        'municipal': 0.3,
        'importado': 0.4,}


def test_consulta_sucesso(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.ResponseMockup(RESPOSTA_SUCESSO, requests.codes.ok)
    monkeypatch.setattr(requests, 'get', mockreturn)
    p = get_servico('0123')
    assert p.codigo == '0123'
    assert p.tipo == 'NBS'
    assert p.aliquota_nacional == Decimal(str(p.nacional))
    assert p.aliquota_importado == Decimal(str(p.importado))
    assert p.aliquota_estadual == Decimal(str(p.estadual))
    assert p.aliquota_municipal == Decimal(str(p.municipal))


def test_servico_nao_encontrado(monkeypatch):
    def mockreturn(endpoint, params=()):
        return pytest.ResponseMockup({}, requests.codes.not_found)
    monkeypatch.setattr(requests, 'get', mockreturn)
    with pytest.raises(ErroServicoNaoEncontrado):
        p = get_servico('0123')


def test_erro_identificacao(monkeypatch):
    def mockreturn(endpoint, params=()):
        return pytest.ResponseMockup({}, requests.codes.forbidden)
    monkeypatch.setattr(requests, 'get', mockreturn)
    with pytest.raises(ErroIdentificacao):
        p = get_servico('0123')


def test_erro_inesperado(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.ResponseMockup({}, requests.codes.teapot)
    monkeypatch.setattr(requests, 'get', mockreturn)
    with pytest.raises(requests.HTTPError):
        p = get_servico('12340101')
