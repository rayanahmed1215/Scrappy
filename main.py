from dotenv import load_dotenv
load_dotenv()

from router.router import Router
from models.local import run_local_model
from models.remote import run_remote_model


# Main entry point for Scrappy CLI
def main():

    # Infinite loop for continuous user interaction
    while True:

        # Get user input query
        query = input("You: ")

        # Exit condition
        if query.lower() in {"exit", "quit"}:
            break

        # Route query to decide which model to use (local or remote)
        route = Router().route(query)

        # Run model based on routing decision
        if route == "local":
            response = run_local_model(query)
        else:
            response = run_remote_model(query)

        # Output routing decision + model response
        print(f"Route: {route}")
        print(f"Scrappy: {response}")


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()