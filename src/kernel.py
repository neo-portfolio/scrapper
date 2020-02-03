from fun_corr import corr


def kernel(symbol1, symbol2):
    corr12 = corr(symbol1, symbol2)

    with driver.session() as session:
        query = make_query(symbol1, symbol2, corr12)
        session.run(query)
