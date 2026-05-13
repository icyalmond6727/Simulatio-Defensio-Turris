"""
A custom implementation of the Quick Sort algorithm utilizing the 'Median of Three' 
pivot selection method to mitigate worst-case O(N^2) scenarios, ensuring a stable O(N log N) average time complexity.
Used heavily for z-index sorting in the graphics pipeline.
"""
def quick_sort(arr, key = lambda x: x):
    """
    Sorts an array in-place using a recursive Quick Sort algorithm.
    
    Args:
        arr (list): The list of elements to sort.
        key (callable, optional): A function to extract a comparison key from each element.
                                  Defaults to the identity function.
                                  
    Returns:
        list: A new, sorted copy of the input array.
    """
    sorted_arr = arr.copy()

    def median_of_three(arr, l, m, r, key = lambda x: x):
        """
        Optimizes pivot selection by finding the median value among the first, middle, 
        and last elements, moving it to the correct position for partitioning.
        """
        if key(arr[m]) > key(arr[r]):
            arr[m], arr[r] = arr[r], arr[m]
        if key(arr[l]) > key(arr[r]):
            arr[l], arr[r] = arr[r], arr[l]
        if key(arr[l]) > key(arr[m]):
            arr[l], arr[m] = arr[m], arr[l]


    def partition(arr, l, r, key = lambda x: x):
        """
        Partitions a sub-array around a pivot element such that elements smaller than 
        the pivot are on the left, and larger elements are on the right.
        """
        m = (l + r) // 2
        median_of_three(arr, l, m, r, key)
        arr[m], arr[r] = arr[r], arr[m]

        pivot = l - 1

        for i in range(l, r):
            if key(arr[i]) <= key(arr[r]):
                pivot += 1
                arr[i], arr[pivot] = arr[pivot], arr[i]

        pivot += 1
        arr[r], arr[pivot] = arr[pivot], arr[r]
        return pivot

    def _sort(arr, l, r, key = lambda x: x):
        """
        The core recursive Quick Sort logic, incorporating tail call optimization 
        strategies by sorting the smaller partition first to limit recursion depth.
        """
        if l >= r:
            return arr

        while l < r:
            pivot = partition(arr, l, r, key)

            if pivot - l < r - pivot:
                _sort(arr, l, pivot - 1, key)
                l = pivot + 1
            else:
                _sort(arr, pivot + 1, r, key)
                r = pivot - 1
        
        return arr

    _sort(sorted_arr, 0, len(sorted_arr) - 1, key)
    return sorted_arr