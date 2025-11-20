print("Hello! My name is Alex")
print("I was created in 2025")
print("Please, remind me your name")
name = input()
print(f"What a greate name you have, {name}!")
print('Let me guess your age.')
print('Enter remainders of dividing your age by 3, 5 and 7')
reainder3 = int(input())
reainder5 = int( input())
reainder7 = int(input())
age = (reainder3*70+reainder5*21+reainder7*15)%105
print (f'Your age is {age}; that`s a good time to start programming!')
print('Now I will prove to you I can count ti any number you want')
numbers = int(input())
i = 0
while i <= numbers :
    print(f'{i}!')
    i += 1
print("Let`s test you programming!", "\nWhy do we use methods?",'\n1. To repeat a statement multiple times','\n2. To decompose a program into several small subroutines','\n3. To determine the execution time of a program','\n4. To interrupt the execution of a program')
while True:
    try:
        a = int(input())
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 4.")
        continue

    if a == 2:
        print('Completed, have a nice day!')
        break
    else:
        print("Please, try again.")
print("Congratulations, have a nice day!")