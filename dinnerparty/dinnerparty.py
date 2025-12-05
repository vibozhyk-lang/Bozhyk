import random

# Етап 1: зчитування кількості друзів
num_friends = int(input("Enter the number of friends joining (including you):\n> "))

if num_friends <= 0:
    print("No one is joining for the party")
else:
    print("Enter the name of every friend (including you), each on a new line:")
    friends = {}
    for _ in range(num_friends):
        name = input()
        friends[name] = 0

    # Етап 2: поділ рахунку
    total_amount = float(input("Enter the total amount:\n> "))
    split_amount = round(total_amount / num_friends, 2)
    for friend in friends:
        friends[friend] = split_amount

    # Етап 3: опція "щасливчика"
    use_lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')

    if use_lucky == "Yes":
        lucky_one = random.choice(list(friends.keys()))
        print(f"{lucky_one} is the lucky one!")

        # Етап 4: перерахунок для решти
        split_amount = round(total_amount / (num_friends - 1), 2)
        for friend in friends:
            friends[friend] = 0 if friend == lucky_one else split_amount
    else:
        print("No one is going to be lucky")

    print(friends)