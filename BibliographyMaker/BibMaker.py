# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 13:31:02 2014
create a bibliography
@author: Chris
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from Tkinter import *
import tkFileDialog, tkSimpleDialog
from urllib2 import urlopen
from bib_reformat import Reference, RefToBibTex,WebtoRef,BibToRef
import threading
import pickle
import re
import os
import Tkinter

Literature = "/home/chris/Documents/Literature"

os.chdir(Literature)

class Win:
    
    def __init__(self,master):
        self.master = master
        self.frame = Frame(master = self.master, width = 100)
        self.frame.grid()
        
        self.menubar = Tkinter.Menu(self.master)
        
        self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Create Bib for Tex file", command =  self.CreateBib)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.master.config(menu= self.menubar)
        
        self.ebutton = Button(self.frame, text = 'Select PDF', command = self.AddPDF)
        self.ebutton.grid()
        
        self.deletebutton = Button(self.frame, text = 'delete citation', command = self.DeleteCitation)
        self.deletebutton.grid()
        
        self.savebutton = Button(self.frame,text = "savebibliography", command = self.WriteBib)
        self.savebutton.grid()
        
        self.loadbutton = Button(self.frame, text = "loadbibliography", command = self.LoadBib)
        self.loadbutton.grid()
        
        self.editbutton = Button(self.frame, text = "editbibliography", command = self.EditCitation)
        self.editbutton.grid(row = 0,column = 1)
        
        self.loadwebbutton = Button(self.frame, text = 'Load Web', command = self.LoadWeb)
        self.loadwebbutton.grid(row  = 1, column =1)
        
        self.addbutton = Button(self.frame, text = 'Add Citation', command = self.AddCitation)
        self.addbutton.grid(row = 2, column = 1)
        self.bibliography = []
        self.bibpath = ''
        
        

        self.list_var = StringVar()
        
        self.listframe = Frame(self.master)
        self.listframe.grid(row = 4, column = 0, columnspan = 5,padx = 10,pady=10)
        self.list = Listbox(self.listframe, listvariable = self.list_var, width = 50,height = 30)
        self.list.pack(side = LEFT)
        
        self.scrollbar = Scrollbar(self.listframe)
        self.scrollbar.pack(side = RIGHT,fill = Y)
        
        self.list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list.yview)
        return None
    def AddPDF(self):
        import pdb
        options = {}
        options['defaultextension'] = '.pdf'
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = Literature
        options['multiple'] = True
        options['title'] = 'Open PDF...'
        options['parent'] = self.master
        

        str_name_list = tkFileDialog.askopenfilenames(**options)
        if str_name_list != '':
            self.lookup(str_name_list)
        return 0
        
       
    def lookup(self,str_name_list):
        if type(str_name_list) == tuple:
            str_name_list = list(str_name_list)
            print str_name_list
        elif type(str_name_list) == unicode:
            str_name_list = str_name_list.encode('unicode_escape')
            
            str_name_list = re.split('} {',str_name_list)
            
            for x in range(len(str_name_list)):
                str_name_list[x] = str_name_list[x].replace('{','')
                str_name_list[x] = str_name_list[x].replace('}','')
                
            
        else:
            print 'error in open string'
            
        self.bibliography = list()
            
        for name in str_name_list:
            
            
            docstring = convert_pdf_to_txt(name)
            if docstring != -1:
                doi = return_doi(docstring)
                if doi== -1:

                    doi = tkSimpleDialog.askstring("Enter DOI","PDF not properly converted.  Enter DOI. Enter nothing to skip.")
                    if doi == ''or doi==None:
                        ref = Reference('skip___'+name,'','','', '', '' ,'')
                else:
                    html = citation_search(doi)
                    if html!=-1:
                        ref = create_reference(html)
                    else:
                        print "citation search failed", name
                         # (authors,title,journal,year,volume,issue,pages)
                        ref = Reference('unknown___'+name,'','','', '', '' ,'')
                        
            else:
                doi = tkSimpleDialog.askstring("Enter DOI","DOI not found in PDF.  Enter DOI. Enter nothing to skip.")
                if doi == '' or doi == None:
                    ref = Reference('unknown___'+name,'','','', '', '' ,'')
                else:
                    html = citation_search(doi)
                    if html!=-1:
                        ref = create_reference(html)
                    else:
                        print "citation search failed", name
                        ref = Reference('','skip___'+name,'','', '', '' ,'')

            ref.filepath = name
            ref.url = name
            self.bibliography += [ref]

            self.list.insert(END,ref['title'])
        print "done"
        return 0
        
    def WriteBib(self):
        options = {}
        options['defaultextension'] = '.bib'
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = 'C:/Users/Chris/Dropbox/Thesis'
        
        options['title'] = 'Save bib...'
        options['parent'] = self.master
        
        n = tkFileDialog.asksaveasfilename(**options)
        if n == '':
            return 0
        f = open(n,'w')

        f.write(RefToBibTex(self.bibliography))
      
        f.close()
        print 'Wrote bibtex', n
        
        return 0
    def DeleteCitation(self):
        i = self.list.curselection()
        for r in i:
            self.list.delete(int(r))
            del self.bibliography[int(r)]
           
            
        return 0
    def SaveBib(self):
        
        options = {}
        options['defaultextension'] = '.bib'
        options['filetypes'] = [('all files', '.*')]
        if self.bibpath == '':
            options['initialdir'] = 'C:/Users/Chris/Dropbox/Thesis'
        else:
            options['initialdir'] = os.path.dirname(self.bibpath)
        
        options['title'] = 'Save bib file...'
        options['parent'] = self.master
        
        n = tkFileDialog.asksaveasfilename(**options)
        if n !='':
        
            threading.Thread(target = self.savebibthread, args = (n,)).start()
        return 0
    def savebibthread(self, filename):
        f = open(filename,'r')
        text = f.read()
        f.close()
        self.bibliography = BibToRef(text)
        for i in self.bibliography:
            self.list.insert(END,i['authors'])
        
            
        

        print "loaded from", filename
        return 0
        
    def LoadBib(self):    
        import re
        options = {}
        options['defaultextension'] = '.pyb'
        options['filetypes'] = [('all files', '.*')]
        options['multiple'] = False
        options['title'] = 'Open RRResults...'
        options['parent'] = self.master
        options['initialdir'] = 'C:/Users/Chris/Dropbox/Thesis'
    
        
        filename = tkFileDialog.askopenfilename(**options)
        
        if filename != '':
            self.bibpath = filename
            athread = threading.Thread(target = self.loadbibthread, args = (filename,))
            athread.daemon = True 
            athread.start()
        return 0
    def loadbibthread(self,filename):

        f = open(filename,'r')
        text = f.read()
        f.close()
        
        
        
        number_of_repeated_sources = 0
        number_of_new_sources = 0
        for a in BibToRef(text):
            
            for x in self.bibliography:
                if a.isthesameas(x):
                   
                    number_of_repeated_sources += 1
                    break
            else:
                number_of_new_sources +=1
                self.bibliography.append(a)
                self.list.insert(END,a['authors'])
        print "Added", number_of_new_sources, "new sources."
        print "Found", number_of_repeated_sources, "repeats."
        

        print "loaded from", filename

        return 0
        
    def CreateBib(self):
        
        options = {}
        options['defaultextension'] = '.pyb'
        options['filetypes'] = [('all files', '.*')]
        options['multiple'] = False
        options['title'] = 'Open RRResults...'
        options['parent'] = self.master
        options['initialdir'] = 'C:/Users/Chris/Dropbox/Thesis'
    
        
        filename = tkFileDialog.askopenfilename(**options)
        
        if filename == '':
            return -1
            
        f = open(filename, 'rb' )
        source = f.read()
        f.close()
        start = 0
        progress = -1
        
        tag_list = set()
        while True:
            
            start = source.find('~\cite{',start)+7
            if start == -1:
                break
            elif progress>start:
                break
            
            end = source.find('}',start)
            if end == -1:
                print "found problem"
            if end<start:
                print "got to end"
                return 0
            
            for a in source[start:end].split(','):
               
                tag_list.add(a.replace(' ',''))
                
            progress = start
        
        new_bib = list()
      
        for tag in tag_list:
            for ref in self.bibliography:
                if ref['key']==tag:
                    new_bib.append(ref)
                    break
            else:
                print "could not find", tag
            
        
        n = 'C:/Users/Chris/Dropbox/Thesis/Newbib.bib'#tkFileDialog.asksaveasfilename(**options)
        if n == '':
            return 0
        f = open(n,'w')

        f.write(RefToBibTex(new_bib))
      
        f.close()
        print 'Wrote bibtex', n
        return new_bib
                
     
        
    def EditCitation(self):
        i = int(self.list.curselection()[0])
        
            
        self.top = Tkinter.Toplevel()
        self.top.title("Edit Citation")
        self.frame= Tkinter.Frame(master = self.top,width=200, height=300)
        self.frame.pack(expand =True)
        
        
        self.menubar = Tkinter.Menu(self.top)
        
        self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Save", command =  lambda: self.SaveCitation(i))
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.top.config(menu= self.menubar)
  
        self.t_var = StringVar()
        
        self.t = Tkinter.Text(self.frame)
        self.t.pack(side = Tkinter.LEFT)
        
        
        ref = self.bibliography[i]
 

        a = RefToBibTex([ref]) 
        self.t.delete(1.0,END)             
        self.t.insert(0.0,a)
        
        return 0
        
    def AddCitation(self):
        
        self.top = Tkinter.Toplevel()
        self.top.title("Edit Citation")
        self.frame= Tkinter.Frame(master = self.top,width=200, height=300)
        self.frame.pack(expand =True)
        
        
        self.menubar = Tkinter.Menu(self.top)
        
        self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Save", command =  lambda: self.SaveCitation(END))
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.t_var = StringVar()
        
        self.t = Tkinter.Text(self.frame)
        self.t.pack(side = Tkinter.LEFT)
        
        self.top.config(menu= self.menubar)
  
        return 0
    def SaveCitation(self,i):
         if i == END:
             ref = BibToRef(self.t.get(0.0,END))[0]

             self.bibliography.append(ref)

             self.list.insert(END,ref['authors'])
         
         else:
             ref = BibToRef(self.t.get(0.0,END))[0]
             self.bibliography[i]=ref
             
             self.list.delete(i)
             self.list.insert(i,ref['authors'])
         self.top.destroy()
        
        
         
         return 0
    def LoadWeb(self):
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = 'C:/Users/Chris/Dropbox/Thesis'
        
        options['title'] = 'Load web file...'
        options['parent'] = self.master
        
        n = tkFileDialog.askopenfilename(**options)
        if n !='':
        
            number_of_repeated_sources = 0
            number_of_new_sources = 0
            for a in WebtoRef(n):
                goahead = True
                for x in self.bibliography:
                    if a['title'] == x['title']:
                        goahead = False
                        
                        number_of_repeated_sources += 1
                        break
                if goahead == True:
                    number_of_new_sources +=1
                    self.bibliography.append(a)
                    self.list.insert(END,a['authors'])
            print "Added", number_of_new_sources, "new sources."
            print "Found", number_of_repeated_sources, "repeats."
               
            
        return 0


        
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 1
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    out= retstr.getvalue()
    retstr.close()
    return out
    
#def convert_pdf(path):
#    
#    rsrcmgr = PDFResourceManager()
#    retstr = StringIO()
#    codec = 'utf-8'
#    laparams = LAParams()
#    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#
#    fp = file(path, 'rb')
#    process_pdf(rsrcmgr, device, fp)
#    fp.close()
#    device.close()
#
#    str = retstr.getvalue()
#    retstr.close()
#
#    return str
    
def return_doi(docstring):
    
    x = docstring.find('10.')
    y = docstring.find(' ', x)
    
    if x==-1:
        return '-1'
    
    if docstring[x+7]== '/':
        doi = docstring[x:y]
    else:
        return '-1'

    return doi

def citation_search(doi):
    
    rootstring = 'http://rd8hp6du2b.search.serialssolutions.com/?sid=sersol%3ARefinerQuery&citationsubmit=Search&url_ver=Z39.88-2004&l=RD8HP6DU2B&rfr_id=info%3Asid%2Fsersol%3ARefinerQuery&SS_LibHash=RD8HP6DU2B&SS_ReferentFormat=JournalFormat&rft_id=info%3Adoi%2F'#10.1021%2Fjp305539v&rft.genre=article
    doistring  = doi.replace('/','%2F')
    
    
    fullurl = rootstring+doistring
    response = urlopen(fullurl)
    html= str(response.read())
   
    return html
    
def create_reference(html):
    
    value_list = {"title":None,
                  "SS_authors":None,
                  "date":None,
                  "issue":None,
                  "volume":None,
                  "spage":None,
                  "atitle":None,
                  "genre":None,
                  "doi":None,
                  "pages":None
                  }
    
    for key in value_list.keys():
        x = html.find( '<input type="hidden" name="'+key+'" value="')
        if x == -1:
            x = html.find( 'rft.'+key+'=')
            if x ==-1:     
                print 'not found'
                pass
            else:
                y = html.find('&amp',x)
                value_list[key] = html[x:y]
        else:
            y = html.find('" />',x)
            value_list[key] = html[x+36+len(key):y]
       
        
       # (authors,title,journal,year,volume,issue,pages)
    ref = Reference(authors = value_list['SS_authors'],
                     title = value_list['atitle'],
                    journal = value_list['title'],
                    year = value_list['date'],
                    volume = value_list['volume'],
                    number = value_list['issue'],
                    pages = value_list['pages'])
    
    return ref
 

def RenameACSTitle():
    import os
    os.chdir('/home/chris/Desktop/Ppaers')
    for i in os.listdir('.')[0:2]:
        doi = i.replace('.pdf','')
        if len(doi) == 9:
            z = citation_search(doi)
            
            return z
            newname = create_reference(z)['title']
            
            if newname != '':
                print i,newname
                #os.rename(i,newname)
            
   
    return 0
           
   

#root = Tk()
#win = Win(root)
#root.mainloop()

    

