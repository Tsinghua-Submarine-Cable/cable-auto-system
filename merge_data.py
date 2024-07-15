from py2neo import Graph, Node, NodeMatcher, Relationship
import pymongo
import telegeography
import infrapedia

from utils import *

def get_supplier_by_cable(graph, cable_name):
    query = """
    MATCH (cable:cable {name: $cable_name})-[:supplied_by]->(supplier)
    RETURN supplier
    """

    result = graph.run(query, cable_name=cable_name)

    return [record['supplier']['name'] for record in result]

def get_landing_points_by_cable(graph, cable_name):
    query = """
    MATCH (cable:cable {name: $cable_name})-[:landing_at]->(landing_point)
    RETURN landing_point
    """

    result = graph.run(query, cable_name=cable_name)

    return [{'id': record['landing_point']['id'], 'name': record['landing_point']['name'], 'country': record['landing_point']['country']} for record in result]

def get_cables_by_landing_point(graph, lp_name):
    query = """
    MATCH (cable:cable)-[:landing_at]->(lp:landing_point {name: $lp_name})
    RETURN cable
    """

    result = graph.run(query, lp_name=lp_name)

    return [{'id': record['cable']['id'], 'name': record['cable']['name']} for record in result]

def merge_data():
    # telegeography.insert_neo4j()
    # infrapedia.insert_neo4j()

    graph = Graph('bolt://localhost:7687', user='neo4j', password='thuthuthu')
    matcher = NodeMatcher(graph)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["merged_data_" + formatted_date]
    my_col = my_db["cable"]
    lp_col = my_db["landing_point"]
    all_col = my_db["all"]

    my_col.delete_many({})
    lp_col.delete_many({})
    all_col.delete_many({})

    # 查询所有标签为cable的节点
    cable_nodes = list(matcher.match("cable"))
    for cable in cable_nodes:
        dic = {
            'id': cable['id'],
            'name': cable['name'],
            'length': cable['length'],
            'design_capacity': cable['design_capacity'],
            'fiber_pairs': cable['fiber_pairs'],
            'rfs': cable['rfs'],
            'rfs_year': cable['rfs_year'],
            'eol': cable['eol']
        }

        suppliers = get_supplier_by_cable(graph, cable['name'])
        dic['suppliers'] = suppliers
        lps = get_landing_points_by_cable(graph, cable['name'])
        dic['landing_points'] = lps

        my_col.insert_one(dic)
        all_col.insert_one({
            'id': cable['id'],
            'name': cable['name']
        })

    lp_nodes = list(matcher.match("landing_point"))
    for lp in lp_nodes:
        dic = {
            'id': lp['id'],
            'name': lp['name'],
            'country': lp['country'],
            'coordinates': lp['coordinates'],
            'cable': get_cables_by_landing_point(graph, lp['name'])
        }
        lp_col.insert_one(dic)


if __name__=='__main__':
    merge_data()
