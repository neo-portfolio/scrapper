from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

def kernel(s1, s2, beta12):

    def add_symbol(tx, symbol1, symbol2, beta12):
        tx.run("MERGE (a:STOCK {name: $name1}) "
               "MERGE (a)-[:correlated {beta: $beta}]->(b:STOCK {name: $name2})",
               name1=symbol1, name2=symbol2, beta=beta12)


    with driver.session() as session:
        session.write_transaction(add_symbol, s1, s2, beta12)

    driver.close()
