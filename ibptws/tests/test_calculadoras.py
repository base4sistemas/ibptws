# -*- coding: utf-8 -*-
#
# ibptws/tests/test_calculadoras.py
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

from ibptws.calculadoras import DeOlhoNoImposto
from ibptws.calculadoras import CEM


def test_deolhonoimposto_inicio():
    calc = DeOlhoNoImposto()
    assert calc.carga_federal().is_zero()
    assert calc.carga_federal_nacional().is_zero()
    assert calc.carga_federal_importado().is_zero()
    assert calc.carga_estadual().is_zero()
    assert calc.carga_municipal().is_zero()
    assert calc.total_tributos().is_zero()
    assert calc.total().is_zero()
    assert calc.percentual_sobre_total().is_zero()


def test_deolhonoimposto_um_item(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.instancia_resp_sucesso_produto
    monkeypatch.setattr(requests, 'get', mockreturn)
    
    valor = Decimal('10') # subtotal do produto
    
    # os valores das alíquotas retornadas estão em conftest.py
    carga_fed_nac = valor * (Decimal('4.2') / CEM)
    carga_fed_imp = valor * (Decimal('4.8') / CEM)
    carga_estadual = valor * (Decimal('18') / CEM)
    
    calc = DeOlhoNoImposto()
    calc.produto('12340101', 0, valor)
    
    assert calc.total() == valor, 'Total nao confere com o valor do unico item'
    assert calc.total() > calc.total_tributos(), 'Soma dos valores dos '\
            'itens menor ou igual ao valor total dos tributos'
            
    assert calc.carga_federal_nacional() == carga_fed_nac
    assert calc.carga_federal_importado() == carga_fed_imp
    assert calc.carga_federal() == carga_fed_nac + carga_fed_imp
    assert calc.carga_estadual() == carga_estadual
    assert calc.carga_municipal().is_zero()
    
    assert calc.total_tributos() == sum([
            carga_fed_nac, carga_fed_imp, carga_estadual,])
    
    assert calc.total() == valor
    
    # testa o reinicio da calculadora
    calc.reiniciar()
    assert calc.carga_federal().is_zero()
    assert calc.carga_federal_nacional().is_zero()
    assert calc.carga_federal_importado().is_zero()
    assert calc.carga_estadual().is_zero()
    assert calc.carga_municipal().is_zero()
    assert calc.total_tributos().is_zero()
    assert calc.total().is_zero()
    assert calc.percentual_sobre_total().is_zero()


def test_deolhonoimposto_multiplos_itens(monkeypatch):
    def mockreturn(endpoint, params={}):
        dados = {
                '12340101': pytest.instancia_resp_sucesso_produto,
                '12340202': pytest.instancia_resp_sucesso_produto_alt_a,
                '12340303': pytest.instancia_resp_sucesso_produto_alt_b,
                '0123': pytest.instancia_resp_sucesso_servico,
                '0124': pytest.instancia_resp_sucesso_servico_alt_a,}
        return dados.get(params.get('codigo'))
    monkeypatch.setattr(requests, 'get', mockreturn)
    
    calc = DeOlhoNoImposto()

    calc.produto('12340101', 0, Decimal('5.00'))
            # nacional     4,2% : 0,21
            # importado    4,8% : 0,24
            # estadual      18% : 0,9
            # muncipal       0% : 0          total tributos: 1,35
            
    calc.produto('12340202', 0, Decimal('15.50'))
            # nacional     4,2% : 0,651
            # importado   5,41% : 0,83855
            # estadual       0% : 0
            # muncipal       0% : 0          total tributos: 1,48955
            
    calc.produto('12340303', 0, Decimal('7.30'))
            # nacional     4,2% : 0,3066
            # importado   6,18% : 0,45114
            # estadual      12% : 0,876
            # muncipal       0% : 0          total tributos: 1,63374
            
    calc.servico('0123', Decimal('100'))
            # nacional   13,45% : 13,45
            # importado  14,05% : 14,05
            # estadual       0% :  0
            # muncipal    4,33% :  4,33      total tributos: 31,83
            
    calc.servico('0124', Decimal('575.77'))
            # nacional   13,45% : 77,441065
            # importado  14,05% : 80,895685
            # estadual       0% :  0
            # muncipal    3,55% : 20,439835  total tributos: 178,776585
    
    # total (soma dos valores dos itens) : R$ 703,57
    # valor total dos tributos           : R$ 215,079875
    # % total dos tributos sobre o valor : 30,569790497%
    
    carga_fed_nac = sum([
            Decimal('0.21'),
            Decimal('0.651'),
            Decimal('0.3066'),
            Decimal('13.45'),
            Decimal('77.441065'),])
    
    carga_fed_imp = sum([
            Decimal('0.24'),
            Decimal('0.83855'),
            Decimal('0.45114'), # inclui os zeros para ilustrar
            Decimal('14.05'),
            Decimal('80.895685'),])
            
    carga_estadual = sum([
            Decimal('0.9'),
            Decimal('0'),
            Decimal('0.876'),
            Decimal('0'),
            Decimal('0'),])
            
    carga_municipal = sum([
            Decimal('0'),
            Decimal('0'),
            Decimal('0'),
            Decimal('4.33'),
            Decimal('20.439835'),])
    
    total_tributos = sum([
            carga_fed_nac,
            carga_fed_imp,
            carga_estadual,
            carga_municipal,])
    
    total = Decimal('703.57')
    p_sobre_total = total_tributos / total
            
    assert calc.total() == total, 'Total nao confere com o valor do unico item'
    assert calc.total() > calc.total_tributos(), 'Soma dos valores dos '\
            'itens menor ou igual ao valor total dos tributos'
            
    assert calc.carga_federal_nacional() == carga_fed_nac
    assert calc.carga_federal_importado() == carga_fed_imp
    assert calc.carga_federal() == carga_fed_nac + carga_fed_imp
    assert calc.carga_estadual() == carga_estadual
    assert calc.carga_municipal() == carga_municipal
    
    assert calc.total_tributos() == total_tributos
    
    assert calc.total() == total
    assert calc.percentual_sobre_total() == p_sobre_total
    
    # testa o reinicio da calculadora
    calc.reiniciar()
    assert calc.carga_federal().is_zero()
    assert calc.carga_federal_nacional().is_zero()
    assert calc.carga_federal_importado().is_zero()
    assert calc.carga_estadual().is_zero()
    assert calc.carga_municipal().is_zero()
    assert calc.total_tributos().is_zero()
    assert calc.total().is_zero()
    assert calc.percentual_sobre_total().is_zero()
