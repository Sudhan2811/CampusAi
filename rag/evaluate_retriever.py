
from rag.retriever import Retriever


def main():

    retriever = Retriever()
    retriever.load()

    test_cases = [
        {
            "question": "When does B.Tech registration start?",
            "expected": ["7th august 2026", "01:00 pm"],
            "answerable": True
        },
        {
            "question": "Which portals are required for registration?",
            "expected": [
                "nitsriadmission.samarth.edu.in",
                "gaasherp.nitsri.ac.in"
            ],
            "answerable": True
        },
        {
            "question": "What photograph is required?",
            "expected": ["passport-size photograph", "blue or white"],
            "answerable": True
        },
        {
            "question": "What is the contact email for registration issues?",
            "expected": ["teamerp@nitsri.ac.in"],
            "answerable": True
        },
        {
            "question": "What is the hostel mess fee?",
            "expected": ["hostel mess fee"],
            "answerable": False
        },
        {
            "question": "Who is the director of NIT Srinagar?",
            "expected": ["director of nit srinagar"],
            "answerable": False
        }
    ]

    total = len(test_cases)
    evidence_found = 0
    answerable_total = 0
    answerable_found = 0
    unanswerable_total = 0
    unanswerable_without_evidence = 0

    print("\n===== RAG EVIDENCE EVALUATION =====")

    for test in test_cases:

        results = retriever.search(
            test["question"],
            top_k=3
        )

        # Use the same combined-context approach as rag_pipeline.py
        context = "\n\n".join(
            result["chunk"] for result in results
        ).lower()

        # Check whether every expected phrase appears
        # in the combined retrieved context.
        found = all(
            phrase.lower() in context
            for phrase in test["expected"]
        )

        if found:
            evidence_found += 1

        if test["answerable"]:
            answerable_total += 1
            if found:
                answerable_found += 1
        else:
            unanswerable_total += 1
            if not found:
                unanswerable_without_evidence += 1

        print(f"\nQuestion: {test['question']}")
        print(f"Expected answerable: {test['answerable']}")
        print(f"Evidence found in top 3: {found}")

        if results:
            print(
                f"Top similarity: {results[0]['score']:.4f}"
            )
            print(
                f"Retrieved chunks: {len(results)}"
            )
        else:
            print("Retrieved chunks: 0")

    print("\n===== SUMMARY =====")
    print(f"Total test questions: {total}")
    print(
        f"Evidence found overall: {evidence_found}/{total}"
    )
    print(
        f"Answerable evidence coverage: "
        f"{answerable_found}/{answerable_total}"
    )
    print(
        f"Unanswerable questions without expected evidence: "
        f"{unanswerable_without_evidence}/{unanswerable_total}"
    )

    print(
        "\nNote: This is a small keyword-based test. "
        "It evaluates retrieval evidence, not the truthfulness "
        "of Nova's generated answers."
    )


if __name__ == "__main__":
    main()
