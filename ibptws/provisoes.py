# -*- coding: utf-8 -*-
#
# ibptws/provisoes.py
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

import redis

from .produtos import get_produto, Produto
from .servicos import get_servico, Servico


EXPIRA_EM_24H = 24 * 60 * 60


class ProvisaoBase(object):
    """
    Classe base para o provisionamento da consulta, tornando possível o
    armazenamento das consultas dos valores aproximados dos tributos em
    cache, acelerando a consulta para produtos e serviços recém consultados.
    
    Esta classe em particular não faz esse provisionamento, apenas fornece
    uma base para os métodos básicos que darão suporte ao provisionamento.
    Uma implementação de provisionamento mínima deverá sobrescrever os métodos
    :meth:`get_produto` e :meth:`get_servico`.
    
    .. versionadded:: 0.3
    """
    
    def get_produto(self, ncm, ncm_ex):
        """
        Obtém as alíquotas para um produto conforme seu NCM/SH e exceção.
        As implementações de provisionamento deverão sobrescrever este método
        para obter os dados do provisionamento ou do web services do IBPT,
        quando não houver um provisionamento disponível.
        
        :param str ncm: O código NCM/SH do produto.
        :param int ncm_ex: A exceção da NCM. Note que, diferentemente da
            função :func:`~ibptws.produtos.get_produto`, este argumento não é
            opcional. Informe ``0`` se não houver exceção.
            
        :return: Retorna os dados do produto solicitado.
        :rtype: ibptws.produtos.Produto
        """
        raise NotImplementedError()
        
    
    def get_servico(self, nbs):
        """
        Obtém as alíquotas para um serviço conforme seu código NBS.
        As implementações de provisionamento deverão sobrescrever este método
        para obter os dados do provisionamento ou do web services do IBPT,
        quando não houver um provisionamento disponível.
        
        :param str nbs: O código NBS do serviço.

        :return: Retorna os dados do serviço solicitado.
        :rtype: ibptws.servicos.Servico
        """
        raise NotImplementedError()
        
        
class SemProvisao(ProvisaoBase):
    """
    Implementa uma base não provisionada, para ser utilizada como padrão em
    serviços que poderiam ser provisionados se houvesse uma implementação de
    provisionamento adequada. É contraditório mas esta classe não faz nenhum
    provisionamento, apenas acessa o web services do IBPT quando forem
    solicitados produtos e serviços.
    
    .. versionadded:: 0.3
    """
    
    def get_produto(self, ncm, ncm_ex):
        return get_produto(ncm, ncm_ex)
        
    
    def get_servico(self, nbs):
        return get_servico(nbs)


class ProvisaoViaRedis(ProvisaoBase):
    """
    Implementa um provisionamento baseado em um servidor `Redis`_.
    Produtos e serviços solicitados serão obtidos do web services do IBPT e
    então provisionados, com uma expiração padrão de 24h de modo que, dentro
    desse prazo, toda solicitação feita para um produto ou serviço provisionados
    serão obtidos de um servidor Redis, ao invés de acessar o web services.
    
    .. versionadded:: 0.3
    """
    
    def __init__(self, redis=None, expires=EXPIRA_EM_24H, **kwargs):
        """
        Inicia uma instância de :class:`ProvisaoViaRedis`.
        
        :param redis: Uma instância do servidor Redis. Normalmente, deverá ser
            uma instância ``redis.StrictRedis``(veja `redis-py`_). Mas poderá
            ser qualquer implementação que se comporte da mesma maneira. Se
            este argumento não for informado, será criada uma instância de
            ``redis.StrictRedis``, cujos argumentos deverão ser os mesmos
            argumentos esperados pela classe ``StrictRedis``.
            
        :param int expires: Especifica o tempo que uma consulta à produto ou
            serviço deverá durar até que expire, exigindo que seja feita uma
            nova consulta ao web services. Em segundos. Padrão é 24 horas.

        """
        self._redis = redis
        self._expires = expires
        self._kwargs = kwargs
        
    
    def _connect(self):
        self._redis = redis.StrictRedis(**self._kwargs)
        
        
    def _sanear(self, classe_entidade, dados):
        entidade = classe_entidade(**{k.lower():v for k,v in dados.items()})
        return getattr(self, '_sanear_{}'.format(
                classe_entidade.__name__.lower()))(entidade)
                
                
    def _sanear_produto(self, produto):
        return produto._replace(
                codigo=produto.codigo.decode('utf-8'),
                uf=produto.uf.decode('utf-8'),
                descricao=produto.descricao.decode('utf-8'),
                ex=int(produto.ex),
                nacional=float(produto.nacional),
                importado=float(produto.importado),
                estadual=float(produto.estadual))
                
    
    def _sanear_servico(self, servico):
        return servico._replace(
                codigo=servico.codigo.decode('utf-8'),
                uf=servico.uf.decode('utf-8'),
                descricao=servico.descricao.decode('utf-8'),
                tipo=servico.tipo.decode('utf-8'),
                nacional=float(servico.nacional),
                importado=float(servico.importado),
                estadual=float(servico.estadual),
                municipal=float(servico.municipal))
                

    def _get(self, metodo, classe_entidade, chave, *args, **kwargs):
        if self._redis is None:
            self._connect()
        
        dados = self._redis.hgetall(chave)
        
        if dados:
            # compõe a entidade dos dados obtidos do provisionamento, porém,
            # dados provisionados no Redis são convertidos para strings, por
            # isso é necessário sanear os atributos da entidade resultante
            # convertendo para os tipos Python corretos...
            entidade = self._sanear(classe_entidade, dados)
        else:
            # não foi possível obter do provisionamento,
            # obtém do web services do IBPT...
            entidade = metodo(*args, **kwargs)
            # ...e provisiona os dados obtidos
            with self._redis.pipeline() as pipe:
                pipe.hmset(chave, unicode_to_str(entidade._asdict()))
                pipe.expire(chave, self._expires)
                pipe.execute()

        return entidade
        
        
    def get_produto(self, ncm, ncm_ex):
        chave = 'ncm:{}:{}'.format(ncm, ncm_ex)
        return self._get(get_produto, Produto, chave, ncm, ncm_ex)
        
    
    def get_servico(self, nbs):
        chave = 'nbs:{}'.format(nbs)
        return self._get(get_servico, Servico, chave, nbs)


def unicode_to_str(self, d):
    """
    Runs through dictionary keys, converting every unicode value to str.
    """
    convert = lambda v: v.encode('utf-8') if isinstance(v, unicode) else v
    return {k: convert(v) for k, v in d.items()}
