import customtkinter as ctk
import threading
import time

# ---------------- Backend Logic ---------------- #

def process_inputs(input_a, input_b):
    time.sleep(0.6)

    combined = f"{input_a.strip()} {input_b.strip()}"
    words = combined.split()
    unique = set(w.lower() for w in words)

    return (
        f"MERGED OUTPUT\n"
        f"{'-'*40}\n"
        f"{combined}\n\n"
        f"STATISTICS\n"
        f"{'-'*40}\n"
        f"Total words   : {len(words)}\n"
        f"Unique words  : {len(unique)}\n"
        f"Characters    : {len(combined)}\n"
        f"Input A tokens: {len(input_a.split())}\n"
        f"Input B tokens: {len(input_b.split())}\n"
    )


# ---------------- UI Setup ---------------- #

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NLPMapperApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Navigation System Analyzer")
        self.geometry("900x650")

        self.build_ui()

    # ---------------- UI ---------------- #

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="INERTIAL NAVIGATION SYSTEM",
            font=("Courier", 22, "bold")
        )
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(
            self,
            text="Frequency + Diameter → Navigation System",
            font=("Courier", 12)
        )
        subtitle.pack(pady=5)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        main_frame.grid_columnconfigure((0,1,2), weight=1)

        # INPUT A
        label_a = ctk.CTkLabel(main_frame,text="INPUT A")
        label_a.grid(row=0,column=0,pady=10)

        self.box_a = ctk.CTkTextbox(main_frame,height=150)
        self.box_a.grid(row=1,column=0,padx=10,sticky="ew")

        # RUN BUTTON
        self.run_button = ctk.CTkButton(
            main_frame,
            text="RUN",
            width=100,
            command=self.run_processing
        )
        self.run_button.grid(row=1,column=1,padx=10)

        # INPUT B
        label_b = ctk.CTkLabel(main_frame,text="INPUT B")
        label_b.grid(row=0,column=2,pady=10)

        self.box_b = ctk.CTkTextbox(main_frame,height=150)
        self.box_b.grid(row=1,column=2,padx=10,sticky="ew")

        # OUTPUT
        output_label = ctk.CTkLabel(
            main_frame,
            text="Recommended Navigation System"
        )
        output_label.grid(row=2,column=0,columnspan=3,pady=20)

        self.output_box = ctk.CTkTextbox(main_frame,height=220)
        self.output_box.grid(row=3,column=0,columnspan=3,sticky="nsew")

        # STATUS BAR
        self.status = ctk.CTkLabel(self,text="Ready",anchor="w")
        self.status.pack(fill="x",padx=20,pady=10)

    # ---------------- Actions ---------------- #

    def run_processing(self):

        a = self.box_a.get("1.0","end").strip()
        b = self.box_b.get("1.0","end").strip()

        if not a or not b:
            self.status.configure(text="⚠ Please enter both inputs")
            return

        self.status.configure(text="Processing...")
        self.run_button.configure(state="disabled")

        def worker():

            result = process_inputs(a,b)

            self.after(0,lambda: self.show_output(result))

        threading.Thread(target=worker).start()

    def show_output(self,result):

        self.output_box.delete("1.0","end")
        self.output_box.insert("1.0",result)

        self.status.configure(text="Done")
        self.run_button.configure(state="normal")


# ---------------- Run App ---------------- #

if __name__ == "__main__":

    app = NLPMapperApp()
    app.mainloop()