from tkinter import *
from tkinter import messagebox
import requests as req
from PIL import ImageTk,Image
from io import BytesIO
import urllib.parse

class CustomRequest:
    def __init__(self,method,args):
        self.args=args
        self.method=method

inc=0

def fetch_information(title,poster,date,rating):
    global inc
    inc = inc + 1
    text[f"a{inc}"].config(text=title[:20] + "..." if len(title) > 20 else title)
    
    if check_var.get():
        text2[f"a{inc}{inc}"].config(text=date if date != "N/A" else "Unknown")
    else:
        text2[f"a{inc}{inc}"].config(text="")

    if check_var2.get():
        text3[f"a{inc}{inc}{inc}"].config(text=f"Rating: {rating}" if rating != "N/A" else "Not rated")
    else:
        text3[f"a{inc}{inc}{inc}"].config(text="")

    if poster != "N/A":
        try:
            response = req.get(poster)
            image_data = response.content
            img = Image.open(BytesIO(image_data))
            re_img = img.resize((140, 200), Image.Resampling.LANCZOS)
            photo2 = ImageTk.PhotoImage(re_img)
            image[f"b{inc}"].config(image=photo2)
            image[f"b{inc}"].image = photo2
        except Exception as e:
            print(f"Error loading image: {e}")
            image[f"b{inc}"].config(image="")
    else:
        image[f"b{inc}"].config(image="")
        
def search():
    global inc
    inc = 0
    
    # Clear existing results
    for i in range(1, 6):
        text[f"a{i}"].config(text="")
        text2[f"a{i}{i}"].config(text="")
        text3[f"a{i}{i}{i}"].config(text="")
        image[f"b{i}"].config(image="")

    custom_request = CustomRequest("GET", {"search":Search.get()})

    if custom_request.method == "GET":
        search = urllib.parse.quote(custom_request.args.get("search", ""))
        url = f"https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=5"
        response = req.get(url)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                messagebox.showinfo("Info", "No books found for the given search term.")
                return

            for item in items:
                volume_info = item.get("volumeInfo", {})
                title = volume_info.get("title", "N/A")
                published_date = volume_info.get("publishedDate", "N/A")
                rating = volume_info.get("averageRating", "N/A")
                image_link = volume_info.get("imageLinks", {})
                image_url = image_link.get("thumbnail") if "thumbnail" in image_link else "N/A"

                fetch_information(title, image_url, published_date, rating)

            if check_var.get() or check_var2.get():
                frame11.place(x=160, y=600)
                frame22.place(x=360, y=600)
                frame33.place(x=560, y=600)
                frame44.place(x=760, y=600)
                frame55.place(x=960, y=600)
            else:
                frame11.place_forget()
                frame22.place_forget()
                frame33.place_forget()
                frame44.place_forget()
                frame55.place_forget()
        else:
            messagebox.showinfo("Error", "Failed to fetch data from Google Books API.")
    
def show_menu(event):
    menu.post(event.x_root,event.y_root)

root=Tk()
root.title("Book Recommender System")
root.geometry("1250x700+200+100")
root.config(bg="#111119")
root.resizable(False,False)

#icon
icon_image=PhotoImage(file="Images/icon.png")
root.iconphoto(False,icon_image)
#bg image
heading_image=PhotoImage(file="Images/background.png")
Label(root,image=heading_image,bg="#111119").place(x=-2,y=-2)
#logo
logo_image=PhotoImage(file="Images/logo.png")
Label(root,image=logo_image,bg="#0099ff").place(x=300,y=80)
#heading
heading=Label(root,text="BOOK RECOMMENDATION",font=("lato",30,"bold"),bg="#0099ff",fg="white")
heading.place(x=410,y=90)
#search bg image
search_image=PhotoImage(file="Images/Rectangle 2.png")
Label(root,image=search_image,bg="#0099ff").place(x=300,y=155)
#search entry
Search=StringVar()
search_entry=Entry(root,textvariable=Search,width=20,font=("lato",25),bg="white",fg="black",bd=0)
search_entry.place(x=415,y=172)
#search button
search_button_image=PhotoImage(file="Images/Search.png")
search_button=Button(root,image=search_button_image,bd=0,bg="#0099ff",cursor="hand2",activebackground="#0099ff",command=search)
search_button.place(x=860,y=169)
#setting Button
sett_button_image=PhotoImage(file="Images/setting.png")
sett_button=Button(root,image=sett_button_image,bd=0,bg="#0099ff",cursor="hand2",activebackground="#0099ff")
sett_button.place(x=1050,y=175)
sett_button.bind('<Button-1>',show_menu)

#menu for search
menu=Menu(root,tearoff=0)
check_var=BooleanVar()
menu.add_checkbutton(label="Publish Date",variable=check_var,command=search)

check_var2=BooleanVar()
menu.add_checkbutton(label="Rating",variable=check_var2,command=search)
#logout button
logg_button_image=PhotoImage(file="Images/logout.png")
logg_button=Button(root,image=logg_button_image,bd=0,bg="#0099ff",cursor="hand1",activebackground="#0099ff",command=lambda:root.destroy())
logg_button.place(x=1150,y=20)

# first Frame
frame1=Frame(root,width=150,height=240,bg="white")
frame2=Frame(root,width=150,height=240,bg="white")
frame3=Frame(root,width=150,height=240,bg="white")
frame4=Frame(root,width=150,height=240,bg="white")
frame5=Frame(root,width=150,height=240,bg="white")
frame1.place(x=160,y=350)
frame2.place(x=360,y=350)
frame3.place(x=560,y=350)
frame4.place(x=760,y=350)
frame5.place(x=960,y=350)

#book title
text={
    'a1':Label(frame1,text="Book Title",font=("arial,10"),fg="green"),
    'a2':Label(frame2,text="Book Title",font=("arial,10"),fg="green"),
    'a3':Label(frame3,text="Book Title",font=("arial,10"),fg="green"),
    'a4':Label(frame4,text="Book Title",font=("arial,10"),fg="green"),
    'a5':Label(frame5,text="Book Title",font=("arial,10"),fg="green")
}
text["a1"].place(x=10,y=4)
text["a2"].place(x=10,y=4)
text["a3"].place(x=10,y=4)
text["a4"].place(x=10,y=4)
text["a5"].place(x=10,y=4)

#poster
image={
    'b1':Label(frame1),
    'b2':Label(frame2),
    'b3':Label(frame3),
    'b4':Label(frame4),
    'b5':Label(frame5)
}
image["b1"].place(x=3,y=30)
image["b2"].place(x=3,y=30)
image["b3"].place(x=3,y=30)
image["b4"].place(x=3,y=30)
image["b5"].place(x=3,y=30)

#second Frame
frame11=Frame(root,width=150,height=50,bg="#e6e6e6")
frame22=Frame(root,width=150,height=50,bg="#e6e6e6")
frame33=Frame(root,width=150,height=50,bg="#e6e6e6")
frame44=Frame(root,width=150,height=50,bg="#e6e6e6")
frame55=Frame(root,width=150,height=50,bg="#e6e6e6")

#published
text2={
    'a11':Label(frame11,text="date",font=("arial",10),bg="#e6e6e6",fg="red"),
    'a22':Label(frame22,text="date",font=("arial",10),bg="#e6e6e6",fg="red"),
    'a33':Label(frame33,text="date",font=("arial",10),bg="#e6e6e6",fg="red"),
    'a44':Label(frame44,text="date",font=("arial",10),bg="#e6e6e6",fg="red"),
    'a55':Label(frame55,text="date",font=("arial",10),bg="#e6e6e6",fg="red")
}
text2["a11"].place(x=10,y=4)
text2["a22"].place(x=10,y=4)
text2["a33"].place(x=10,y=4)
text2["a44"].place(x=10,y=4)
text2["a55"].place(x=10,y=4)
#rating
text3={
    'a111':Label(frame11,text="rating",font=("arial",10),bg="#e6e6e6"),
    'a222':Label(frame22,text="rating",font=("arial",10),bg="#e6e6e6"),
    'a333':Label(frame33,text="rating",font=("arial",10),bg="#e6e6e6"),
    'a444':Label(frame44,text="rating",font=("arial",10),bg="#e6e6e6"),
    'a555':Label(frame55,text="rating",font=("arial",10),bg="#e6e6e6")
}
text3["a111"].place(x=20,y=30)
text3["a222"].place(x=20,y=30)
text3["a333"].place(x=20,y=30)
text3["a444"].place(x=20,y=30)
text3["a555"].place(x=20,y=30)

root.mainloop()