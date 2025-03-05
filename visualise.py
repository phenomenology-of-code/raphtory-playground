from raphtory import Graph
from raphtory.graphql import GraphServer
import pandas as pd
import os
import time

# URL for lord of the rings data from our main tutorial
url = "https://raw.githubusercontent.com/Raphtory/Data/main/lotr-with-header.csv"
df = pd.read_csv(url)

# Load the lord of the rings graph from the dataframe
graph = Graph()
graph.load_edges_from_pandas(df, "time", "src_id", "dst_id")

# Create a working_dir for your server and save your graph into it 
# You can save any number of graphs here or create them via the server once it's running
os.makedirs("graphs/", exist_ok=True)
graph.save_to_file("graphs/lotr_graph")

# Launch the server and get a client to it.
server = GraphServer(work_dir="graphs/").start()
client = server.get_client()

# Run a basic query to get the names of the characters + their degree
results = client.query("""{
             graph(path: "lotr_graph") {
                 nodes {
                    list{
                        name
                        degree
                       }   
                    }
                 }
             }""")

print(results)

# Keep the server running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server stopped.")
