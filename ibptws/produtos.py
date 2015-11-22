# -*- coding: utf-8 -*-
#
# ibptws/produto.py
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
from .excecoes import ErroProdutoNaoEncontrado


_Produto = namedtuple('_Produto',
        'codigo uf ex descricao nacional importado estadual')


class Produto(_Produto):
    """
    Resposta à consulta de produtos.

    .. warning::

        O atributo ``ex`` (exceção à regra aplicada no NCM) não é uma string,
        mas um número inteiro.

        Note também que os atributos ``nacional``, ``estadual`` e ``importado``
        são valores de ponto flutuante. Para obter objetos :class:`Decimal`,
        utilize os atributos :attr:`aliquota_nacional`,
        :attr:`aliquota_importado` e :attr:`aliquota_estadual`.

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


def get_produto(codigo_ncm, excecao=0):
    """Consulta o servico de produtos, procurando pelo código NCM e,
    opcionalmente, pela exceção à regra aplicada no NCM.

    :param str codigo_ncm: Código NCM do produto a ser consultado.

    :param int excecao: **Opcional** Exceção à regra aplicada ao NCM.

    :return: Retorna uma instância de :class:`Produto` contendo os detalhes do
        NCM e dos valores aproximados dos tributos que incidem sobre ele.

    :rtype: ibptws.produto.Produto

    :raises ErroProdutoNaoEncontrato: se o NCM/exceção não forem encontrados.

    :raises ErroIdentificacao: se o token ou o CNPJ configurados tiverem
        expirado ou não estiverem corretos.
    """

    response = requests.get(conf.endpoint.produtos, params=dict(
            token=conf.token, cnpj=conf.cnpj, uf=conf.estado,
            codigo=codigo_ncm, ex=excecao))

    if response.status_code == requests.codes.ok:
        data = response.json()
        return Produto(**{k.lower():v for k,v in data.items()})

    elif response.status_code == requests.codes.not_found:
        raise ErroProdutoNaoEncontrado('NCM={!r}, EX={!r}'.format(
                codigo_ncm, excecao))

    elif response.status_code == requests.codes.forbidden:
        raise ErroIdentificacao('IBPT token={!r}, cnpj={!r}, UF={!r}'.format(
                conf.token, conf.cnpj, conf.estado))

    response.raise_for_status()
