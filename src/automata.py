"""Aqui vou implementar dfa."""


class ErroException(Exception):
    """Aqui crio uma exceção personalizada.

    Args:
        mensagem (str): descrição do erro encontrado.
    """

    def __init__(self, mensagem):
        """Aqui inicializa a exceção.

        Args:
            mensagem (str): Mensagem do erro.
        """
        self.mensagem = mensagem
        super().__init__(self.mensagem)


def load_automata(filename: str) -> Tuple[Set[str], Set[str], Dict[Tuple[str, str], str], str, Set[str]]:
    """Carrega um autômato a partir de um arquivo."""
    try:
        with open(filename, encoding='utf-8') as file:
            lines = file.read().splitlines()

        if len(lines) < 5:
            raise ErroException("Descrição incompleta do autômato.")

        alfabeto = set(lines[1].strip().split())
        estados = set(lines[1].strip().split())
        estado_inicial = lines[3].strip()
        estados_finais = set(lines[2].strip().split())

        if estado_inicial not in estados:
            raise ErroException("Estado inicial não está no conjunto de estados.")

        if not estados_finais.issubset(estados):
            raise ErroException("Estados finais não estão no conjunto de estados.")

        delta = {}

        for rule in lines[4:]:
            parts = rule.split()
            if len(parts) != 3:
                raise ErroException("Formato inválido da regra de transição.")
            origem, simbolo, destino = parts
            if origem not in estados or (simbolo not in alfabeto and simbolo != '&') or destino not in estados:
                raise ErroException("Componentes da regra inválidos.")
            if (origem, simbolo) not in delta:
                delta[(origem, simbolo)] = destino
            else:
                if isinstance(delta[(origem, simbolo)], list):
                    delta[(origem, simbolo)].append(destino)
                else:
                    delta[(origem, simbolo)] = [delta[(origem, simbolo)], destino]

        return estados, alfabeto, delta, estado_inicial, estados_finais

    except FileNotFoundError as exc:
        raise FileNotFoundError("Arquivo não encontrado.") from exc
    except Exception as e:
        raise ErroException(f"Erro ao carregar o autômato: {e}") from e


def process(automato: Tuple[Set[str], Set[str], Dict[Tuple[str, str], str], str, Set[str]], words: List[str]) -> Dict[str, str]:
    """Processa uma lista de palavras no autômato DFA."""
    estados, sigma, delta, q0, final_states = automato
    results = {}

    for word in words:
        current_state = q0
        valid = True

        for symbol in word:
            if symbol not in sigma and symbol != '&':
                results[word] = "INVÁLIDA"
                valid = False
                break
            if (current_state, symbol) in delta:
                current_state = delta[(current_state, symbol)]
            else:
                results[word] = "REJEITA"
                valid = False
                break

        if valid:
            if current_state in final_states:
                results[word] = "ACEITA"
            else:
                results[word] = "REJEITA"

    return results
