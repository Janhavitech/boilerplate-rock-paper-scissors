from collections import deque

BEAT = {"R": "P", "P": "S", "S": "R"}   # BEAT[x] = the move that beats x


def player(prev_play, state={}):
    # A new game starts when prev_play is "": reset everything
    if prev_play == "":
        state.clear()
        state["me"] = []                       # my moves so far
        state["abbey_seen"] = ["R"]            # abbey stores a first "R"
        state["pairs"] = {a + b: 0 for a in "RPS" for b in "RPS"}
        state["preds"] = None                  # predictions made last round
        state["window"] = {n: deque(maxlen=25)
                           for n in ("quincy", "kris", "mrugesh", "abbey")}

    me = state["me"]
    t = len(me)

    # 1. Check last round's predictions against what the opponent really did
    if state["preds"] is not None:
        for name, predicted in state["preds"].items():
            state["window"][name].append(predicted == prev_play)

    # 2. Predict the opponent's next move with each bot's own rule
    last = me[-1] if me else "R"

    mr_seen = [""] + me
    last_ten = mr_seen[-10:]
    mr_best = max(["R", "P", "S", ""], key=last_ten.count)
    if mr_best == "":
        mr_best = "S"

    options = {k: state["pairs"][k] for k in (last + "R", last + "P", last + "S")}
    abbey_guess = max(options, key=options.get)[-1]

    preds = {
        "quincy": ["R", "R", "P", "P", "S"][(t + 1) % 5],
        "kris": BEAT[last],
        "mrugesh": BEAT[mr_best],
        "abbey": BEAT[abbey_guess],
    }
    state["preds"] = preds

    # 3. Pick the bot whose predictions have been right most often, then beat it
    if t < 3:
        guess = "P"
    else:
        scores = {n: sum(state["window"][n]) for n in preds}
        best = max(scores, key=scores.get)
        guess = BEAT[preds[best]]

    # 4. Remember my move (abbey counts pairs of my moves)
    me.append(guess)
    state["abbey_seen"].append(guess)
    seen = state["abbey_seen"]
    state["pairs"][seen[-2] + seen[-1]] += 1
    return guess