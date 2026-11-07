1


from typing import Generic, TypeVar, List, Dict

T = TypeVar('T')


class Graph(Generic[T]):
    """Generic Unweighted Directed Graph implementation."""
    def __init__(self):
        self.vertices: Dict[str, T] = {}
        self.adj_list: Dict[str, List[str]] = {}

    def add_vertex(self, node_id: str, data: T) -> bool:
        if node_id in self.vertices:
            return False
        self.vertices[node_id] = data
        self.adj_list[node_id] = []
        return True

    def add_edge(self, u: str, v: str) -> bool:
        if u in self.vertices and v in self.vertices:
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
                return True
        return False

    def remove_edge(self, u: str, v: str) -> bool:
        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[u].remove(v)
            return True
        return False

    def get_prerequisites(self, node_id: str) -> List[str]:
        return [u for u, neighbors in self.adj_list.items() if node_id in neighbors]

    def get_unlocked_courses(self, node_id: str) -> List[str]:
        return self.adj_list.get(node_id, [])


class Course:
    """Course domain entity class."""
    def __init__(self, code: str, name: str, credits: int, level: str):
        self.code = code
        self.name = name
        self.credits = credits
        self.level = level

    def display_info(self, override_visibility: bool = True) -> str:
        if override_visibility or self.level.lower() == 'core':
            return f"[{self.code}] {self.name:<28} | Credits: {self.credits} | Level: {self.level}"
        return f"[{self.code}] {self.name:<28} | [Details Hidden - Elective]"


def setup_sample_graph() -> Graph[Course]:
    g = Graph[Course]()
    courses = [
        Course("CS101", "Introduction to Programming", 3, "Core"),
        Course("CS201", "Data Structures", 4, "Core"),
        Course("CS301", "Algorithms", 4, "Core"),
        Course("CS302", "Database Systems", 3, "Core"),
        Course("CS401", "Software Engineering", 3, "Core"),
        Course("CS405", "Machine Learning Concepts", 3, "Elective")
    ]
    for c in courses:
        g.add_vertex(c.code, c)

    g.add_edge("CS101", "CS201")
    g.add_edge("CS101", "CS301")
    g.add_edge("CS201", "CS301")
    g.add_edge("CS201", "CS302")
    g.add_edge("CS301", "CS401")
    g.add_edge("CS301", "CS405")
    return g


def main():
    graph = setup_sample_graph()

    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. Add Edge On-Demand (Y -> X)")
        print("6. Remove Edge On-Demand (Y -> X)")
        print("7. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\nAvailable Courses:")
            for idx, (code, course) in enumerate(graph.vertices.items(), 1):
                print(f"{idx}. {code} {course.name}")

        elif choice == "2":
            code = input("Enter Course Code: ").strip().upper()
            if code in graph.vertices:
                print(graph.vertices[code].display_info(override_visibility=True))
            else:
                print("Course not found.")

        elif choice == "3":
            code = input("Enter Course Code: ").strip().upper()
            if code in graph.vertices:
                prereqs = graph.get_prerequisites(code)
                print(f"\nPrerequisites for {code}:")
                print("\n".join([f"- {p} ({graph.vertices[p].name})" for p in prereqs]) if prereqs else "- None")
            else:
                print("Course not found.")

        elif choice == "4":
            code = input("Enter Course Code: ").strip().upper()
            if code in graph.vertices:
                unlocked = graph.get_unlocked_courses(code)
                print(f"\nCourses unlocked by {code}:")
                print("\n".join([f"- {u} ({graph.vertices[u].name})" for u in unlocked]) if unlocked else "- None")
            else:
                print("Course not found.")

        elif choice == "5":
            target = input("Enter Target Course (X): ").strip().upper()
            req = input("Enter Prerequisite to Add (Y): ").strip().upper()
            if graph.add_edge(req, target):
                print(f"Edge Added: {req} ---> {target}")
            else:
                print("Failed to add edge.")

        elif choice == "6":
            target = input("Enter Target Course (X): ").strip().upper()
            req = input("Enter Prerequisite to Remove (Y): ").strip().upper()
            if graph.remove_edge(req, target):
                print(f"Edge Removed: {req} -x-> {target}")
            else:
                print("Failed to remove edge.")

        elif choice == "7":
            print("Exiting program. Goodbye!")
            break


if __name__ == "__main__":
    main()