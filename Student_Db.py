#Author: Saman Kashanchi
#Student ID: 2301023
#Assignment3 Database

import sqlite3
import pandas as pd
from pandas import DataFrame

#connecting to the database
conn = sqlite3.connect('StudentDb.db')
mycursor = conn.cursor()

# a.Write a python function to importthe students.csvfile
# into your newly created Students table
def InsertCsvData():
    mycursor.execute('DELETE FROM Students')
    with open("students.csv") as inputFile:
        title = 0
        for line in inputFile:
            if title == 0:
                title += 1
                continue
            else:
                fillings = line.split(",")
                fillings.append(title)
                mycursor.execute('INSERT INTO Students(FirstName,LastName,Address,City,State,ZipCode,MobilePhoneNumber,Major,GPA,StudentID) VALUES(?,?,?,?,?,?,?,?,?,?)',fillings)
                conn.commit()
                fillings.clear()
                title += 1



#The UI of the program(MENU)
def Menu():
    while True:
        print("\n")
        print("---------------------- MENU ---------------------- ")
        print("1. Display all students and their records.")
        print("2. Add a new student.")
        print("3. Update a students information.")
        print("4. Delete a Student")
        print("5. Search/Display students by Major, GPA, City, State or Advisor.")
        print("6. Exit Program")
        choice = input("Enter the number of the option you would like to execute: ")
        if choice == "1":
            print("\n")
            displayStudents()
        elif choice == "2":
            print("\n")
            addStudent()
        elif choice == "3":
            print("\n")
            updateStudent()
        elif choice == "4":
            print("\n")
            deleteStudent()
        elif choice == "5":
            print("\n")
            searchStudent()
        elif choice == "6":
            print("\n")
            print("Exiting....")
            conn.commit()
            break
        else:
            print("\n")
            print("Invalid input. Try Again.")
            print("\n")
            continue

# b.DisplayAll Students and all of their attributes.
# i.Create the necessary SELECT statement to produce this output
def displayStudents():
    mycursor.execute('SELECT * FROM Students')
    Data = mycursor.fetchall()
    df = DataFrame(Data, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
    print(df)

# c.Add NewStudents
def addStudent():

    newFirstName = input("First Name of the Student: ")
    newLastName = input("Last Name of the Student: ")
    #ERROR Check for GPA entry
    while True:
        try:
            newGPA = float(input("GPA of the Student as decimal: "))
            break
        except ValueError:
            print("Try again please use decimal format")
    newMajor = input("Major: ")
    newFacultyAdvisor = input("Faculty Advisor: ")
    newAddress = input("Address: ")
    newCity = input("City: ")
    newState = input("State: ")

    #ERROR Check for ZipCode entry
    while True:
        try:
            newZipCode = int(input("ZipCode: "))
            break
        except ValueError:
            print("Try again with 5 digits: ")
    #ERROR Check for PhoneNumber entry
    while True:
        try:
            newPhoneNumber = input("Mobile Phone Number: ")
            break
        except ValueError:
            print("Try again with only digits: ")

    nStudentID = mycursor.execute('SELECT StudentId from Students where StudentId = (SELECT max(StudentId) from Students) ').fetchall()
    df = pd.DataFrame(nStudentID)
    newId = df[0][0]
    newId = int(newId)+1

    mycursor.execute('INSERT INTO Students(StudentID,FirstName,LastName,GPA,Major,FacultyAdvisor,Address,City,State,ZipCode,MobilePhoneNumber,isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (newId,newFirstName,newLastName,newGPA,newMajor,newFacultyAdvisor,newAddress,newCity,newState,newZipCode,newPhoneNumber,0))
    conn.commit()
    print("Added student successfully.")

# d.Update Students
def updateStudent():
    nSID = input("ID of the student you would like to update: ")
    mycursor.execute('SELECT * FROM Students WHERE StudentID = ?', (nSID,))
    output = mycursor.fetchall()
    #ERROR CHECK TO MAKE SURE STUDENT EXISTS
    if output == []:
        print("Invalid Input. Please Try Again.")
        updateStudent()
    else:
        print("The following are available to update:")
        print("1. Major")
        print("2. Advisor")
        print("3. Mobile Number")
        choice = input("Press b if you wish to go back to menu.\nEnter the number of the attribute you would like to alter: ")
        if choice == 'b':
            Menu()
            quit()
        if choice == "1":
            newMajor = input("Students New Major: ")
            mycursor.execute('UPDATE Students SET Major = ? WHERE studentID = ?', (newMajor,nSID))
            conn.commit()
            print("Information Successfully Updated")
        elif choice == "2":
            newAdvisor = input("Students New Faculty Advisor: ")
            mycursor.execute('UPDATE Students SET FacultyAdvisor = ? WHERE studentID = ?', (newAdvisor,nSID))
            conn.commit()
            print("Updated Information Successfully")
        elif choice == "3":
            while True:
                try:
                    newPhoneNumber = input("Students New Mobile Number: ")
                    break
                except ValueError:
                    print("Try again with only digits: ")
            mycursor.execute('UPDATE Students SET MobilePhoneNumber = ? WHERE studentID = ?', (newPhoneNumber,nSID))
            conn.commit()
            print("Updated Information Successfully")
        else:
            #recursion function if invalid input
            print("Invalid input. Try Again")
            updateStudent()

#e.Delete Students by StudentId
def deleteStudent():
    nSID = input("Press b if you wish to go back to menu.\nID of the student to delete: ")
    if nSID == 'b':
        Menu()
        quit()
    mycursor.execute('SELECT * FROM Students WHERE StudentID = ?', (nSID,))
    output = mycursor.fetchall()
    #check if input valid
    if output == []:
        print("Invalid Input. Please Try Again.")
        deleteStudent()
    else:
        mycursor.execute('UPDATE Students SET isDeleted = ? WHERE studentID = ?', (1,nSID))
    conn.commit()
    print("Student Successfully Deleted")

#f.Search/DisplaystudentsbyMajor, GPA, City, State and Advisor.
def searchStudent():

    print("1. Major")
    print("2. GPA")
    print("3. City")
    print("4. State")
    print("5. Faculty Advisor")

    choice = input("Press b if you wish to go back to menu.\nSelect one of features above that you would like to filter the Students by: ")

    if choice == 'b':
        Menu()
        quit()

    while True:
        if choice == "1":
            #Distinct majors that are avialabe
            mycursor.execute('SELECT DISTINCT Major FROM Students')
            output = mycursor.fetchall()
            df = DataFrame(output, columns=['Majors'])
            print(df)
            filter = input("Major you would like to see: ")
            mycursor.execute('SELECT * FROM Students WHERE Major = ?', (filter,))
            output = mycursor.fetchall()
            #ERROR CHECK FOR INCORRECT MAJOR INPUT
            if output == []:
                print("Invalid Input. Please Try Again.")
                searchStudent()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "2":
            filter = input("GPA you would like to see: ")
            mycursor.execute('SELECT * FROM Students WHERE GPA = ?', (filter,))
            output = mycursor.fetchall()
            # ERROR CHECK FOR INCORRECT GPA INPUT
            if output == []:
                print("Invalid Input. Please Try Again.")
                searchStudent()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "3":
            #Distinct cities that are avialabe
            mycursor.execute('SELECT DISTINCT City FROM Students')
            output = mycursor.fetchall()
            df = DataFrame(output, columns=['Cities'])
            print(df)
            filter = input("City you would like to see: ")
            mycursor.execute('SELECT * FROM Students WHERE City = ?', (filter,))
            output = mycursor.fetchall()
            # ERROR CHECK FOR INCORRECT city INPUT
            if output == []:
                print("Invalid Input. Please Try Again.")
                searchStudent()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "4":
            #Distinct cities that are avialabe
            mycursor.execute('SELECT DISTINCT State FROM Students')
            output = mycursor.fetchall()
            df = DataFrame(output, columns=['States'])
            print(df)
            filter = input("State you would like to see: ")
            mycursor.execute('SELECT * FROM Students WHERE State = ?', (filter,))
            output = mycursor.fetchall()
            # ERROR CHECK FOR INCORRECT state INPUT
            if output == []:
                print("Invalid Input. Please Try Again.")
                searchStudent()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        elif choice == "5":
            # Distinct Faculty Advisor that are avialabe
            mycursor.execute('SELECT DISTINCT FacultyAdvisor FROM Students')
            output = mycursor.fetchall()
            df = DataFrame(output, columns=['Advisors'])
            print(df)
            filter = input("Faculty Advisor you would like to see: ")
            mycursor.execute('SELECT * FROM Students WHERE FacultyAdvisor = ?', (filter,))
            output = mycursor.fetchall()
            # ERROR CHECK FOR INCORRECT Faculty Advisor INPUT
            if output == []:
                print("Invalid Input. Please Try Again.")
                searchStudent()
                break
            else:
                df = DataFrame(output, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address','City', 'State', 'ZipCode', 'MobilePhoneNUmber', 'isDeleted'])
                print(df)
                break
        else:
            print("Invalid Input. Please Try Again.")
            searchStudent()
            break