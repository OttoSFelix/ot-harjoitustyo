

def total_score(score):
    """
    Returns the total score of a match based on the points
    
    Args:
        score: point score of a match in string format eg. '7, -8, 9, 6'
    
    Returns:
        total score in sets eg. 3-1 if no points given in an acceptable format
        fail if points not given in an acceptable format
    """
    score = score.split(',')
    try:
        for n, s in enumerate(score):
            if s == '':
                score[n] = 0
            score[n] = int(score[n])
        player = 0
        opponent = 0
        for s in score:
            if s >= 0:
                player += 1
            else:
                opponent +=1
        if player > opponent:
            outcome = 'win'
        else:
            outcome = 'lose'
        return (f'{player}-{opponent}', outcome)
    except:
        return ('fail', 'fail')


def reverse_score(score):
    """
    Changes each score of a set to its opposite

    Args:
        score: original score of a match in string format eg. '7, -8, 9, 6'
    Returns:
        reversed score if score given in a correct format
        fail if score given in an incorrect format
    """
    try:
        score = score.split(',')
        for n, s in enumerate(score):
            if s == '':
                score[n] = 0
            score[n] = int(score[n])
            score[n] = -score[n]
        for n, s in enumerate(score):
            score[n] = str(s)
        return ','.join(score)
    except:
        return 'fail'
