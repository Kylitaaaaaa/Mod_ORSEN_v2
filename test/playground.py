relation_string = "1 Object, 1 HasProperty 2"

relations_split = relation_string.split(",")

relations = []
# for r in relations_split:
#     r = r.strip()
#     pattern = r.split(" ")
#     print(pattern)

[relations.append(r.strip().split(" ")) for r in relations_split]
print(relations)
xd = ' '.join(relations[1])
print(xd)