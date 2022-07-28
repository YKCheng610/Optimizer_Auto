import subprocess
import sys

global edge_types
global vertex_types
global triplets

def compute_vertex_cnts():
  print("Counting vertices:")
  for vertex in vertex_types:
    print(vertex)
    cmd = f"curl -s --user tigergraph:tigergraph -X POST \"localhost:14240/gsqlserver/gsql/stats/card?graph=ldbc_snb&vertex={vertex}\""
    subprocess.run(cmd, shell=True)


def compute_edge_cnts():
  print("Counting edges between given src and tgt:")
  for src,edge,tgt in triplets:
    print(src + " - " + edge + " - " + tgt)
    cmd = f"curl -s --user tigergraph:tigergraph -X POST \"localhost:14240/gsqlserver/gsql/stats/card?graph=ldbc_snb&edge={edge}&from={src}&to={tgt}\""
    subprocess.run(cmd, shell=True)

def delete_card():
  print("Deleting old cardinalities...")
  cmd = f"curl -s --user tigergraph:tigergraph -X DELETE \"localhost:14240/gsqlserver/gsql/stats/card?graph=ldbc_snb\""
  subprocess.run(cmd, shell=True)

def show_card():
  cmd = f"curl -s --user tigergraph:tigergraph -X GET \"localhost:14240/gsqlserver/gsql/stats/card?graph=ldbc_snb\" | jq ."
  subprocess.run(cmd, shell=True)

def compute_histograms():
  print("COMPUTING HISTOGRAM for PERSON vertex on firstName attribute")
  cmd = f"curl -s --user tigergraph:tigergraph -X POST \"http://localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb&vertex=Person&attribute=firstName&buckets=10&compute=true\" | jq ."
  subprocess.run(cmd, shell=True)

  print("COMPUTING HISTOGRAM for PERSON vertex on lastName attribute")
  cmd = f"curl -s --user tigergraph:tigergraph -X POST \"http://localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb&vertex=Person&attribute=lastName&buckets=10&compute=true\" | jq ."
  subprocess.run(cmd, shell=True)

  print("COMPUTING HISTOGRAM for PERSON vertex on gender attribute")
  cmd = f"curl -s --user tigergraph:tigergraph -X POST \"http://localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb&vertex=Person&attribute=gender&buckets=2&compute=true\" | jq ."
  subprocess.run(cmd, shell=True)

  print("COMPUTING HISTOGRAM for CONTINENT vertex on name attribute")
  cmd = f"curl -s --user tigergraph:tigergraph -X POST \"http://localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb&vertex=Continent&attribute=name&buckets=2&compute=true\" | jq ."
  subprocess.run(cmd, shell=True)

  print("COMPUTING HISTOGRAM for CONTINENT vertex on id attribute")
  cmd = f"curl -s --user tigergraph:tigergraph -X POST \"http://localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb&vertex=Continent&attribute=id&buckets=2&compute=true\" | jq ."
  subprocess.run(cmd, shell=True)

if __name__ == "__main__":
  edge_types = ["HAS_TAG","REPLY_OF", "IS_PART_OF", "IS_LOCATED_IN", "HAS_MODERATOR", "HAS_MEMBER", "HAS_TYPE", "CONTAINER_OF", "IS_SUBCLASS_OF", "LIKES", "HAS_CREATOR", "WORK_AT", "STUDY_AT", "HAS_INTEREST", "KNOWS"]
  vertex_types = ["Continent", "City", "Country", "Person", "University", "Company", "Post", "Comment", "Forum", "Tag", "TagClass"]
  triplets = []
  triplets.append(("City", "IS_PART_OF", "Country"))
  triplets.append(("Country", "IS_PART_OF_REVERSE", "City"))
  triplets.append(("Country", "IS_PART_OF", "Continent"))
  triplets.append(("Continent", "IS_PART_OF_REVERSE", "Country"))
  triplets.append(("Person", "IS_LOCATED_IN", "City"))
  triplets.append(("City", "IS_LOCATED_IN_REVERSE", "Person"))
  triplets.append(("University", "IS_LOCATED_IN", "City"))
  triplets.append(("City", "IS_LOCATED_IN_REVERSE", "University"))
  triplets.append(("Comment", "IS_LOCATED_IN", "Country"))
  triplets.append(("Country", "IS_LOCATED_IN_REVERSE", "Comment"))
  triplets.append(("Post", "IS_LOCATED_IN", "Country"))
  triplets.append(("Country", "IS_LOCATED_IN_REVERSE", "Post"))
  triplets.append(("Company", "IS_LOCATED_IN", "Country"))
  triplets.append(("Country", "IS_LOCATED_IN_REVERSE", "Company"))
  triplets.append(("Forum", "HAS_MODERATOR", "Person"))
  triplets.append(("Person", "HAS_MODERATOR_REVERSE", "Forum"))
  triplets.append(("Forum", "HAS_MEMBER", "Person"))
  triplets.append(("Person", "HAS_MEMBER_REVERSE", "Forum"))
  triplets.append(("Forum", "CONTAINER_OF", "Post"))
  triplets.append(("Post", "CONTAINER_OF_REVERSE", "Forum"))
  triplets.append(("Person", "HAS_INTEREST", "Tag"))
  triplets.append(("Person", "KNOWS", "Person"))
  triplets.append(("Tag", "HAS_INTEREST_REVERSE", "Person"))
  triplets.append(("Person", "STUDY_AT", "University"))
  triplets.append(("University", "STUDY_AT_REVERSE", "Person"))
  triplets.append(("Person", "WORK_AT", "Company"))
  triplets.append(("Company", "WORK_AT_REVERSE", "Person"))
  triplets.append(("Person", "LIKES", "Post"))
  triplets.append(("Post", "LIKES_REVERSE", "Person"))
  triplets.append(("Person", "LIKES", "Comment"))
  triplets.append(("Comment", "LIKES_REVERSE", "Person"))
  triplets.append(("Comment", "HAS_CREATOR", "Person"))
  triplets.append(("Person", "HAS_CREATOR_REVERSE", "Comment"))
  triplets.append(("Post", "HAS_CREATOR", "Person"))
  triplets.append(("Person", "HAS_CREATOR_REVERSE", "Post"))
  triplets.append(("Comment", "REPLY_OF", "Comment"))
  triplets.append(("Comment", "REPLY_OF_REVERSE", "Comment"))
  triplets.append(("Comment", "REPLY_OF", "Post"))
  triplets.append(("Post", "REPLY_OF_REVERSE", "Comment"))
  triplets.append(("Comment", "HAS_TAG", "Tag"))
  triplets.append(("Tag", "HAS_TAG_REVERSE", "Comment"))
  triplets.append(("Post", "HAS_TAG", "Tag"))
  triplets.append(("Tag", "HAS_TAG_REVERSE", "Post"))
  triplets.append(("Forum", "HAS_TAG", "Tag"))
  triplets.append(("Tag", "HAS_TAG_REVERSE", "Forum"))
  triplets.append(("Tag", "HAS_TYPE", "TagClass"))
  triplets.append(("TagClass", "HAS_TYPE_REVERSE", "Tag"))
  triplets.append(("TagClass", "IS_SUBCLASS_OF", "TagClass"))
  triplets.append(("TagClass", "IS_SUBCLASS_OF_REVERSE", "TagClass"))

  """
  Usage:
  python3 statistics.py [-card|-hist]
  Parameters:
  -card = deletes existing stats and reocmputes vertex and edge counts
  -hist = computes histograms for a defined set of attributes of specific vertices (hardcoded for now)
  Both params can be specified.

  Examples:
  python3 statistics.py -card
  python3 statistics.py -card -hist
  """

  if len(sys.argv) < 2:
    print("Specify -card (cardinality) and/or -hist (histogram)")
    sys.exit()

  computeCard = False
  computeHist = False

  for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-card":
      computeCard = True
    if sys.argv[i] == "-hist":
      computeHist = True

  if computeCard:
    delete_card()
    compute_vertex_cnts()
    compute_edge_cnts()
    show_card()
  
  if computeHist:
    compute_histograms()