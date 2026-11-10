from dotenv import load_dotenv
load_dotenv()

from router.router import Router, load_examples
from models.local import HANDLERS


# Main entry point for Scrappy CLI
def main():

    # Seed examples come from router/examples.json (the same ones the eval uses).
    # Unsure queries fall back to talk, which stays local.
    router = Router()
    router.add_rules(load_examples())

    # Infinite loop for continuous user interaction
    while True:

        # Get user input query
        query = input("You: ")

        # Exit condition
        if query.lower() in {"exit", "quit"}:
            break

        # Route query to decide which handler runs it (code, talk or refine)
        decision = router.decide(query)
        response = HANDLERS[decision["route"]](query)

        # Output routing decision, why it was made, and the response
        print(f"Route: {decision['route']} ({decision['reason']})")
        print(f"Scrappy: {response}")


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()
