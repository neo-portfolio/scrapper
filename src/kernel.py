def correlation(symbol1, symbol2, beta12):
    text = ("MATCH(a: User {name: '%s'}), (b: User {name: '%s'})"
        "\nCREATE(a) - [: correlated {beta: '%s'}]->(b)"
        "\nRETURN   a, b"
        % (symbol1, symbol2, beta12))
    return text


