# By Jesse M, 23/09/2025
# On a plane to Manila !!!

# This program finds the determinants of any-size matrices via either:
#  1. co-factor expansion
#  2. row echelon form

# NOTE:
# - REF can sometimes fail due to floating point precision issues

def _det_cofactor(M):
    n_rows = len(M)
    n_cols = len(M[0])

    # If we have a single-element matrix, return its single element.
    if (n_rows == 1) and (n_cols == 1):
        return M[0][0]
    
    # We do co-factor expansion using row 1
    sum = 0
    for col in range(n_cols):
        reduced_M = copy_mat(M)

        # Remove row 1 from reduced M
        reduced_M.pop(0)
        # Remove column 'col' from reduced M
        for i in range(n_rows - 1):
            reduced_M[i].pop(col)

        # Note: row = 0 => (-1) ** (row + col) = (-1) ** col
        sum += ((-1) ** col) * (M[0][col]) * _det_cofactor(reduced_M)
    
    return float(sum)

def copy_mat(M):
    M_copy = []
    for row in M:
        M_copy.append(row.copy())

    return M_copy

def print_mat(M):
    for row in M:
        print(row)
    print()

def ref(M, return_det_sign=False):
    # Empty sets have no REF
    if M == []:
        return []
    
    # Create a copy of M
    M = copy_mat(M)
    
    n_rows = len(M)
    n_cols = len(M[0])

    det_sign = 1

    top_row = 0
    while top_row < n_rows:
        # Find row with leading entry
        min_lent_col = float("inf")
        for row in range(top_row, n_rows):
            lent_col = lent_i(M[row])

            if lent_col < min_lent_col:
                min_lent_col = lent_col
                min_lent_row = row

        # If this row isn't the topmost row, swap it to the top.
        if not min_lent_row == top_row:
            M[top_row], M[min_lent_row] = M[min_lent_row], M[top_row]
            det_sign *= -1

        lent = M[top_row][min_lent_col]

        for sub_row in range(top_row + 1, n_rows):
            subr_lent_col = lent_i(M[sub_row])

            if subr_lent_col > min_lent_col:
                continue

            subr_lent = M[sub_row][subr_lent_col]
            
            # Rn -> Rn - k*Rm
            for col in range(n_cols):
                M[sub_row][col] -= subr_lent / lent * M[top_row][col]

        top_row += 1
    
    if return_det_sign:
        return (M, det_sign)
    else:
        return M

def lent_i(row):
    """
    Gets the index of the leading entry in a row.
    """

    n_cols = len(row)

    for col in range(n_cols):
        if row[col] != 0:
            return col

    return col

def det(M, method="ref"):
    # det(empty set) = 0.
    if M == []:
        return 0
    
    n_rows = len(M)
    n_cols = len(M[0])

    # Only square matrices have determinants.
    if n_rows != n_cols:
        raise ValueError("matrix must be square.")
    
    if method == "ref":
        ref_M, det_sign = ref(M, return_det_sign=True)

        # Multiply the entries in the diagonal
        prod = 1
        for i in range(n_rows):
            prod *= ref_M[i][i]

        if prod == 0:
            return 0.0

        return prod * det_sign


    elif method == "co-factor":
        return _det_cofactor(M)

def cas_format(M):
    row_strs = []
    for row in M:
        row_strs.append(str.join(", ", map(str, row)))
    
    mat_str = str.join("; ", row_strs)

    return f"[{mat_str}]"

M = [
    [2, 10,  8,  4, 22],
    [0,  3,  5, -6, 16],
    [0,  0,  4, -3,  3],
    [0,  0,  0,  0,  6],
    [0,  0,  0, -5,  9]
]

det_ref = det(M, method="ref")
det_cofac = det(M, method="co-factor")

print(det_ref)
print(det_cofac)

cas = cas_format(M)
print(cas)

print_mat(ref(M))
