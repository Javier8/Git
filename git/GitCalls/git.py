# -*- coding: utf-8 *-*
import subprocess
import os
import re

class Git():

    def __init__(self):


        self.staged = {"M":set(),"A":set(),"D":set()}

        self.no_staged = {"M":set(),"?":set(),"D":set()}


        self.files_text = {}

    def init(self,path):

        run_dir = os.getcwd()
        os.chdir(path)
        check = subprocess.check_output(['git','init'])
        os.chdir(run_dir)

        return check

    def check_git(self,path):

        run_dir = os.getcwd()
        os.chdir(path)
        check = subprocess.call(['git','status'])
        os.chdir(run_dir)

        if check == 0:
            return True
        else:
            return False


    def status(self,path):

        p = os.getcwd()
        os.chdir(path)
        call = subprocess.check_output(["git","status","--porcelain"])
        os.chdir(p)

        pattern = re.compile("(.)([^ ])?  ?(.*)")

        data = pattern.findall(call)

        print data

        for changes in data:

            if changes[0] == ' ':

                self.no_staged[changes[1]].add(changes[2])

            elif changes[0] == '?':
                self.no_staged[changes[0]].add(changes[2])

            elif changes[1] == '':
                self.staged[changes[0]].add(changes[2])
            else:

                self.staged[changes[0]].add(changes[2])
                self.no_staged[changes[1]].add(changes[2])


    def text(self,path,file,state=False,file_text=False):



        file_text = unicode(file_text).splitlines()
        source = ""
        source_info = {}
        n = 0


        p = os.getcwd()
        os.chdir(path)

        if state:
            call = subprocess.check_output(["git","diff",state,file])
        else:
            call = subprocess.check_output(["git","diff",file])

        os.chdir(p)

        text = False

        for line in call.splitlines():

            if line.startswith("@"):
                text = True
                pattern = r"@@ .(\d+),(\d+) .(\d+),(\d+) @@"
                s = re.compile(pattern)
                pos = s.search(line).groups()
                current = int(pos[2])-1
                continue


            if text == True:

                if line.startswith('+'):


                    source_info[current] = '+'
                    source += line[1:]
                    file_text[current] = line[1:]
                elif line.startswith('-'):

                    source_info[current] = '-'
                    source +=line[1:]
                    file_text.insert(current,line[1:])


                else:
                    source_info[current] = '='
                    source += line[1:]
                    file_text[current] = line[1:]

                source+="\n"
                n+=1
                current += 1

        final =""
        for t in file_text:
            final+=t.decode("utf-8")+"\n"
        return(source,source_info,final)

    def add(self,path,file):

        p = os.getcwd()
        os.chdir(path)
        call = subprocess.check_output(["git","add",file])
        os.chdir(p)

    def unstage(self,path,file):

        p = os.getcwd()
        os.chdir(path)
        call = subprocess.check_output(["git","checkout","--",file])
        os.chdir(p)

    def commit(self,path,file,msg):


        p = os.getcwd()
        os.chdir(path)
        call = subprocess.call(["git","commit",file,'-m',msg])
        os.chdir(p)

    def uncommit(self,path,file):


        p = os.getcwd()
        os.chdir(path)
        call = subprocess.call(["git","reset","HEAD",file])
        os.chdir(p)


    def branch(self,path):

        p = os.getcwd()
        os.chdir(path)
        call = subprocess.check_output(["git","branch"])
        os.chdir(p)

        branches = []

        for x in call.splitlines():

            if x.startswith("*"):
                branches.insert(0,x[2:])

            else:
                branches.append(x[2:])

        return branches

    def change_branch(self,path,branch):

        p = os.getcwd()
        os.chdir(path)
        call = subprocess.call(["git","checkout",branch])
        os.chdir(p)



    def add_branch(self,path,branch):


        p = os.getcwd()
        os.chdir(path)
        call = subprocess.call(["git","branch",branch])
        os.chdir(p)


    def delete_branch(self,path,branch):

        if branch != "master":
            p = os.getcwd()
            os.chdir(path)
            call = subprocess.call(["git","branch","-d",branch])
            os.chdir(p)
            if call ==1:
                return "Branch ''{0}'' not fully merged".format(branch)
    def merge_branches(self,path,branch):


        p = os.getcwd()
        os.chdir(path)
        call = subprocess.call(["git","merge",branch])
        os.chdir(p)
        if call == 1:
            return "Cant merge branches"

    def force_delete_branch(self,path,branch):

        if branch != "master":
            p = os.getcwd()
            os.chdir(path)
            call = subprocess.call(["git","branch","-D",branch])
            os.chdir(p)
