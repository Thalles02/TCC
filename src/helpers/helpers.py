import random
import string


def generate_token():
    first_char = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=19))

    return first_char + rest


def get_ordered_table_columns(
    all_record_keys: set,
    table_identifier: str, # Pode ser o token da tabela, usado para adivinhar o nome da coluna ID
    columns_to_hide: set,
    priority_columns_after_id: list = None,
    default_fallback_column_name: str = "ID" # Usado se records for vazio e all_record_keys for {"id"}
                                            # ou se nenhuma outra coluna for encontrada
) -> list:
    """
    Ordena as colunas para exibição em uma tabela.
    A ordem de prioridade é:
    1. Coluna de ID (inferida a partir de table_identifier, "id", ou prefixo "id_").
    2. Colunas em `priority_columns_after_id` (ex: "criado_em").
    3. Outras colunas visíveis, em ordem alfabética.
    Colunas em `columns_to_hide` são sempre omitidas.
    """
    if priority_columns_after_id is None:
        priority_columns_after_id = ["criado_em"] # Default

    # Se não há chaves de entrada (ex: API não retornou campos), retorna um fallback.
    if not all_record_keys:
        return [default_fallback_column_name] # Ou uma lista vazia, dependendo do desejado

    visible_keys = all_record_keys.difference(columns_to_hide)

    # Se todas as colunas foram escondidas ou não havia colunas visíveis para começar
    if not visible_keys:
        # Se all_record_keys era originalmente {"id"} (fallback para records vazios)
        # e "id" não está em columns_to_hide, isso não deveria acontecer.
        # Mas se todas as chaves eram para esconder, retornamos o fallback.
        return [default_fallback_column_name]

    ordered_columns_list = []
    processed_keys = set()

    # Etapa 1: Identificar e adicionar a coluna de ID principal
    # Tentativa A: O table_identifier (token da tabela) é o nome da coluna ID
    if table_identifier in visible_keys:
        ordered_columns_list.append(table_identifier)
        processed_keys.add(table_identifier)
    # Tentativa B: A coluna se chama exatamente "id"
    elif "id" in visible_keys:
        ordered_columns_list.append("id")
        processed_keys.add("id")
    # Tentativa C: Procurar por colunas que começam com "id_"
    else:
        # Pega a primeira em ordem alfabética para consistência
        id_prefix_candidates = sorted([
            key for key in visible_keys if key.startswith("id_") and key not in processed_keys
        ])
        if id_prefix_candidates:
            chosen_id_col = id_prefix_candidates[0]
            ordered_columns_list.append(chosen_id_col)
            processed_keys.add(chosen_id_col)

    # Etapa 2: Adicionar colunas prioritárias (ex: "criado_em")
    for col_name in priority_columns_after_id:
        if col_name in visible_keys and col_name not in processed_keys:
            ordered_columns_list.append(col_name)
            processed_keys.add(col_name)

    # Etapa 3: Adicionar as colunas restantes em ordem alfabética
    remaining_visible_keys = sorted(list(visible_keys.difference(processed_keys)))
    ordered_columns_list.extend(remaining_visible_keys)

    # Fallback final: se a lista ainda estiver vazia mas havia chaves visíveis
    # (isso pode acontecer se as chaves visíveis não se encaixaram em nenhuma regra acima)
    # Ou se o conjunto inicial era apenas o fallback "id" e ele foi pego.
    if not ordered_columns_list and visible_keys:
        return sorted(list(visible_keys)) # Simplesmente retorna as visíveis ordenadas
    elif not ordered_columns_list: # Se realmente não há nada para mostrar
        return [default_fallback_column_name]


    return ordered_columns_list