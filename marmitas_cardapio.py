import abc
from datetime import datetime, time

# Classe abstrata (Abstração): define a interface comum para tipos de usuário.
class Usuario(abc.ABC):
    def __init__(self, nome):
        # Atributo protegido (Encapsulamento parcial)
        self._nome = nome

    # Método (comportamento da classe)
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    # Método abstrato — força as subclasses a implementarem (Polimorfismo)
    @abc.abstractmethod
    def get_tipo(self):
        pass

    # Método abstrato — demonstra que diferentes subclasses podem implementar de forma distinta (Polimorfismo)
    @abc.abstractmethod
    def calcular_preco_final(self, preco_original):
        """Retorna preço final para o tipo de usuário"""
        pass

# Herança: Docente herda de Usuario (Herança)
class Docente(Usuario):
    def __init__(self, nome):
        super().__init__(nome)
        self._tipo = 'docente'

    # Implementação concreta do método abstrato (Polimorfismo)
    def get_tipo(self):
        return self._tipo

    # Implementação concreta do método abstrato (Polimorfismo)
    def calcular_preco_final(self, preco_original):
        return preco_original  # Docentes pagam preço normal

# Herança: Discente herda de Usuario (Herança)
class Discente(Usuario):
    def __init__(self, nome):
        super().__init__(nome)
        self._tipo = 'discente'

    def get_tipo(self):
        return self._tipo

    def calcular_preco_final(self, preco_original):
        return 3.00  # Preço fixo de R$3,00 para discentes

# Classe Marmita: representa um objeto Marmita (Objeto)
# Uso de atributos privados (Encapsulamento) e propriedades para acesso controlado
class Marmita:
    def __init__(self, nome, preco_original):
        self.__nome = nome  # atributo privado (Encapsulamento)
        self.__preco_original = float(preco_original)  # atributo privado (Encapsulamento)

    # Método (getter) para acessar atributo privado
    @property
    def nome(self):
        return self.__nome

    @property
    def preco_original(self):
        return self.__preco_original

    # Método especial para exibir a marmita
    def __str__(self):
        return f"{self.nome} - Preco original: R${self.preco_original:.2f}"

# Classe Pedido: representa o objeto pedido com seus métodos (Objeto, Métodos)
class Pedido:
    def __init__(self, usuario: Usuario, marmita: Marmita):
        # Atributos protegidos (Encapsulamento)
        self._usuario = usuario
        self._marmita = marmita
        self._horario_pedido = datetime.now()

    # Método que usa comportamento do usuário (polimorfismo via calcular_preco_final)
    def calcular_total(self):
        # Polimorfismo: calcular_preco_final retorna valor diferente para cada tipo de usuário
        return self._usuario.calcular_preco_final(self._marmita.preco_original)

    # Método que resume o pedido (método que combina atributos e comportamentos)
    def resumo(self):
        tipo = self._usuario.get_tipo()
        nome = self._usuario.nome
        preco_original = self._marmita.preco_original
        preco_final = self.calcular_total()
        total = self.calcular_total()
        
        resumo_str = f"Resumo do pedido:\n"
        resumo_str += f"Usuario: {nome} ({tipo})\n"
        resumo_str += f"Marmita: {self._marmita.nome}\n"
        resumo_str += f"Preco original: R${preco_original:.2f}\n"
        
        if tipo == 'discente':
            resumo_str += f"Preco com subsidio: R${preco_final:.2f}\n"
        else:
            resumo_str += f"Preco final: R${preco_final:.2f}\n"
            
        resumo_str += f"Total a pagar: R${total:.2f}\n"
        resumo_str += f"Horario do pedido: {self._horario_pedido.strftime('%H:%M')}\n"
        
        # Verifica se está no horário de entrega
        status_entrega = self.verificar_horario_entrega()
        resumo_str += f"Status de entrega: {status_entrega}"
        
        return resumo_str

    def verificar_horario_entrega(self):
        """Verifica se o pedido está dentro do horário de entrega"""
        hora_atual = self._horario_pedido.time()
        
        # Horários de entrega
        almoco_inicio = time(11, 30)  # 11:30
        almoco_fim = time(14, 0)      # 14:00
        jantar_inicio = time(18, 0)    # 18:00
        jantar_fim = time(20, 30)      # 20:30
        
        if (almoco_inicio <= hora_atual <= almoco_fim):
            return "ENTREGA NO HORARIO DE ALMOCO (11:30-14:00)"
        elif (jantar_inicio <= hora_atual <= jantar_fim):
            return "ENTREGA NO HORARIO DE JANTAR (18:00-20:30)"
        else:
            return "FORA DO HORARIO DE ENTREGA - Aguarde o proximo horario"

# SistemaMarmitas: classe que gerencia cardápios e busca (Classe com métodos utilitários)
class SistemaMarmitas:
    def __init__(self):
        # cardápio único para ambos os tipos
        self.cardapio = [
            Marmita("bucho", 8.00),
            Marmita("strogonof", 12.00),
            Marmita("feijao", 6.00),
            Marmita("guizado", 10.00),
            Marmita("porco assado", 15.00)
        ]
        self.vendidas = []
        self.usuarios_ativos = []  # controla os usuários ativos

    # método para adicionar usuário ativo
    def adicionar_usuario(self, usuario):
        self.usuarios_ativos.append(usuario)

    # método para remover usuário ativo
    def remover_usuario(self, usuario):
        if usuario in self.usuarios_ativos:
            self.usuarios_ativos.remove(usuario)

    # Método que imprime o cardápio (Método)
    def mostrar_cardapio(self):
        print("\n" + "="*50)
        print("CARDAPIO DISPONIVEL:")
        print("="*50)
        for i, m in enumerate(self.cardapio, 1):
            print(f"{i}. {m}")
        print("\nINFORMACOES DE PRECOS:")
        print("  Docentes: Preco normal (sem subsidio)")
        print("  Discentes: R$3,00 (qualquer marmita)")
        print("="*50)

    # Método que busca uma marmita pelo nome (Método)
    def buscar_marmita(self, nome):
        nome = nome.strip().lower()
        for m in self.cardapio:
            if m.nome.lower() == nome:
                return m
        return None

    def buscar_marmita_por_numero(self, numero):
        """Busca marmita por número na lista (1-based)"""
        try:
            if 1 <= numero <= len(self.cardapio):
                return self.cardapio[numero - 1]
        except (ValueError, IndexError):
            pass
        return None

    def registrar_venda(self, marmita):
        self.vendidas.append(marmita)

    # Só doa marmitas depois que não tem usuários ativos
    def doar_nao_vendidas(self):
        if self.usuarios_ativos:
            print("\nAinda ha usuarios ativos. As marmitas nao podem ser doadas agora.")
            return
        
        nao_vendidas = [m for m in self.cardapio if m not in self.vendidas]
        if nao_vendidas:
            print("\n" + "="*50)
            print("MARMITAS PARA DOACAO A COMUNIDADE:")
            print("="*50)
            for m in nao_vendidas:
                print(f" - {m.nome}")
            print("="*50)
        else:
            print("\nTodas as marmitas foram vendidas!")

    def mostrar_horarios_entrega(self):
        """Mostra os horários de entrega disponíveis"""
        print("\nHORARIOS DE ENTREGA:")
        print("  Almoco: 11:30 as 14:00")
        print("  Jantar: 18:00 as 20:30")
        print(f"  Horario atual: {datetime.now().strftime('%H:%M')}")

# Função principal (Função): orquestra a criação de objetos e chamada de métodos
def main():
    sistema = SistemaMarmitas()
    
    print("="*50)
    print("        SISTEMA INTELIGENTE DE MARMITAS - UFOPA")
    print("="*50)
    
    while True:
        sistema.mostrar_horarios_entrega()
        
        tipo = input("\nVoce e docente ou discente? ").strip().lower()
        if tipo not in ('docente', 'discente'):
            print("Tipo invalido. Digite 'docente' ou 'discente'.")
            continue

        # Exibir cardápio
        sistema.mostrar_cardapio()

        nome = input("Digite seu nome: ").strip()
        if not nome:
            print("Nome nao pode estar vazio.")
            continue

        # Criação de objetos
        if tipo == 'docente':
            usuario = Docente(nome)
        else:
            usuario = Discente(nome)

        sistema.adicionar_usuario(usuario)

        # Opção de escolha por número ou nome
        escolha_input = input("Escolha uma marmita (digite o numero ou nome): ").strip()
        
        # Tenta buscar por número primeiro
        try:
            numero_escolha = int(escolha_input)
            marmita = sistema.buscar_marmita_por_numero(numero_escolha)
        except ValueError:
            # Se não for número, busca por nome
            marmita = sistema.buscar_marmita(escolha_input)

        if marmita is None:
            print("Marmita nao encontrada. Tente novamente.")
            sistema.remover_usuario(usuario)
            continue

        # Criando pedido
        pedido = Pedido(usuario, marmita)
        
        print("\n" + "="*50)
        print(pedido.resumo())
        print("="*50)

        # Registrar a venda
        sistema.registrar_venda(marmita)
        sistema.remover_usuario(usuario)

        # Verificar se há mais usuários
        continuar = input("\nMais algum usuario quer fazer um pedido? (s/n): ").strip().lower()
        if continuar not in ('s', 'sim', 'y', 'yes'):
            break

    # Doar marmitas não vendidas após todos os pedidos
    print("\n" + "="*50)
    sistema.doar_nao_vendidas()
    print("="*50)
    print("\nObrigado por usar o Sistema de Marmitas!")
    print("Fim do programa.")

if __name__ == "__main__":
    main()