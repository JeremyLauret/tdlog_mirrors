import re

def cap_letter_to_rank(cap_letter):
    """
       :return: The rank in the alphabet of cap_letter
       
       >>> cap_letter_to_rank('A')
       0
       >>> cap_letter_to_rank('Z')
       25
    """
    rank = ord(cap_letter) - ord('A')
    assert 0 <= rank <= 25, "Error : the given string is not a capital letter."
    return rank

def rank_to_cap_letter(rank):
    """
       :return: The capital letter of rank rank in the alphabet
       
       >>> rank_to_cap_letter(0)
       'A'
       >>> rank_to_cap_letter(25)
       'Z'
    """
    assert 0 <= rank <= 25, ("Error : there is no letter number {} in the "
                             "alphabet.".format(rank))
    return chr(ord('A') + rank)
    
def case_insensitive_stop(string):
    """
       :return: True if string is equal to "stop" in a case insensitive sense,
       False if it is not.
    
       >>> case_insensitive_stop("StoP")
       True
       >>> case_insensitive_stop("stap")
       False
    """
    return re.match('stop', string, re.IGNORECASE) != None

if __name__ == '__main__':
    import doctest
    doctest.testmod()