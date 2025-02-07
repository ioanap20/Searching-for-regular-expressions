try:
    from dg import *
except Exception:
    pass


# Question 5
def contains_pattern(s, text):
    if text == "" or s == "":
        return False
        
    modified_regex = "(.)*" + s + "(.)*"
    
    nfa = NFA(modified_regex)
    return nfa.check_text(text)

class NFA:
    def __init__(self, s): # s is the string containing the regular expression
        self.s = s
        self.m = len(self.s)
        self.dg = DG(len(s) + 1) # the directed graph that stores the epsilon links
        self.lp = [-1 for _ in range(len(s))]
        self.rp = [-1 for _ in range(len(s))]
        self.left_right_match_or() # assigns lp and rp according to parentheses matches
        self.build_eps_links() # assigns the epsilon links in self.dg

    def __str__(self):
        n = self.m
        str_lp = 'lp: '
        str_rp = 'rp: '
        for i in range(self.m):
            if self.lp[i] == -1:
                str_lp += '-1  '
            elif self.lp[i] < 10:
                str_lp += str(self.lp[i]) + '   '
            else: str_lp += str(self.lp[i]) + '  '
            if self.rp[i] == -1:
                str_rp += '-1  '
            elif self.rp[i] < 10:
                str_rp += str(self.rp[i]) + '   '
            else: str_rp += str(self.rp[i]) + '  '
        str_lp += '\n'
        str_rp += '\n'

        str_dg = str(self.dg)

        s = '------------------\nRegular expression\n------------------\n' + 're: ' + '   '.join(self.s) + '\n'
        return s + str_lp + str_rp #+ '------------------\nCorresponding NFA\n------------------\n' + str_dg

    ## Question 1
    def left_right_match(self):
        stack = []
        for i in range(self.m):
            if self.s[i] == '(':
                stack.append(i)
            elif self.s[i] == ')':
                j = stack.pop()
                self.lp[i] = j
                self.rp[j] = i
        
        
            
    
    ## Question 2
    def left_right_match_or(self):
        stack = []  
        for i in range(self.m):
            if self.s[i] == '(':
                stack.append(i)  
            elif self.s[i] == '|':
                stack.append(i)  
            elif self.s[i] == ')':
                or_indices = []  
                while stack:
                    j = stack.pop()
                    if self.s[j] == '(':
                        
                        self.lp[i] = j
                        self.rp[j] = i
                        
                        for k in or_indices:
                            self.lp[k] = j
                            self.rp[k] = i
                        break
                    elif self.s[j] == '|':
                        or_indices.append(j)
    ## Question 3
    def build_eps_links(self):        
        for i in range(self.m):
            if self.s[i] in ['(', ')', '*']:
                self.dg.add_link(i, i+1)
                
            if self.s[i] == '|':
                self.dg.add_link(self.lp[i], i+1)
                self.dg.add_link(i, self.rp[i])
                
            if self.s[i] == '*':
                if self.lp[i - 1] != -1 :  
                    start = self.lp[i - 1] 
                    end = i   
                    self.dg.add_link(end, start)  
                    self.dg.add_link(start, end)  

    ## Question 4
    # Complexity: O(m)
    # Because: First we have the cost of explore_from_subset which is O(number of edges + number of vertices)
    # Then for each caracter in w (n characters) we have to go through the for loop which costs O(number of vertices) and then we do
    # the explore_from_subset 
    def check_text(self, w):
        n = len(w)  
        m = self.m  

        current_states = set(self.dg.explore_from_subset([0]))

        for char in w:
            next_states = set()
            for state in current_states:
                if state < m and (self.s[state] == char or self.s[state] == '.'):  
                    next_states.add(state + 1)

            current_states = set(self.dg.explore_from_subset(next_states))

        return m in current_states
