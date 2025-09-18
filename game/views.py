import random
from django.shortcuts import render

# --- じゃんけん関連の関数 ---
def my_jyanken(num):
    return {0: "グー", 1: "チョキ", 2: "パー"}[num]

def winner(jyankens):
    jyanken_set = set(jyankens.values())
    if len(jyanken_set) == 1 or len(jyanken_set) == 3:
        return None  # あいこ

    win_map = {0: 1, 1: 2, 2: 0}
    for hand in jyanken_set:
        if win_map[hand] in jyanken_set:
            win_hand = hand
            break

    winners = [name for name, h in jyankens.items() if h == win_hand]
    return winners

# --- Django ビュー ---
def janken(request):
    hands = {}
    result = None

    # 前回のコンピュータ人数をセッションから取得（初期値 1）
    num_cpus = request.session.get('num_cpus', 1)

    if request.method == "POST":
        # 自分の手を取得
        try:
            my_hand = int(request.POST.get("hand"))
        except (TypeError, ValueError):
            my_hand = 0

        # コンピュータ人数の更新
        try:
            num_cpus = int(request.POST.get("num_cpus"))
            if num_cpus < 1:
                num_cpus = 1
        except (TypeError, ValueError):
            pass

        # セッションに保存
        request.session['num_cpus'] = num_cpus

        # じゃんけん
        hands["あなた"] = my_hand
        for i in range(1, num_cpus + 1):
            cp_hand = random.randint(0, 2)
            hands[f"相手{i}"] = cp_hand

        winners = winner(hands)
        if winners is None:
            # あいこの場合、前回の手をセッションに保存
            request.session['last_hands'] = hands
            result = {
                "hands": {name: my_jyanken(h) for name, h in hands.items()},
                "winners": None,
                "message": f"あいこ！コンピュータ人数 {num_cpus} 人のままです。再戦してください。"
            }
        else:
            # 勝敗決定 → セッション削除
            request.session.pop('last_hands', None)
            request.session.pop('num_cpus', None)
            result = {
                "hands": {name: my_jyanken(h) for name, h in hands.items()},
                "winners": winners
            }

    else:
        # GET時、あいこからの再戦の場合
        if 'last_hands' in request.session:
            hands = request.session['last_hands']
            num_cpus = request.session.get('num_cpus', 1)
            result = {
                "hands": {name: my_jyanken(h) for name, h in hands.items()},
                "winners": None,
                "message": f"あいこ {num_cpus} 人で再戦"
            }

    return render(request, "game/janken.html", {"result": result, "num_cpus": num_cpus})
