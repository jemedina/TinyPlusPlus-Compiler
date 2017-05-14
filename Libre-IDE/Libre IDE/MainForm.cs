using ScintillaNET;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Libre_IDE
{
    public partial class MainForm : Form
    {
        private Point _imageLocation = new Point(13, 5);
        private Point _imgHitArea = new Point(13, 2);
        private const string BASE_PATH = "C:\\Users\\";
        public MainForm()
        {
            InitializeComponent();
        }

        private void salirToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close();
        }
        private void disableCompilationButtons()
        {
            button1.Enabled = false;
        }
        private void enableCompilationButtons()
        {
            button1.Enabled = true;
        }
        private void MainForm_Load(object sender, EventArgs e)
        {
            //Set up gui
            setDefaultLayouts();
            intEditor();
            calculateToolBarLabelsPosition();
            //ListDirectory(treeView1, BASE_PATH);
            
        }

        private void setDefaultLayouts()
        {
            showErrorStatusWindow();
            showCompilationStatusWindow();
            hideFilesWindow();
            disableCompilationButtons();
        }
        private void intEditor()
        {
            if (codeTabControl.TabCount == 0)
                codeTabControl.TabPages.Add(new CodeTabPage("New File*",this));
        }

        public void addTab(string path = null)
        {
            if (path == null)
                codeTabControl.TabPages.Add(new CodeTabPage("New File*",this));
            else
                codeTabControl.TabPages.Add(new CodeTabPage(path,true,this));
            int lastPage = codeTabControl.TabPages.Count;
            codeTabControl.SelectTab(lastPage-1);
        }

        private void abrirToolStripMenuItem_Click(object sender, EventArgs e)
        {
            addTab();

            enableFileActionButtons();
        }

        private void abrirToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "Any File (*.*) | *.*";
            ofd.InitialDirectory = "C:\\Users\\%User%\\Documents";
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string path = ofd.FileName;
                this.addTab(path);
                enableFileActionButtons();
            }
        }

        private void progresoDeCompilacionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!progresoDeCompilacionToolStripMenuItem.Checked)
            {
                progresoDeCompilacionToolStripMenuItem.Checked = true;
                showCompilationStatusWindow();
            }
            else
            {
                progresoDeCompilacionToolStripMenuItem.Checked = false;
                hideCompilationStatusWindow();
            }
        }


        public void hideCompilationStatusWindow()
        {
            editionContainer.Panel2Collapsed = true;
            editionContainer.Panel2.Hide();

            progresoDeCompilacionToolStripMenuItem.Checked = false;
        }
        public void showCompilationStatusWindow()
        {
            editionContainer.Panel2Collapsed = false;
            editionContainer.Panel2.Show();
            progresoDeCompilacionToolStripMenuItem.Checked = true;
        }
        public void hideErrorStatusWindow()
        {
            mainSplitContainer.Panel2Collapsed = true;
            mainSplitContainer.Panel2.Hide();

            erroresDeCompilacionToolStripMenuItem.Checked = false;
        }
        public void showErrorStatusWindow()
        {
            mainSplitContainer.Panel2Collapsed = false;
            mainSplitContainer.Panel2.Show();

            erroresDeCompilacionToolStripMenuItem.Checked = true;
        }

        public void hideFilesWindow()
        {
            fileContainer.Panel1Collapsed = true;
            fileContainer.Panel1.Hide();
        }
        public void showFilesWindow()
        {
            fileContainer.Panel1Collapsed = false;
            fileContainer.Panel1.Show();
        }

        private void erroresDeCompilacionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!erroresDeCompilacionToolStripMenuItem.Checked)
            {
                erroresDeCompilacionToolStripMenuItem.Checked = true;
                showErrorStatusWindow();
            }
            else
            {
                erroresDeCompilacionToolStripMenuItem.Checked = false;
                hideErrorStatusWindow();
            }
        }

       /* private void gestorDeArchivosToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!gestorDeArchivosToolStripMenuItem.Checked)
            {
                gestorDeArchivosToolStripMenuItem.Checked = true;
                showFilesWindow();
            }
            else
            {
                gestorDeArchivosToolStripMenuItem.Checked = false;
                hideFilesWindow();
            }
        }*/

        private void guardarComoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "Any File (*.*) | *.*";
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                string pathToSaveFile = saveFileDialog.FileName;
                CodeTabPage tabPage = (CodeTabPage) codeTabControl.SelectedTab;
                tabPage.saveFile(pathToSaveFile);
                enableCompilationButtons();
            }
        }

        public TabPage getCurrentTab()
        {
            return codeTabControl.SelectedTab;
        }

        public void setColumnOnLabel(int col)
        {
            this.statusColsLabel.Text = "Col: " + col;
        }
        public void setRowOnLabel(int row)
        {
            this.statusLinesLabel.Text = "Lín: " + row + this.generateSpaces(10);
        }

        
        private string generateSpaces(int number ){ 
            StringBuilder builder = new StringBuilder();
            for(int i = 0; i < number ; i++) {
                builder.Append(" ");
            }
            return builder.ToString();
        }

        private void calculateToolBarLabelsPosition()
        {
            toolStripSpacement1.Text = this.generateSpaces(Convert.ToInt32(Math.Floor(this.Width / 4.6)));
        }

        private void windowResized(object sender, EventArgs e)
        {
            calculateToolBarLabelsPosition();
        }

        private void ListDirectory(TreeView treeView, string path)
        {
            treeView.Nodes.Clear();
            var rootDirectoryInfo = new DirectoryInfo(path);
            treeView.Nodes.Add(CreateDirectoryNode(rootDirectoryInfo));
        }

        private static TreeNode CreateDirectoryNode(DirectoryInfo directoryInfo)
        {
            var directoryNode = new TreeNode(directoryInfo.Name);
            try
            {

            foreach (var directory in directoryInfo.GetDirectories())
                directoryNode.Nodes.Add(CreateDirectoryNode(directory));
            foreach (var file in directoryInfo.GetFiles())
                directoryNode.Nodes.Add(new TreeNode(file.Name));
            }
            catch (Exception ex) { MessageBox.Show(ex.ToString()); }
            
            return directoryNode;
        
            }

        private void openFile(object sender, TreeNodeMouseClickEventArgs e)
        {
            MessageBox.Show(File.Exists(BASE_PATH+e.Node.FullPath).ToString());
        }

        private void guardarToolStripMenuItem_Click(object sender, EventArgs e)
        {
            CodeEditor codeEditor = ((CodeTabPage)codeTabControl.SelectedTab).getCodeEditor();
            if (!codeEditor.hasPath())
            {
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "Any File (*.*) | *.*";
                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    string pathToSaveFile = saveFileDialog.FileName;
                    CodeTabPage tabPage = (CodeTabPage)codeTabControl.SelectedTab;
                    tabPage.saveFile(pathToSaveFile);
                    enableCompilationButtons();
                }
            }
            else
            {
                codeEditor.saveFile();
            }

        }

        public ContextMenuStrip getContextMenuStrip1()
        {
            return this.contextMenuStrip1;
        }


        private void cerrarActualToolStripMenuItem_Click(object sender, EventArgs e)
        {
            codeTabControl.TabPages.Remove(codeTabControl.SelectedTab);
            if (codeTabControl.TabCount == 0)
            {
                cerrarActualToolStripMenuItem.Enabled = false;
                guardarToolStripMenuItem.Enabled = false;
                guardarComoToolStripMenuItem.Enabled = false;
                pictureBox3.Enabled = false;
                pictureBox4.Enabled = false;
                pictureBox3.Cursor = Cursors.Cross;
                pictureBox4.Cursor = Cursors.Cross;
            }
        }
        private void enableFileActionButtons()
        {
            cerrarActualToolStripMenuItem.Enabled = true;
            guardarToolStripMenuItem.Enabled = true;
            guardarComoToolStripMenuItem.Enabled = true;
            pictureBox3.Enabled = true;
            pictureBox4.Enabled = true;
            pictureBox3.Cursor = Cursors.Hand;
            pictureBox4.Cursor = Cursors.Hand;
        }

        private void pictureBox4_MouseEnter(object sender, EventArgs e)
        {

            PictureBox senderImage = (PictureBox)sender;
            senderImage.BackColor = Color.Gray;
        }

        private void pictureBox4_MouseLeave(object sender, EventArgs e)
        {

            PictureBox senderImage = (PictureBox)sender;
            senderImage.BackColor = SystemColors.ActiveCaptionText;
        }
        public ToolStripMenuItem getSaveToolButton()
        {
            return this.guardarToolStripMenuItem;
        }

        public PictureBox getSaveButton()
        {
            return pictureBox3;
        }

        public void setLines(int l)
        {
            this.toolStripStatusLabel.Text = "Lineas: " + l;
        }

        private void showCompillingView(object sender, EventArgs e)
        {
            showCompilationStatusWindow();
        }
        private void runLexico(object sender, EventArgs e)
        {
            runLexico();
        }

        private void runLexico()
        {
            CodeTabPage tabPage = (CodeTabPage)codeTabControl.SelectedTab;
            Process process = new Process();
            CheckForIllegalCrossThreadCalls = false;
            process.StartInfo.FileName = @"cmd";
            process.StartInfo.Arguments = "/c tinypp -l \"" + tabPage.getCodeEditor().getPath() + "\"";
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.CreateNoWindow = true;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;


            process.ErrorDataReceived += new DataReceivedEventHandler(OutputHandler);
            process.Start();
            //* Read one element asynchronously
            process.BeginErrorReadLine();
            //* Read the other one synchronously
            string output = process.StandardOutput.ReadToEnd();
            lexerOutTextBox.Text += output;

            process.Close();
        }
        void OutputHandler(object sendingProcess, DataReceivedEventArgs outLine)
        {
                string line = outLine.Data;
                Console.WriteLine(line);
                this.BeginInvoke(new MethodInvoker(() =>
                {
                    lexerErrTextBox.AppendText(outLine.Data+"\n" ?? string.Empty);
                }));
            
        }
        private void codeTabControl_SelectedIndexChanged(object sender, EventArgs e)
        {
            
            CodeTabPage tabPage = (CodeTabPage)codeTabControl.SelectedTab;
            if (tabPage != null && tabPage.getCodeEditor().hasPath())
            {
                enableCompilationButtons();
            }
            else
            {
                disableCompilationButtons();
            }
        }

    }

   
}
