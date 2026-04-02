# First Draft for basic simplicity checking

def check_simple(query: str) -> bool:

    # Check 1 Common Simple words  
    simple_keywords = {"hello", "hi", "thanks", "bye"}

    tokens = set(query.lower().split())

    if(tokens & simple_keywords):
        return True
    
    # Check 2 Query Length
    if (len(query)<50):
        return True
    
    return False


def route_query(query: str)-> str:
    if check_simple(query):
        return "local"
    return "remote"

