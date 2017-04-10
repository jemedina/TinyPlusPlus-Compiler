using ScintillaNET;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
/*   // full path of python interpreter  
            string python = @"C:\Users\Edgardo\AppData\Local\Programs\Python\Python36-32\python.exe";

            // python app to call  
            string myPythonApp = "lexico.py";

            // Create new process start info 
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo(python);

            // make sure we can read the output from stdout 
            myProcessStartInfo.UseShellExecute = false;
            myProcessStartInfo.RedirectStandardOutput = true;

            // start python app with 3 arguments  
            // 1st argument is pointer to itself, 2nd and 3rd are actual arguments we want to send 
            myProcessStartInfo.Arguments = myPythonApp + " " + ruta;

            Process myProcess = new Process();
            // assign start information to the process 
            myProcess.StartInfo = myProcessStartInfo;

            // start process 
            myProcess.Start();

            // Read the standard output of the app we called.  
            StreamReader myStreamReader = myProcess.StandardOutput;
            string myString = myStreamReader.ReadLine();

            // wait exit signal from the app we called 
            myProcess.WaitForExit();

            // close the process 
            myProcess.Close();

            String ruta1 = "C:\\Users\\Edgardo\\Documents\\Visual Studio 2017\\Projects\\Mandarina Studio\\Mandarina Studio\\tokens.txt";
            using (StreamWriter sw1 = new StreamWriter(ruta1))
            {
                await sw1.WriteLineAsync(aLex.Text);
            }

            String ruta2 = "C:\\Users\\Edgardo\\Documents\\Visual Studio 2017\\Projects\\Mandarina Studio\\Mandarina Studio\\erroresLexicos.txt";
            using (StreamWriter sw2 = new StreamWriter(ruta2))
            {
                await sw2.WriteLineAsync(erroresLexicos.Text);
            }*/
namespace Libre_IDE
{
    class CodeEditor : Scintilla
    {
        private string path;
        private string fileName;
        private MainForm mainForm;
        private string initialContent;
        public CodeEditor(MainForm mainForm)
        {
            this.mainForm = mainForm;
            this.setupEditor();
            this.path = null;
            this.initialContent = null;
            this.fileName = "New File";
        }

        public CodeEditor(string path, MainForm mainForm)
        {
            // TODO: Complete member initialization
            this.mainForm = mainForm;
            this.setupEditor();
            this.path = path;
            this.openFile();

            this.initialContent = this.Text;
        }
        public bool isModified() {
            return !this.Text.Equals(this.initialContent);
        }
        private void setupEditor()
        {
            this.Margins[0].Width = 60;
            this.Margins[0].Type = MarginType.Number;
            this.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.MultipleSelection = true;
            this.MultiPaste = MultiPaste.Each;
            this.AdditionalSelectionTyping = true;
            this.HScrollBar = true;
            this.ScrollWidth = 1;

            var marker = this.Markers[3];
            marker.Symbol = MarkerSymbol.FullRect;
            marker.SetBackColor(Color.Gray);
            marker.SetForeColor(Color.Black);

            //this.KeyUp += new System.Windows.Forms.KeyEventHandler(this.keyDown);
            //this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.keyDown);
            this.UpdateUI += CodeEditor_UpdateUI;
            //temp
            setupCsharp();
        }

        void CodeEditor_UpdateUI(object sender, UpdateUIEventArgs e)
        {
            updateLinesAndColumnsView();
            checkSavedStatus();
            for (int i = 0; i < this.Lines.Count; i++)
            {
                this.Lines[i].MarkerDelete(3);
            }
            var line = this.Lines[this.getCurrentRow()];
            line.MarkerAdd(3);

            
        }
        private void checkSavedStatus()
        {
            if (this.isModified())
            {
                mainForm.getCurrentTab().Text = this.fileName + "*";
                mainForm.getSaveButton().Enabled = true;
                mainForm.getSaveToolButton().Enabled = true;
                mainForm.getSaveButton().Cursor = Cursors.Hand;
            }
            else
            {
                mainForm.getCurrentTab().Text = this.fileName;
                mainForm.getSaveButton().Enabled = false;
                mainForm.getSaveButton().Cursor = Cursors.No;
                mainForm.getSaveToolButton().Enabled = false;
            }
        }
        private void setupCsharp()
        {
            // Configuring the default style with properties
            // Configuring the default style with properties
            // we have common to every lexer style saves time.
            this.StyleResetDefault();
            this.Styles[Style.Default].Font = "Consolas";
            this.Styles[Style.Default].Size = 18;
            this.StyleClearAll();

            // Configure the CPP (C#) lexer styles
            this.Styles[Style.Cpp.Default].ForeColor = Color.Silver;
            this.Styles[Style.Cpp.Comment].ForeColor = Color.FromArgb(0, 128, 0); // Green
            this.Styles[Style.Cpp.CommentLine].ForeColor = Color.FromArgb(0, 128, 0); // Green
            this.Styles[Style.Cpp.CommentLineDoc].ForeColor = Color.FromArgb(128, 128, 128); // Gray
            this.Styles[Style.Cpp.Number].ForeColor = Color.Olive;
            this.Styles[Style.Cpp.Word].ForeColor = Color.Blue;
            this.Styles[Style.Cpp.Word2].ForeColor = Color.Blue;
            this.Styles[Style.Cpp.Character].ForeColor = Color.FromArgb(163, 21, 21); // Red
            this.Styles[Style.Cpp.Verbatim].ForeColor = Color.FromArgb(163, 21, 21); // Red
            this.Styles[Style.Cpp.Operator].ForeColor = Color.Purple;
            this.Styles[Style.Cpp.Preprocessor].ForeColor = Color.Maroon;
            this.Lexer = Lexer.Cpp;
            this.SetKeywords(0, "do main if then else end while repeat until cin cout real int boolean");
        }    
        private void openFile()
        {
            StreamReader reader = new StreamReader(path);
            this.Text = reader.ReadToEnd();
            this.fileName = Path.GetFileName(path);
            reader.Close();

        }

        public string getName()
        {
            return this.fileName;
        }

        public void saveFile(string path)
        {
            StreamWriter writer = File.CreateText(path);
            writer.Write(this.Text);
            writer.Flush();
            this.path = path;
            this.fileName = Path.GetFileName(path);
            this.initialContent = this.Text;
            checkSavedStatus();
        }

        public void saveFile()
        {
            StreamWriter writer = File.CreateText(path);
            writer.Write(this.Text);
            writer.Flush();
            writer.Close();
            this.fileName = Path.GetFileName(path);
            this.initialContent = this.Text;
            checkSavedStatus();
        }
        public bool hasPath()
        {
            return this.path != null;
        }

        public string getPath()
        {
            return path;
        }

        public int getCurrentColumn()
        {
            return this.GetColumn(this.CurrentPosition);
        }

        public int getCurrentRow()
        {
            return this.CurrentLine;
        }


        public void updateLinesAndColumnsView()
        {
            CodeEditor currentCodeEditor = ((CodeTabPage)mainForm.getCurrentTab()).getCodeEditor();
            mainForm.setColumnOnLabel(currentCodeEditor.getCurrentColumn()+1);
            mainForm.setRowOnLabel(currentCodeEditor.getCurrentRow()+1);
            mainForm.setLines(currentCodeEditor.Lines.Count);
        }

    }
}
