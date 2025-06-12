from tkinter import *
from tkinter import scrolledtext
import weaviate
from weaviate.classes.init import Auth
import os

class DiscreteMathTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Discrete Math Tutor")
        self.root.geometry('800x600')
        
        # Initialize Weaviate connection
        self.client = None
        self.collection = None
        self.connect_to_weaviate()
        
        # Create GUI elements
        self.create_widgets()
    
    def connect_to_weaviate(self):
        try:
            weaviate_url = os.environ["WEAVIATE_URL"]
            weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
            cohere_api_key = os.environ["COHERE_APIKEY"]
            
            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=weaviate_url,
                auth_credentials=Auth.api_key(weaviate_api_key),
                headers={"X-Cohere-Api-Key": cohere_api_key},
            )
            self.collection = self.client.collections.get("discreteMath")
        except Exception as e:
            print(f"Failed to connect to Weaviate: {e}")
            # You might want to show an error message in the GUI here
    
    def create_widgets(self):
        # Welcome label
        self.lbl = Label(self.root, text="Welcome to the Discrete Math Tutor!", font=('Arial', 14))
        self.lbl.pack(pady=10)
        
        # Topic frame
        topic_frame = Frame(self.root)
        topic_frame.pack(pady=10)
        
        self.topic_label = Label(topic_frame, text="Enter a topic:")
        self.topic_label.grid(column=0, row=0, padx=5)
        
        self.topic_entry = Entry(topic_frame, width=30)
        self.topic_entry.grid(column=1, row=0, padx=5)
        
        # Question frame
        question_frame = Frame(self.root)
        question_frame.pack(pady=10)
        
        self.question_label = Label(question_frame, text="Enter your question:")
        self.question_label.grid(column=0, row=0, padx=5)
        
        self.question_entry = Entry(question_frame, width=50)
        self.question_entry.grid(column=1, row=0, padx=5)
        
        # Button
        self.btn = Button(self.root, text="Get Answer", 
                         fg="blue", command=self.get_answer)
        self.btn.pack(pady=10)
        
        # Response area
        self.response_label = Label(self.root, text="Answer:")
        self.response_label.pack(pady=5)
        
        self.response_text = scrolledtext.ScrolledText(self.root, 
                                                     width=70, 
                                                     height=15,
                                                     wrap=WORD)
        self.response_text.pack(pady=10, padx=10)
        
        # Status bar
        self.status_var = StringVar()
        self.status_var.set("Ready")
        self.status_bar = Label(self.root, textvariable=self.status_var, 
                               relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
    
    def get_answer(self):
        topic = self.topic_entry.get()
        question = self.question_entry.get()
        
        if not topic or not question:
            self.status_var.set("Please enter both topic and question")
            return
        
        if not self.client or not self.collection:
            self.status_var.set("Not connected to Weaviate")
            return
        
        try:
            self.status_var.set("Querying Weaviate...")
            self.btn.config(state=DISABLED, text="Processing...")
            self.root.update()  # Force UI update
            
            response = self.collection.generate.near_text(
                query=topic,
                limit=2,
                grouped_task=question
            )
            
            # Clear previous response
            self.response_text.delete(1.0, END)
            
            # Process the response
            if hasattr(response, 'generated'):
                # Handle the response properly based on its structure
                if isinstance(response.generated, str):
                    # If it's already a string, use it directly
                    self.response_text.insert(END, response.generated)
                elif isinstance(response.generated, (list, tuple)):
                    # If it's a list of responses, join them
                    combined = "\n\n".join(
                        str(item) if not isinstance(item, str) else item 
                        for item in response.generated
                    )
                    self.response_text.insert(END, combined)
                else:
                    # Fallback - convert whatever we got to string
                    self.response_text.insert(END, str(response.generated))
            else:
                self.response_text.insert(END, "No answer was generated.")
            
            self.status_var.set("Query completed successfully")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.response_text.delete(1.0, END)
            self.response_text.insert(END, f"An error occurred: {str(e)}")
        finally:
            self.btn.config(state=NORMAL, text="Get Answer")

if __name__ == "__main__":
    root = Tk()
    app = DiscreteMathTutor(root)
    root.mainloop()
