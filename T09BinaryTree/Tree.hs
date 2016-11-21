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
       | k == key = deleteRoot (Node key value left right)

deleteRoot :: Ord k => BinaryTree k v -> BinaryTree k v
deleteRoot (Node key value Nil Nil) = Nil
deleteRoot (Node key value left Nil) = left
deleteRoot (Node key value Nil right) = right
deleteRoot (Node key value left right) = Node r_key r_value (delete r_key left) right
	where Node r_key r_value _ _ = getRightestElement left

getRightestElement (Node key value left Nil) = Node key value left Nil
getRightestElement (Node key value left right) = getRightestElement right
