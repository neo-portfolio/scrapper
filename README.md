# Scrapper

A scrapper to create the Neo4j database

# Installation

### Clone:
- With SSH (they won't ask you for your password at every push/pull): `git clone git@github.com:neo-portfolio/scrapper.git`
- With HTTP: `git clone https://github.com/neo-portfolio/scrapper.git`


    cd scrapper
    pip3 install --user -r requirements.txt

## Install Neo4j

- Download from Neo4j community edition from [Neo4j official page](https://neo4j.com/download-center/)
- Follow instructions on the page
- Add to path
    - `export NEO4J_HOME=<PATH/TO/YOUR/FOLDER>`
    - `export PATH=$PATH:$NEO4J_HOME/bin`
 
 
## Launch Neo4j
 
- `neo4j start`
- In your browser, go to `localhost:7474` to open the neat data visualizer
- Default password = default user = `neo4j`

## Install dependencies

`pip3 install --user -r requirements.txt`