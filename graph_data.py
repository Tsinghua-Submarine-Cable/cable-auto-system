from py2neo import Graph, Node, Relationship
import pymongo

from utils import *

# 连接到Neo4j数据库
# graph = Graph('bolt://localhost:7687', user='neo4j', password='thuthuthu')
#
# # 创建一个节点
# alice = Node('Person', name='Alice', age=30)
# graph.create(alice)
#
# # 创建另一个节点
# bob = Node('Person', name='Bob', age=25)
# graph.create(bob)
#
# # 创建两个节点之间的关系
# relationship = Relationship(alice, 'KNOWS', bob)
# graph.create(relationship)
#
# # 查询所有Person节点
# people = graph.run('MATCH (p:Person) RETURN p.name, p.age').data()
#
# # 打印查询结果
# for person in people:
#     print(person)

def delete_label_in_neo4j(graph, label):
    delete_query = 'MATCH (n:{}) DETACH DELETE n'.format(label)
    graph.run(delete_query)

def delete_cable_in_neo4j(graph):
    delete_query = 'MATCH (n:cable) DETACH DELETE n'
    graph.run(delete_query)

def delete_lp_in_neo4j(graph):
    delete_query = 'MATCH (n:landing_point) DETACH DELETE n'
    graph.run(delete_query)


if __name__=='__main__':
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    formatted_date = '2024-06-12'
    my_db = myclient['telegeography_data_' + formatted_date]
    my_col = my_db['cable']

    graph = Graph('bolt://localhost:7687', user='neo4j', password='thuthuthu')
    delete_cable_in_neo4j(graph)
    delete_lp_in_neo4j(graph)
    delete_label_in_neo4j(graph, 'owner')
    delete_label_in_neo4j(graph, 'supplier')


    for x in my_col.find({}):
        cable_node = Node('cable', name=x['name'])
        graph.merge(cable_node, 'cable', 'name')
        for lp in x['landing_points']:
            lp_geo = my_db['landing-point-geo'].find_one({'properties.id': lp['id']})
            lp_node = Node('landing_point', name=lp['name'], coordinate=lp_geo['geometry']['coordinates'])
            graph.merge(lp_node, 'landing_point', 'name')
            relationship = Relationship(cable_node, 'landing_at', lp_node, probibility=1.0)
            graph.create(relationship)

        onwers = x['owners'].split(' ,')
        for owner in onwers:
            owner_node = Node('owner', name=owner)
            graph.merge(owner_node, 'owner', 'name')
            relationship = Relationship(cable_node, 'owned_by', owner_node, probibility=1.0)
            graph.create(relationship)

        if x['suppliers'] is not None:
            suppliers = x['suppliers'].split(' ,')
            for supplier in suppliers:
                supplier_node = Node('supplier', name=supplier)
                graph.merge(supplier_node, 'supplier', 'name')
                relationship = Relationship(cable_node, 'supplied', owner_node, probibility=1.0)
                graph.create(relationship)


        if x['url'] is not None:
            url_node = Node('url', name=x['url'])
            graph.merge(url_node, 'url', 'name')
            relationship = Relationship(cable_node, 'has_website', url_node, probibility=1.0)
            graph.create(relationship)
