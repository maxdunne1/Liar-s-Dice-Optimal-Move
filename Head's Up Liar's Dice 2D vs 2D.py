import numpy as np
import sys

# Increase recursion limit
sys.setrecursionlimit(10000)

# Probabilities
     
def optimal(bids, your_dice):
    first_in = (
        (
            (.4, .2, .2, .2), (.5, 0, .1, .4)
        ),
        (
            (.6, .1, .1, .2), (.5, 0, .3, 2)
        )
    )
    second_in = (
            (0.5, 0.1, 0.3, 0.1), 
            (0.6, 0.2, 0.1, 0.1), 
            (0.7, 0.2, 0.05, 0.05),
    )
    count3 = (
            (.7, .2, .1, 0),
            (.8, .2, 0, 0)
        ) 
 
    
    # Possible Rolls and Possible Bids
    def rolls():
        roll = np.full((6,6), '', dtype=object)
        
        for i in range(6):
            for j in range(6):
                roll[i,j] = (i + 1, j + 1)
        
        return roll
    def allMoves2v2():
        
        moves = []
        faces = [2,3,4,5,6,1]
        
        for i in range(1,5):
            for num in faces:
                moves.append((i, num))
                
        moves.remove((2, 1))
        moves.remove((3, 1))
        moves.insert(16, (2, 1))  
        moves.insert(22, (3, 1))  
        
        return moves
    def response2v2(bids):
        count, face = bids[-1]
        if count == None:
            return allMoves2v2()
        else:
            moves = allMoves2v2()
            ind = moves.index((count, face))
            resp = moves[ind + 1:]
            return resp

    # Range Builder
    def ranges(bids, first_in, second_in, count3):
        
        def convertRange(arr):
            
            matrix = np.full((6, 6), 0, dtype= object)
            
            for i in range(6):
                for j in range(6):
                    if i == j:
                        matrix[i,j] = arr[i,j]
                    elif i < j:
                        matrix[i,j] = 2 * arr[i,j]
            
            return matrix.astype(np.float64)
        
        def firstInRange(bids, first_in, second_in, count3):
            first_bid = bids[0]
            count, face = first_bid
            matrix = np.full((6,6), '', dtype= object)
            roll = rolls()
            
            # Types
            if count == 1:
                if face != 1:
                    for i in range(6):
                        for j in range(6):
                            current = roll[i,j]
                            one_count = current.count(1)
                            face_count = current.count(face)
                            
                            if face_count == 1 and one_count == 0:
                                matrix[i,j] = 'Highest'
                            elif face_count + one_count == 2:
                                matrix[i,j] = 'High'
                            elif one_count == 1 and face_count == 0:
                                matrix[i,j] = 'Low'
                            else:
                                matrix[i,j] = 'Lowest'
                else:
                    for i in range(6):
                        for j in range(6):
                            current = roll[i,j]
                            one_count = current.count(1)
                            
                            if one_count == 1:
                                matrix[i,j] = 'Highest'
                            elif one_count == 2:
                                matrix[i,j] = 'Low'
                            else:
                                matrix[i,j] = 'Lowest'
            elif count == 2:
                if face != 1:
                    for i in range(6):
                        for j in range(6):
                            current = roll[i,j]
                            one_count = current.count(1)
                            face_count = current.count(face)
                            
                            if face_count + one_count == 2:
                                matrix[i,j] = 'Highest'
                            elif face_count == 1 and one_count == 0:
                                matrix[i,j] = 'High'
                            elif one_count == 1 and face_count == 0:
                                matrix[i,j] = 'Low'
                            else:
                                matrix[i,j] = 'Lowest'
                else:
                    for i in range(6):
                        for j in range(6):
                            current = roll[i,j]
                            one_count = current.count(1)
                            
                            if one_count == 2:
                                matrix[i,j] = 'Highest'
                            elif one_count == 1:
                                matrix[i,j] = 'Low'
                            else:
                                matrix[i,j] = 'Lowest'
            
            # Probabilities 
            if count == 1:
                if face != 1:
                    p_highest, p_high, p_low, p_lowest = first_in[0][0]
                else:
                    p_highest, p_high, p_low, p_lowest = first_in[0][1]
            else:
                if face != 1:
                    p_highest, p_high, p_low, p_lowest = first_in[1][0]
                else:
                    p_highest, p_high, p_low, p_lowest = first_in[1][1]

            # Probability Matrix
            highest_count = np.sum(matrix == 'Highest')
            high_count = np.sum(matrix == 'High')
            low_count = np.sum(matrix == 'Low')
            lowest_count = np.sum(matrix == 'Lowest')
            p_matrix = np.full((6, 6), 0, dtype= object)
            
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if matrix[i,j] == 'Highest':
                        p_matrix[i,j] = round(p_highest / highest_count, 3)
                    elif matrix[i,j] == 'High':
                        p_matrix[i,j] = round(p_high / high_count, 3)
                    elif matrix[i,j] == 'Low':
                        p_matrix[i,j] = round(p_low / low_count, 3)
                    elif matrix[i,j] == 'Lowest':
                        p_matrix[i,j] = round(p_lowest / lowest_count, 3)
                        
            return p_matrix
        def secondInRange(bids, first_in, second_in, count3):
            bids = bids[:2]
            one_range = second_in[0]
            two_range = second_in[1]
            three_range = second_in[2]
            
            difference = bids[1][0] - bids[0][0]
            same = True if bids[1][1] == bids[0][1] else False
            roll = rolls()
            type_matrix = np.full((6,6), '', dtype=object)
            p_matrix = np.full((6,6), 0, dtype=object)
            
            
            for i in range(6):
                for j in range(6):
                    current = roll[i,j]
                    one_count = current.count(1)
                    face1_count = current.count(bids[0][1])
                    face2_count = current.count(bids[1][1])
                    
                    if bids[0][1] != 1 and bids[1][1] != 1:
                        if same == True:
                            if difference == 1:
                                if face1_count == 1 and one_count == 0:
                                    type_matrix[i,j] = 'Highest'
                                elif face1_count + one_count == 2:
                                    type_matrix[i,j] = 'High'
                                elif face1_count == 0 and one_count == 1:
                                    type_matrix[i,j] = 'Low'
                                else:
                                    type_matrix[i,j] = 'Lowest'
                            elif difference == 2:
                                if face1_count + one_count == 2:
                                    type_matrix[i,j] = 'Highest'
                                elif face1_count == 1 and one_count == 0:
                                    type_matrix[i,j] = 'High'
                                elif face1_count == 0 and one_count == 1:
                                    type_matrix[i,j] = 'Low'
                                else:
                                    type_matrix[i,j] = 'Lowest'
                        else:
                            if difference == 0:
                                if bids[0][0] == 1:
                                    if face1_count > 0:
                                        type_matrix[i,j] = 'Lowest'
                                    elif face1_count + face2_count + one_count == 0:
                                        type_matrix[i,j] = 'Low'
                                    elif face2_count > 0 and face1_count == 0:
                                        type_matrix[i,j] = 'High'
                                    else:
                                        type_matrix[i,j] = 'Highest'
                                elif bids[0][0] == 2:
                                    if face2_count + one_count == 2:
                                        type_matrix[i,j] = 'Highest'
                                    elif face2_count == 1 and one_count == 0:
                                        type_matrix[i,j] = 'High'
                                    elif face2_count == 0 and one_count == 1:
                                        type_matrix[i,j] = 'Low'
                                    else:
                                        type_matrix[i,j] = 'Lowest' 
                            elif difference == 1:
                                if face2_count + one_count == 2:
                                    type_matrix[i,j] = 'Highest'
                                elif face2_count == 1 and one_count == 0:
                                    type_matrix[i,j] = 'High'
                                elif face2_count == 0 and one_count == 1:
                                    type_matrix[i,j] = 'Low'
                                else:
                                    type_matrix[i,j] = 'Lowest'
                            elif difference == 2:
                                if face2_count + one_count == 2:
                                    type_matrix[i,j] = 'Highest'
                                elif face2_count == 1 and one_count == 0:
                                    type_matrix[i,j] = 'High'
                                elif face2_count == 0 and one_count == 1:
                                    type_matrix[i,j] = 'Low'
                                else:
                                    type_matrix[i,j] = 'Lowest'
                    elif bids[1][1] != 1:
                        if difference == 1:
                            if face2_count == 1 and one_count == 0:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count + one_count == 2:
                                type_matrix[i,j] = 'High'
                            elif one_count == 1 and face2_count == 0:
                                type_matrix[i,j] = 'Low'
                            else:
                                type_matrix[i,j] = 'Lowest'
                        elif difference == 2:
                            if face2_count + one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count == 1 and one_count == 0:
                                type_matrix[i,j] = 'High'
                            elif one_count == 1 and face2_count == 0:
                                type_matrix[i,j] = 'Low'
                            else:
                                type_matrix[i,j] = 'Lowest'
                    else:
                        if difference == 1:
                            if one_count == 1:
                                type_matrix[i,j] = 'Highest'
                            elif one_count == 2:
                                type_matrix[i,j] = 'Low'
                            else:
                                type_matrix[i,j] = 'Lowest'
                        elif difference == 2:
                            if one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            elif one_count == 1:
                                type_matrix[i,j] = 'Low'
                            else:
                                type_matrix[i,j] = 'Lowest'
                        
            count_highest = (type_matrix == 'Highest').sum()
            count_high = (type_matrix == 'High').sum()
            count_low = (type_matrix == 'Low').sum()
            count_lowest = (type_matrix == 'Lowest').sum()
            
            if bids[0][1] != 1 and bids[1][1] != 1:
                if difference == 0:
                    if bids[1][0] == 1:
                        p_highest, p_high, p_low, p_lowest = one_range
                    elif bids[1][0] == 2:
                        p_highest, p_high, p_low, p_lowest = two_range
                elif difference == 1:
                    if same is True:
                        p_highest, p_high, p_low, p_lowest = one_range
                    else:
                        p_highest, p_high, p_low, p_lowest = two_range
                elif difference == 2:
                    if same is True:
                        p_highest, p_high, p_low, p_lowest = two_range
                    else:
                        p_highest, p_high, p_low, p_lowest = three_range
            elif bids[1][1] != 1:
                if difference == 1:
                    p_highest, p_high, p_low, p_lowest = one_range
                elif difference == 2:
                    p_highest, p_high, p_low, p_lowest = two_range
            else:
                if difference == 1:
                    p_highest, p_high, p_low, p_lowest = first_in[0][1]
                elif difference == 2:
                    p_highest, p_high, p_low, p_lowest = first_in[1][1]
                    
            for i in range(6):
                for j in range(6):
                    if type_matrix[i,j] == 'Highest':
                        p_matrix[i,j] = round(p_highest / count_highest, 3)
                    elif type_matrix[i,j] == 'High':
                        p_matrix[i,j] = round(p_high / count_high, 3)
                    elif type_matrix[i,j] == 'Low':
                        p_matrix[i,j] = round(p_low / count_low, 3)
                    elif type_matrix[i,j] == 'Lowest':
                        p_matrix[i,j] = round(p_lowest / count_lowest, 3)
                        
            return p_matrix
        def thirdBidRange(bids, first_in, second_in, count3):
            roll = rolls()
            matrix1 = firstInRange([bids[0]], first_in, second_in, count3)
            matrix2 = secondInRange(bids[1:], first_in, second_in, count3)
            matrix = np.full((6,6), 0, dtype=object)

            
            if bids[1][0] < 3:
                for i in range(6):
                    for j in range(6):
                        matrix[i,j] = round((1 / 3) * matrix[i,j] + (2 / 3) * matrix2[i,j], 3)
                return matrix
            else:
                type_matrix = np.full((6,6), '', dtype=object)
                for i in range(6):
                    for j in range(6):
                        current = roll[i,j]
                        one_count = current.count(1)
                        face1_count = current.count(bids[1][1])
                        face2_count = current.count(bids[2][1])

                        if bids[1][0] == 3 and bids[2][0] == 3:
                            p_highest, p_high, p_low, p_lowest = count3[0]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            elif face2_count + one_count == 2 and face2_count != 2:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count == 1 and face1_count + one_count != 0:
                                type_matrix[i,j] = 'High'
                            else: 
                                type_matrix[i,j] = 'Low'
                        elif bids[1][0] == 3 and bids[2][0] == 4:
                            p_highest, p_high, p_low, p_lowest = count3[1]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            if face1_count + one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            if face1_count + one_count == 1:
                                type_matrix[i,j] = 'High'
                                    
                count_highest = (type_matrix == 'Highest').sum()
                count_high = (type_matrix == 'High').sum()
                count_low = (type_matrix == 'Low').sum()
                count_lowest = (type_matrix == 'Lowest').sum()
                p_matrix  = np.full((6,6), 0, dtype=object)
                
                for i in range(6):
                    for j in range(6):
                        if type_matrix[i,j] == 'Highest':
                            p_matrix[i,j] = round(p_highest / count_highest, 3)
                        elif type_matrix[i,j] == 'High':
                            p_matrix[i,j] = round(p_high / count_high, 3)
                        elif type_matrix[i,j] == 'Low':
                            p_matrix[i,j] = round(p_low / count_low, 3)
                        elif type_matrix[i,j] == 'Lowest':
                            p_matrix[i,j] = round(p_lowest / count_lowest, 3)
                
                zero_count = 0
                adjust = 0

                for i in range(6):
                    for j in range(6):
                        if p_matrix[i,j] == 0:
                            zero_count += 1
                            adjust += matrix1[i,j]
                            matrix1[i,j] = 0
                            
                for i in range(6):
                    for j in range(6):
                        if matrix1[i,j] == 0:
                            matrix[i,j] = 0
                        else:
                            matrix[i,j] = round((1 / 3) * (matrix1[i,j] + (adjust / zero_count)) + (2 / 3) * (p_matrix[i,j]), 3)
                            
                        
                return matrix
        def fourthBidRange(bids, first_in, second_in, count3):
            
            roll = rolls()
            matrix1 = secondInRange(bids[:2], first_in, second_in, count3)
            matrix2 = secondInRange(bids[2:], first_in, second_in, count3)
            matrix = np.full((6,6), 0, dtype=object)
            
            if bids[2][0] < 3:
                for i in range(6):
                    for j in range(6):
                        matrix[i,j] = round((1 / 3) * matrix1[i,j] + (2 / 3) * matrix2[i,j], 3)
                return matrix
            else:
                type_matrix = np.full((6,6), '', dtype=object)
                for i in range(6):
                    for j in range(6):
                        current = roll[i,j]
                        one_count = current.count(1)
                        face1_count = current.count(bids[1][1])
                        face2_count = current.count(bids[2][1])

                        if bids[2][0] == 3 and bids[3][0] == 3:
                            p_highest, p_high, p_low, p_lowest = count3[0]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            elif face2_count + one_count == 2 and face2_count != 2:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count == 1 and face1_count + one_count != 0:
                                type_matrix[i,j] = 'High'
                            else: 
                                type_matrix[i,j] = 'Low'
                        elif bids[2][0] == 3 and bids[3][0] == 4:
                            p_highest, p_high, p_low, p_lowest = count3[1]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            if face1_count + one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            if face1_count + one_count == 1:
                                type_matrix[i,j] = 'High'
                                    
                count_highest = (type_matrix == 'Highest').sum()
                count_high = (type_matrix == 'High').sum()
                count_low = (type_matrix == 'Low').sum()
                count_lowest = (type_matrix == 'Lowest').sum()
                p_matrix  = np.full((6,6), 0, dtype=object)
                
                for i in range(6):
                    for j in range(6):
                        if type_matrix[i,j] == 'Highest':
                            p_matrix[i,j] = round(p_highest / count_highest, 3)
                        elif type_matrix[i,j] == 'High':
                            p_matrix[i,j] = round(p_high / count_high, 3)
                        elif type_matrix[i,j] == 'Low':
                            p_matrix[i,j] = round(p_low / count_low, 3)
                        elif type_matrix[i,j] == 'Lowest':
                            p_matrix[i,j] = round(p_lowest / count_lowest, 3)
                        
                
                zero_count = 0
                adjust = 0

                for i in range(6):
                    for j in range(6):
                        if p_matrix[i,j] == 0:
                            zero_count += 1
                            adjust += matrix1[i,j]
                            matrix1[i,j] = 0
                            
                for i in range(6):
                    for j in range(6):
                        if matrix1[i,j] == 0:
                            matrix[i,j] = 0
                        else:
                            matrix[i,j] = round((1 / 3) * (matrix1[i,j] + (adjust / zero_count)) + (2 / 3) * (p_matrix[i,j]), 3)
                            
                        
                return matrix
        def fifthBidRange(bids, first_in, second_in, count3):
            roll = rolls()
            matrix1 = firstInRange([bids[0]], first_in, second_in, count3)
            matrix2 = thirdBidRange(bids[:3], first_in, second_in, count3)
            matrix3 = thirdBidRange(bids[2:], first_in, second_in, count3)
            matrix = np.full((6,6), 0, dtype=object)
            
            if bids[3][0] < 3:
                for i in range(6):
                    for j in range(6):
                        matrix[i,j] = round((1 / 6) * matrix1[i,j] + (1 / 3) * matrix2[i,j] + matrix3[i,j] * (1 / 2), 3)
            else:
                type_matrix = np.full((6,6), '', dtype=object)
                for i in range(6):
                    for j in range(6):
                        current = roll[i,j]
                        one_count = current.count(1)
                        face1_count = current.count(bids[1][1])
                        face2_count = current.count(bids[2][1])

                        if bids[3][0] == 3 and bids[4][0] == 3:
                            p_highest, p_high, p_low, p_lowest = count3[0]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            elif face2_count + one_count == 2 and face2_count != 2:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count == 1 and face1_count + one_count != 0:
                                type_matrix[i,j] = 'High'
                            else: 
                                type_matrix[i,j] = 'Low'
                        elif bids[3][0] == 3 and bids[4][0] == 4:
                            p_highest, p_high, p_low, p_lowest = count3[1]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            if face1_count + one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            if face1_count + one_count == 1:
                                type_matrix[i,j] = 'High'
                                    
                count_highest = (type_matrix == 'Highest').sum()
                count_high = (type_matrix == 'High').sum()
                count_low = (type_matrix == 'Low').sum()
                count_lowest = (type_matrix == 'Lowest').sum()
                p_matrix  = np.full((6,6), 0, dtype=object)
                
                for i in range(6):
                    for j in range(6):
                        if type_matrix[i,j] == 'Highest':
                            p_matrix[i,j] = round(p_highest / count_highest, 3)
                        elif type_matrix[i,j] == 'High':
                            p_matrix[i,j] = round(p_high / count_high, 3)
                        elif type_matrix[i,j] == 'Low':
                            p_matrix[i,j] = round(p_low / count_low, 3)
                        elif type_matrix[i,j] == 'Lowest':
                            p_matrix[i,j] = round(p_lowest / count_lowest, 3)
                        
                
                zero_count1 = 0
                zero_count2 = 0
                adjust2 = 0
                adjust1 = 0

                for i in range(6):
                    for j in range(6):
                        if p_matrix[i,j] == 0:
                            zero_count1 += 1
                            zero_count2 += 1
                            adjust1 += matrix1[i,j]
                            adjust2 += matrix2[i,j]
                            matrix1[i,j] = 0
                            matrix2[i,j] = 0
                            
                for i in range(6):
                    for j in range(6):
                        if matrix1[i,j] == 0:
                            matrix[i,j] = 0
                        else:
                            matrix[i,j] = round((1 / 6) * (matrix1[i,j] + (adjust1 / zero_count1)) + (1 / 3) * (matrix2[i,j] + (adjust2 / zero_count2)) + p_matrix[i,j] * (1 / 2), 3)
                            
            return matrix      
        def sixthBidRange(bids, first_in, second_in, count3):
            roll = rolls()
            matrix1 = secondInRange(bids[:2], first_in, second_in, count3)
            matrix2 = fourthBidRange(bids[:4], first_in, second_in, count3)
            matrix3 = fifthBidRange(bids[1:], first_in, second_in, count3)
            matrix = np.full((6,6), 0, dtype=object)
            
            if bids[4][0] < 3:
                for i in range(6):
                    for j in range(6):
                        matrix[i,j] = round((1 / 6) * matrix1[i,j] + (1 / 3) * matrix2[i,j] + matrix3[i,j] * (1 / 2), 3)
            else:
                type_matrix = np.full((6,6), '', dtype=object)
                for i in range(6):
                    for j in range(6):
                        current = roll[i,j]
                        one_count = current.count(1)
                        face1_count = current.count(bids[1][1])
                        face2_count = current.count(bids[2][1])

                        if bids[4][0] == 3 and bids[5][0] == 3:
                            p_highest, p_high, p_low, p_lowest = count3[0]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            elif face2_count + one_count == 2 and face2_count != 2:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count == 1 and face1_count + one_count != 0:
                                type_matrix[i,j] = 'High'
                            else: 
                                type_matrix[i,j] = 'Low'
                        elif bids[4][0] == 3 and bids[5][0] == 4:
                            p_highest, p_high, p_low, p_lowest = count3[1]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            if face1_count + one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            if face1_count + one_count == 1:
                                type_matrix[i,j] = 'High'
                                    
                count_highest = (type_matrix == 'Highest').sum()
                count_high = (type_matrix == 'High').sum()
                count_low = (type_matrix == 'Low').sum()
                count_lowest = (type_matrix == 'Lowest').sum()
                p_matrix  = np.full((6,6), 0, dtype=object)
                
                for i in range(6):
                    for j in range(6):
                        if type_matrix[i,j] == 'Highest':
                            p_matrix[i,j] = round(p_highest / count_highest, 3)
                        elif type_matrix[i,j] == 'High':
                            p_matrix[i,j] = round(p_high / count_high, 3)
                        elif type_matrix[i,j] == 'Low':
                            p_matrix[i,j] = round(p_low / count_low, 3)
                        elif type_matrix[i,j] == 'Lowest':
                            p_matrix[i,j] = round(p_lowest / count_lowest, 3)
                        
                
                zero_count1 = 0
                zero_count2 = 0
                adjust2 = 0
                adjust1 = 0

                for i in range(6):
                    for j in range(6):
                        if p_matrix[i,j] == 0:
                            zero_count1 += 1
                            zero_count2 += 1
                            adjust1 += matrix1[i,j]
                            adjust2 += matrix2[i,j]
                            matrix1[i,j] = 0
                            matrix2[i,j] = 0
                            
                for i in range(6):
                    for j in range(6):
                        if matrix1[i,j] == 0:
                            matrix[i,j] = 0
                        else:
                            matrix[i,j] = round((1 / 6) * (matrix1[i,j] + (adjust1 / zero_count1)) + (1 / 3) * (matrix2[i,j] + (adjust2 / zero_count2)) + p_matrix[i,j] * (1 / 2), 3)
                            
            return matrix
        def seventhBidRange(bids, first_in, second_in, count3):
            roll = rolls()
            matrix1 = firstInRange([bids[0]], first_in, second_in, count3)
            matrix2 = thirdBidRange(bids[:3], first_in, second_in, count3)
            matrix3 = fifthBidRange(bids[:5], first_in, second_in, count3)
            matrix4 = sixthBidRange(bids[1:], first_in, second_in, count3)
            matrix = np.full((6,6), 0, dtype=object)
            
            if bids[5][0] < 3:
                for i in range(6):
                    for j in range(6):
                        matrix[i,j] = round((1 / 6) * matrix1[i,j] + (1 / 3) * matrix2[i,j] + matrix3[i,j] * (1 / 2), 3)
            else:
                type_matrix = np.full((6,6), '', dtype=object)
                for i in range(6):
                    for j in range(6):
                        current = roll[i,j]
                        one_count = current.count(1)
                        face1_count = current.count(bids[1][1])
                        face2_count = current.count(bids[2][1])

                        if bids[5][0] == 3 and bids[6][0] == 3:
                            p_highest, p_high, p_low, p_lowest = count3[0]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            elif face2_count + one_count == 2 and face2_count != 2:
                                type_matrix[i,j] = 'Highest'
                            elif face2_count == 1 and face1_count + one_count != 0:
                                type_matrix[i,j] = 'High'
                            else: 
                                type_matrix[i,j] = 'Low'
                        elif bids[5][0] == 3 and bids[6][0] == 4:
                            p_highest, p_high, p_low, p_lowest = count3[1]
                            if face1_count + one_count == 0:
                                type_matrix[i,j] = 'Lowest'
                            if face1_count + one_count == 2:
                                type_matrix[i,j] = 'Highest'
                            if face1_count + one_count == 1:
                                type_matrix[i,j] = 'High'
                                    
                count_highest = (type_matrix == 'Highest').sum()
                count_high = (type_matrix == 'High').sum()
                count_low = (type_matrix == 'Low').sum()
                count_lowest = (type_matrix == 'Lowest').sum()
                p_matrix  = np.full((6,6), 0, dtype=object)
                
                for i in range(6):
                    for j in range(6):
                        if type_matrix[i,j] == 'Highest':
                            p_matrix[i,j] = round(p_highest / count_highest, 3)
                        elif type_matrix[i,j] == 'High':
                            p_matrix[i,j] = round(p_high / count_high, 3)
                        elif type_matrix[i,j] == 'Low':
                            p_matrix[i,j] = round(p_low / count_low, 3)
                        elif type_matrix[i,j] == 'Lowest':
                            p_matrix[i,j] = round(p_lowest / count_lowest, 3)
                        
                
                zero_count1 = 0
                zero_count2 = 0
                zero_count3 = 0
                adjust2 = 0
                adjust1 = 0
                adjust3 = 0

                for i in range(6):
                    for j in range(6):
                        if p_matrix[i,j] == 0:
                            zero_count1 += 1
                            zero_count2 += 1
                            zero_count3 += 1
                            adjust1 += matrix1[i,j]
                            adjust2 += matrix2[i,j]
                            adjust3 += matrix3[i,j]
                            matrix1[i,j] = 0
                            matrix2[i,j] = 0
                            
                for i in range(6):
                    for j in range(6):
                        if matrix1[i,j] == 0:
                            matrix[i,j] = 0
                        else:
                            matrix[i,j] = round((1 / 12) * (matrix1[i,j] + (adjust1 / zero_count1)) + (1 / 6) * (matrix2[i,j] + (adjust2 / zero_count2)) + (1 / 4) * (matrix3[i,j] + (adjust3 / zero_count3)) + p_matrix[i,j] * (1 / 2), 3)
                            
            return matrix


        num_bids = len(bids)
        if num_bids == 1:
            matrix = firstInRange(bids, first_in, second_in, count3)
        elif num_bids == 2:
            matrix = secondInRange(bids, first_in, second_in, count3)
        elif num_bids == 3:
            matrix = thirdBidRange(bids, first_in, second_in, count3)
        elif num_bids == 4:
            matrix = fourthBidRange(bids, first_in, second_in, count3)
        elif num_bids == 5:
            matrix = fifthBidRange(bids, first_in, second_in, count3)
        elif num_bids == 6:
            matrix = sixthBidRange(bids, first_in, second_in, count3)
        elif num_bids == 7:
            matrix = seventhBidRange(bids, first_in, second_in, count3)
        else:
            dif = num_bids - 7
            matrix = seventhBidRange(bids[dif:], first_in, second_in, count3)
            
        return convertRange(matrix)

    # Expected Win Probability of calling Calza or Liar
    def liarEWP(bids, first_in, second_in, count3, your_dice):
        def pOne(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one == 1:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one == 1:
                            p += matrix[i,j]
            return p   

        def pZero(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one == 0:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one == 0:
                            p += matrix[i,j]
            return p
    
        
        
        
        bid_prev = bids[-1]
        
        count, face = bid_prev
        if face != 1:
            count_face = your_dice.count(face)
            count_one = your_dice.count(1)
            need = count - count_face - count_one
        else:
            count_one = your_dice.count(1)
            need = count - count_one
        p = 0
        
        if need <= 0:
            p = 0
        elif need == 1:
            p = pZero(face, bids, first_in, second_in, count3 )
        elif need == 2:
            p = pOne(face, bids, first_in, second_in, count3 ) + pZero(face, bids, first_in, second_in, count3 )
        elif need == 3:
            p = 1
        elif need == 4:
            p = 1
        
                    
        ev = (3 /4) * p + (1 / 4) * (1 - p)
        
        return round(ev, 3), p
    def calzaEWP(bids, first_in, second_in, count3, your_dice):
        
        def pZero(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one == 0:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one == 0:
                            p += matrix[i,j]
            return p
        def pOne(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one == 1:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one == 1:
                            p += matrix[i,j]
            return p   
        def pTwo(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one == 2:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one == 2:
                            p += matrix[i,j]
            return p          
        
        
        count, face = bids[-1]
        if face != 1:
            count_face = your_dice.count(face)
            count_one = your_dice.count(1)
            need = count - count_face - count_one
        else:
            count_one = your_dice.count(1)
            need = count - count_one

        if need < 0:
            p = 0
        elif need == 0:
            p = pZero(face, bids, first_in, second_in, count3)
        elif need == 1:
            p = pOne(face, bids, first_in, second_in, count3)
        elif need == 2:
            p = pTwo(face, bids, first_in, second_in, count3)
        elif need == 3:
            p = 0
        elif need == 4:
            p = 0
            
        ev = (11 / 16) * p + (1 / 4) * (1 - p)
        
        return round(ev, 3), p

    # Safest Bids
    def safestOptions(bids):
        count, face = bids[-1]
        response = response2v2(bids)
        if count == 1:
            ind = response.index((2, 6))
            safe_response = response[:ind + 1]
        if count == 2:
            if face != 1:
                safe_response = response[: 5]
                safe_response.insert(6 - face, (2, 1))
            else:
                safe_response = response[: 5]
        if count == 3 and face != 1:
            safe_response = response[: 6]
        if count == 4 and face != 1:
            safe_response = response
        if count == 3 and face == 1:
            safe_response = [(4,1)]
        if count == 4 and face == 1:
            safe_response = []
            
        return safe_response
    def pBids(bids, your_dice, first_in, second_in, count3, floor):
        def pGEOne(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one >= 1:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one >= 1:
                            p += matrix[i,j]
            return p  
        def pTwo(face, bids, first_in, second_in, count3):
            matrix = ranges(bids, first_in, second_in, count3)
            roll = rolls()
            p = 0
            if face != 1:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_face = current.count(face)
                        count_one = current.count(1)
                        
                        if count_face + count_one == 2:
                            p += matrix[i,j]
            else:
                for i in range(len(roll)):
                    for j in range(len(roll[i])):
                        current = roll[i,j]
                        count_one = current.count(1)
                        
                        if count_one == 2:
                            p += matrix[i,j]
            return p          

        arr = safestOptions(bids)
        need = [0] * len(arr)
        prob = [0] * len(arr)
        visual = [0] * len(arr)
        
        for i in range(len(arr)):
            count, face = arr[i]
            if face == 1:
                need[i] = count - your_dice.count(1)
            else:
                need[i] = count - your_dice.count(1) - your_dice.count(face)
            
            
            if need[i] <= 0:
                prob[i] = 1
            elif need[i] == 1:
                prob[i] = round(pGEOne(face, bids, first_in, second_in, count3), 4)
            elif need[i] == 2:
                prob[i] = round(pTwo(face, bids, first_in, second_in, count3), 4)
            else:
                prob[i] == 0
            
            visual[i] = (arr[i], prob[i])
            
        visual.sort(key=lambda x: x[1], reverse=True)
        
        result = [row[0] for row in visual if row[1] > floor]
        
        return result

    def outcome(bids, call, dice1, dice2):
        count, face = bids[-1]
        
        one_count = dice1.count(1) + dice2.count(1)
        face_count = dice1.count(face) + dice2.count(face)
        
        if call == 'Liar':
            if one_count + face_count >= count:
                return 'Not a Lie'
            else:
                return 'Lie'
        else:
            if one_count + face_count == count:
                return 'Calza'
            else:
                return 'Not Calza'

        
    EWPLiar, p_liar = liarEWP(bids, first_in, second_in, count3, your_dice)
    EWPCalza, p_calza = calzaEWP(bids, first_in, second_in, count3, your_dice)
    print(EWPCalza, EWPLiar)
    
    
    p = min(p_liar, p_calza)
    
    if EWPLiar >= .75:
        return .75, 'Liar'
    
    possible_bids = pBids(bids, your_dice, first_in, second_in, count3, floor=p)
    
    if len(possible_bids) == 0:
        if max(EWPLiar,EWPCalza) == EWPCalza:
            return EWPCalza,  'Calza'
        else:
            return EWPLiar, 'Liar'
    
    opp_range = ranges(bids, first_in, second_in, count3)
    signif_range = np.full((6,6), 0, dtype=object)
    for i in range(6):
        for j in range(6):
            if opp_range[i,j] > .05:
                signif_range[i,j] = opp_range[i,j]
    
    total = sum(sum(signif_range))
    
    for i in range(6):
        for j in range(6):
            if opp_range[i,j] > .05:
                signif_range[i,j] = round(signif_range[i,j] / total, 3)
                
    
    best_bid_ewp = 0
    best_bid_ewp_move = None
    
    for bid in possible_bids:
        new_bids = bids + [bid]
        bid_ewp = 0
        for i in range(6):
            for j in range(6):
                dice_ewp = 0
                weight = signif_range[i,j]
                if weight == 0:
                    continue
                
                _, opp_move = optimal(bids=new_bids,  
                                    your_dice = [i + 1, j + 1])
                
                if opp_move == 'Liar':
                    outc = outcome(bids, 'Liar', your_dice, [i + 1, j + 1])
                    
                    if outc == 'Lie':
                        dice_ewp = .25
                    else:
                        dice_ewp = .75
                elif opp_move == 'Calza':
                    outc = outcome(bids, 'Calza', your_dice, [i + 1, j + 1])
                    
                    if outc == 'Calza':
                        dice_ewp = .3125
                    else:
                        dice_ewp = .75
                        
                else:
                    newest_bids = new_bids + [opp_move]
                    
                    dice_ewp = optimal(bids=newest_bids,
                                        your_dice = your_dice)[0]
                    
                bid_ewp += weight * dice_ewp
                
        if bid_ewp >= best_bid_ewp:
            best_bid_ewp = bid_ewp
            best_bid_ewp_move = bid
            
    EWPBid = round(best_bid_ewp, 3)
    best_move = best_bid_ewp_move
    
    print(EWPBid, EWPLiar, EWPCalza)
    
    if max(EWPBid, EWPLiar, EWPCalza) == EWPBid:
        return EWPBid, best_move
    elif max(EWPBid, EWPLiar, EWPCalza) == EWPCalza:
        return EWPCalza, 'Calza'
    else:
        return EWPLiar, 'Liar'
    


a = optimal(
    bids=[(1,2),(2,6)],
    your_dice=[2,5]
)

print(a)
    