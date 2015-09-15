
IBPT Web Services
=================

.. image:: https://img.shields.io/pypi/status/ibptws.svg
    :target: https://pypi.python.org/pypi/ibptws/
    :alt: Development status

.. image:: https://img.shields.io/badge/python%20version-2.7%2C%203-blue.svg
    :target: https://pypi.python.org/pypi/ibptws/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/ibptws.svg
    :target: https://pypi.python.org/pypi/ibptws/
    :alt: License

.. image:: https://img.shields.io/pypi/v/ibptws.svg
    :target: https://pypi.python.org/pypi/ibptws/
    :alt: Latest version

-------

Implementa uma camada fina para acesso aos *web services* do `IBPT`_, para
auxiliar no cumprimento à `Lei 12.741/2012`_, popularmente conhecida como  "De
Olho no Imposto". O Instituto Brasileiro de Planejamento e Tributação, IBPT,
calcula e fornece os valores aproximados dos tributos para produtos e serviços
com base no código `NCM`_ (Nomenclatura Comum do Mercosul, para produtos) e no
código `NBS`_ (Nomenclatura Brasileira de Serviços).

Para que o acesso aos *web services* seja possível, é preciso cadastrar-se no
`IBPT`_ para obter seu **token** de acesso.


Utilização
----------

Exemplo básico de configuração e consulta de produto:

.. sourcecode:: Python

    >>> from ibptws import conf
    >>> from ibptws import get_produto

    >>> conf.token = 'ZyW9z...' # cadastre-se no IBPT para obter seu token
    >>> conf.cnpj = '08427847000169'
    >>> conf.estado = 'SP'

    >>> get_produto('02091021')
    Produto(codigo=u'2091021', uf=u'SP', ex=0, descricao=u'Gordura de porco,fresca,refrigerada ou congelada', nacional=4.2, estadual=12.0, importado=6.39)

Similarmente, para consultar um serviço faça:

.. sourcecode:: Python

    >>> from ibptws import get_servico
    >>> get_servico('0101')
    Servico(codigo=u'101', uf=u'SP', descricao=u'An\xe1lise e desenvolvimento de sistemas.', tipo=u'NBS', nacional=13.45, estadual=0.0, municipal=3.9, importado=15.45)


Testes
------

Infelizmente, ainda não existem testes implementados. Gostaria de ajudar?


Isenção de Responsabilidade
===========================

Os autores deste projeto não tem qualquer relação com o Instituto Brasileiro de
Planejamento e Tributação (IBPT), e este, por sua vez, não avaliza o uso desta
biblioteca de código. Utilize por sua conta e risco.


.. _`IBPT`: https://deolhonoimposto.ibpt.org.br
.. _`NCM`: http://www.mdic.gov.br//sitio/interna/interna.php?area=5&menu=1090
.. _`NBS`: http://www.mdic.gov.br/sitio/interna/interna.php?area=4&menu=3412
.. _`Lei 12.741/2012`: http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12741.htm
