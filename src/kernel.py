from neo4j import GraphDatabase
from fun_corr import corr

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

def kernel(s1, s2, alpha1, alpha2, beta):

    corr12 = corr(s1, s2)

    def add_symbol(tx, s1, s2, alpha1, alpha2, r1, r2, std1, std2, beta1, beta2,  corr12):
        tx.run("MERGE (a:STOCK {name: $name1, alpha: $alpha1, beta: $beta1, r: $r1, std: $std1}, ) "
               "MERGE (a)-[:correlated {corr: $corr}]->(b:STOCK {name: $name2, alpha: $alpha2, beta: $beta2, r: $r2, std: $std2})",
               name1=s1, name2=s2, alpha1=alpha1, alpha2=alpha2, r1=r1, r2=r2,
               std1=std1, std2=std2, beta1=beta1, beta2=beta2, corr=corr12)


    with driver.session() as session:
        session.write_transaction(add_symbol, s1, s2, alpha1, alpha2, beta, corr)

    driver.close()
