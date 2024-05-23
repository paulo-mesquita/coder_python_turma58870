class Retangulo:
    """
    Esta é a classe Retangulo que representa um retângulo geométrico.
    Ela possui dois atributos: base e altura, e dois métodos: area() e perimetro().
    """

    def __init__(self, base, altura):
        """
        Método construtor da classe Retangulo.
        Inicializa a base e a altura do retângulo com os valores fornecidos.

        :param base: A base do retângulo.
        :param altura: A altura do retângulo.
        """
        self.base = base
        self.altura = altura

    def area(self):
        """
        Calcula e retorna a área do retângulo.
        A área de um retângulo é dada pelo produto da base pela altura.

        :return: A área do retângulo.
        """
        return self.base * self.altura

    def perimetro(self):
        """
        Calcula e retorna o perímetro do retângulo.
        O perímetro de um retângulo é dado por 2 vezes a soma da base com a altura.

        :return: O perímetro do retângulo.
        """
        return 2 * (self.base + self.altura)
