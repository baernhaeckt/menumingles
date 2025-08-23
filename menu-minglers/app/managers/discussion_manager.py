
import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinySocialNetwork, TinyWorld
from tinytroupe.extraction import ResultsExtractor
from tinytroupe.factory import TinyPersonFactory


class DiscussionManager:

    def __init__(self):
        pass

    def discuss_topic(self, world_name: str, situation: str, topic: str, people: list[dict], initiator: dict, extraction_objective: str, turns: int = None) -> str:

        if turns is None:
            turns = len(people) + 1

        persons = [TinyPerson(person) for person in people]
        initiator = TinyPerson(initiator)

        persons.append(initiator)

        world = TinyWorld(world_name, persons)
        world.make_everyone_accessible()

        initiator.listen(topic)

        world.run(turns)

        extractor = ResultsExtractor()
        results = extractor.extract_results_from_agent(
            initiator,
            extraction_objective=extraction_objective,
            situation=situation
        )

        return results
