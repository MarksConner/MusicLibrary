import customtkinter
import tkinter
#from main import main

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x500")
label = tkinter.Label(root)

label.pack()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Music Library Database", font=("Roboto", 24))
label.pack(pady=12, padx=10)

root.mainloop()