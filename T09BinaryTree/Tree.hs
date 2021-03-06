import Prelude hiding (lookup)

-- Реализовать двоичное дерево поиска без балансировки (4 балла)
data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” требует, чтобы элементы типа k можно было сравнивать 
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k (Node key value left right) 
      | k == key = Just value 
      | k > key = lookup k right
      | k < key = lookup k left 
lookup _ Nil = Nothing

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil
insert k v (Node key value left right)
       | k == key = Node k v left right
       | k > key = Node key value left (insert k v right)
       | k < key = Node key value (insert k v left) right

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete _ Nil = Nil
delete k (Node key value left right)
       | k > key = Node key value left (delete k right) 
       | k < key = Node key value (delete k left) right
       | k == key = pasteToLeftistElement right left

pasteToLeftistElement Nil set_left = set_left
pasteToLeftistElement (Node key value left right) set_left = Node key value (pasteToLeftistElement left set_left) right

