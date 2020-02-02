from neo4j import GraphDatabase
from fun_corr import corr

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

def make_query(symbol1, symbol2, corr12):
    return "MATCH (a:Company {name: '%s'}), (b:Company {name: '%s'})\
    CREATE (a)-[:Correlated {corr: %d}]->(b)" % (symbol1, symbol2, corr12)
               

def kernel(symbol1, symbol2):
    corr12 = corr(s1, s2)

    with driver.session() as session:
        session.run(make_query(symbol1, symbol2, corr12))
