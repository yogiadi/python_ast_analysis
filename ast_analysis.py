import ast, sys, re, os
from pprint import pprint as pp


def main():
    analysis_file = open("dask_report.txt","w")
    for path, dirs, files in os.walk('dask'):
        for file in files:
            if file.endswith('.py'):
                source = open(os.path.join(path,file), "r")
                tree = ast.parse(source.read())
                analyzer = Analyzer()
                analyzer.visit(tree)
                codelist=analyzer.report()
                analysis_file.write('\n' + os.path.join(path,file) + '\n\n')
                [analysis_file.write(line+'\n') for line in codelist]
    analysis_file.close()

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = []
        self.depth=0
        self.module_dict={}

    def visit_FunctionDef(self, node):
        self.depth = self.depth + 4
        depths = '-'*self.depth
        self.stats.append(depths + ' Func: ' + node.name)
        self.generic_visit(node)
        self.depth = self.depth - 4
    def visit_ClassDef(self, node):
        self.depth = self.depth + 4
        depths = '-'*self.depth 
        self.stats.append(depths + ' Class: ' + node.name)
        self.generic_visit(node)
        self.depth = self.depth - 4
    def visit_Call(self, node):
        self.depth = self.depth + 4
        depths = '-'*self.depth
        try:
            if node.func.value.id in self.module_dict.keys():
                call_func = self.module_dict[node.func.value.id]
            else:
                call_func = node.func.value.id
            if call_func not in dir(__builtins__):
                self.stats.append(depths + ' Call: ' + call_func)
            self.generic_visit(node)
        except:
            pass
        try:
            if node.func.id in self.module_dict.keys():
                call_func = self.module_dict[node.func.id]
            else:
                call_func = node.func.id
            if call_func not in dir(__builtins__):
                self.stats.append(depths + ' Call: ' + call_func)
            self.generic_visit(node)
        except:
            pass
        self.depth = self.depth - 4
    def visit_Import(self, node):
        self.depth = self.depth + 4
        depths = '-'*self.depth
        #[self.stats.append(depths + ' Import: ' + alias.name) for alias in node.names]
        self.generic_visit(node)
        self.depth = self.depth - 4
    def visit_ImportFrom(self, node):
        self.depth = self.depth + 4
        depths = '-'*self.depth
        try:
            #self.stats.append(depths + ' Module: ' + node.module)
            for alias in node.names:
                self.module_dict[alias.name] = node.module + '.'+ alias.name
        except:
            pass
        #[self.stats.append(depths + ' Import From: ' + alias.name) for alias in node.names]
        self.generic_visit(node)
        self.depth = self.depth - 4
    def report(self):
        return self.stats

if __name__ == "__main__":
    main()
