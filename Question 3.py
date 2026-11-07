
import time
import threading


def fibonacci(n: int) -> int:
    """Calculates nth Fibonacci number using naive recursion O(2^n)."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def run_multithreaded_round(targets: list) -> tuple:
    """Runs Fibonacci targets on separate threads and measures elapsed time."""
    threads = []
    results = {}
    timestamps = []

    def worker(idx, val):
        t_start = time.perf_counter_ns()
        res = fibonacci(val)
        t_end = time.perf_counter_ns()
        results[idx] = (val, res)
        timestamps.append((t_start, t_end))

    for idx, n in enumerate(targets):
        t = threading.Thread(target=worker, args=(idx, n))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    t1 = min(ts[0] for ts in timestamps)
    t2 = max(ts[1] for ts in timestamps)
    elapsed_ns = t2 - t1

    formatted_str = ", ".join([f"Fib({results[i][0]})-{results[i][1]}" for i in range(len(targets))])
    return elapsed_ns, f"{formatted_str} | T {elapsed_ns:,} ns"


def run_sequential_round(targets: list) -> tuple:
    """Runs Fibonacci targets sequentially in a single main thread."""
    t_start = time.perf_counter_ns()
    results = [(n, fibonacci(n)) for n in targets]
    t_end = time.perf_counter_ns()

    elapsed_ns = t_end - t_start
    formatted_str = ", ".join([f"Fib({n})-{val}" for n, val in results])
    return elapsed_ns, f"{formatted_str} | T {elapsed_ns:,} ns"


def main():
    targets = [35, 38, 40]
    rounds = 10

    print("=== Fibonacci Computation (With Multithreading) ===")
    mt_times = []
    for r in range(1, rounds + 1):
        ns, line = run_multithreaded_round(targets)
        mt_times.append(ns)
        print(f"Round {r:<2}: {line}")

    avg_mt = sum(mt_times) / rounds
    print(f"Average T (With Multithreading): {avg_mt:,.0f} ns\n")

    print("=== Fibonacci Computation (Without Multithreading) ===")
    seq_times = []
    for r in range(1, rounds + 1):
        ns, line = run_sequential_round(targets)
        seq_times.append(ns)
        print(f"Round {r:<2}: {line}")

    avg_seq = sum(seq_times) / rounds
    print(f"Average T (Without Multithreading): {avg_seq:,.0f} ns\n")

if __name__ == "__main__":
    main()