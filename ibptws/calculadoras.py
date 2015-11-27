# -*- coding: utf-8 -*-
#
# ibptws/calculadoras.py
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

from .provisoes import SemProvisao


ZERO = Decimal('0')
CEM = Decimal('100')


class DeOlhoNoImposto(object):
    """
    Implementa uma calculadora para a Lei 12.741/2012. O propósito é acumular
    os valores de *n* consultas e fornecer o resultado do valor aproximado dos
    tributos em cada esfera aplicável. Por exemplo:
    
    .. sourcecode:: python
    
        >>> calculadora = DeOlhoNoImposto()     # doctest: +SKIP
        >>> for item in itens:                  # doctest: +SKIP
        ...     calculadora.produto(
        ...             item.produto.ncm,
        ...             item.produto.ncm_ex,
        ...             item.subtotal())
        ...
        >>> calculadora.carga_federal()         # doctest: +SKIP
        Decimal('6.73')
        >>> calculadora.carga.estadual()        # doctest: +SKIP
        Decimal('8.47')
        >>> calculadora.total_tributos()        # doctest: +SKIP
        Decimal('15.20')
        
    .. versionadded:: 0.3
        
    """
    
    def __init__(self, provisao=None):
        self._fed_nacionais = []
        self._fed_importados = []
        self._estaduais = []
        self._municipais = []
        self._total = ZERO
        self._provisao = provisao or SemProvisao()
        
    
    def reiniciar(self):
        """
        Reinicia a calculadora, zerando os produtos e serviços acumulados.
        """
        self._fed_nacionais[:] = []
        self._fed_importados[:] = []
        self._estaduais[:] = []
        self._municipais[:] = []
        self._total = ZERO
        
        
    def produto(self, ncm, ncm_ex, valor):
        """
        Acumula os valores aproximados dos tributos sobre o subtotal do produto
        identificado pelo código NCM/SH e exceção.
        
        :param str ncm: Código NCM/SH do produto.
        :param int ncm_ex: Exceção à regra NCM/SG.
        :param Decimal valor: Valor do subtotal do produto, a quantidade
            comercializada pelo valor unitário de venda.
        
        """
        p = self._provisao.get_produto(ncm, ncm_ex)
        self._fed_nacionais.append(valor * (p.aliquota_nacional / CEM))
        self._fed_importados.append(valor * (p.aliquota_importado / CEM))
        self._estaduais.append(valor * (p.aliquota_estadual / CEM))
        self._total += valor
        
    
    def servico(self, nbs, valor):
        """
        Acumula os valores aproximados dos tributos sobre o subtotal do serviço
        identificado pelo código NBS.
        
        :param str nbs: Código NBS do serviço.
        :param Decimal valor: Valor do subtotal do serviço.
        
        """
        s = self._provisao.get_servico(nbs)
        self._fed_nacionais.append(valor * (s.aliquota_nacional / CEM))
        self._fed_importados.append(valor * (s.aliquota_importado / CEM))
        self._estaduais.append(valor * (s.aliquota_estadual / CEM))
        self._municipais.append(valor * (s.aliquota_municipal / CEM))
        self._total += valor
        
        
    def carga_federal(self):
        """
        Retorna o valor aproximado dos tributos na esfera federal, entre os
        produtos nacionais e importados.
        
        :rtype: decimal.Decimal
        """
        return self.carga_federal_nacional() + self.carga_federal_importado()
        
    
    def carga_federal_nacional(self):
        """
        Retorna o valor aproximado dos tributos na esfera federal para produtos
        nacionais.
        
        :rtype: decimal.Decimal
        """
        return sum(self._fed_nacionais or [ZERO,])
        
    
    def carga_federal_importado(self):
        """
        Retorna o valor aproximado dos tributos na esfera federal para produtos
        importados.
        
        :rtype: decimal.Decimal
        """
        return sum(self._fed_importados or [ZERO,])
        
    
    def carga_estadual(self):
        """
        Retorna o valor aproximado dos tributos na esfera estadual.
        :rtype: decimal.Decimal
        """
        return sum(self._estaduais or [ZERO,])
        
    
    def carga_municipal(self):
        """
        Retorna o valor aproximado dos tributos na esfera municipal.
        :rtype: decimal.Decimal
        """
        return sum(self._municipais or [ZERO,])
        
    
    def total_tributos(self):
        """
        Retorna a soma dos valores aproximados dos tributos entre todos os
        produtos e servicos considerados.
        
        :rtype: decimal.Decimal
        """
        return sum([
                self.carga_federal(),
                self.carga_estadual(),
                self.carga_municipal(),])
                
    
    def total(self):
        """
        Retorna a soma dos subtotais dos produtos e servicos calculados.
        :rtype: decimal.Decimal
        """
        return self._total
        
    
    def percentual_sobre_total(self):
        """
        Retorna o percentual que o total dos tributos representa sobre o
        valor total dos produtos e serviços calculados.
        :rtype: decimal.Decimal
        """
        if self.total().is_zero():
            return ZERO
        return self.total_tributos() / self.total()
