# 📄 Resume Processing System  

This is a Python-based backend application designed to automate the processing of resumes received via email. It extracts and filters content based on custom keywords defined by the user, streamlining recruitment workflows.  

## 🚀 Features  
- Extracts text from **PDF** and **DOCX** files  
- Filters resumes based on **keywords**  
- Supports **email-based** resume submission  
- Easy-to-use **batch file execution**  

## 🛠 Requirements  
- **Python 3.8 or higher**  
- **Email client** (such as Outlook)  

## 📥 Installation  

<h2>1️⃣ Clone the Repository </h2>
git clone https://github.com/leoouu/EmailHandler <br/>
cd your-repository

<h2>2️⃣ Install Dependencies</h2>
Run the following commands in the terminal: <br/>
pip install pymupdf <br/>
pip install python-docx <br/>
pip install python-dotenv <br/>


<h2>3️⃣ Configure the File Path</h2> 
Open the "ALTERE O CAMINHO!!" file in a text editor. <br/>

Edit the 7th line to point to the correct path of your main project folder: <br/>
C:\Users\UserName\Desktop\Repository\Project <br/>
Save the file as a .bat file (e.g., Program.bat). 

<h2>4️⃣ Run the Program</h2> 
Simply double-click the .bat file you created, and the program will start correctly! <br/>

## <h2> ✨ Usage </h2>

Once configured, the user can submit resumes via email. The program will: <br/>
1. Automatically download new email attachments (.pdf or .docx). <br/>
2. Extract text from the resumes. <br/>
3. Filter them using the keywords defined by the user. <br/>
4. Output the filtered results to a specific location or log file. <br/>

📝 Note: This setup only needs to be done once. From the second time onwards, just open the .bat file to launch the program. <br/>
