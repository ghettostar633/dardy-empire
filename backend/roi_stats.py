import sqlite3

def get_roi():
    conn = sqlite3.connect("sniper_memory.db")
    cur = conn.cursor()
    cur.execute("SELECT payout FROM sniper_log")
    payouts = []
    for row in cur.fetchall():
        try:
            value = float(row[0].replace("Won", "").replace("$", "").strip())
            payouts.append(value)
        except:
            continue
    conn.close()
    total = sum(payouts)
    count = len(payouts)
    avg = total / count if count else 0
    print(f"Total Payout: {total}, Entries: {count}, Average: {avg:.2f}")
    return total, count, avg

if __name__ == "__main__":
    get_roi()
