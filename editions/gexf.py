import lxml.etree as ET

gexf_doc = """
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <meta lastmodifieddate="{}">
        <creator>https://dig-ed-cat.acdh.oeaw.ac.at</creator>
        <description>The dig-ed-cat-net</description>
    </meta>
    <graph defaultedgetype="directed">
        <nodes></nodes>
        <edges></edges>
    </graph>
</gexf>
"""

ns_gexf = {'gexf': "http://www.gexf.net/1.2draft"}
ns_xml = {'xml': "http://www.w3.org/XML/1998/namespace"}


def create_node(node_id, label):

    """ returns a gexf:node element """

    node = ET.Element("{}node".format("{"+ns_gexf['gexf']+"}"))
    node.attrib['id'] = str(node_id)
    node.attrib['label'] = label
    return node


def create_edge(edge_id, source, target):

    """ returns a gexf:edge element """

    edge = ET.Element("{}edge".format("{"+ns_gexf['gexf']+"}"))
    edge.attrib['id'] = str(edge_id)
    edge.attrib['source'] = str(source)
    edge.attrib['target'] = str(target)
    return edge


def netdict_to_gexf(net, gexf_doc=gexf_doc):

    """ takes a python dict with network info and returns\
    a list of gexf:node, gexf:edge and a gexf:doc"""

    gexf_tree = ET.fromstring(gexf_doc)
    nodes_root = gexf_tree.xpath('//gexf:nodes', namespaces=ns_gexf)[0]
    edges_root = gexf_tree.xpath('//gexf:edges', namespaces=ns_gexf)[0]
    for idx, item in enumerate(net['edges']):
        edge = create_edge(idx, item['from'], item['to'])
        edges_root.append(edge)
    for idx, item in enumerate(net['nodes']):
        node = create_node(item['id'], item['title'])
        nodes_root.append(node)
    xml_stream = ET.tostring(gexf_tree, pretty_print=True, encoding="UTF-8")
    return [nodes_root, edges_root, gexf_tree, xml_stream]
