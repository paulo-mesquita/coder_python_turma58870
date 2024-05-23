# Importa a classe Retangulo do arquivo geometria.py que esta na pasta 'formas'
from formas.geometria import Retangulo

# Cria um objeto da classe Retangulo
retangulo = Retangulo(5, 3)

# 'Printa' os métodos do objeto retangulo
print(f"Area: {retangulo.area()}")
print(f"Perimetro: {retangulo.perimetro()}")
