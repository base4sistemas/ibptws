# -*- coding: utf-8 -*-
#
# ibptws/config.py
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

class Endpoint(object):

    def __init__(self):

        self.produtos = 'http://iws.ibpt.org.br/api/Produtos'
        """Endereço para o web services de produtos."""

        self.servicos = 'http://iws.ibpt.org.br/api/Servicos'
        """Endereço para o web services de serviços."""


class Configuracoes(object):

    def __init__(self):

        self.endpoint = Endpoint()
        """Endereços para os web serviçes do IBPT."""

        self.token = ''
        """Token fornecido pelo IBPT para acesso ao web services."""

        self.cnpj = ''
        """CNPJ da empresa relacionada ao :attr:`token`."""

        self.estado = ''
        """Sigla do Estado (unidade federativa) do domicílio do :attr:`cnpj`."""


conf = Configuracoes()
