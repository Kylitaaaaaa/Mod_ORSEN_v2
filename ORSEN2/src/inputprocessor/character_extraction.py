from src.db.concepts import DBO_Concept

def character_attribute_extraction(nc_text, pos_lemma, pos_dep, pos_text, nc_dep_root):
    characters = {}
    objects = {}
    for i in range(0, len(pos_dep)):
        for j in range(0, len(pos_dep[i])):
            if pos_dep[i][j] == "ROOT":
                
                if DBO_Concept.get_concept_specified("character", DBO_Concept.CAPABLE_OF, pos_lemma[i][j]) is not None:
                        characters = add_character_attribute(i, nc_text, pos_dep, pos_text, nc_dep_root)
                else:
                        print("ELSE", pos_dep[i][j])
                        objects = add_object_attribute(i, nc_text, pos_dep, pos_text, nc_dep_root)

    return characters, objects
