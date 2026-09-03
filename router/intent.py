class intentClassify:

    def classify_intent(self, query: str) -> str:

        rules = {
            "math": ["calculate", "compute", "solve", "equation", "+", "-", "*", "/"],
            "command": ["run", "execute", "do", "build", "create"],
            "ask": ["what", "why", "how", "when", "where", "question"],
            "chat": ["talk", "chat", "discuss", "tell me"],
        }

        scores = {k: 0 for k in rules}

        for intent, keywords in rules.items():
            for keyword in keywords:
                if keyword in query.lower():
                    scores[intent] += 1

        best_intent = max(scores, key=scores.get)

        if scores[best_intent] == 0:
            return "unknown"
        
        return best_intent
