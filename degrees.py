import csv
import sys

from util import Node, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            key = row["name"].lower()
            if key not in names:
                names[key] = {row["id"]}
            else:
                names[key].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target using BFS.
    """

    # Edge case
    if source == target:
        return []

    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()

    while not frontier.empty():
        node = frontier.remove()
        explored.add(node.state)

        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id in explored or frontier.contains_state(person_id):
                continue

            child = Node(
                state=person_id,
                parent=node,
                action=(movie_id, person_id)
            )

            # Goal check
            if person_id == target:
                path = []
                while child.parent is not None:
                    path.append(child.action)
                    child = child.parent
                path.reverse()
                return path

            frontier.add(child)

    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))

    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for pid in person_ids:
            person = people[pid]
            print(f"ID: {pid}, Name: {person['name']}, Birth: {person['birth']}")
        pid = input("Intended Person ID: ")
        if pid in person_ids:
            return pid
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    neighbors = set()
    for movie_id in people[person_id]["movies"]:
        for pid in movies[movie_id]["stars"]:
            neighbors.add((movie_id, pid))
    return neighbors


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")

    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
        return

    print(f"{len(path)} degrees of separation.")
    path = [(None, source)] + path

    for i in range(len(path) - 1):
        person1 = people[path[i][1]]["name"]
        person2 = people[path[i + 1][1]]["name"]
        movie = movies[path[i + 1][0]]["title"]
        print(f"{i + 1}: {person1} and {person2} starred in {movie}")


if __name__ == "__main__":
    main()
