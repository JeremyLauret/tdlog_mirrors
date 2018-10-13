def cap_letter_to_rank(cap_letter):
    """
       :return: The rank in the alphabet of cap_letter
    """
    rank = ord(cap_letter) - ord('A')
    assert 0 <= rank <= 25, "Error : the given string is not a capital letter."
    return rank

def rank_to_cap_letter(rank):
    """
       :return: The capital letter of rank rank in the alphabet
    """
    assert 0 <= rank <= 25, "Error : there is no letter number {} in the alphabet.".format(rank)
    return chr(ord('A') + rank)