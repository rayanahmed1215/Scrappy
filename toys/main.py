from router import route_query
from models.local import run_local_model
from models.remote import run_remote_model


def main():
    while True:
        query = input("You: ")

        if query.lower() in {"exit", "quit"}:
            break

        route = route_query(query)

        if route == "local":
            response = run_local_model(query)
        else:
            response = run_remote_model(query)

        print(f"Route: {route}")
        print(f"Scrappy: {response}")


if __name__ == "__main__":
    main()