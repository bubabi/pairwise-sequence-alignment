import logging

match_score = 5
mismatch_penalty = -4
gap_opening = -10
gap_extend = -5

def init_matrix(rows, cols):
    # 5, 6
    mat = [[0]*cols for row in range(rows)]

    for i in range(1, rows):
        mat[i][0] = gap_opening*i
    for j in range(1, cols):
        mat[0][j] = gap_opening*j
  
    logging.info('Matrix initialized...')
    
    return mat


def print_matrix(matrix):
    logging.info('Matrix printing...')
    for row in matrix:
        print(''.join(['{0:>{w}}'.format(item, w=5) for item in row]), end='\n\n')


def isMatch(char_a, char_b):
    return match_score if char_a == char_b else mismatch_penalty


def global_alignment(M, s1, s2, rows, cols):
    for i in range(1, rows):
        for j in range(1, cols):
            M[i][j] = max(
                            M[i-1][j-1] + isMatch(s1[j-1],s2[i-1]), 
                            M[i-1][j] + gap_opening, 
                            M[i][j-1] + gap_opening
                        )

    i, j = rows-1, cols-1
    aligned_s1, aligned_s2, mid = (' ')*3

    while i>0 and j>0:
        diagonal = isMatch(s1[j-1], s2[i-1])
        if M[i-1][j-1] == M[i][j] - diagonal:
            aligned_s1 += s1[j-1]
            aligned_s2 += s2[i-1]
            if diagonal == match_score:
                mid += '|'
            else:
                mid += ' '
            i = i - 1
            j = j - 1
        elif M[i-1][j]== M[i][j] - gap_opening :
            aligned_s1 += '–'
            aligned_s2 += s2[i-1]
            mid += ' '
            i = i - 1
        elif M[i][j-1] == M[i][j] - gap_opening:
            aligned_s1 += s1[j-1]
            aligned_s2 += '–'
            mid += ' '
            j = j - 1

    print(aligned_s1[::-1] + '\n' + mid[::-1] + '\n' + aligned_s2[::-1])

    return M


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    sequence_a = 'ACTACTAGATTACTGACGGATAAGGTACTTTAGAGGCTTGCAACCA'
    sequence_b = 'ACTACTCACGGATCAGGTACTTTAGAGGCA'
    rows, cols = len(sequence_b)+1, len(sequence_a)+1


    D = init_matrix(rows, cols)
    D = global_alignment(D, sequence_a, sequence_b, rows, cols)

    