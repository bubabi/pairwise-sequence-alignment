import logging

match_score = 5
mis_match_penalty = -4
gap_opening = -10
gap_extend = -5

# match_score = 1
# mis_match_penalty = -1
# gap_opening = -2
# gap_extend = -2

def init_matrix(rows, cols, algorithm='global'):
    # 5, 6
    mat = [[0]*cols for row in range(rows)]
    gap_mat = [[0]*cols for row in range(rows)]
    gap_mat[1][0] = 1
    gap_mat[0][1] = 1

    if algorithm == 'global':
        for i in range(1, rows):
            mat[i][0] = mat[i-1][0] + gap_penalty(gap_mat, i-1, 0)
            gap_mat[i][0] = 1
        for j in range(1, cols):
            mat[0][j] = mat[0][j-1] + gap_penalty(gap_mat, 0, j-1)
            gap_mat[0][j] = 1
    elif algorithm == 'local':
        for i in range(1, rows):
            mat[i][0] = 0
            gap_mat[i][0] = 1
        for j in range(1, cols):
            mat[0][j] = 0
            gap_mat[0][j] = 1
    else:
        print("Please enter a valid algorithm... ('global' or 'local')")
  
    logging.info('Matrix initialized...')
    # print_matrix(mat)
    # print_matrix(gap_mat)

    return mat, gap_mat


def print_matrix(matrix):
    logging.info('Matrix printing...')
    for row in matrix:
        print(''.join(['{0:>{w}}'.format(item, w=5) for item in row]), end='\n\n')


def is_match(char_a, char_b):
    return match_score if char_a == char_b else mis_match_penalty


def gap_penalty(gap_matrix, row_idx, col_idx):
    return gap_extend if gap_matrix[row_idx][col_idx] == 1 else gap_opening


def global_alignment(M, gap_matrix, s1, s2, rows, cols):
    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = M[i-1][j-1] + is_match(s1[j-1], s2[i-1])
            vgap = M[i-1][j] + gap_penalty(gap_matrix, i-1, j)
            hgap = M[i][j-1] + gap_penalty(gap_matrix, i, j-1)

            options = [diagonal, vgap, hgap]
            index_max = options.index(max(options))

            if max(options) == M[i - 1][j] + gap_penalty(gap_matrix, i - 1, j) or max(options) == M[i][j - 1] + gap_penalty(gap_matrix, i, j - 1):
                gap_matrix[i][j] = 1

            M[i][j] = options[index_max]
            

    # print_matrix(gap_matrix)

    i, j = rows-1, cols-1
    aligned_s1, aligned_s2, mid = (' ')*3

    while i>0 and j>0:
        diagonal = M[i][j] - is_match(s1[j-1], s2[i-1])
        vgap = M[i][j] - gap_penalty(gap_matrix, i-1, j)
        hgap = M[i][j] - gap_penalty(gap_matrix, i, j-1)

        if M[i-1][j-1] == diagonal:   
            aligned_s1 += s1[j-1]
            aligned_s2 += s2[i-1]
            if is_match(s1[j-1], s2[i-1]) == match_score:
                mid += '|'
            else:
                mid += ' '
            i = i - 1
            j = j - 1
        elif M[i-1][j] == vgap:
            aligned_s1 += '-'
            aligned_s2 += s2[i-1]
            mid += ' '
            i = i - 1
        elif M[i][j-1] == hgap:
            aligned_s1 += s1[j-1]
            aligned_s2 += '-'
            mid += ' '
            j = j - 1

    print(aligned_s1[::-1] + '\n' + mid[::-1] + '\n' + aligned_s2[::-1])

    return M, M[rows-1][cols-1]


def local_alignment(M, gap_matrix, s1, s2, rows, cols):

    max_score = 0
    optimal_point = (0, 0)

    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = M[i-1][j-1] + is_match(s1[j-1], s2[i-1])
            vgap = M[i-1][j] + gap_penalty(gap_matrix, i-1, j)
            hgap = M[i][j-1] + gap_penalty(gap_matrix, i, j-1)

            options = [0, diagonal, vgap, hgap]
            index_max = options.index(max(options))

            if options[index_max] == vgap or options[index_max] == hgap:
                gap_matrix[i][j] = 1

            M[i][j] = options[index_max]

            if M[i][j] > max_score:
                max_score = M[i][j]
                optimal_point = (i, j)
    
    # print_matrix(gap_matrix)
    # print_matrix(M)

    i, j = optimal_point[0], optimal_point[1]
    aligned_s1, aligned_s2, mid = (' ')*3

    while i>0 and j>0:
        diagonal = M[i][j] - is_match(s1[j-1], s2[i-1])
        vgap = M[i][j] - gap_penalty(gap_matrix, i-1, j)
        hgap = M[i][j] - gap_penalty(gap_matrix, i, j-1)

        if M[i-1][j-1] == diagonal:   
            aligned_s1 += s1[j-1]
            aligned_s2 += s2[i-1]
            if is_match(s1[j-1], s2[i-1]) == match_score:
                mid += '|'
            else:
                mid += ' '
            i = i - 1
            j = j - 1
        elif M[i-1][j] == vgap:
            aligned_s1 += '-'
            aligned_s2 += s2[i-1]
            mid += ' '
            i = i - 1
        elif M[i][j-1] == hgap:
            aligned_s1 += s1[j-1]
            aligned_s2 += '-'
            mid += ' '
            j = j - 1
        elif M[i][j] == 0:
            break

    print(aligned_s1[::-1] + '\n' + mid[::-1] + '\n' + aligned_s2[::-1])
    
    return M, max_score


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    sequence_a = 'ACTACTAGATTACTGACGGATAAGGTACTTTAGAGGCTTGCAACCA'
    sequence_b = 'ACTACTCACGGATCAGGTACTTTAGAGGCA'
    rows, cols = len(sequence_b)+1, len(sequence_a)+1


    D, gap_matrix = init_matrix(rows, cols, algorithm='local')
    D, score = local_alignment(D, gap_matrix, sequence_a, sequence_b, rows, cols)
    
    # print_matrix(gap_matrix)
    # print_matrix(D)

    print(score)

    