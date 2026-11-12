from core.llm.output_parser import (
    OutputParser
)

response = """

The report indicates right lower lobe pneumonia.



Azithromycin is prescribed
to treat the infection.




Follow-up after 7 days.


"""

parsed = OutputParser.parse(
    response
)

print(parsed)