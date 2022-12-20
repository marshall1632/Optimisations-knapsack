import sys

from DeliveryECproblem import DeliveryProblem

Name = []
kg = []
value = []
max = []

def run_assignment(filepath):
    try:
        boxes = []
        with open(filepath) as file:
            temp = file.readline()
            while temp != '***\n':
                temp = file.readline()
            capacity = int(file.readline())
            max.append(capacity)
            quota = int(file.readline())
            number_objects = int(file.readline())
            lines = file.readlines()
            count = 1
            for line in range(len(lines)):
                if lines[line] == "***\n":
                    print("\n*******************Problem number : ", count, "*******************\n")
                    run_evolution(number_objects, boxes, capacity, quota)
                    count += 1
                    continue
                s = lines[line].split()
                if len(s) == 3:
                    col = s[0].strip()
                    col2 = int(s[1].strip())
                    col3 = int(s[2].strip())
                    Name.append(col)
                    kg.append(col2)
                    value.append(col3)
            print(Name)
            print(kg)
            print(value)
            print(max)
            print("\n*******************Problem number : ", count, "*******************\n")
            run_evolution(number_objects=number_objects, boxes=boxes, capacity=capacity, quota=quota)
    except FileNotFoundError:
        print("The file does not exist\n")
        input("Press enter to exit-- ")
        sys.exit()




def solution(genome1, boxes):
    print("<------ Solution -------->")
    total_weight = 0
    total_value = 0
    subset = "{ "
    for j in range(len(genome1)):
        if genome1[j] != 0:
            total_weight += int(boxes[j][1])
            total_value += int(boxes[j][2])
            subset += boxes[j][0] + " "
    print("Solution set : ", subset + "}", "\nTotal Weight : ", total_weight, "\nTotal Value : ", total_value)


def display_boxes(boxes, weight_limit, value):
    print("<------ Items ------>")
    print("Name\tWeight\tValue")
    for row in range(len(boxes)):
        print(boxes[row][0] + "\t", boxes[row][1], "\t", boxes[row][2].strip())
    print("Capacity : ", weight_limit, "\nQuota : ", value, "\n")


def run_evolution(number_objects, boxes, capacity, quota):
    problem = DeliveryProblem(number_objects=number_objects, boxes=boxes, quota=quota, capacity=capacity)
    population = problem.generate_population()
    results = problem.run_evolution(population=population)
    fittest_individual = results[0]
    display_boxes(boxes=boxes, weight_limit=capacity, value=quota)
    solution(fittest_individual, boxes)
    print("Found in generation : ", results[1], "\n")


if __name__ == '__main__':
    while True:
        file_name = input("Please enter file path and name : ")
        print()
        run_assignment(filepath=file_name)
        check = input("Do you want to continue (y|n) : ")
        if check != 'Y' and check != 'y':
            break
        print()
    input("Press enter to exit-- ")
