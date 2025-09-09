import argparse, csv
from blockchain import chain_rule, finality_rule
from node import Node
from network import Network
from blockchain import Blockchain
import random

def run_scenario(scenario, seed, rounds, k, base7=None):
    logs = []

    # Scenario 1–6: k = 4, Scenario 7: user chọn base scenario + k tùy chỉnh
    if scenario in [1, 2, 3, 4]:
        k = 4
        scenario_base = scenario
    elif scenario in [5, 6]:
        k = 4
        scenario_base = scenario
    elif scenario == 7:
        if base7 is None or base7 not in range(1, 7):
            raise ValueError("Scenario 7 yêu cầu base scenario từ 1 đến 6")
        scenario_base = base7
        if k is None:
            raise ValueError("Scenario 7 yêu cầu nhập k")
    else:
        raise ValueError("Scenario phải từ 1 đến 7")

    # Tạo nodes và blockchains
    nodes = [Node(i, stake=1) for i in range(5)]
    chains = [Blockchain() for _ in nodes]
    for i, n in enumerate(nodes):
        n.attach_chain(chains[i])

    rng = random.Random(seed)
    network = Network(nodes, drop_rate=0.1, seed=seed)

    for r in range(rounds):
        block = None

        base = scenario_base

        # Partition logic cho scenario 5 và 6
        if base in [5, 6] and 3 <= r <= 5:
            # Nhóm 1: node 0,1; Nhóm 2: node 2,3,4
            group1 = nodes[:2]
            group2 = nodes[2:]
            if base == 5:
                block = nodes[0].mine_block_pow([f"tx{r}"])
            else:
                block = nodes[0].mine_block_hybrid([f"tx{r}"])
            # broadcast trong nhóm
            for n in group1:
                for peer in group1:
                    if peer != n:
                        peer.chain.add_block(block, k)
            for n in group2:
                for peer in group2:
                    if peer != n:
                        peer.chain.add_block(block, k)
        else:
            # Normal scenarios
            if base == 1:
                block = nodes[0].mine_block_pow([f"tx{r}"])
                network.broadcast_block(nodes[0], block)
            elif base == 2:
                block = nodes[0].mine_block_hybrid([f"tx{r}"])
                network.broadcast_block(nodes[0], block)
            elif base == 3:
                block = nodes[0].mine_block_pow([f"tx{r}"])
                if rng.random() > 0.5:
                    network.broadcast_block(nodes[0], block)
            elif base == 4:
                block = nodes[0].mine_block_hybrid([f"tx{r}"])
                if rng.random() > 0.5:
                    network.broadcast_block(nodes[0], block)
            elif base == 5:
                block = nodes[0].mine_block_pow([f"tx{r}"])
                for n in nodes[:len(nodes)//2]:
                    n.chain.add_block(block, k)
            elif base == 6:
                block = nodes[0].mine_block_hybrid([f"tx{r}"])
                for n in nodes[:len(nodes)//2]:
                    n.chain.add_block(block, k)

        # Main chain & finalized
        main_chain = chain_rule([n.chain for n in nodes])
        finalized = finality_rule(main_chain.chain, k) if k else []

        # Ghi log: chain length + finalized + chain từng node
        node_lengths = [len(n.chain.chain) for n in nodes]
        logs.append([
            scenario, seed, rounds, r + 1, len(main_chain), k if k else "", node_lengths
        ])

        # Terminal output
        print(f"[Round {r + 1}] main_chain length={len(main_chain)}, finalized={len(finalized)}")
        for i, n_len in enumerate(node_lengths):
            print(f"   Node {i} chain length={n_len}")

    return logs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=int, default=1, help="Scenario number (1-7)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--rounds", type=int, default=10, help="Số vòng lặp")
    parser.add_argument("--k", type=int, default=None, help="Parameter k (cho finality rule, chỉ dùng scenario 7)")
    parser.add_argument("--base7", type=int, default=None, help="Chọn base scenario 1–6 cho scenario 7")
    args = parser.parse_args()

    logs = run_scenario(args.scenario, args.seed, args.rounds, args.k, args.base7)

    with open("log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["scenario", "seed", "rounds", "round", "block_height", "k", "node_lengths"])
        writer.writerows(logs)

    print(f"Scenario {args.scenario} done.")
