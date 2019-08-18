from numpy import random
from src.objects.ServerInstance import ServerInstance
from src.inputprocessor.infoextraction import getCategory, CAT_STORY, CAT_COMMAND, CAT_ANSWER
from src.dialoguemanager import DBO_Move, Move
from src.dialoguemanager import Follow_Up, DBO_Follow_Up
from src.db.concepts import DBO_Concept, DBO_Local_Concept
from src.objects.concepts.Concept import Concept
from src.objects.eventchain.EventFrame import EventFrame, FRAME_EVENT, FRAME_DESCRIPTIVE
from src.dialoguemanager.story_generation import to_sentence_string, get_subject_string

from src.objects.storyworld.Character import Character
from src.objects.storyworld.Object import Object

import random as ran

from sys import exit

STORY_THRESHOLD = 3
GENERAL_RESPONSE_THRESHOLD = 5

#what score should be met to change the dbtype "local" to "global"
SCORE_THRESHOLD = 5

MOVE_FEEDBACK = 1
MOVE_GENERAL_PUMP = 2
MOVE_SPECIFIC_PUMP = 3
MOVE_HINT = 4
MOVE_REQUESTION = 5
MOVE_UNKNOWN = 6
MOVE_PROMPT = 7
MOVE_SUGGESTING = 8
MOVE_FOLLOW_UP1 = 9
MOVE_FOLLOW_UP2 = 10

NODE_START = 0
NODE_END = 1
NODE_EITHER = 2

CONVERT_INFINITIVE = "inf"
CONVERT_1PRSG = "1sg"
CONVERT_2PRSG = "2sg"
CONVERT_3PRSG = "3sg"
CONVERT_PRPL = "pl"
CONVERT_PRPART = "part"

CONVERT_PAST = "p"
CONVERT_1PASG = "1sgp"
CONVERT_2PASG = "2sgp"
CONVERT_3PASG = "3sgp"
CONVERT_PAPL = "ppl"
CONVERT_PAPART = "ppart"

server = ServerInstance()

def retrieve_output(coreferenced_text, world_id, userid, dm_fileWriter):
    dm_fileWriter.write("GETTING SUITABLE ORSEN RESPONSE\n")
    world = server.get_world(world_id)
    if len(world.responses) > 0:
        last_response_type_num = world.responses[len(world.responses)-1].type_num
    else:
        last_response_type_num = -1
    output = ""
    choice = -1

    if len(world.event_chain) <=  1 and ("my name is" in coreferenced_text or
            (("hello" in coreferenced_text or "hi" in coreferenced_text)
                  and ("I am" in coreferenced_text or "I'm" in coreferenced_text)) ):
        return Move.Move(template=["Nice to meet you! So how does your story start?"], type_num=MOVE_REQUESTION)

    if coreferenced_text == "":  # if no input found
        world.empty_response += 1

        if world.empty_response == 1:
            if last_response_type_num in [MOVE_FEEDBACK, MOVE_HINT]:
                output = Move.Move(template=["I'm sorry, I did not understand what you just said. Can you say it again?"], type_num=MOVE_REQUESTION)
            elif last_response_type_num == MOVE_GENERAL_PUMP:
                output = generate_response(MOVE_SPECIFIC_PUMP, world, [], coreferenced_text, dm_fileWriter)
            elif last_response_type_num == MOVE_SPECIFIC_PUMP:
                output = generate_response(MOVE_HINT, world, [], coreferenced_text, dm_fileWriter)
                output.template = ["What if "]+output.template
            else:
                output = Move.Move(template=["I'm not sure I heard you?"], type_num=MOVE_REQUESTION)

        if world.empty_response >= 2 and world.empty_response <=4:
            if last_response_type_num == MOVE_GENERAL_PUMP:
                output = generate_response(MOVE_SPECIFIC_PUMP, world, [], coreferenced_text, dm_fileWriter)
            elif last_response_type_num == MOVE_SPECIFIC_PUMP:
                output = generate_response(MOVE_HINT, world, [], coreferenced_text, dm_fileWriter)
                output.template = ["What if "] + output.template
            else:
                choice = random.randint(MOVE_GENERAL_PUMP, MOVE_SPECIFIC_PUMP+1)
                output = generate_response(choice, world, [], coreferenced_text, dm_fileWriter)

        elif world.empty_response > 4:
            choice = MOVE_REQUESTION
            output = Move.Move(template=["I don't think I can hear you, are you sure you want to continue?"], type_num=choice)
    else:
        world.empty_response = 0
        category = getCategory(coreferenced_text)
        dm_fileWriter.write("category: " + str(category) + "\n")

        if len(world.responses) >= 3:
            if (last_response_type_num == MOVE_FOLLOW_UP2):
                print("world.continue_suggesting", world.continue_suggesting)
                print("GO HERE PLEASE")
                # and world.responses[len(world.responses)-3].type_num == MOVE_SUGGESTING):
                prev_response = world.responses[len(world.responses)-1]
                relation_list = prev_response.choices_relationID
                coreferenced_text = coreferenced_text.upper() # Capitalizes the entire string
                answer = coreferenced_text.split(" ") #Assuming answers are like this A and B or A B C. If like this ABC di gagana

                counter = 0
                for x in range(len(relation_list)):
                    for y in range(len(answer)):
                        if relation_list[x][0] == answer[y]:
                            counter += 1
                            #Get the entire local concept
                            local_concept = DBO_Local_Concept.get_concept_by_id(int(relation_list[x][1]))
                            dm_fileWriter.write("Deduct Local Concept ID: " + str(local_concept.id) + "\n")

                            if local_concept.userid != userid:
                                new_score = local_concept.score - 1     #Minus the score
                                dm_fileWriter.write("Local Concept score: " + str(local_concept.score) + "\n")
                                dm_fileWriter.write("Local Concept new score: " + str(new_score) + "\n")
                                DBO_Local_Concept.update_score(local_concept.id, new_score) #Update the score
                                dm_fileWriter.write("\n")
                if counter == 0:
                    world.notInChoices += 1
                else:
                    world.inChoices += 1

                category = -1  

        if last_response_type_num == MOVE_SUGGESTING or last_response_type_num == MOVE_FOLLOW_UP1:
            print("last_response_type_num")
            if last_response_type_num == MOVE_FOLLOW_UP1:
                print("HELLP")
            category = CAT_ANSWER

        if category == -1:
            dm_fileWriter.write("category: " + str(category) + "\n")
            output = suggest_again(world, coreferenced_text, dm_fileWriter)
        
        elif category == CAT_STORY:
            if len(world.event_chain) <= STORY_THRESHOLD:
                dm_fileWriter.write("<< STILL IN GENERALIZED THRESHOLD >> \n")
                print("<< STILL IN GENERALIZED THRESHOLD >>")
                choice = random.randint(MOVE_FEEDBACK, MOVE_GENERAL_PUMP+1)
                #choice = MOVE_FEEDBACK
            elif world.general_response_count == GENERAL_RESPONSE_THRESHOLD:
                dm_fileWriter.write("<< GENERAL THRESHOLD REACHED - ATTEMPTING SPECIFIC RESPONSE >> \n")
                choice = random.randint(MOVE_SPECIFIC_PUMP, MOVE_SPECIFIC_PUMP+1)
            else:
                #WEIGHTED RANDOMIZER
                choice = world.compute_weights_dialogue(dm_fileWriter)
                
                # Make sure that the same dialogue move would not be chosen for 4 times in a row
                if len(world.responses) >= 3:
                    while choice == world.responses[len(world.responses)-3].type_num and \
                          choice == world.responses[len(world.responses)-2].type_num and \
                          choice == world.responses[len(world.responses)-1].type_num:
                        choice = world.compute_weights_dialogue(dm_fileWriter)

            output = generate_response(choice, world, [], coreferenced_text, dm_fileWriter)

        elif category == CAT_ANSWER:
            if last_response_type_num == MOVE_REQUESTION:
                output = Move.Move(template=["Ok, let's keep going then!"], type_num=MOVE_UNKNOWN)
            
            if last_response_type_num == MOVE_SUGGESTING:
                coreferenced_text = coreferenced_text.lower()
                print(coreferenced_text)
                if "yes" in coreferenced_text:
                    world.continue_suggesting = 0
                    world.suggest_continue_count = 0
                    world.yes += 1

                    last_rep_follow_up_rels = world.responses[len(world.responses)-1].follow_up_relations

                    dm_fileWriter.write("User answered yes to suggestion. \n")
                    for x in range(len(last_rep_follow_up_rels)):
                        #Get the entire local concept
                        local_concept = DBO_Local_Concept.get_concept_by_id(int(last_rep_follow_up_rels[x][1]))
                        dm_fileWriter.write("Add Local Concept ID: " + str(local_concept.id) + "\n")

                        if local_concept.userid != userid:
                            new_score = local_concept.score + 1     #Add the score
                            dm_fileWriter.write("Local Concept score: " + str(local_concept.score) + "\n")
                            dm_fileWriter.write("Local Concept new score: " + str(new_score) + "\n")
                            DBO_Local_Concept.update_score(local_concept.id, new_score) #Update the score

                            #If score exceeds, change assertion/concept type to global
                            if new_score >= SCORE_THRESHOLD:
                                dm_fileWriter.write("Local Concept ID: " + str(local_concept.id) + " was moved to Global \n")
                                DBO_Local_Concept.update_valid(local_concept.id, 0)
                                DBO_Concept.add_concept(Concept(local_concept.id, local_concept.first, local_concept.relation, local_concept.second))
                        dm_fileWriter.write("\n")
                    #NEW RESPONSE
                    output = Move.Move(template=["Ok, let's keep going then!"], type_num=MOVE_UNKNOWN)
                
                elif "no" in coreferenced_text:
                    output = Move.Move(template=["Why not? Don't you like it or do you think it's wrong?"], type_num=MOVE_FOLLOW_UP1)
                    world.continue_suggesting = 1
                    world.suggest_continue_count += 1
                    world.no += 1

                    prev_response = world.responses[len(world.responses)-1]
                    output.move_id = prev_response.move_id
                    output.follow_up_relations =  prev_response.follow_up_relations
                    output.dict_nodes = prev_response.dict_nodes
                    output.subjects_for_suggestion = prev_response.subjects_for_suggestion
              
                else:
                    output = Move.Move(template=["Sorry, I don't understand. Please answer by yes or no"], type_num=MOVE_SUGGESTING)
                    prev_response = world.responses[len(world.responses)-1]
                    output.move_id = prev_response.move_id
                    output.follow_up_relations =  prev_response.follow_up_relations
                    output.dict_nodes = prev_response.dict_nodes
                    output.subjects_for_suggestion = prev_response.subjects_for_suggestion

            elif last_response_type_num == MOVE_FOLLOW_UP1: #and world.continue_suggesting == 1:  
                print("world.continue_suggesting", world.continue_suggesting)
                print("GO HERE PLEASE")
                coreferenced_text = coreferenced_text.lower()
                
                if "don't like" in coreferenced_text or "dont like" in coreferenced_text:
                    # Suggest again?
                    world.dontLike += 1
                    output = suggest_again(world, coreferenced_text, dm_fileWriter)

                elif "wrong" in coreferenced_text:
                    # Output using the hardcoded templates. Move should be MOVE_ANSWER? MOVE_FOLLOW_UP
                    print("NOT YET DONE")
                    world.wrong += 1
                    prev_response = world.responses[len(world.responses)-1]

                    #Follow Up Functions
                    temp_response = get_follow_up_string(prev_response)
                    
                    if temp_response == None:
                        # MINUS, this means there is only one relation sa move template
                        #Get the entire local concept
                        last_rep_follow_up_rels = prev_response.follow_up_relations
                        local_concept = DBO_Local_Concept.get_concept_by_id(int(last_rep_follow_up_rels[0][1]))
                        dm_fileWriter.write("User answered no to suggestion. \n")
                        dm_fileWriter.write("Deduct Local Concept ID: " + str(local_concept.id) + "\n")
                        if local_concept.userid != userid:
                            new_score = local_concept.score - 1.0     #Minus the score
                            dm_fileWriter.write("Local Concept score: " + str(local_concept.score) + "\n")
                            dm_fileWriter.write("Local Concept new score: " + str(new_score) + "\n")
                            dm_fileWriter.write("\n")
                            DBO_Local_Concept.update_score(local_concept.id, new_score) #Update the score

                        output = suggest_again(world, coreferenced_text, dm_fileWriter)
                    else:
                        output = Move.Move(template=["Which one is wrong? " + temp_response.get_string_template()], type_num=MOVE_FOLLOW_UP2)                                       
                        dm_fileWriter.write("Follow Up # 2. \n")
                        output.move_id = prev_response.move_id
                        output.follow_up_relations =  prev_response.follow_up_relations
                        output.dict_nodes = prev_response.dict_nodes
                        output.choices_relationID = temp_response.choices_relationID
                        output.subjects_for_suggestion = prev_response.subjects_for_suggestion

                        print(temp_response.choices_relationID)
                        dm_fileWriter.write("MULTIPLE CHOICE" + str(temp_response.choices_relationID) + "\n")
                
                else:
                    output = Move.Move(template=["Sorry, I don't understand. Please answer by don't like or wrong"], type_num=MOVE_FOLLOW_UP1)
                    prev_response = world.responses[len(world.responses)-1]
                    output.move_id = prev_response.move_id
                    output.follow_up_relations =  prev_response.follow_up_relations
                    output.dict_nodes = prev_response.dict_nodes 
                    output.subjects_for_suggestion = prev_response.subjects_for_suggestion

            else:
                choice = random.randint(MOVE_FEEDBACK, MOVE_HINT+1)
                output = generate_response(choice, world, [], coreferenced_text, dm_fileWriter)

        elif category == CAT_COMMAND:
            # TEMP TODO: check for further commands
            choice = random.randint(MOVE_FEEDBACK, MOVE_SPECIFIC_PUMP+1)
            
            '''
            is_hint = "your turn" in coreferenced_text or \
                        "talk" in coreferenced_text or \
                        ("give" in coreferenced_text and "hint" in coreferenced_text)

            is_either = "help" in coreferenced_text or \
                        "stuck" in coreferenced_text
            
            is_suggesting = ("suggest" in coreferenced_text and "sentence" in coreferenced_text) or \
                            ("give" in coreferenced_text and "idea" in coreferenced_text) or \
                            "what happens next" in coreferenced_text or \
                            "trial" in coreferenced_text
            '''
            is_hint = "hint" in coreferenced_text
            is_suggesting = "suggest" in coreferenced_text or \
                        "help" in coreferenced_text or \
                        "stuck" in coreferenced_text

            if "help me start" in coreferenced_text:
                output = generate_response(MOVE_PROMPT, world, [], coreferenced_text, dm_fileWriter)
                world.add_response(output)
                return output

            # if len(world.responses) == 0:
            #     concepts = DBO_Concept.get_concept_like(txt_relation, second=txt_concept)
            #if is_either:
            #    choice = random.randint(MOVE_GENERAL_PUMP, MOVE_HINT+1) #between suggesting and hinting
            if is_hint:
                choice = MOVE_HINT
            elif is_suggesting:
                choice = MOVE_SUGGESTING

            output = generate_response(choice, world, [], coreferenced_text, dm_fileWriter)

        else:
            output = Move.Move(template=["I don't know what to say."], type_num=MOVE_UNKNOWN)
    
    # AFTER GETTING THE TEMPLATE

    #Check if the move is suggesting, then change the variable

    if output.type_num == MOVE_SUGGESTING:
        world.continue_suggesting = 1
        print("LINE 324")
        print("world.continue_suggesting", world.continue_suggesting)

        if world.subject_suggest == None:
            choice_index = random.randint(0, len(output.subjects_for_suggestion))
            world.subject_suggest = output.subjects_for_suggestion[choice_index]

        # TAKE NOTE
        #world.subject_suggest = output.subjects_for_suggestion[0]
        print("MEOW", world.subject_suggest)

    # TAKE NOTE
    #elif output.type_num != MOVE_UNKNOWN:
    elif output.type_num == MOVE_FOLLOW_UP1 or output.type_num == MOVE_FOLLOW_UP2:
        world.continue_suggesting = 1

    else:
        world.continue_suggesting = 0
        world.subject_suggest = None

    world.add_response(output)
    world.add_response_type_count(output)

    #Feedback would be added
    feedback_add = feedback_random(output.type_num)
    if feedback_add == 1 and category == CAT_STORY:
        feedback_output = generate_response(MOVE_FEEDBACK, world, [], coreferenced_text, dm_fileWriter)
        # print("OOF", feedback_output.get_string_response())
        # prevents instances like, Oh so that's what happens, what happens next?
        if "happens" in output.get_string_response() or "happened" in output.get_string_response():
            if "happens" in feedback_output.get_string_response():
                print("do nothing. No combination")
            else:
                combination_response(output.type_num, world)
                output.template.insert(0, feedback_output.get_string_response() + " ")
        else:
            combination_response(output.type_num, world)
            output.template.insert(0, feedback_output.get_string_response() + " ")

    return output

#Note this one is when a move_code has been decided. If there is no concepts then change move_code to feedback.
def generate_response(move_code, world, remove_index, text, dm_fileWriter):

    subject_list = []

    #DBO should be accessing the local concept
    DATABASE_TYPE = DBO_Concept
    if move_code == MOVE_SUGGESTING:
        DATABASE_TYPE = DBO_Local_Concept
        db_type = "local"
    else:
        DATABASE_TYPE = DBO_Concept
        db_type = "global"

    print(DATABASE_TYPE)

    choices = []
    subject = None

    if len(world.responses) > 0:
        last_response_id = world.responses[len(world.responses)-1].move_id

        print("LAST USED TEMPLATE RESPONSE: ", last_response_id)
    else:
        last_response_id = -1

    if move_code == MOVE_FEEDBACK:
        dm_fileWriter.write("ATTEMPTED MOVE CODE: FEEDBACK \n")
        pre_choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_FEEDBACK)

        if len(world.event_chain) > 0:
            last = world.event_chain[len(world.event_chain)-1]
            for item in pre_choices:
                if last.event_type == FRAME_EVENT and "happen" in item.get_string_response():
                    choices.append(item)
                if "happen" not in item.get_string_response():
                    choices.append(item)
        else:
            choices = pre_choices

    elif move_code == MOVE_GENERAL_PUMP:
        dm_fileWriter.write("ATTEMPTED MOVE CODE: GENERAL PUMP \n")
        pre_choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_GENERAL_PUMP)

        if len(world.event_chain) > 0:
            last = world.event_chain[len(world.event_chain)-1]
            for item in pre_choices:
                if last.event_type == FRAME_EVENT and "happen" in item.get_string_response():
                    choices.append(item)
                if "happen" not in item.get_string_response():
                    choices.append(item)
        else:
            choices = pre_choices

    elif move_code == MOVE_SPECIFIC_PUMP:
        dm_fileWriter.write("ATTEMPTED MOVE CODE: SPECIFIC PUMP \n")
        choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_SPECIFIC_PUMP)

    elif move_code == MOVE_HINT:
        #choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_HINT)
        # Since same templates naman
        dm_fileWriter.write("ATTEMPTED MOVE CODE: HINT \n")
        choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_SUGGESTING)
    
    elif move_code == MOVE_SUGGESTING:
        dm_fileWriter.write("ATTEMPTED MOVE CODE: SUGGESTING \n")
        choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_SUGGESTING)

    elif move_code == MOVE_REQUESTION:
        # TODO: requestioning decisions to be made
        choices = ["requestioning..."]
    elif move_code == MOVE_PROMPT:
        dm_fileWriter.write("ATTEMPTED MOVE CODE: PROMPT \n")
        choices = DBO_Move.get_templates_of_type("prompt")
        usable_concepts = DATABASE_TYPE.get_concept_like("IsA", second="role")
        choice = random.randint(0, len(choices))
        choice2 = random.randint(0, len(usable_concepts))
        if len(usable_concepts) > 0:
            move = choices[choice]
            #Change fill up for prompts
            # a = []
            # a.append(usable_concepts[choice2].first)
            # move.fill_blank(a)
            a = usable_concepts[choice2].first
            move.fill_blank_prompt(a)

            print("FINAL MOVE DECISION:")
            dm_fileWriter.write("FINAL MOVE DECISION: \n")
            dm_fileWriter.write(str(move) + "\n")
            print(str(move))
            return move

    index_loop = 0

    #This is where move was first initialize
    while True:
        index_loop += 1
        index = random.randint(0, len(choices))
        move = choices[index]

        dm_fileWriter.write("ATTEMPTED MOVE ID: " + str(move.move_id) + "\n")
        # Check if the template has already been use through move.move_id
        # Dapat hindi siya yun last na use. Dapat hindi siya nasa remove_index
        if move.move_id != last_response_id and move.move_id not in remove_index:
            move.type_num = move_code
            break

        print("Loop count: ", index_loop)
        if index_loop > 20:
            '''exit(0)'''
            remove_index.append(move.move_id)
            dm_fileWriter.write("CHANGE MOVE \n")

            # if wala mahanap sa suggesting
            if world.continue_suggesting == 1: 
                # CELINA -IDK, don't uncomment the one below
                # return generate_response(MOVE_SPECIFIC_PUMP, world, remove_index, text, dm_fileWriter)
                # UNCOMMENT
                output = Move.Move(template=["I don't know much about " + world.subject_suggest[1].name + ". Please help me learn by telling me more about " + world.subject_suggest[1].name + "."], type_num=MOVE_SPECIFIC_PUMP)
                # output = Move.Move(template=["I don't know much about " + world.subject_suggest[1] + ". Please help me learn by telling me more about " + world.subject_suggest[1] + "."], type_num=MOVE_SPECIFIC_PUMP)
                dm_fileWriter.write("FINAL MOVE: SPECIFIC PUMPING \n")
                return output

            else:
                return generate_response(MOVE_FEEDBACK, world, remove_index, text, dm_fileWriter)
    
    print("Generating fillable template...")
    print(str(move))
    dm_fileWriter.write("Generating fillable template... \n")
    dm_fileWriter.write(str(move) + "\n\n")

    '''DEBUUGING, UNCOMMENT THIS Force to choose suggesting
    choices = DBO_Move.get_templates_of_type(DBO_Move.TYPE_SUGGESTING)
    move_code = MOVE_SUGGESTING
    
    move = choices[1]
    move.type_num = move_code

    if len(world.responses) > 0:
        last_response_type_num = world.responses[len(world.responses)-1].type_num
        print(last_response_type_num)
        print(MOVE_SUGGESTING)
        if last_response_type_num == MOVE_UNKNOWN:
            move = choices[1]
            move.type_num = move_code'''
    
    used_concept_list = [["" for x in range(0)] for y in range(len(move.dependent_nodes))]
    subject_suggest_list = [["" for x in range(0)] for y in range(len(move.dependent_nodes))]

    result_move = fill_up_response(move, world, 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
    # print("ASSASAS", result_move)

    '''FILLS UP THE TEMPLATES'''
    if result_move != None:
        keys = [ k for k in result_move.dict_nodes]
        print(keys)
        for x in range(len(keys)):
            for y in range(len(result_move.template)):
                if result_move.template[y] == keys[x]:
                    result_move.template[y] =  result_move.dict_nodes.get(keys[x])
    else:
        dm_fileWriter.write("CHANGE MOVE \n")
        remove_index.append(move.move_id)
        return generate_response(move_code, world, remove_index, text, dm_fileWriter)
    
    print(result_move.template)

    print("SUBJECTSSS: ", subject_list)    
    header_text(move_code, move, world)

    print("FINAL MOVE DECISION:")
    print(str(result_move))

    dm_fileWriter.write("FINAL MOVE DECISION \n")
    dm_fileWriter.write(str(result_move) + "\n")
    dm_fileWriter.write(str(result_move.template) + "\n")
    return result_move


#print("HELLO")
def fill_up_response(move, world, curr_blank, used_concept_list, subject_suggest_list, return_back, dm_fileWriter):
    print("IZ HERE", move.template)

    DATABASE_TYPE = DBO_Local_Concept
    dbtype = "L"

    dm_fileWriter.write("curr blank" + str(curr_blank) + "\n")
    dm_fileWriter.write("dictionary_nodes" + str(move.dict_nodes) + "\n")
    dm_fileWriter.write("used concept list" + str(used_concept_list) + "\n\n")

    print("Dictionary", move.dict_nodes)
    print("curr_blank: ", curr_blank)
    print("Used CL", used_concept_list)


    if curr_blank == len(move.relations)+1:
        for x in range(len(move.blanks)):
            if move.blanks[x] in DATABASE_TYPE.RELATIONS:
                #only need the last one sa used concept list kasi yun naman yun ginamit
                temp = used_concept_list[x][-1].split(":")
                dm_fileWriter.write("FINAL USED CONCEPT: " + str(used_concept_list[x][-1]) + "\n")
                if temp[0] == "G":
                    world.global_concept_list.append(temp[1])
                elif temp[0] == "L":
                    world.local_concept_list.append(temp[1])
                    move.follow_up_relations.append([x, temp[1]])
                
            elif move.blanks[x] == "Character" or move.blanks[x] == "Object":
                temp = ""
                if move.blanks[x] == "Character":
                    temp = "Character"
                elif move.blanks[x] == "Object":
                    temp = "Object"
                move.subjects_for_suggestion.append([temp, subject_suggest_list[x][-1]])
                dm_fileWriter.write("SUBJECT SUGGESTION LIST: " + str(move.subjects_for_suggestion) + "\n")

        dm_fileWriter.write("TEMPLATE COMPLETED \n")
        return move

    elif curr_blank == 0:
        used_concept_list[curr_blank].clear()
        subject_suggest_list[curr_blank].clear()
        dm_fileWriter.write("CHANGE MOVE \n")
        return None
    
    if return_back == True:
        print(move.dependent_nodes[curr_blank-1])
        used_concept_list[curr_blank].clear()
        subject_suggest_list[curr_blank].clear()
        dm_fileWriter.write("MOVE BACK \n")

        if move.dependent_nodes[curr_blank-1] != "None":
            move.dict_nodes[move.dependent_nodes[curr_blank-1]] = ""
            print(move.dict_nodes)

        if move.dependent_nodes[curr_blank-1] == "None":
            dm_fileWriter.write("DEPENDENT NODE = NONE, MOVE BACK \n")
            return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)
    
    if move.blanks[0] == "None":
        return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)

    blank_type = move.blanks[curr_blank-1]
    dm_fileWriter.write("CURR BLANK TYPE: " + str(blank_type) + "\n")

    if blank_type in DATABASE_TYPE.RELATIONS:
        usable_concepts = []
        bin_assertion_template = move.relations[curr_blank-1]

        if move.type_num == MOVE_HINT:
            DATABASE_TYPE = DBO_Concept
            dbtype = "G"

        # This while loop is for the DATABASE_TYPE
        # Priority would be the Local then if no concept, change to global
        while len(usable_concepts) <= 0:
            result_nodes = node_decider(bin_assertion_template, move.dict_nodes, move.subject_type_list)

            if result_nodes[0] == "NODE_START":
                usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, first=result_nodes[1])
            elif result_nodes[0] == "NODE_END":
                usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, second=result_nodes[1])
            elif result_nodes[0] == "NODE_BOTH":
                usable_concepts = DATABASE_TYPE.get_concept_like(blank_type, first=result_nodes[1], second=result_nodes[2])
            else:
                usable_concepts = []
            
            dm_fileWriter.write("RSEULT NODES: " + str(result_nodes[0]) + "\n")
            dm_fileWriter.write("Length of usable concepts: " + str(len(usable_concepts)) + "\n")

            # START OF REMOVE USED CONCEPT
            # dict_nodes.values pa? Baka no need na
            assertionL = []
            assertionG = []
            dm_fileWriter.write("Previous used concepts \n")
            for x in used_concept_list[curr_blank-1]:
                temp = x.split(":")
                if temp[0] == "G":
                    assertionG.append(temp[1])
                else:
                    assertionL.append(temp[1])
            
            dm_fileWriter.write("Global Assertions Used: " + str(assertionG) + "/n")
            dm_fileWriter.write("Global Assertions Used: " + str(assertionL) + "/n")
            temp_index = []
            print("local", assertionL)

            for remove_index in range(len(usable_concepts)):
                if dbtype == "G":
                    assertionG = assertionG + world.global_concept_list
                    if str(usable_concepts[remove_index].id) in assertionG:
                        temp_index.append(remove_index)
                elif dbtype == "L":
                    assertionL = assertionL + world.local_concept_list
                    if str(usable_concepts[remove_index].id) in assertionL:
                        temp_index.append(remove_index)

            temp_index.sort()
            temp_index.reverse()
            for x in temp_index:   
                del usable_concepts[x]
            # END OF REMOVE USED CONCEPT

            # Switching of Database Type
            if len(usable_concepts) == 0 and dbtype == "G":
                dm_fileWriter.write("CANNOT FIND SUITABLE CONCEPTS FROM GLOBAL DB \n")
                break
  
            elif len(usable_concepts) == 0 and dbtype == "L":
                dm_fileWriter.write("CANNOT FIND SUITABLE CONCEPTS FROM LOCAL DB. SWITCHING TO GLOBAL DB \n")
                DATABASE_TYPE = DBO_Concept
                dbtype = "G"
        #END OF LOOP
        dm_fileWriter.write("FINAL Length of usable concepts: " + str(len(usable_concepts)) + "\n")
        
        if len(usable_concepts) == 0:
           return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)
           ### ADD REMOVER OF THE INDEX
        
        if len(usable_concepts) > 0:
            # Also check if the concept was already use here, use loops
            concept_index = random.randint(0,len(usable_concepts))
            concept = usable_concepts[concept_index]

            #  concept = usable_concepts[0]

            dm_fileWriter.write("DBTYPE: " + str(dbtype) + "\n")
            if result_nodes[0] == "NODE_START":
                move.dict_nodes[bin_assertion_template[2]] = concept.second

                dm_fileWriter.write("NODE START: SECOND \n")
                dm_fileWriter.write(str(concept.first) + " " + str(concept.relation) + " " + str(concept.second))  
            elif result_nodes[0] == "NODE_END":
                move.dict_nodes[bin_assertion_template[0]] = concept.first

                dm_fileWriter.write("NODE END: FIRST \n")
                dm_fileWriter.write(str(concept.first) + " " + str(concept.relation) + " " + str(concept.second))    
            elif result_nodes[0] == "NODE_BOTH":
                move.dict_nodes[bin_assertion_template[0]] = concept.first
                move.dict_nodes[bin_assertion_template[2]] = concept.second

                dm_fileWriter.write("NODE BOTH: BOTH \n")
                dm_fileWriter.write(str(concept.first) + " " + str(concept.relation) + " " + str(concept.second))   

            used_concept_list[curr_blank-1].append(dbtype + ":" + str(concept.id))

            #START - AVOID USING THE SAME NODE IN ONE SENTENCE
            rev_dict = {} 
            for key, value in move.dict_nodes.items(): 
                rev_dict.setdefault(value, set()).add(key) 
      
            result = [key for key, values in rev_dict.items() 
                                        if len(values) > 1] 
                                        
            if len(result) > 0:
                if result[0] != "":
                    dm_fileWriter.write("SAME NODE IN ONE SENTENCE \n")
                    return fill_up_response(move, world, curr_blank, used_concept_list, subject_suggest_list, False, dm_fileWriter)
            
            #END - AVOID USING THE SAME NODE IN ONE SENTENCE

            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
    
    elif blank_type == "Object":
        charas = world.get_top_characters()
        objects = world.get_top_objects()
        list_choices = charas + objects

        # DEBUUGING 
        # list_choices = ["cake"] #PUT THIS HERE, IF SA IBA CAUSES INFINITE LOOP. CELINA YOU DUMB
        if world.continue_suggesting == 1 and world.subject_suggest != None:
            if world.subject_suggest[0] == "Object":
                list_choices = [world.subject_suggest[1]]

        # START OF REMOVE USED CONCEPT 
        temp_index = []
        
        blacklist = used_concept_list[curr_blank-1] + list(move.dict_nodes.values())
        for x in range(len(list_choices)):
            if list_choices[x].id in blacklist: #<-uncomment this after
            # DEBUUGING if list_choices[x] in blacklist:
                temp_index.append(x)
        
        temp_index.sort()
        temp_index.reverse()

        for x in temp_index:   
            del list_choices[x]
        # END OF REMOVE USED CONCEPT
        dm_fileWriter.write("Previous used concepts "+ str(blacklist) +"\n")
        dm_fileWriter.write("length of choices "+ str(len(list_choices)) +"\n")
        if len(list_choices) > 0:
            choice_index = random.randint(0, len(list_choices))
            subject = list_choices[choice_index]

            # DEBUUGING, COMMENT THIS OUT
            if len(subject.type) > 0:  
                choice_index = random.randint(0, len(subject.type))
                decided_subject = subject.type[choice_index]
                print("SUBJECT TYPE: ", decided_subject)

                move.subject_type_list.append([curr_blank, decided_subject])

            ''' CELINA - IDK, DON'T UNCOMMENT
            if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
                subject = world.subject_suggest[1]'''
            
            # DEBUUGING, COMMENT THIS OUT
            #move.dict_nodes[str(curr_blank)] = subject.id
            move.dict_nodes[move.nodes[curr_blank-1]] = subject.id
            used_concept_list[curr_blank-1].append(subject.id)

            subject_suggest_list[curr_blank-1].append(subject) #Maintain this

            ''' DEBUUGING, UNCOMMENT THIS
            #move.dict_nodes[str(curr_blank)] = subject
            move.dict_nodes[move.nodes[curr_blank-1]] = subject
            used_concept_list[curr_blank-1].append(subject)'''

            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
        else:
            dm_fileWriter.write("MOVE BACK \n")
            return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)

    
    elif blank_type == "Item":
        objects = world.get_top_objects()

        if world.continue_suggesting == 1 and world.subject_suggest != None:
            if world.subject_suggest[0] == "Item":
                list_choices = [world.subject_suggest[1]]

        # START OF REMOVE USED CONCEPT 
        temp_index = []
        blacklist = used_concept_list[curr_blank-1] + list(move.dict_nodes.values())
        for x in range(len(objects)):
            if objects[x].id in blacklist:
                temp_index.append(x)
        
        temp_index.sort()
        temp_index.reverse()

        for x in temp_index:   
            del objects[x]
        # END OF REMOVE USED CONCEPT
        dm_fileWriter.write("Previous used concepts "+ str(blacklist) +"\n")
        dm_fileWriter.write("length of choices "+ str(len(objects)) +"\n")

        if len(objects) > 0:
            choice_index = random.randint(0, len(objects))
            subject = objects[choice_index]
      
            ''' CELINA - IDK  DON'T UNCOMMENT
            if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
                subject = world.subject_suggest[1] '''

            #move.dict_nodes[str(curr_blank)] = subject.id
            move.dict_nodes[move.nodes[curr_blank-1]] = subject.id
            used_concept_list[curr_blank-1].append(subject.id)
            subject_suggest_list[curr_blank-1].append(subject)
            
            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
        else:
            dm_fileWriter.write("MOVE BACK \n")
            return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)
    
    elif blank_type == "Character":
        charas = world.get_top_characters(5)

        # DEBUUGING, UNCOMMENT THIS charas = ["dog"]
        if world.continue_suggesting == 1 and world.subject_suggest != None:
            if world.subject_suggest[0] == "Character":
                list_choices = [world.subject_suggest[1]]

        # START OF REMOVE USED CONCEPT 
        temp_index = []
        blacklist = used_concept_list[curr_blank-1] + list(move.dict_nodes.values())
        for x in range(len(charas)):
            if charas[x].id in blacklist:
            #if charas[x] in blacklist:
                temp_index.append(x)
        
        temp_index.sort()
        temp_index.reverse()

        for x in temp_index:   
            del charas[x]
        # END OF REMOVE USED CONCEPT

        dm_fileWriter.write("Previous used concepts "+ str(blacklist) +"\n")
        dm_fileWriter.write("length of choices "+ str(len(charas)) +"\n")
        if len(charas) > 0:
            choice_index = random.randint(0, len(charas))
            subject = charas[choice_index]
            
            # DEBUUGING, COMMENT THIS OUT
            if len(subject.type) > 0:  
                choice_index = random.randint(0, len(subject.type))
                decided_subject = subject.type[choice_index]
                print("SUBJECT TYPE: ", decided_subject)

                move.subject_type_list.append([curr_blank, decided_subject])
            
            ''' CELINA - IDK, DON'T UNCOMMENT THIS
            if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
                subject = world.subject_suggest[1] '''
            
            #move.dict_nodes[str(curr_blank)] = subject.id
            move.dict_nodes[move.nodes[curr_blank-1]] = subject.id
            used_concept_list[curr_blank-1].append(subject.id)
            
            subject_suggest_list[curr_blank-1].append(subject)
            
            ''' DEBUUGING, UNCOMMENT THIS
            #move.dict_nodes[str(curr_blank)] = subject
            move.dict_nodes[move.nodes[curr_blank-1]] = subject
            used_concept_list[curr_blank-1].append(subject)'''

            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
        else:
            dm_fileWriter.write("MOVE BACK \n")
            return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)

    elif blank_type == "Repeat":
        if len(world.event_chain) > 0:
            #move.dict_nodes[str(curr_blank)] = to_sentence_string(world.event_chain[len(world.event_chain)-1])
            move.dict_nodes[move.nodes[curr_blank-1]] = to_sentence_string(world.event_chain[len(world.event_chain)-1])
            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
        else:
            dm_fileWriter.write("MOVE BACK \n")
            return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)
    
    # I'm not using pronouns pa - celina
    elif blank_type == "Pronoun":
        subject = None #object, character
        if subject is None:
            #move.dict_nodes[str(curr_blank)] = "it"
            move.dict_nodes[move.nodes[curr_blank-1]] = "it"
            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
        else:
            if isinstance(subject, Object):
                #move.dict_nodes[str(curr_blank)] = "they"
                move.dict_nodes[move.nodes[curr_blank-1]] = "they"
            elif subject.gender == "":
                #move.dict_nodes[str(curr_blank)] = "they"
                move.dict_nodes[move.nodes[curr_blank-1]] = "they"
            elif subject.gender == "M":
                #move.dict_nodes[str(curr_blank)] = "he"
                move.dict_nodes[move.nodes[curr_blank-1]] = "he"
            elif subject.gender == "F":
                #move.dict_nodes[str(curr_blank)] = "she"
                move.dict_nodes[move.nodes[curr_blank-1]] = "she"
            else:
                #move.dict_nodes[str(curr_blank)] = subject.name
                move.dict_nodes[move.nodes[curr_blank-1]] = subject.name
            dm_fileWriter.write("MOVE FORWARD \n")
            return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)
        
        dm_fileWriter.write("MOVE BACK \n")
        return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)
    
    elif blank_type == "Event":
        loop_back = len(world.event_chain)-1
        loops = 0
        while loop_back >= 0 and loops < 5:
            event = world.event_chain[loop_back]
            
            if event.event_type == FRAME_EVENT:
                if event.action != "":
                    #move.dict_nodes[str(curr_blank)] = get_subject_string(event) + " " + event.action
                    move.dict_nodes[move.nodes[curr_blank-1]] = get_subject_string(event) + " " + event.action
                    dm_fileWriter.write("MOVE FORWARD \n")
                    return fill_up_response(move, world, curr_blank + 1, used_concept_list, subject_suggest_list, False, dm_fileWriter)

            loop_back -= 1
            loops += 1            

        if loop_back == -1 or loops >= 5:
            dm_fileWriter.write("MOVE BACK \n")
            return fill_up_response(move, world, curr_blank - 1, used_concept_list, subject_suggest_list, True, dm_fileWriter)

def node_decider(bin_assertion_template,  dict_nodes, subject_type_list):
    starting_node = bin_assertion_template[0]
    ending_node = bin_assertion_template[2]

    #subject_type_list = [[1, "person"]]

    #print("ASJS", len(subject_type_list))
    result_nodes = []
    if starting_node in dict_nodes.keys() and ending_node in dict_nodes.keys():
        if dict_nodes[starting_node] != "" and dict_nodes[ending_node] != "":
            start = dict_nodes[starting_node]
            end = dict_nodes[ending_node]

            if len(subject_type_list) > 0:
                for x in range(len(subject_type_list)):
                    if int(starting_node) == subject_type_list[x][0]:
                        start = subject_type_list[x][1]
                    elif int(ending_node) == subject_type_list[x][0]:
                        end = subject_type_list[x][1]
            result_nodes.extend(["NODE_BOTH", start, end]) 

        elif dict_nodes[starting_node] != "":
            start = dict_nodes[starting_node]

            if len(subject_type_list) > 0:
                for x in range(len(subject_type_list)):
                    if int(starting_node) == subject_type_list[x][0]:
                        start = subject_type_list[x][1]

            result_nodes.extend(["NODE_START", start])

        elif dict_nodes[ending_node] != "":
            end = dict_nodes[ending_node]

            if len(subject_type_list) > 0:
                for x in range(len(subject_type_list)):
                    if int(ending_node) == subject_type_list[x][0]:
                        end = subject_type_list[x][1]
            result_nodes.extend(["NODE_END", end])

        else:
            #TODO? If not under object or character or item?
            return "NODE_NEITHER" 

    if starting_node not in dict_nodes.keys():
        #this condition is not being used for now
        result_nodes.extend(["NODE_START", starting_node])
        
    # 1 IsA weather    
    elif ending_node not in dict_nodes.keys():
        result_nodes.extend(["NODE_END", ending_node])

    return result_nodes

def feedback_random(type_num):
    if type_num == MOVE_GENERAL_PUMP or type_num == MOVE_SPECIFIC_PUMP or type_num == MOVE_HINT or type_num == MOVE_SUGGESTING:
        return random.randint(0,2)
    else:
        return -1

def combination_response(type_num, world):
    type = -1
    if type_num == MOVE_GENERAL_PUMP:
        type = 11        
    elif type_num == MOVE_SPECIFIC_PUMP:
        type = 12
    elif type_num == MOVE_HINT: 
        type = 13
    elif type_num == MOVE_SUGGESTING:
        type = 14

    world.add_combination_response_type_count(type)

def header_text(move_code, move, world):
    if move_code == MOVE_SUGGESTING:
        move.template.insert(0, "What if ")
        move.template.append("?")
    
    elif move_code == MOVE_HINT:
        elements = ["Then ", "I think ", "Hmm, I think "]
        header = random.choice(elements) 
        move.template.insert(0, header)
        
    ''' CELINA -IDK, DON't UNCOMMENT THIS
    if world.continue_suggesting == 1 and move_code == MOVE_SPECIFIC_PUMP:
        move.template.insert(0, "I don't know much about " + world.subject_suggest[1].name + ". Please help me learn more. ")
        move.template.append("?")'''

def get_dbtype_concept_list(DATABASE_TYPE, world):
    if DATABASE_TYPE == DBO_Concept:
        return world.global_concept_list
    elif DATABASE_TYPE == DBO_Local_Concept:
        return world.local_concept_list

def get_follow_up_string(prev_response):
    temp = []

    temp = DBO_Follow_Up.get_specific_follow_up_template(prev_response.move_id)
    if temp == None:
        return None

    temp.fill_blank_template(prev_response.follow_up_relations, prev_response.dict_nodes)

    return temp

def suggest_again(world, coreferenced_text, dm_fileWriter):
    if world.suggest_continue_count == 3:
        world.suggest_continue_count = 0
        output = Move.Move(template=["I don't know much about " + world.subject_suggest[1].name + ". Please help me learn by telling me more about " + world.subject_suggest[1].name + "."], type_num=MOVE_SPECIFIC_PUMP)
        # DEBUUGING output = Move.Move(template=["I don't know much about " + world.subject_suggest[1] + ". Please help me learn by telling me more about " + world.subject_suggest[1] + "."], type_num=MOVE_SPECIFIC_PUMP)
        # CELINA - IDK, DON'T UNOCOMMENT THIS
        # choice = MOVE_SPECIFIC_PUMP
        # output = generate_response(choice, world, [], coreferenced_text, dm_fileWriter)
                
    else:
        choice = MOVE_SUGGESTING
        output = generate_response(choice, world, [], coreferenced_text, dm_fileWriter)
    
    return output