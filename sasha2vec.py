def mapping(rep):
    for k, v in smapper.items():
        if rep in v:
            return k
    return '009'

smapper = {
'001': ['plastic bag', 'ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin'],
'002': ['plastic bin'],
'003': ['CD DVD'],
'004': ['magazine'],
'005': ['toilet paper'],
'006': ['egg package'],
'007': ['paper package'],
'008': ['plastic container']
}
