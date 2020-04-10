import pygame

from queue import Queue

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (240, 0, 100)
color_options = [RED, ORANGE, BLUE, GREEN]

pygame.init()
font = pygame.font.SysFont('Consolas', 40)

class Node :
    def __init__(self, data) :
        self.data = data
        self.left = None
        self.right = None

def create_level_wise(arr) :
    if len(arr) == 0 :
        return None
    
    q = Queue()
    root = Node(arr[0])
    q.put(root)

    i = 1
    while not q.empty() :
        parent = q.get()

        if arr[i] == -1 :
            parent.left = None
        else :
            temp = Node(arr[i])
            parent.left = temp
            q.put(temp)

        i += 1

        if arr[i] == -1 :
            parent.right = None
        else :
            temp = Node(arr[i])
            parent.right = temp
            q.put(temp)

        i += 1

    return root

def height_of_tree(root) :
    if root is None : 
        return 0

    return 1 + max(height_of_tree(root.left), height_of_tree(root.right))

def display_tree(root) :
    q = Queue()

    h = height_of_tree(root)
    q.put((root, h, SCREEN_WIDTH // 2, 50))
    
    while not q.empty() :
        parent, h, x, y = q.get()

        pygame.draw.circle(win, (255,255,255), (x, y), 40)

        if parent.left is not None :
            left_x = x - 20 * h ** 1.5
            left_y = y + 150
            q.put((parent.left, h - 1, int(left_x), left_y))
            pygame.draw.line(win, (255,255,255), (x, y), (int(left_x), left_y))
        
        if parent.right is not None :
            right_x = x + 20 * h ** 1.5
            right_y = y + 150
            q.put((parent.right, h - 1, int(right_x), right_y))
            pygame.draw.line(win, (255,255,255), (x, y), (int(right_x), right_y))

        pygame.draw.circle(win, (0, 0, 0), (x, y), 38)
        text = font.render(str(parent.data), True, (255, 255, 255))
        win.blit(text, (x - 15, y - 15))

def create_using_inorder_and_postorder(inorder, postorder):
    if len(inorder) == 0 :
        return None

    root_data = postorder[-1]
    root = Node(root_data)

    root_index = inorder.index(root_data)
    
    left_inorder = inorder[ : root_index]
    right_inorder = inorder[ root_index + 1 : ]

    left_postorder = postorder[ : len(left_inorder)]
    right_postorder = postorder[len(left_inorder) : len(postorder) - 1]

    left_sub_tree = create_using_inorder_and_postorder(left_inorder, left_postorder)
    right_sub_tree = create_using_inorder_and_postorder(right_inorder, right_postorder)

    root.left = left_sub_tree
    root.right = right_sub_tree

    return root

# arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
# root = create_level_wise(arr)

inorder = ['D','B','F','E','A','G','C','L','J','H','K']
postorder = ['D','F','E','B','G','L','J','K','H','C','A']

root = create_using_inorder_and_postorder(inorder, postorder)

run = True
while run :

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    win.fill(0)
    display_tree(root)
    pygame.display.update()