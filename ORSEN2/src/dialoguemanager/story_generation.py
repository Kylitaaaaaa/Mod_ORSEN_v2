import inflect
from src.objects.eventchain.EventFrame import FRAME_DESCRIPTIVE, FRAME_EVENT, FRAME_CREATION, EventFrame
from src.objects.storyworld.Character import Character
inflect_engine = inflect.engine()


def generate_basic_story(world):
    final_story = ""
    for event in world.event_chain:
        final_story += to_sentence_string(event) + " "
    return final_story


def generate_collated_story(world):
    chain_index = 0
    event_chain = world.event_chain
    final_story = ""

    while chain_index < len(event_chain):
        default = False
        current_event = event_chain[chain_index]
        if chain_index == len(event_chain) - 1:
            next_event = None
        else:
            next_event = event_chain[chain_index+1]

        if next_event is not None:
            current_string = to_sentence_string(current_event)
            next_string = to_sentence_string(next_event)

            if current_event.subject == next_event.subject:
                if current_event.event_type == FRAME_EVENT and next_event.event_type == FRAME_EVENT:
                    pronoun = get_possible_pronoun(current_event, next_event, world)

                    if pronoun is not None:
                        next_string.replace(get_subject_string(current_event), pronoun)

                    final_story += current_string + ", then " + next_string
                    chain_index += 1

                elif current_event.event_type == FRAME_DESCRIPTIVE and next_event.event_type == FRAME_DESCRIPTIVE:
                    combined_frame = EventFrame(-1, FRAME_DESCRIPTIVE)
                    combined_frame.subject = current_event.subject
                    combined_frame.attributes = current_event.attributes + next_event.attributes

                    final_story += to_sentence_string(combined_frame)
                    final_story += ". "
                    chain_index += 1
                else:
                    default = True
            else:
                default = True
        else:
            default = True

        if default:
            final_story += to_sentence_string(current_event)
            final_story += ". "

        chain_index += 1

    return final_story


def to_sentence_string(event):
    string = ""
    verb_string = ""
    subject_string = get_subject_string(event)

    if len(event.subject) > 1 or (inflect_engine.singular_noun(event.subject[0]) is True):
        verb_string += " were "
    else:
        verb_string += " was "

    if event.event_type == FRAME_EVENT:
        string = subject_string + " " + str(event.action) + " "

        ido_names = []
        for item in event.indirect_object:
            ido_names.append(item)
        string += (inflect_engine.join(tuple(ido_names)) + " ")

        do_names = []
        for item in event.direct_object:
            do_names.append(item)
        string += inflect_engine.join(tuple(do_names))

        if event.preposition != "":
            string += " " + str(event.preposition) + " " + str(event.obj_of_preposition)

    else:
        attr_string = inflect_engine.join(tuple(event.attributes))

        if event.event_type == FRAME_DESCRIPTIVE:
            string = subject_string + verb_string + attr_string
        elif event.event_type == FRAME_CREATION:
            article = ""
            if inflect_engine.singular_noun(event.subject[0]) is False:
                article = inflect_engine.a(event.subject[0])
            if len(article.split()) > 0:
                article_string = article.split()[0]
            else:
                article_string = ""
            string = "There" + verb_string + article_string + " " + attr_string + " " + subject_string

    return string


def get_subject_string(event):
    subject_names = []
    for item in event.subject:
        subject_names.append(item)
    return inflect_engine.join(tuple(subject_names))


def get_possible_pronoun(current_event, next_event, world):
    subject = current_event.get_subject(0, world)
    if len(current_event.subject) > 1 or (inflect_engine.singular_noun(current_event.subject[0]) is True):
        return "they"
    elif isinstance(subject, Character) and subject.gender is not None and subject.gender != "":
        gender = subject.gender
        if gender == "F":
            return "she"
        elif gender == "M":
            return "he"
        else:
            return None
    else:
        return None
