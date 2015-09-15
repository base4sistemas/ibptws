# -*- coding: utf-8 -*-
#
# ibptws/excecoes.py
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

class ErroIdentificacao(Exception):
    """Lançado quando não for possível identificar o token ou o CNPJ,
    resultando um erro HTTP 403 na consulta ao serviço.
    """


class ErroNaoEncontrado(Exception):
    """Erro de base para os erros que indicam HTTP 404 (not found)."""


class ErroProdutoNaoEncontrado(ErroNaoEncontrado):
    """Lançado quando a consulta do serviço de Produtos não for
    capaz de localizar o produto solicitado, resultando em um erro
    HTTP 404 na consulta ao serviço.
    """


class ErroServicoNaoEncontrado(ErroNaoEncontrado):
    """Lançado quando a consulta de Serviços não for capaz de localizar o
    serviço solicitado, resultando em um erro HTTP 404 na consulta.
    """
