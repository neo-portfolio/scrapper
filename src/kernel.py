from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

def kernel(s1, s2, alpha1, alpha2, beta, corr):

    def add_symbol(tx, symbol1, symbol2, alpha1, alpha2, beta12, corr12):
        tx.run("MERGE (a:STOCK {name: $name1, alpha: $alpha1}, ) "
               "MERGE (a)-[:correlated {beta: $beta, corr: $corr}]->(b:STOCK {name: $name2, alpha: $alpha2})",
               name1=symbol1, name2=symbol2, beta=beta12, corr=corr12, alpha1=alpha1, alpha2=alpha2)


    with driver.session() as session:
        session.write_transaction(add_symbol, s1, s2, alpha1, alpha2, beta, corr)

    driver.close()
