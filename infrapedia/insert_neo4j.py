from py2neo import Graph, Node, Relationship
import pymongo
import re

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

def get_cable_name_set(graph):
    query = """
    MATCH (c:cable)
    RETURN c.name AS name
    """
    result = graph.run(query)

    names = [record["name"] for record in result]
    return set(names)

def get_landing_point_names_dic(graph):
    # 查询所有标签为landing_point的节点，并获取它们的name属性
    query = """
    MATCH (lp:landing_point)
    RETURN lp.name AS name
    """

    result = graph.run(query)

    # 收集所有name属性到一个列表中
    names = [record["name"] for record in result]
    dic = {}
    for name in names:
        dic[name.split(', ')[0]] = name  # 从简化名字到全名
    return dic

def get_landing_point_short_name_of_cable(graph, cable_name):
    query = """
    MATCH (cable:cable {name: $cable_name})-[:CONNECTED_TO]->(lp:landing_point)
    RETURN lp.name AS landing_point_name
    """

    result = graph.run(query, cable_name=cable_name)
    lp_names = [record["name"].split(', ')[0] for record in result]
    return lp_names


def get_id_by_name(input_string):
    # Convert the input string to lowercase
    transformed_string = input_string.lower()

    # Replace parentheses, commas, and spaces with hyphens
    transformed_string = re.sub(r'[(),\s]+', '-', transformed_string)

    # Remove trailing hyphens (if any)
    transformed_string = transformed_string.strip('-')

    return transformed_string

def insert_neo4j():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    my_db = myclient['infrapedia_data_' + formatted_date]
    my_col = my_db['cable']

    graph = Graph('bolt://localhost:7687', user='neo4j', password='thuthuthu')

    lp_name_dic = get_landing_point_names_dic(graph)
    lp_name_set = set(lp_name_dic.keys())
    new_lp_cnt = 0

    cable_name_set = get_cable_name_set(graph)

    for x in my_col.find({}):
        cable_name = x['telegeography_name']
        if cable_name == '':
            cable_name = x['name']
        lp_short_names = get_landing_point_short_name_of_cable(graph, cable_name)
        cable_node = Node('cable', name=cable_name, design_capacity=x['design_capacity'], fiber_pairs=x['fiber_pairs'])
        if cable_name not in cable_name_set:
            cable_node['data_source'] = 'infrapedia'
            cable_node['id'] = get_id_by_name(cable_name)
            cable_node['length'] = x['length']

        graph.merge(cable_node, 'cable', 'name')
        for lp in x['landing_points']:
            short_name = lp['name'].split(', ')[0]
            if short_name in lp_name_set:
                continue
            new_lp_cnt += 1
            print(cable_name, lp['name'])
            lp_node = Node('landing_point', name=lp['name'], id=get_id_by_name(lp['name']), datasource='infrapedia', country=lp['country'])
            graph.merge(lp_node, 'landing_point', 'name')
            relationship = Relationship(cable_node, 'landing_at', lp_node, probibility=0.3)
            graph.merge(relationship)


        onwers = x['owners']
        for owner in onwers:
            owner_node = Node('owner', name=owner)
            graph.merge(owner_node, 'owner', 'name')
            relationship = Relationship(cable_node, 'owned_by', owner_node, probibility=1.0)
            graph.merge(relationship)

        if x['url'] is not None:
            url_node = Node('url', name=x['url'])
            graph.merge(url_node, 'url', 'name')
            relationship = Relationship(cable_node, 'has_website', url_node, probibility=1.0)
            graph.merge(relationship)

    print(new_lp_cnt)


if __name__=='__main__':
    insert_neo4j()
