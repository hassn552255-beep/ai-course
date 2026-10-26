from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


def basics(*people):
    """Every person is a knight or a knave, never both."""
    rules = And()
    for knight, knave in people:
        rules.add(Or(knight, knave))
        rules.add(Not(And(knight, knave)))
    return rules


def says(knight, knave, statement):
    """A knight's statement is true; a knave's statement is false."""
    return And(
        Implication(knight, statement),
        Implication(knave, Not(statement))
    )


# Puzzle 0: A says "I am both a knight and a knave."
knowledge0 = And(
    basics((AKnight, AKnave)),
    says(AKnight, AKnave, And(AKnight, AKnave))
)

# Puzzle 1: A says "We are both knaves." B says nothing.
knowledge1 = And(
    basics((AKnight, AKnave), (BKnight, BKnave)),
    says(AKnight, AKnave, And(AKnave, BKnave))
)

# Puzzle 2: A says "We are the same kind." B says "We are of different kinds."
same = Or(And(AKnight, BKnight), And(AKnave, BKnave))
different = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    basics((AKnight, AKnave), (BKnight, BKnave)),
    says(AKnight, AKnave, same),
    says(BKnight, BKnave, different)
)

# Puzzle 3 (Bonus): A says either "I am a knight." or "I am a knave.",
# but we don't know which. B says "A said 'I am a knave'."
# B also says "C is a knave." C says "A is a knight."
#
# "A said X" is encoded as: A's saying X is consistent with A's type,
# i.e. (A is a knight) <=> X.
a_said_knight = Biconditional(AKnight, AKnight)   # X = "I am a knight"
a_said_knave = Biconditional(AKnight, AKnave)     # X = "I am a knave"
knowledge3 = And(
    basics((AKnight, AKnave), (BKnight, BKnave), (CKnight, CKnave)),
    Or(a_said_knight, a_said_knave),              # A said one of the two
    says(BKnight, BKnave, a_said_knave),          # B: "A said 'I am a knave'"
    says(BKnight, BKnave, CKnave),                # B: "C is a knave"
    says(CKnight, CKnave, AKnight)                # C: "A is a knight"
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3 (Bonus)", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()