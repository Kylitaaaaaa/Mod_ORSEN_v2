from src.dialoguemanager import Follow_Up, DBO_Follow_Up

p = DBO_Follow_Up.get_specific_follow_up_template(61)

print(p.follow_up_template)

follow_up_relations = [[1, "13"], [3, "14"]]
dict_nodes = {'1': 'person', '2': 'eat', '3': 'cake'}
print(dict_nodes)

p.fill_blank_template(follow_up_relations, dict_nodes)
p.get_string_template()

print(p.final_response)

'''
def fill_up_response(move, world, remove_index, text, DATABASE_TYPE):
    subject_list = []

    for blank_type in move.blanks:
            print("CURRENT SUBJECTS: ", subject_list)
            subject = None # IDK????
            replace_subject_type_name = 0
            
            has_a_specified_concept = ":" in blank_type

            if has_a_specified_concept:
                split_relation = str(blank_type).split(":")
                relation_index = -1
                replacement_index = -1

                for i in range(0, len(split_relation)):
                    if split_relation[i] in DATABASE_TYPE.RELATIONS:
                        relation_index = i
                    else:
                        replacement_index = i

                usable_concepts = []
                txt_relation = split_relation[relation_index]
                to_replace = split_relation[replacement_index]

                if to_replace in ["setting"]:
                    if to_replace == "setting":
                        print("SETTING DECISION:")
                        if subject is None or subject.inSetting['LOC'] is None:
                            print("No viable SUBJECT or SUBJECT LOCATION... switching move.")
                            return None
                        else:
                            txt_concept = subject.inSetting['LOC']

                else:
                    txt_concept = to_replace

                if relation_index == 0:
                    usable_concepts = DATABASE_TYPE.get_concept_like(txt_relation, second=txt_concept)
                elif relation_index == 1:
                    usable_concepts = DATABASE_TYPE.get_concept_like(txt_relation, first=txt_concept)
                else:
                    print("ERROR: Index not found.")
                
                #if may laman ang usable_concepts
                if len(usable_concepts) > 0 :
                    concept_string = ""
                    concept_index = random.randint(0,len(usable_concepts)) #randomize it, get one

                    if relation_index == 0:
                        concept_string = usable_concepts[concept_index].first #get the first concept
                    elif relation_index == 1:
                        concept_string = usable_concepts[concept_index].second

                    move.template[move.template.index(to_replace)] = concept_string #from the templates, look for the index of the to_replace
                    move.blank_dictionary_move[to_replace] = concept_string                
            elif blank_type in DATABASE_TYPE.RELATIONS:

                # CHOOSE THE CONCEPT
                decided_concept = ""
                decided_node = -1

                loop_total = 0
                if subject is None:
                    charas = world.get_top_characters()
                    objects = world.get_top_objects()

                    list_choices = charas + objects
                    while True:
                        if len(list_choices) > 0:
                            loop_total += 1
                            choice_index = random.randint(0, len(list_choices))
                            decided_item = list_choices[choice_index]

                            # make sure that the same subject is not used twice in one sentence.
                            # Very ugly code, need to fix
                            while decided_item.name in subject_list:
                                list_choices.pop(choice_index)

                                if len(list_choices) == 0:
                                    break

                                choice_index = random.randint(0, len(list_choices))
                                decided_item = list_choices[choice_index]

                        if len(list_choices) == 0:
                            decided_item = None
                            print("AAAAaAA")
                            break

                        subject = decided_item
                        print(subject.name)
                        print(subject.type)

                        if world.continue_suggesting == 1:
                            subject = world.subject_suggest
                            print("SUBJECT SUGGEST", subject)
                            decided_node = NODE_START

                        if len(subject.type) > 0:
                            # decided_concept = subject.name[random.randint(0, len(subject.type))]
                            choice_index = random.randint(0, len(subject.type))
                            decided_concept = subject.type[choice_index]
                            print("SUBJECT TYPE: ", decided_concept)
                            
                            subject_list.append(subject.name) #SUBJECT CELINA, person, human, etc. 
                            replace_subject_type_name = 1
                            decided_node = NODE_START
                        else:
                            if isinstance(decided_item, Object):
                                decided_concept = decided_item.name
                                subject = decided_item
                                subject_list.append(subject) #SUBJECT CELINA
                                decided_node = NODE_START
                                print("DC", decided_concept)
                                print("OBJECT KA BA")

                            #NEVER ATA DUMAAN DITO SA ELIF, di ko alam para saan ito
                            elif isinstance(decided_item, Character):
                                # get... something... relationship??
                                # TODO: use relationship or something to get a concept
                                found_attr = DATABASE_TYPE.HAS_PROPERTY
                                decided_concept = decided_item.name
                                subject = decided_item

                                if blank_type == DATABASE_TYPE.HAS_PREREQ or blank_type == DATABASE_TYPE.CAUSES:
                                    found_attr = DATABASE_TYPE.CAPABLE_OF
                                    decided_node = NODE_START

                                elif blank_type == DATABASE_TYPE.IS_A or blank_type == DATABASE_TYPE.PART_OF or DATABASE_TYPE.USED_FOR:
                                    found_attr = DATABASE_TYPE.IS_A
                                    decided_node = NODE_START
                                    
                                for item in decided_item.attributes:
                                    if item.relation == found_attr and not item.isNegated:
                                        decided_concept = item.name
                                        break

                                if decided_concept == "":
                                    return None

                        if decided_node != -1 or loop_total > 10:
                            break

                    if blank_type == DATABASE_TYPE.AT_LOCATION:
                        list_settings_names = []
                        list_settings_names = world.settings

                        # use for the subject continuous. It "normally" gets the location 
                        # frog went to forest. 
                        # If not continous suggestion, it would get forest at the decided concept
                        # if continuous, and subject is frog then disregard this
                        if world.continue_suggesting == 0 or world.subject_suggest.name in list_settings_names:
                            settings = world.settings

                            print("length settings", len(settings))
                            if len(settings) > 0:
                                decided_concept = settings[ran.choice(list(settings.keys()))].name
                                decided_node = NODE_END
                            else:
                                return None

                        #else:
                        #    decided_node = NODE_START
                    
                    if world.continue_suggesting == 1:
                            subject = world.subject_suggest
                            print("SUBJECT SUGGEST", subject)
                            decided_node = NODE_START
                # find
                # This part looks for the concept. Example Girl went to mall. So if decided_node is NODE_END. 
                # It would look for concepts na ang second ay mall
                if decided_node == NODE_START:
                    usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, first=decided_concept)
                elif decided_node == NODE_END:
                    usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, second=decided_concept)
                elif decided_node == NODE_EITHER: #Not being used?
                    usable_concepts = DATABASE_TYPE.get_concept(decided_concept, blank_type)
                else:
                    usable_concepts = []

                #If there is none found, change template.
                if len(usable_concepts) == 0:
                    print("LP1:", loop_total)
                    return None

                while len(usable_concepts) == 0:
                    loop_total += 1
                    print("LP2:", loop_total)
                    usable_concepts = DATABASE_TYPE.get_concept_like(blank_type)
                    if loop_total > 10:
                        break
                        
                print("DECIDED CONCEPT: "+decided_concept)
                print("Num usable concept", len(usable_concepts))
                #Usable concepts for local is limited to those that are valid. Valid = 1
                remove_concept = []
                if len(usable_concepts) > 0:
                    # Also check if the concept was already use here, use loops
                    concept_index = random.randint(0,len(usable_concepts))
                    concept = usable_concepts[concept_index]

                    dbtype_concept_list = get_dbtype_concept_list(DATABASE_TYPE, world)

                    #Make sure the same concept is not used again for this world.
                    while concept.id in dbtype_concept_list:
                        usable_concepts.remove(concept)

                        if len(usable_concepts) == 0:
                            return None

                        concept_index = random.randint(0,len(usable_concepts))
                        concept = usable_concepts[concept_index]
                        #print("USABLE CON2", len(usable_concepts))

                    if replace_subject_type_name == 1:
                        concept.first = subject.name

                    move.template[move.template.index("start")] = concept.first
                    move.template[move.template.index("end")] = concept.second

                    move.blank_dictionary_move["start"] = concept.first
                    move.blank_dictionary_move["end"] = concept.second

                    # No need to swap sa iba, this is the only one because start and end from db
                    
                    # Get the concept id, this is for adding the score
                    move.concept_id = concept.id

                    if DATABASE_TYPE == DBO_Concept:
                        world.global_concept_list.append(concept.id)
                    elif DATABASE_TYPE == DBO_Local_Concept:
                        world.local_concept_list.append(concept.id)
                    
                    print("USED GLOBAL ASSERTIONS ID: ", world.global_concept_list)
                    print("USED LOCAL ASSERTIONS ID: ", world.local_concept_list)

                else:
                    print("ERROR: NO USABLE CONCEPTS decided:",decided_concept)
                    return None

            elif blank_type == "Object":

                if subject is None:
                    charas = world.get_top_characters()
                    objects = world.get_top_objects()
                    list_choices = charas + objects

                    if len(list_choices) > 0:
                        choice_index = random.randint(0, len(list_choices))
                        subject = list_choices[choice_index]
                        subject_list.append(subject) #SUBJECT CELINA
                    else:
                        return None

                if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
                    subject = world.subject_suggest

                move.template[move.template.index("object")] = subject.id
                move.blank_dictionary_move["object"] = subject.id

            elif blank_type == "Item":

                if subject is None:
                    objects = world.get_top_objects()

                    if len(objects) > 0:
                        choice_index = random.randint(0, len(objects))
                        subject = objects[choice_index]
                        subject_list.append(subject) #SUBJECT CELINA
                    else:
                        return None
                
                if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
                    subject = world.subject_suggest

                move.template[move.template.index("item")] = subject.id
                move.blank_dictionary_move["item"] = subject.id

            elif blank_type == "Character":
                if subject is None or not isinstance(subject, Character):
                    charas = world.get_top_characters(5)
                    if len(charas) > 0:
                        choice_index = random.randint(0, len(charas))
                        subject = charas[choice_index]
                        # Line 668 sa Dialogue Planner
                        # subject = charas[0]
                        #add condition here that shows na bawal ang character dito na same sa suggest subject?
                    else:
                        return None
                else:
                    chara = subject
                
                #NAG SA_SAME SUBJECT DAHIL DITO????
                if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
                    subject = world.subject_suggest

                subject_list.append(subject.id) #SUBJECT CELINA
                move.template[move.template.index("character")] = subject.id
                move.blank_dictionary_move["character"] = subject.id

            elif blank_type == "inSetting":
                if subject is None:
                    return None
                elif subject.inSetting is None:
                    return None
                else:
                    move.template[move.template.index("inSetting")] = subject.inSetting['LOC']
                    move.blank_dictionary_move["inSetting"] = subject.inSetting['LOC']

            elif blank_type == "Repeat":

                if len(world.event_chain) > 0:
                    move.template[move.template.index("repeat")]\
                        = to_sentence_string(world.event_chain[len(world.event_chain)-1])
                    move.blank_dictionary_move["repeat"]\
                        = to_sentence_string(world.event_chain[len(world.event_chain)-1])
                else:
                    return None

            elif blank_type == "Pronoun":
                if subject is None:
                    move.template[move.template.index("pronoun")] = "it"
                    move.blank_dictionary_move["pronoun"] = "it"
                else:
                    if isinstance(subject, Object):
                        move.template[move.template.index("pronoun")] = "they"
                        move.blank_dictionary_move["pronoun"] = "they"
                    elif subject.gender == "":
                        move.template[move.template.index("pronoun")] = "they"
                        move.blank_dictionary_move["pronoun"] = "they"
                    elif subject.gender == "M":
                        move.template[move.template.index("pronoun")] = "he"
                        move.blank_dictionary_move["pronoun"] = "he"
                    elif subject.gender == "F":
                        move.template[move.template.index("pronoun")] = "she"
                        move.blank_dictionary_move["pronoun"] = "she"
                    else:
                        move.template[move.template.index("pronoun")] = subject.name
                        move.blank_dictionary_move["pronoun"] = subject.name

            elif blank_type == "Event":
                loop_back = len(world.event_chain)-1
                loops = 0
                while loop_back >= 0 and loops < 5:
                    event = world.event_chain[loop_back]

                    if event.event_type == FRAME_EVENT:
                        if event.action != "":
                            if "eventverb" in move.template:
                                move.template[move.template.index("eventverb")] = event.action
                                move.blank_dictionary_move["eventverb"] = event.action
                            if "object" in move.template:
                                move.template[move.template.index("object")] = get_subject_string(event)
                                move.blank_dictionary_move["object"] = get_subject_string(event)

                    loop_back -= 1
                    loops += 1

                if loop_back == -1 or loops >= 5:
                    return None
    
    return move
'''