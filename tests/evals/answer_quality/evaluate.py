import asyncio
import json
import os
from pathlib import Path

import httpx

BASE_URL = os.getenv("DOCUASK_BASE_URL", "http://localhost:8000")
DATASET_PATH = Path(__file__).with_name("dataset.jsonl")
RESULTS_PATH = Path(__file__).with_name("results.jsonl")


def load_dataset() -> list[dict]:
    with DATASET_PATH.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


async def evaluate_case(
    client: httpx.AsyncClient,
    case: dict,
) -> dict:
    response = await client.post(
        "/answer",
        json={
            "question": case["question"],
            "conversation_id": None,
        },
    )
    response.raise_for_status()
    payload = response.json()

    return {
        **case,
        "actual_answer": payload.get("answer", ""),
        "sources": payload.get("sources", []),
    }


async def main() -> None:
    cases = load_dataset()
    results = []

    async with httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=120.0,
    ) as client:
        for case in cases:
            try:
                result = await evaluate_case(client, case)
                results.append(result)
                print(f"[OK] {case['id']}")
            except Exception as exc:
                result = {
                    **case,
                    "error": f"{type(exc).__name__}: {exc}",
                }
                results.append(result)
                print(f"[FAIL] {case['id']}: {exc}")

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        for result in results:
            file.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"\nCompleted {len(results)} cases.")
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
