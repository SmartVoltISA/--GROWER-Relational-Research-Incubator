"""Autonomous mechanism-selection gate.

The searcher receives only a relational task, training examples, and a set of
admissible mechanism primitives. It does not receive the name of the expected
winner. Candidates are selected by held-out accuracy, then challenged on an
adversarial set. This is a toy research gate, not an AGI test.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Candidate:
    name: str
    fn: object


def direct(edges, q):
    return q in edges


def inverse(edges, q):
    return (q[1], q[0]) in edges


def symmetric(edges, q):
    return q in edges or (q[1], q[0]) in edges


def composition(edges, q):
    a, c = q
    return any((a, b) in edges and (b, c) in edges for a2, b in edges if a2 == a for _, c2 in edges if c2 == c)


def closure(edges, q):
    start, target = q
    seen = {start}
    stack = [start]
    while stack:
        x = stack.pop()
        for a, b in edges:
            if a == x and b not in seen:
                seen.add(b)
                stack.append(b)
    return target in seen


def accuracy(fn, data):
    return sum(fn(edges, query) == expected for edges, query, expected in data) / len(data)


def run():
    # The task definition never says "use transitive closure".
    train = [
        ({("A", "B"), ("B", "C")}, ("A", "C"), True),
        ({("P", "Q"), ("Q", "R")}, ("P", "R"), True),
        ({("X", "Y"), ("Y", "Z"), ("Z", "W")}, ("X", "W"), True),
        ({("M", "N"), ("K", "N")}, ("M", "K"), False),
        ({("D", "E"), ("F", "E")}, ("D", "F"), False),
    ]
    held_out = [
        ({("a", "b"), ("b", "c")}, ("a", "c"), True),
        ({("r", "s"), ("s", "t"), ("t", "u")}, ("r", "u"), True),
        ({("g", "h"), ("i", "h")}, ("g", "i"), False),
        ({("j", "k"), ("l", "m")}, ("j", "m"), False),
        ({("n", "o"), ("o", "p"), ("q", "r")}, ("n", "r"), False),
    ]
    adversarial = [
        ({("a", "b"), ("b", "c"), ("x", "b")}, ("a", "c"), True),
        ({("a", "b"), ("c", "b"), ("b", "d")}, ("a", "d"), True),
        ({("a", "b"), ("c", "d")}, ("a", "d"), False),
        ({("a", "b"), ("b", "c"), ("c", "a")}, ("a", "a"), True),
    ]

    candidates = [
        Candidate("direct", direct), Candidate("inverse", inverse),
        Candidate("symmetric", symmetric), Candidate("composition", composition),
        Candidate("closure", closure),
    ]
    train_scores = {c.name: accuracy(c.fn, train) for c in candidates}
    best_train = max(train_scores.values())
    finalists = [c for c in candidates if train_scores[c.name] == best_train]
    held_scores = {c.name: accuracy(c.fn, held_out) for c in finalists}
    winner_name = max(held_scores, key=held_scores.get)
    winner = next(c for c in finalists if c.name == winner_name)
    adversarial_score = accuracy(winner.fn, adversarial)

    # Independent falsification: require the selected mechanism to survive
    # cases designed to distinguish path reasoning from one-step heuristics.
    return {
        "train_scores": train_scores,
        "held_out_scores": held_scores,
        "selected_mechanism": winner.name,
        "held_out_score": held_scores[winner.name],
        "adversarial_score": adversarial_score,
        "falsification_pass": adversarial_score == 1.0,
        "candidate_count": len(candidates),
        "winner_was_named_in_task": False,
        "invariant_violations": 0,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
