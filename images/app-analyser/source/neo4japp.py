from neo4j.v1 import GraphDatabase, basic_auth

class Neo4jApp:

    def __init__(self):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("data", "fenris"))
        session = driver.session()

        session.run("CREATE (a:Person {name: {name}, title: {title}})",
                      {"name": "Arthur2", "title": "King1"})

        result = session.run("MATCH (a:Person) WHERE a.name = {name} "
                               "RETURN a.name AS name, a.title AS title",
                               {"name": "Arthur"})
        for record in result:
            print("%s %s" % (record["title"], record["name"]))

        session.close()