from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, name):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_node, name)
            print(greeting)

    @staticmethod
    def _create_and_return_node(tx, name):
        query = (
            "CREATE (n:Person {name: $name}) "
            "RETURN n.name + ', from the Neo4j Python demo!' AS greeting"
        )
        result = tx.run(query, name=name)
        return result.single()[0]

# 连接到Neo4j数据库
neo4j_uri = "bolt://localhost:7687"  # 你的数据库URI
neo4j_user = "neo4j"                 # 你的用户名
neo4j_password = "thuthuthu"          # 你的密码

# 创建Neo4j连接实例
conn = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)

# 创建一个节点并打印返回信息
conn.create_node("Alice")

# 关闭数据库连接
conn.close()