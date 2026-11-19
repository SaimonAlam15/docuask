from sentence_transformers import CrossEncoder


def score(model_name: str, query: str, headings: list[str], content: str):
    model = CrossEncoder(model_name)
    candidate = f"{'\n'.join(headings)}\n\n{content}"
    scores = model.predict([(query, candidate)])
    print(scores)


if __name__ == "__main__":
    score(
        "BAAI/bge-reranker-base",
        "What was the name of the institution from which Saimon Alam got his bachelors degree?",
        [],
        """Degree: B.Sc in C.S.E
Institution: ULAB
Location: Dhaka, Bangladesh
Years: 2011 - 2014""",
    )
