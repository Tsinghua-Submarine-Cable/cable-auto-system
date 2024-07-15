from py2neo import Graph, Node, Relationship
import pymongo

from utils import *

def delete_label_in_neo4j(graph, label):
    delete_query = 'MATCH (n:{}) DETACH DELETE n'.format(label)
    graph.run(delete_query)

def delete_cable_in_neo4j(graph):
    delete_query = 'MATCH (n:cable) DETACH DELETE n'
    graph.run(delete_query)

def delete_lp_in_neo4j(graph):
    delete_query = 'MATCH (n:landing_point) DETACH DELETE n'
    graph.run(delete_query)

def insert_neo4j():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    my_db = myclient['telegeography_data_' + formatted_date]
    my_col = my_db['cable']

    graph = Graph('bolt://localhost:7687', user='neo4j', password='thuthuthu')
    delete_cable_in_neo4j(graph)
    delete_lp_in_neo4j(graph)
    delete_label_in_neo4j(graph, 'owner')
    delete_label_in_neo4j(graph, 'supplier')
    delete_label_in_neo4j(graph, 'country')

    for x in my_col.find({}):
        cable_node = Node('cable', name=x['name'], id=x['id'], length=x['length'], rfs=x['rfs'], rfs_year=x['rfs_year'])
        graph.merge(cable_node, 'cable', 'name')
        for lp in x['landing_points']:
            lp_geo = my_db['landing-point-geo'].find_one({'properties.id': lp['id']})
            lp_node = Node('landing_point', name=lp['name'], id=lp['id'], coordinate=lp_geo['geometry']['coordinates'], country=lp['country'])
            graph.merge(lp_node, 'landing_point', 'name')
            relationship = Relationship(cable_node, 'landing_at', lp_node, probibility=1.0)
            graph.merge(relationship)

        onwers = x['owners'].split(', ')
        for owner in onwers:
            owner_node = Node('owner', name=owner)
            graph.merge(owner_node, 'owner', 'name')
            relationship = Relationship(cable_node, 'owned_by', owner_node, probibility=1.0)
            graph.merge(relationship)

        if x['suppliers'] is not None:
            suppliers = x['suppliers'].split(', ')
            for supplier in suppliers:
                supplier_node = Node('supplier', name=supplier)
                graph.merge(supplier_node, 'supplier', 'name')
                relationship = Relationship(cable_node, 'supplied_by', supplier_node, probibility=1.0)
                graph.merge(relationship)


        if x['url'] is not None:
            url_node = Node('url', name=x['url'])
            graph.merge(url_node, 'url', 'name')
            relationship = Relationship(cable_node, 'has_website', url_node, probibility=1.0)
            graph.merge(relationship)

if __name__=='__main__':
    insert_neo4j()
