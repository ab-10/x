import sys
import rdflib
from visual_genome import api as vg

OUT_DIR = "out"
GRAPH_FILENAME = "vg_graph.n"

print("STATUS: obtaining image IDs")

# TODO: improve argument parsing
if(sys.argv[1] == "--complete"):
    vg_image_ids = vg.get_all_image_ids()
else:
    # Obtains the first 100 image IDs
    vg_image_ids = vg.get_image_ids_in_range(start_index=0, end_index=9)

print("STATUS: Creating a graph in memory.")

vg_graph = rdflib.Graph()

# TODO: improve namespaces
instance_namespace = rdflib.namespace.Namespace(
    "https://visualgenome.org/instance#")
label_namespace = rdflib.namespace.Namespace(
    "https://visualgenome.org/label#")
synset_namespace = rdflib.namespace.Namespace(
    "https://visualgenome.org/synset#")

for image_id in vg_image_ids:
    print("STATUS: obtaining scene graph for image " + str(image_id))
    scene_graph = vg.get_scene_graph_of_image(image_id)
    for instance in scene_graph.objects:

        print(instance)

        instance_node = rdflib.term.BNode()
        vg_graph.add(
            (instance_node,
             instance_namespace.image_url,
             rdflib.URIRef(scene_graph.image.url)))

        vg_graph.add(
            (instance_node,
             instance_namespace.x,
             rdflib.Literal(
                 instance.x)))
        vg_graph.add(
            (instance_node,
             instance_namespace.y,
             rdflib.Literal(
                 instance.y)))
        vg_graph.add(
            (instance_node,
             instance_namespace.width,
             rdflib.Literal(
                 instance.width)))
        vg_graph.add(
            (instance_node,
             instance_namespace.height,
             rdflib.Literal(instance.height)))
        # TODO: include attributes
        # TODO: include raltionships between bounding boxes

        # TODO: create single node for each synset and label, and link the
        # instance_node to said nodes

        for label in instance.names:
            vg_graph.add(
                (instance_node,
                 instance_namespace.label,
                 rdflib.Literal(label)))

        # TODO: create connections between synset nodes and their definitions
        for synset in instance.synsets:
            if(synset is None):
                continue
            vg_graph.add(
                (instance_node, instance_namespace.synset,
                 synset_namespace[synset.name]))

print("STATUS: writing graph to file.")

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

with open(OUT_DIR + "/" + GRAPH_FILENAME, "wb") as graph_file:
    graph_file.write(vg_graph.serialize(format="n3"))
