import pygame

from queue import Queue

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def display_tree(root) :
    q = Queue()

    h = get_height(root)
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

pygame.init()
font = pygame.font.SysFont('Consolas', 40)

class Node : 
    def __init__(self, data) :
        self.data = data
        self.left = None 
        self.right = None
        self.height = 1

def get_height(root) :
    if root is None :
        return 0

    return 1 + max(get_height(root.left), get_height(root.right))

def balance_factor(root) :
    if root is None :
        return 0

    return get_height(root.left) - get_height(root.right)

def rotate_right(root) :
    
    new_root = root.left
    root.left = new_root.right
    new_root.right = root

    new_root.height = get_height(new_root)
    new_root.right.height = get_height(new_root.right)

    return new_root

def rotate_left(root) :

    new_root = root.right
    root.right = new_root.left
    new_root.left = root

    new_root.height = get_height(new_root)
    new_root.left.height = get_height(new_root.left)

    return new_root

def insert(root, val) :
    if root is None :
        return Node(val)

    if val < root.data :
        root.left = insert(root.left, val)

    else :
        root.right = insert(root.right, val)

    root.height = get_height(root)

    b_f = balance_factor(root)

    if b_f > 1 :
    
        # left left case 
        if balance_factor(root.left) > 0 :
            root = rotate_right(root)

        # left right case
        else :
            root.left = rotate_left(root.left)
            root = rotate_right(root)

    elif b_f < - 1 :

        # right right case 
        if balance_factor(root.right) < 0 :
            root = rotate_left(root)

        # right left case :
        else :
            root.right = rotate_right(root.right)
            root = rotate_left(root)

    return root

play = False
run = True
while run :

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] :
        play = True
        pygame.time.delay(200)

    if play :
        arr = [50, 20, 60, 10, 8, 15, 32, 46, 11, 48]
        root = None

        for ele in arr :

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    quit()
                    run = False

            win.fill(0)

            root = insert(root, ele)
            display_tree(root)

            pygame.time.delay(1000)
            pygame.display.update()