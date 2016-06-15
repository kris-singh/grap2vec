'''
__author__ : kris singh
__date__:
__filename__ : perms.py
__descpription__: generate permutation of a string
__email__: cs15mtech11007@iith.ac.in
'''
def swap(string,index_1,index_2):
    #@params - string : the input string to be permuted
    #@params - index_1:  index of char to be swaped
    #@params - index_2: index of char to be swaped
    #print string
    temp = string[index_1]
    string[index_1] = string[index_2]
    string[index_2] = temp
    return "".join(string)

def perms(string):
    #@params- string:the input string we want to permute
    #base case string of length of size 2
    #print string
    base_str = []
    if len(string) == 2:
        #print "here"
        base_str.append(string)
        base_str.append(swap(list(string),0,1))
        return base_str
    else:
        strings_return = []
        for key,value in enumerate(string):
            #print key,value
            #swap the last el of the given string
            new_string = swap(list(string),len(string) - 1,key)
            org_string = new_string
            #recurse for new string of length n-1
            new_string = list(new_string)[:-1]
            returned_strings = perms("".join(new_string))
            for i in returned_strings:
                i = list(i)
                i.append(org_string[-1])
                strings_return.append(i)
        return strings_return

if __name__ == "__main__":
    string1 = "123"
    result_list = perms(string1)
    final_list = []
    for i in result_list:
        final_list.append("".join(i))
    if len(set(final_list)) == len(final_list):
        print final_list,len(final_list)
    else:
        print "error"

