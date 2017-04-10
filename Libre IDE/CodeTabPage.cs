using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Libre_IDE
{
    class CodeTabPage : TabPage
    {
        private CodeEditor codeEditor;
        private MainForm mainForm;
        public CodeTabPage(string title,MainForm mainForm) {

            this.Text = title;

            this.codeEditor = new CodeEditor(mainForm);

            this.Controls.Add(codeEditor);

            this.mainForm = mainForm;
            
        }

        public CodeTabPage(string path, bool withFile,MainForm mainForm)
        {
            // TODO: Complete member initialization

            this.codeEditor = new CodeEditor(path,mainForm);

            this.Text = codeEditor.getName();

            this.Controls.Add(codeEditor);

            this.mainForm = mainForm;
        
        }

        public void saveFile(string tabPage)
        {
            codeEditor.saveFile(tabPage);
            this.Text = codeEditor.getName();
        }

        internal CodeEditor getCodeEditor()
        {
            return this.codeEditor;
        }

    }
}
