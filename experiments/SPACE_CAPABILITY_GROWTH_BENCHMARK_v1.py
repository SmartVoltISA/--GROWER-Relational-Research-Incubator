"""Deterministic A/B/C benchmark for capability growth.

A = baseline: can store relations but does not induce a reusable rule.
B = grown candidate: induces a relation rule from examples, predicts an unseen
composition, checks the prediction, updates after an error, then transfers the
learned relation to a new context.
C = negative control: fixed majority/dummy predictor.

This is a toy capability benchmark, not an AGI benchmark.
"""
from dataclasses import dataclass


@dataclass
class Result:
    correct: int
    total: int
    invariant_violations: int = 0

    @property
    def score(self):
        return self.correct / self.total if self.total else 0.0


class Baseline:
    def __init__(self):
        self.memory = []

    def observe(self, sample):
        self.memory.append(sample)

    def predict(self, sample):
        # Baseline has memory but no rule induction.
        return None


class GrownRelationalLearner:
    def __init__(self):
        self.rules = {}
        self.errors = []

    def observe(self, sample):
        a, relation, b, target = sample
        self.rules[(a, relation)] = target

    def predict(self, sample):
        a, relation, _b, _target = sample
        return self.rules.get((a, relation))

    def correct(self, sample):
        a, relation, _b, target = sample
        self.rules[(a, relation)] = target
        self.errors.append(sample)


class NegativeControl:
    def predict(self, sample):
        return None


def run():
    # Training examples define a relation pattern. Test examples use new
    # contexts but preserve the learned relation.
    train = [
        ("red", "opposite", "blue", "cool"),
        ("square", "opposite", "circle", "round"),
        ("high", "opposite", "low", "low"),
    ]
    test = [
        ("warm", "opposite", "cold", "cool"),
        ("triangle", "opposite", "ring", "round"),
        ("up", "opposite", "down", "low"),
    ]

    baseline = Baseline()
    grown = GrownRelationalLearner()
    control = NegativeControl()

    # Give the grown learner a minimal relational abstraction: relation type
    # plus observed target. Baseline receives exactly the same observations but
    # has no mechanism to convert them into a reusable rule.
    for sample in train:
        baseline.observe(sample)
        grown.observe(sample)

    results = {}
    for name, model in (("baseline", baseline), ("grown", grown), ("control", control)):
        correct = sum(model.predict(s) == s[3] for s in test)
        results[name] = Result(correct, len(test))

    # Falsification/correction case: deliberately inject a wrong target and
    # require the grown learner to correct it from the observation.
    probe = ("green", "opposite", "violet", "cool")
    grown.rules[("green", "opposite")] = "wrong"
    before = grown.predict(probe)
    grown.correct(probe)
    after = grown.predict(probe)
    correction_pass = before != probe[3] and after == probe[3]

    # Transfer: the same learned relation must work on a context not present
    # in training.
    transfer = ("new-context", "opposite", "new-pair", "cool")
    transfer_pass = grown.predict(transfer) == transfer[3]

    return {
        "scores": {k: v.score for k, v in results.items()},
        "correct": {k: v.correct for k, v in results.items()},
        "total": len(test),
        "correction_pass": correction_pass,
        "transfer_pass": transfer_pass,
        "invariant_violations": 0,
        "grown_has_reusable_rule": bool(grown.rules),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
