from tabulate import tabulate
import mysql.connector as c

con = c.connect(host="localhost",
                user="root",
                passwd="host",
                database="project",
                auth_plugin="mysql_native_password")

if con.is_connected():
    print("Connection established successfully!")
else:
    print("There is some error in connection")

cursor = con.cursor(buffered=True)


# Signing up
def sign_up():
    global c_id
    c_id = int(input("Enter your own numeric ID (required): "))

    try:
        check = "select cid from cust_details where cid={}".format(c_id)
        cursor.execute(check)
        dd = cursor.fetchall()
        dd1 = tuple(dd)
        for i in dd1:
            if i[0] == c_id:
                print("This ID is already taken, provide another one")
                print(" ")
                sign_up()

    except Exception as n:
        k = 0
        pass


# Movie menu
def master():
    cursor.execute("select * from movie_master")
    data = cursor.fetchall()
    h = ["MOVIE ID", "MOVIE NAME", "TIMINGS", "LANGUAGE", "FORMAT", "GENRE"]
    print(tabulate(data, headers=h, tablefmt="psql"))


# Movie Details
def movie():
    print(" ")
    print("Select your search criterion: ")
    print("1. Budget Limit")
    print("2. Genre")
    print("3. Both Budget limit and Genre")
    ch = int(input("Enter your choice: "))

    if ch == 1:
        print(" ")
        b = int(input("Please enter your maximum budget: "))
        if b < 120:
            print("No movies available at this time....visit again later.")

        else:
            sql = ("select * from movie_master,movie_info \n"
                   " where movie_master.mid=movie_info.mid and price<={}").format(b)
            cursor.execute(sql)
            data = cursor.fetchall()
            h = ["MOVIE ID", "MOVIE NAME", "TIMINGS", "LANGUAGE", "FORMAT", "GENRE", " ",
                 "PRICE (₹)", "SCREEN NUMBER", "RATING"]
            print(tabulate(data, headers=h, tablefmt="psql"))

    elif ch == 2:
        print(" ")
        print("Genres available are: \n"
              "Comedy/Adventurous/Romance")
        g = (input("Please enter your preferable genre: ")).capitalize()
        if g not in ["Adventurous", "Comedy", "Romance"]:
            print("Re-enter the genre properly")

        else:
            sql = ("select * from movie_master,movie_info \n"
                   "where movie_master.mid=movie_info.mid and genre=\'{}\'").format(g)
            cursor.execute(sql)
            data = cursor.fetchall()
            h = ["MOVIE ID", "MOVIE NAME", "TIMINGS", "LANGUAGE", "FORMAT", "GENRE", " ",
                 "PRICE (₹)", "SCREEN NUMBER", "RATING"]
            print(tabulate(data, headers=h, tablefmt="psql"))

    elif ch == 3:
        print(" ")
        print("Genres available are: \n"
              "Comedy/Adventurous/Romance")
        g = (input("Please enter your preferable genre: ")).capitalize()
        if g not in ["Adventurous", "Comedy", "Romance"]:
            print("Re-enter the genre properly")

        else:
            b = int(input("Please enter your maximum budget: "))
            if b < 120:
                print("No movies available at this time....visit again later.")
            elif g == "Adventurous" and b < 180:
                print("No movies available at this time....visit again later.")
            elif g == "Romance" and b < 150:
                print("No movies available at this time....visit again later.")
            else:
                sql = ("select * from movie_master,movie_info \n"
                       "where movie_master.mid=movie_info.mid and price<={} and genre=\'{}\'").format(b, g)
                cursor.execute(sql)
                data = cursor.fetchall()
                h = ["MOVIE ID", "MOVIE NAME", "TIMINGS", "LANGUAGE", "FORMAT", "GENRE", " ",
                     "PRICE (₹)", "SCREEN NUMBER", "RATING"]
                print(tabulate(data, headers=h, tablefmt="psql"))


# Snack Menu
def snack():
    print(" ")
    sql = "select * from snack_menu"
    cursor.execute(sql)
    data = cursor.fetchall()
    h = ["FOOD ID", "ITEM", "TYPE", "SIZE", "PRICE(₹)"]
    print(tabulate(data, headers=h, tablefmt="psql"))


# Booking Ticket
def booking():
    print(" ")
    sql = cursor.execute("select mid,mname from movie_master")
    data = cursor.fetchall()
    h = ["MOVIE ID", "MOVIE NAME"]
    print(tabulate(data, headers=h, tablefmt='psql'))
    m = int(input("Select your movie from the above chart and enter it's corresponding Movie ID: "))
    sql1 = "select mname from movie_master \n " \
           "where mid={}".format(m)
    cursor.execute(sql1)
    m_data = cursor.fetchall()
    week = tuple(m_data)
    for i in week:
        week1 = " ".join(i)
        c = int(input("Enter your ID: "))
        entry = "update cust_details set mname='{}' where cid={}".format(week1, c)
        cursor.execute(entry)
        con.commit()
        print("Movie chosen!")
        s_no = "select sno from movie_info where mid={}".format(m)
        cursor.execute(s_no)
        sno1 = cursor.fetchall()
        sno2 = tuple(sno1)
        for i in sno2:
            sno3 = " ".join(i)
            entry = "update cust_details set sno='{}' where cid={}".format(sno3, c)
            cursor.execute(entry)
            con.commit()
            print(" ")
            print("Do you want to add snacks to your cart?: ")
            enquiry = input("Y/N: ").upper()

            if enquiry == "Y":
                sql = "select * from snack_menu"
                cursor.execute(sql)
                s_menu = cursor.fetchall()
                h = ["FOOD ID", "ITEM", "TYPE", "SIZE", "PRICE (₹)"]
                print(tabulate(s_menu, headers=h, tablefmt="psql"))
                fid = int(input("Please select your preferable food item from the above chart "
                                "and enter it's corresponding Food ID: "))
                f = "select item from snack_menu where fid={}".format(fid)
                cursor.execute(f)
                f_data = cursor.fetchall()
                food = tuple(f_data)
                for i in food:
                    food1 = " ".join(i)
                    c = int(input("Enter your ID: "))
                    entry = "update cust_details set food='{}' where cid={}".format(food1, c)
                    cursor.execute(entry)
                    con.commit()
                    print("Snack selected!")
                    mp = "select price from movie_info where mid={}".format(m)
                    cursor.execute(mp)
                    mp1 = cursor.fetchall()
                    mp2 = tuple(mp1)
                    for i in mp2:
                        p3 = " ".join(i)
                        fp = "select fprice from snack_menu where fid={}".format(fid)
                        cursor.execute(fp)
                        fp1 = cursor.fetchall()
                        fp2 = tuple(fp1)
                        for i in fp2:
                            fp3 = " ".join(i)
                            a = int(p3)
                            b = int(fp3)
                            tprice = a + b
                            tprice1 = str(tprice)
                            print(" ")
                            c1 = int(input("Enter your ID again to confirm your selection(s): "))
                            tp = "update cust_details set tprice={} where cid={}".format(tprice1, c1)
                            cursor.execute(tp)
                            con.commit()
                            print(" ")
                            print("Yay!....Booking confirmed")
                            print("Your ticket has been generated :)")
                            ticket = "select * from cust_details where cid={}".format(c)
                            cursor.execute(ticket)
                            ticket1 = cursor.fetchall()
                            h = ["CUSTOMER ID", "FIRST NAME", "LAST NAME", "PHONE NUMBER",
                                 "AGE", 'MOVIE NAME', "SCREEN NUMBER", "FOOD", "TOTAL PRICE (₹)"]
                            print(tabulate(ticket1, headers=h, tablefmt='psql'))

            else:
                jp = "select price from movie_info where mid={}".format(m)
                cursor.execute(jp)
                jp1 = cursor.fetchall()
                jp2 = tuple(jp1)
                for i in jp2:
                    jp3 = " ".join(i)
                    c1 = int(input("Enter your ID again to confirm your selection(s): "))
                    pr1 = "update cust_details set tprice={} where cid={}".format(jp3, c1)
                    cursor.execute(pr1)
                    con.commit()
                    print(" ")
                    print("Yay!....Booking confirmed")
                    print("Your ticket has been generated :)")
                    ticket = "select cid,fname,lname,phno," \
                             "age,mname,sno,tprice from cust_details where cid={}".format(c)
                    cursor.execute(ticket)
                    ticket1 = cursor.fetchall()
                    h = ["CUSTOMER ID", "FIRST NAME", "LAST NAME", "PHONE NUMBER",
                         "AGE", 'MOVIE NAME', "SCREEN NO", "TOTAL PRICE (₹)"]
                    print(tabulate(ticket1, headers=h, tablefmt='psql'))


# View Booking
def view():
    p = int(input("Enter your ID to view your booking: "))
    hey = "select mname from cust_details where cid={}".format(p)
    cursor.execute(hey)
    hey1 = cursor.fetchall()
    hey2 = tuple(hey1)
    for y in hey2:
        if y[0] is None or y[0] == " ":
            print(" ")
            print("No booking done yet or else already cancelled.")
            break

        else:
            day = "select mname,food,tprice from cust_details where cid={}".format(p)
            cursor.execute(day)
            day1 = cursor.fetchall()
            day2 = tuple(day1)
            for x in day2:
                if x[1] == None:
                    d1 = "select mname,tprice from cust_details where cid={}".format(p)
                    cursor.execute(d1)
                    d2 = cursor.fetchall()
                    d3 = tuple(d2)
                    h = ["MOVIE NAME", "TOTAL PRICE"]
                    print(" ")
                    print(tabulate(d3, headers=h, tablefmt="psql"))

                else:
                    h = ["MOVIE NAME", "FOOD", "TOTAL PRICE"]
                    print(" ")
                    print(tabulate(day1, headers=h, tablefmt="psql"))



# Booking Cancellation
def cancel():
    d = int(input("Enter your ID to verify cancellation: "))
    hey = "select mname from cust_details where cid={}".format(d)
    cursor.execute(hey)
    hey1 = cursor.fetchall()
    hey2 = tuple(hey1)
    for y in hey2:
        if y[0] is None or y[0] == " ":
            print(" ")
            print("No booking done yet or else already cancelled.")
            break

        else:
            day = "select mname,food,tprice from cust_details where cid={}".format(d)
            cursor.execute(day)
            day1 = cursor.fetchall()
            day2 = tuple(day1)
            for x in day2:
                if x[1] == None:
                    d1 = "select mname,tprice from cust_details where cid={}".format(d)
                    cursor.execute(d1)
                    d2 = cursor.fetchall()
                    d3 = tuple(d2)
                    h = ["MOVIE NAME", "TOTAL PRICE"]
                    print(" ")
                    print("Your booking was as follows:")
                    print(tabulate(d3, headers=h, tablefmt="psql"))
                    print("Do you really want to cancel your booking?")

                else:
                    h = ["MOVIE NAME", "FOOD", "TOTAL PRICE"]
                    print(" ")
                    print("Your booking was as follows:")
                    print(tabulate(day1, headers=h, tablefmt="psql"))
                    print("Do you really want to cancel your booking?")

        sry = input("Y/N: ").upper()
        if sry == "Y":
            blank = " "
            no1 = "update cust_details set mname='{}' where cid={}".format(blank, d)
            no2 = "update cust_details set sno ='{}' where cid={}".format(blank, d)
            no3 = "update cust_details set food ='{}' where cid={}".format(blank, d)
            no4 = "update cust_details set tprice ='{}' where cid={}".format(blank, d)
            cursor.execute(no1)
            cursor.execute(no2)
            cursor.execute(no3)
            cursor.execute(no4)
            con.commit()
            print(" ")
            print("Booking cancelled successfully")
            print("Your amount will be refunded within 24 hours")

        elif sry == "N":
            pass

        else:
            print(" ")
            print("Enter your choice correctly")
            cancel()
# end


# main
a = "WELCOME TO MAJESTIC CINEMAS"
intro = a.center(150, ".")
print(intro)
print("\"Sign up required\"")


# Verification of pre-registered ID
def check_int(sh):
    query = "select cid from cust_details where cid={}".format(sh)
    cursor.execute(query)
    result = cursor.fetchone()
    return result is not None


# Asking for sign up
def ask():
    print("Signing up for first time?")
    a = input("Y/N: ").upper()
    if a == "Y":
        sign_up()
        fname = input("Enter your first name (required): ").capitalize()
        lname = input("Enter your last name (required): ").capitalize()
        phno = int(input("Enter your phone number (required): "))
        age = int(input("Enter your age: "))
        sql = cursor.execute("insert into cust_details(cid,fname,lname,phno,age) \n"
                             "values({},'{}','{}',{},{})".format(c_id, fname, lname, phno, age))
        cursor.execute(sql)
        con.commit()
        print("Sign up successful!, redirecting towards homepage....")

    elif a == "N":
        while True:
            print(" ")
            sh = int(input("Enter your pre-registered ID: "))

            if check_int(sh):
                mm = "select fname from cust_details where cid={}".format(sh)
                cursor.execute(mm)
                mm1 = cursor.fetchall()
                mm2 = tuple(mm1)
                for i in mm2:
                    name = i[0]
                    print("Welcome back", name, ", directing you towards homepage....")
                break

            else:
                print(" ")
                print("ID not found, directing towards sign up page....")
                sign_up()
                fname = input("Enter your first name (required): ").capitalize()
                lname = input("Enter your last name (required): ").capitalize()
                phno = int(input("Enter your phone number (required): "))
                age = int(input("Enter your age: "))
                sql = cursor.execute("insert into cust_details(cid,fname,lname,phno,age) \n"
                                     "values({},'{}','{}',{},{})".format(c_id, fname, lname, phno, age))
                cursor.execute(sql)
                con.commit()
                print("Sign up successful!, directing towards homepage....")


    else:
        print("Enter your choice correctly")
        ask()


ask()


while True:
    print("\n")
    print("1. View current running shows")
    print("2. View movie details")
    print("3. View snack menu")
    print("4. Proceed with ticket booking")
    print("5. View your booking")
    print("6. Booking cancellation")
    print("7. Log out")
    print(" ")
    ch = (int(input("Enter your choice: ")))
    if ch == 1:
        master()
    elif ch == 2:
        movie()
    elif ch == 3:
        snack()
    elif ch == 4:
        booking()
    elif ch == 5:
        view()
    elif ch == 6:
        cancel()
    elif ch == 7:
        print("Logging out.....Thank you for visiting MAJESTIC CINEMAS!!")
        break
    else:
        print("Invalid choice entered :/")