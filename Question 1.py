

import time
import random


class Product:
    """Represents a single pharmacy product entity."""
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"ID: {self.product_id} | Name: {self.name:<25} | Price: RM{self.price:<6.2f} | Stock: {self.stock}"


class HashTable:
    """Hash Table using Open Addressing with Linear Probing."""
    DELETED = ("__DELETED__", None)

    def __init__(self, capacity: int = 101):
        self.capacity = capacity
        self.size = 0
        self.slots = [None] * self.capacity

    def hash_function(self, key: int) -> int:
        """Modulo hash function."""
        return key % self.capacity

    def insert(self, key: int, value: object) -> int:
        """Inserts key-value pair using linear probing. Returns slot index."""
        if self.size >= self.capacity:
            raise OverflowError("Hash table capacity full!")

        slot = self.hash_function(key)
        first_deleted = None

        for _ in range(self.capacity):
            # Key update
            if self.slots[slot] is not None and self.slots[slot] != self.DELETED:
                if self.slots[slot][0] == key:
                    self.slots[slot] = (key, value)
                    return slot

            # Record soft-deleted slot to reuse
            if self.slots[slot] == self.DELETED and first_deleted is None:
                first_deleted = slot

            # Slot empty -> break and insert
            if self.slots[slot] is None:
                break

            # Linear Probing step
            slot = (slot + 1) % self.capacity

        target_slot = first_deleted if first_deleted is not None else slot
        self.slots[target_slot] = (key, value)
        self.size += 1
        return target_slot

    def search(self, key: int):
        """Searches key using linear probing. Returns (value, slot_index, probe_count)."""
        slot = self.hash_function(key)
        probes = 0

        for _ in range(self.capacity):
            probes += 1
            if self.slots[slot] is None:
                break
            if self.slots[slot] != self.DELETED and self.slots[slot][0] == key:
                return self.slots[slot][1], slot, probes
            slot = (slot + 1) % self.capacity

        return None, -1, probes


def run_benchmark(num_records: int = 5000):
    """Demonstrates Hash Table vs 1D Array search speed."""
    print("\n" + "=" * 60)
    print(f"  BENCHMARK: Searching among {num_records} items")
    print("=" * 60)

    ht = HashTable(capacity=10007)
    arr = []

    # Insert test dataset
    keys = list(range(1000, 1000 + num_records))
    for k in keys:
        p = Product(k, f"Item-{k}", 10.0, 50)
        ht.insert(k, p)
        arr.append(p)

    target_key = keys[-1]  # Worst-case item at the end of array

    # Hash Table Search Time
    t0 = time.perf_counter()
    ht_res, slot, probes = ht.search(target_key)
    t_ht = time.perf_counter() - t0

    # Array Search Time
    t0 = time.perf_counter()
    arr_res = next((item for item in arr if item.product_id == target_key), None)
    t_arr = time.perf_counter() - t0

    print(f"Target ID: {target_key}")
    print(f"Hash Table Search Time : {t_ht * 1000:.5f} ms (Probes: {probes})")
    print(f"1D Array Search Time   : {t_arr * 1000:.5f} ms")
    if t_ht > 0:
        print(f"Performance Ratio      : Hash Table is {t_arr / t_ht:.1f}x faster!")
    print("=" * 60 + "\n")


def main():
    inventory = HashTable(capacity=101)

    # Pre-populate initial records
    sample_data = [
        Product(1042, "Paracetamol 500mg", 5.90, 120),
        Product(1088, "Amoxicillin 250mg", 14.50, 45),
        Product(2015, "Ibuprofen 400mg", 8.20, 80)
    ]
    for p in sample_data:
        inventory.insert(p.product_id, p)

    while True:
        print("\n=== Pharmacy Inventory System ===")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Run Performance Benchmark")
        print("4. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                p_id = int(input("Enter Product ID: "))
                name = input("Enter Product Name: ")
                price = float(input("Enter Price: "))
                stock = int(input("Enter Stock Quantity: "))
                slot = inventory.insert(p_id, Product(p_id, name, price, stock))
                print(f"Product inserted successfully into slot [{slot}]")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            try:
                p_id = int(input("Enter Product ID to search: "))
                t0 = time.perf_counter()
                res, slot, probes = inventory.search(p_id)
                t_ht = time.perf_counter() - t0

                # Array search for direct timing comparison
                arr = [pair[1] for pair in inventory.slots if pair and pair != HashTable.DELETED]
                t1 = time.perf_counter()
                arr_res = next((x for x in arr if x.product_id == p_id), None)
                t_arr = time.perf_counter() - t1

                if res:
                    print("\nProduct Found!")
                    print(f"Stock: {res.stock}")
                    print(f"ID: {res.product_id} Name: {res.name} | Price: RM{res.price:.2f}")
                    print(f"Search completed in {t_ht:.6f} seconds (Hash Table)")
                    print(f"Search completed in {t_arr:.6f} seconds (Array same record)")
                else:
                    print("Product not found.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            run_benchmark()

        elif choice == "4":
            print("Exiting Inventory System. Goodbye!")
            break


if __name__ == "__main__":
    main()