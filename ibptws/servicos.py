# -*- coding: utf-8 -*-
#
# ibptws/servico.py
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

from collections import namedtuple
from decimal import Decimal

import requests

from .config import conf
from .excecoes import ErroIdentificacao
from .excecoes import ErroServicoNaoEncontrado


_Servico = namedtuple('_Servico',
        'codigo uf descricao tipo nacional importado estadual municipal')

class Servico(_Servico):
    """
    Resposta à consulta de Serviços.

    .. warning::

        Note que os atributos ``nacional``, ``estadual``, ``municipal`` e
        ``importado`` são valores de ponto flutuante. Para obter objetos
        :class:`Decimal`, utilize os atributos :attr:`aliquota_nacional`,
        :attr:`aliquota_importado`, :attr:`aliquota_estadual` e
        :attr:`aliquota_municipal`.

    """
    
    __slots__ = ()
    
    @property
    def aliquota_nacional(self):
        return Decimal(str(self.nacional))
        
    @property
    def aliquota_importado(self):
        return Decimal(str(self.importado))
    
    @property
    def aliquota_estadual(self):
        return Decimal(str(self.estadual))
        
    @property
    def aliquota_municipal(self):
        return Decimal(str(self.municipal))
        

def get_servico(codigo_nbs):
    """Consulta pelos tributos do Serviço, procurando pelo código NBS/LC116.

    :param str codigo_nbs: Código NBS/LC116 do serviço a ser consultado.

    :return: Retorna uma instância de :class:`Servico` contendo os valores
        aproximados dos tributos que incidem sobre ele.

    :rtype: ibptws.servico.Servico

    :raises ErroServicoNaoEncontrato: se o NBS/LC116 não forem encontrados.

    :raises ErroIdentificacao: se o token ou o CNPJ configurados tiverem
        expirado ou não estiverem corretos.
    """

    response = requests.get(conf.endpoint.servicos, params=dict(
            token=conf.token, cnpj=conf.cnpj, uf=conf.estado,
            codigo=codigo_nbs))

    if response.status_code == requests.codes.ok:
        data = response.json()
        return Servico(**{k.lower():v for k,v in data.items()})

    elif response.status_code == requests.codes.not_found:
        raise ErroServicoNaoEncontrado('NBS/LC116={!r}'.format(codigo_nbs))

    elif response.status_code == requests.codes.forbidden:
        raise ErroIdentificacao('IBPT token={!r}, cnpj={!r}, UF={!r}'.format(
                conf.token, conf.cnpj, conf.estado))

    response.raise_for_status()
