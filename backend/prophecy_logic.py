def evolve_prophecy(payouts):
    recent = payouts[-5:] if len(payouts) >= 5 else payouts
    avg = sum(recent) / len(recent) if recent else 0
    if avg > 500:
        return "🔥 Jackpot cycle approaching. Stay locked!"
    elif avg > 100:
        return "💸 Consistent wins. Game is active."
    elif avg > 50:
        return "🌊 Momentum is building. Eyes sharp."
    else:
        return "🧊 Game is cold. Consider changing."
