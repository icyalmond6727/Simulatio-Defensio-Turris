from scenes.defeat_menu import DefeatMenu
from scenes.victory_menu import VictoryMenu

class EventHeap:
    """
    A custom Min-Heap implementation to manage and schedule in-game events.
    Events are sorted based on their execution frame (timestamp) to ensure chronological processing.
    """
    def __init__(self):
        """
        Initializes an empty list to represent the heap.
        
        Returns:
            None
        """
        self.heap = []

    def is_empty(self):
        """
        Checks if the event heap is empty.
        
        Returns:
            bool: True if the heap has no events, False otherwise.
            
        Time Complexity: O(1)
        """
        return len(self.heap) == 0

    def _up_heap(self, index):
        """
        Restores the min-heap property by swapping the element at the given index 
        with its parent if it is smaller than the parent.
        
        Args:
            index (int): The index of the element to bubble up.
            
        Returns:
            None
            
        Time Complexity: O(log n)
        """
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._up_heap(parent)

    def _down_heap(self, index):
        """
        Restores the min-heap property by swapping the element at the given index
        with its smallest child until the property is satisfied.
        
        Args:
            index (int): The index of the element to bubble down.
            
        Returns:
            None
            
        Time Complexity: O(log n)
        """
        min_index = index
        left = 2 * (index + 1) - 1
        right = 2 * (index + 1)

        n = len(self.heap)
        if left < n and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left
        if right < n and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right

        if min_index != index:
            self.heap[index], self.heap[min_index] = self.heap[min_index], self.heap[index]
            self._down_heap(min_index)

    def push(self, event):
        """
        Inserts a new event into the heap and restores the heap property.
        
        Args:
            event (tuple): A tuple representing the event (event_frame, event_type, event_args).
            
        Returns:
            None
            
        Time Complexity: O(log n)
        """
        self.heap.append(event)
        self._up_heap(len(self.heap) - 1)

    def pop(self):
        """
        Removes the event with the smallest execution frame (the root of the min-heap).
        
        Returns:
            None. (To get the element, use top() before popping).
            
        Time Complexity: O(log n)
        """
        if self.is_empty():
            return None
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        if not self.is_empty():
            self._down_heap(0)

    def top(self):
        """
        Retrieves the event with the smallest execution frame without removing it.
        
        Returns:
            tuple or None: The highest priority event as a tuple, or None if the heap is empty.
            
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self.heap[0]
    
    def process_events(self, current_frame, scene):
        """
        Processes all events in the heap that are scheduled to occur at or before the current frame.
        
        Args:
            current_frame (int): The current frame/tick of the game loop.
            scene (Scene): The active game scene to apply event effects to (e.g., spawning, damaging).
            
        Returns:
            None
            
        Time Complexity: O(k log n) where k is the number of processed events.
        """
        while True:
            if self.is_empty():
                break

            event_frame, event_type, event_args = self.top()
            if event_frame > current_frame:
                break
            self.pop()

            if event_type == "damage":
                target_enemy, damage = event_args
                target_enemy.current_health -= damage
            
            elif event_type == "spawn":
                path_index, enemy_name = event_args
                scene.spawn_enemy(path_index, enemy_name)

            elif event_type == "defeat":
                scene.game_manager.change_scene(DefeatMenu(scene.game_manager, scene))

            elif event_type == "victory":
                scene.game_manager.change_scene(VictoryMenu(scene.game_manager, scene))