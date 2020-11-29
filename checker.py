import re

def calculate_profit_rate(filename):
    profit_count = 0
    all_count = 0
    rate_sum = 0
    count = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # --- PROFIT RATE: 1.00 (11/11)
            if line.startswith('--- PROFIT RATE'):
                # print(line)
                ma = re.match('.*: ([\d.]+) \((\d+)/(\d+)\)', line)
                if ma:
                    profit_count += int(ma.group(2))
                    all_count += int(ma.group(3))
                    rate_sum += float(ma.group(1))
                    count += 1
    print("%s %.2f %.2f" % (filename, rate_sum/count, profit_count/all_count))

if __name__ == '__main__':
    calculate_profit_rate('macd-goldcross-check-result')
    calculate_profit_rate('hammer-check-result')
    