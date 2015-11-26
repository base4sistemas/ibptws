# -*- coding: utf-8 -*-

import pytest
import fakeredis

import requests

from ibptws.provisoes import ProvisaoBase
from ibptws.provisoes import SemProvisao
from ibptws.provisoes import ProvisaoViaRedis


def test_provisao_base():
    p = ProvisaoBase()
    with pytest.raises(NotImplementedError):
        p.get_produto('12340101', 0)
    with pytest.raises(NotImplementedError):
        p.get_servico('1234')
        
        
def test_produto_sem_provisao(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.instancia_resp_sucesso_produto
    monkeypatch.setattr(requests, 'get', mockreturn)
    p = SemProvisao()
    produto = p.get_produto('12340101', 0)
    assert produto.codigo == '12340101'
    assert produto.ex == 0


def test_servico_sem_provisao(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.instancia_resp_sucesso_servico
    monkeypatch.setattr(requests, 'get', mockreturn)
    p = SemProvisao()
    produto = p.get_servico('0123')
    assert produto.codigo == '0123'
    assert produto.tipo == 'NBS'
    assert produto.uf == 'SP'


def test_produto_provisaoviaredis_provisionado():
    # insere dados no Redis falso para que a implementação obtenha os
    # dados do provisionamento, ao invés de acessar o web services...
    fredis = fakeredis.FakeStrictRedis()
    fredis.hmset('ncm:12340101:0', pytest.RESPOSTA_SUCESSO_PRODUTO())
    provisao = ProvisaoViaRedis(redis=fredis)
    produto = provisao.get_produto('12340101', 0)
    assert produto.codigo == '12340101'
    assert produto.ex == 0
    

def test_produto_provisaoviaredis_nao_provisionado(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.instancia_resp_sucesso_produto
    monkeypatch.setattr(requests, 'get', mockreturn)
    # agora não há provisionamento; o produto deverá ser obtido do
    # web services, que está em simulação (mocked)
    fredis = fakeredis.FakeStrictRedis()
    provisao = ProvisaoViaRedis(redis=fredis)
    produto = provisao.get_produto('12340101', 0)
    assert produto.codigo == '12340101'
    assert produto.ex == 0
    

def test_servico_provisaoviaredis_provisionado():
    # insere dados no Redis falso para que a implementação obtenha os
    # dados do provisionamento, ao invés de acessar o web services...
    fredis = fakeredis.FakeStrictRedis()
    fredis.hmset('nbs:0123', pytest.RESPOSTA_SUCESSO_SERVICO())
    provisao = ProvisaoViaRedis(redis=fredis)
    servico = provisao.get_servico('0123')
    assert servico.codigo == '0123'
    assert servico.uf == 'SP'
    assert servico.tipo == 'NBS'
    

def test_servico_provisaoviaredis_nao_provisionado(monkeypatch):
    def mockreturn(endpoint, params={}):
        return pytest.instancia_resp_sucesso_servico
    monkeypatch.setattr(requests, 'get', mockreturn)
    # agora não há provisionamento; o serviço deverá ser obtido do
    # web services, que está em simulação (mocked)
    fredis = fakeredis.FakeStrictRedis()
    provisao = ProvisaoViaRedis(redis=fredis)
    servico = provisao.get_servico('0123')
    assert servico.codigo == '0123'
    assert servico.uf == 'SP'
    assert servico.tipo == 'NBS'
    
