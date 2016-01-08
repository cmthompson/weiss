import re
import tkFileDialog

reference_list = []



class Reference(dict):
 
    def __init__(self,**kwargs):
        
        dict.__init__(self,**kwargs)
        
        if not self.has_key('reftype'):
            self['reftype'] = 'ARTICLE'
        if self['reftype'] == 'BOOK':
            self.required_keys = ['authors','title','publisher','year']
        elif self['reftype'] =='ARTICLE':
            self.required_keys = ['authors','title','journal', 'volume', 'number','pages','year']
        else:
            self['reftype'] == 'ARTICLE'
            self.required_keys = ['authors','title','journal', 'volume', 'number','pages','year']
        for k in self.required_keys:
            if k not in self.keys():
                
                self[k] = ""
              
            

        return None
    def isthesameas(self,other):
        chance=0
        if self['reftype'] != other['reftype']:
            return False
        if self['key'] != other['key']:
            return False
        if self['reftype'] =='journal':
            if ref['year'] == ref2['year'] and ref['journal'].upper() == ref2['journal'].upper():
                return True
        
        for i in self.keys():
            if self[i] == other[i]:
                chance +=1
        if chance>4:
            return True
        else:
            return False
        
    def format_bibtex(self):
        tex = str()
        
    
        if self['reftype']=='BOOK':
            tex +=str('@'+self['reftype']+'{'+self['key']+',\n'
            +'AUTHOR = {'+self['authors']+'},\n'
            +'TITLE = "'+self['title']+'",\n'
            +'PUBLISHER = "'+self['publisher']+'",\n'
            +'YEAR = "'+self['year']+'",\n'
            +'}'+'\n'+'\n')
            
        elif self['reftype']=='ARTICLE':
            
    
            tex +=str('@'+self['reftype']+'{'+self['key']+',\n')
            
           
            tex+='AUTHOR = {'+self['authors']+'},\n'
            for x in self.required_keys[1:]:
                if self[x] !='':
                    tex+= str(x.upper()+' = "'+self[x]+'",\n')
#            if self['title']!='':
#                tex+='TITLE = "'+self['title'].title()+'",\n'
#            if self['journal']!='':
#                tex+='JOURNAL = "'+self['journal'].title()+'",\n'
#            if self['volume'!=]
#            +'VOLUME = "'+self['volume']+'",\n'
#            +'NUMBER = "'+self['number']+'",\n'
#            +'PAGES = "'+self['pages']+'",\n'
#            +'YEAR = "'+self['year']+'",\n'
            tex+= str('}'+'\n'+'\n')
        
    
        return tex
            
    def format_name(self,author):
        
        last = author.rsplit(',')[0]
        firstandmiddle = author.rsplit(',')[1].rsplit(' ')
        firstandmiddle.remove('')
        firstandmiddle.pop()
       
        
         
        name = (last,)
        
        inits = ""
        for p in firstandmiddle:
            
            inits += p[0]+"."
        name = name+ (inits,)
        
        return name
    def generate_tag(self):
        first_author = self.authors[0]
        
        tag = first_author[0:3]+self.year[-2:-1]
        return tag

    
    def format_HTML(self):
    
        namelist = ""
        for author in self.authors:
            name = self.format_name(author)
            
            namelist += "<b:Person><b:Last>"+name[0]+"</b:Last><b:First>"+name[1]+"</b:First></b:Person>"
        html =("<b:Source><b:Tag>"+self.generate_tag()+
               "</b:Tag><b:SourceType>JournalArticle</b:SourceType><b:Guid>{7517F6A7-E302-4D78-A2D5-749453596A1C}</b:Guid><b:Author><b:Author><b:NameList>"+
               namelist+"</b:NameList></b:Author></b:Author><b:Title>"+self.title+"</b:Title><b:JournalName>"+self.journal+"</b:JournalName><b:Year>"+self.year+
               "</b:Year><b:Pages>"+self.pages+"</b:Pages><b:Volume>"+self.volume+"</b:Volume><b:Issue>"+self.issue+"</b:Issue></b:Source>")
      
        return html

    
        
def WebtoRef(fname):
    import pdb
    f = open(fname,'r')
    text = f.read()
    text = text.split('\nER')
   
    
    
    reference_list = []
    
    
    #pdb.set_trace()    
    for r in text[:-1]:
        
        au = r.find('\nAU ')
        af = r.find('\nAF ')
        ti = r.find('\nTI ')
        so = r.find('\nSO ')
        vl = r.find('\nVL ')
        iss = r.find('\nIS ')
        bp = r.find('\nBP ')
        ep = r.find('\nEP ')
        di = r.find('\nDI ')
        pd = r.find('\nPD ')
        py = r.find('\nPY ')
        tc = r.find('\nTC ')
        zb = r.find('\nZB ')
        z8 = r.find('\nZ8 ')
        zs = r.find('\nZS ')
        z9 = r.find('\nZ9 ')
        sn = r.find('\nZN ')
        ut = r.find('\nUT ')
        
         
        if af == -1:
            authors = r[au+4:ti].replace('\n ',' and').title()
        if af !=-1:
            authors = r[au+4:af].replace('\n ',' and').title()
        title = r[ti+4:r.find('\n',so)].replace('\n','')
        journal = r[so+4:r.find('\n',so+1)]
        volume = r[vl+4:r.find('\n',vl+1)]
        number = r[iss+4:r.find('\n',iss+1)]
        pages = r[bp+4:r.find('\n',bp+1)]+'-'+r[ep+4:r.find('\n',ep+1)]
        doi = r[di+4:r.find('\n',di+1)]
        year = r[py+4:py+8]
        
        ref = Reference(authors = authors,
                     title = title,
                    journal = journal,
                    year = year,
                    volume = volume,
                    number = number,
                    pages = pages)
    
        reference_list.append(ref)
    return reference_list
        
        
        
    

def BibToRef(text):
    
    ref_list = list()
    text = text.rsplit('@')
    
    for source in text[1:]:
        
        start = 0
        end = source.find('{')
        reftype = source[start:end]
       
        ref = Reference(reftype = reftype)
        
        
        start = end+1
        end = source.find(',',start)
        ref['key'] = source[start:end]
    
        for k in ref.keys():
            
            if k == 'key' or k == 'reftype':
                continue
            elif k == 'authors':
                startline = source.find('AUTHOR')
                if startline == -1:
                    continue
                start = source.find('{',startline)+1
                end = source.find('}',start)
                ref['authors'] = source[start:end]
            elif k == 'number':
                startline = source.find("ISSUE")
                if startline == -1:
                    continue
                start = source.find('{',startline)+1
                end = source.find('}',start)
                ref['number'] = source[start:end]
            else:
                startline = source.find(k.upper())
                if startline == -1:
                    continue
                start = source.find('"',startline)+1
                end = source.find('"',start)
             
                ref[k] = source[start:end].title()
                
        for ref2 in ref_list:
            if ref2.isthesameas(ref): ### Checking for duplicates
                break
        else:
            ref_list.append(ref)
 
    return ref_list

def WordtoTEX(fname):
    import pdb
    reference_list = []
    with open(fname,'r+b') as f:

        text = f.read()
        text = text.rsplit('<b:Source>')
       
        print 'number of sources', len(text)
        for source in text[1:]:
            
            tag = ReadNextHTML(source,'Tag')
            sourcetype = ReadNextHTML(source,'SourceType')
            person = ReadNextHTML(source,'Person')
            author_list = []
            loc = 0
            i = 0
            while person !='':
                
                last = ReadNextHTML(person,'Last')
                
                    
                
                first = ReadNextHTML(person,'First')
                middle = ReadNextHTML(person,'Middle')
                if ' ' in last:
                    print 'modified entry'
                    middle = first+middle
                    first = last.rsplit(' ')[1]
                    last = last.rsplit(' ')[0]
                    
                    
                
               
                author_list.append(last+','+first+middle)
                loc = source.find(last, loc)+1
                
               
                person = ReadNextHTML(source,'Person',startat = loc)
                i+=1
                if i > 50:
                                       
                    print 'exit'
                    break
                
                
                
            title = ReadNextHTML(source,'Title')
            journal = ReadNextHTML(source,'JournalName')
            year = ReadNextHTML(source,'Year')
            pages = ReadNextHTML(source,'Pages')
            issue = ReadNextHTML(source,'Issue')
            volume = ''
            key = author_list[0][0:4]+year
            
            print "update reference usage"
            ref = Reference(authors = author_list,
                     title = title,
                    journal = journal,
                    year = year,
                    volume = volume,
                    number = number,
                    pages = pages,
                    key=key)
            reference_list.append(ref)
        
                
        
        
  
        f.close()
    #text = text.rsplit('<b:Source>')
    
    return reference_list
    
def RefToBibTex(ref_list):
    tex = str()
    #for ref in ref_list:
        #for ref2 in ref_list[ref_list.index(ref)+1:]:
            #if ref.isthesameas(ref2):
                #ref_list.remove(ref2)
    for ref in ref_list:
        tex +=ref.format_bibtex()
    return tex
        
        
        
        
        

def ReadNextHTML(mm, _class,startat= 0):
    
    start =  mm.find('<b:'+_class+'>',startat)
    if start != -1:
        start+=len(_class)+4
    else:
        return ''
    
    
    end =  mm.find('</b:'+_class+'>',start)
   
    i = mm[start:end]
    
    return i
    
    
#
#a = WebtoRef('/home/chris/Dropbox/sources_wang')


#RefToBibTex(a,'/home/chris/Dropbox/Thesis/SFG Theory/SFGTheoryBib2.bib')

def test():
    f = open('/home/chris/Dropbox/SFGTheory.bib')
    text = f.read()
    f.close()
    a = BibToRef(text)
    print a
    return a

def uncap():
    import os
    
    file_list = ['Ch1_SFGTheory/SFGTheory.bib',
                 'Ch2_Experimental/ExpBib.bib',
                 'Ch3_IPAChapter/Thesis_IPA.bib',
                 'Ch4_EthanolChapter/EthanolBib.bib',
                 'Ch5_InductionChapter/InductionBib.bib',
                 'Ch6_UVParticles/Particles.bib',
                 'Ch7_GasLiquid/Orientation.bib',
                 'Ch8_Biointerfaces/Holingabib.bib']
    os.chdir('C:/Users/Chris/Dropbox/Thesis')            
    for f in file_list:
        try:
            r = open(f,'r')
            text = r.read()
            r.close()
            x = BibToRef(text)
            for i in x:
                if 'journal' in i.keys():
                    i['journal'] = i['journal'].title()
            
            
            l = RefToBibTex(x)
            print len(x), x[0]['journal']
            r = open(f,'w')
            r.write(l)
            r.close()
        except:
            print 'error in',  f
    return 0
    
#def CreateBib():
#    
#    import os
#    
#    file_list = ['Ch1_SFGTheory/SFGTheory.',
#                 'Ch2_Experimental/ExpBib.bib',
#                 'Ch3_IPAChapter/Thesis_IPA.bib',
#                 'Ch4_EthanolChapter/EthanolBib.bib',
#                 'Ch5_InductionChapter/InductionBib.bib',
#                 'Ch6_UVParticles/Particles.bib',
#                 'Ch7_GasLiquid/Orientation.bib',
#                 'Ch8_Biointerfaces/Holingabib.bib']
#    os.chdir('C:/Users/Chris/Dropbox/Thesis')       
#        
#    
#    for filename in file_list:
#        
#        f = open(filename, 'rb' )
#        source = f.read()
#        f.close()
#        start = 0
#        progress = -1
#        
#        tag_list = set()
#        while True:
#            
#            start = source.find('~\cite{',start)+7
#            if start == -1:
#                break
#            elif progress>start:
#                break
#            
#            end = source.find('}',start)
#            if end == -1:
#                print "found problem"
#            if end<start:
#                print "got to end"
#                return 0
#            
#            for a in source[start:end].split(','):
#               
#                tag_list.add(a.replace(' ',''))
#                
#            progress = start
#        
#        new_bib = list()
#          
#        for tag in tag_list:
#            for ref in self.bibliography:
#                if ref['key']==tag:
#                    new_bib.append(ref)
#                    break
#            else:
#                print "could not find", tag
#            
#        start = source.find('\bibliography{')+14
#        if start == -1:
#            break
#
#        end = source.find('}',start)
#        if end == -1:
#            print "found problem"
#       
#        
#        n = str('C:/Users/Chris/Dropbox/Thesis' + source[start:end]+'.bib')
#        
#           
#        f = open(n,'w')
#        
#        f.write(RefToBibTex(new_bib))
#          
#        f.close()
#    print 'Wrote bibtex', n
#    return new_bib
#            
#    
#    
#        
#

