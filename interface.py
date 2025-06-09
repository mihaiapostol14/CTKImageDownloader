import os
import requests
from ddgs import DDGS
import customtkinter
from helper import Helper
class Frame(customtkinter.CTkFrame,Helper):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        # add widgets onto the frame, for example:
        # add widgets to app
        self.search = None
        self.max_num = None
        self.label = customtkinter.CTkLabel(self, text='CTKImageDownloader', font=('Arial',20))
        self.label.pack(padx=10, pady=10)

        self.search_entry = customtkinter.CTkEntry(self, width=350, height=40,placeholder_text='Typing Search Image')
        self.search_entry.pack(padx=10, pady=10)


        self.max_count_entry = customtkinter.CTkEntry(self, width=350, height=40,placeholder_text='Typing Count Image')
        self.max_count_entry.pack(padx=10, pady=10)

        self.count_image_label = customtkinter.CTkLabel(self, text='', font=('Arial', 20))
        self.count_image_label.pack(padx=10, pady=5)

        self.download_button = customtkinter.CTkButton(self, text='Download',command=self.download_image)
        self.download_button.pack(padx=20, pady=10)

        self.open_dir_button = customtkinter.CTkButton(self, text='Open', command=self.open_output_directory)
        self.open_dir_button.pack(padx=20, pady=10)

    def download_image(self):
        self.search = self.search_entry.get().strip()
        self.max_num = self.max_count_entry.get().strip()

        if not self.search or not self.max_num.isdigit():
            print("Search text or image count is invalid")
            return

        if not os.path.exists(self.search):
            os.makedirs(self.search)

        with DDGS() as ddgs:
            generator = ddgs.images(
                query=self.search,
                region="wt-wt",
                safesearch="off",
                max_results=int(self.max_num),
            )

            for i, res in enumerate(generator):
                try:
                    img_url = res.get("image")
                    if img_url:
                        response = requests.get(img_url, timeout=10, stream=True)
                        if response.status_code == 200:
                            file_name = f"image_{i+1}.jpg"
                            file_path = os.path.join(self.search, file_name)

                            with open(file_path, "wb") as f:
                                for chunk in response.iter_content(8192):
                                    f.write(chunk)

                            print(f"[{i+1}] Saved: {file_name}")
                except Exception as e:
                    print(f"[{i+1}] Skipped: {e}")

        print("--- Download finished ---")
        self.count_image()

        
    def count_image(self):
        if self.directory_exists(directory_name=self.search):
            self.count_image_label.configure(text=f'Count image {self.search} is {len(os.listdir(self.search))}')
            self.open_dir_button.configure(text=f'Open {self.search}')



    def open_output_directory(self):
        if self.directory_exists(directory_name=self.search):
            os.startfile(self.search)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('CTKImageDownloader')
        self.geometry("350x400")
        self.resizable(False,False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.frame = Frame(master=self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")



app = App()
app.mainloop()

