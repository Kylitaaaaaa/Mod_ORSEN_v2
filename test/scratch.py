from src.dataprocessor import Annotator

annotator = Annotator()
annotator.annotate("Today I don't feel like doing anything.")

annotator.get_annotated()