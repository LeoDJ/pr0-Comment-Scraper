SELECT commentID, postID, text, [user], up-down AS score
FROM comments 
WHERE text LIKE '%cha0s%'
ORDER BY up-down DESC
;